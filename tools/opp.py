"""OPP V0 reference package checks. This is not a CAD or certification engine."""
from __future__ import annotations

import hashlib
import json
import re
import stat
import zipfile
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0-draft.1"
SAFE_PATH = re.compile(r"^[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*(?:\.[A-Za-z0-9_-]+)?$")
LIMITS = {"entries": 10_000, "entry": 256 * 1024**2, "total": 1024**3,
          "json": 100 * 1024**2, "ratio": 200}
KNOWN_PROFILES = {"opp.core", "opp.geometry.step-part21", "opp.dimensions",
                  "opp.gdt.asme", "opp.gdt.iso", "opp.requirements", "opp.as-built",
                  "opp.scan", "opp.fai"}
LENGTH = {"um": Decimal("0.001"), "mm": Decimal(1), "cm": Decimal(10),
          "m": Decimal(1000), "in": Decimal("25.4")}
UNIT_GROUPS = [LENGTH, {"mm2":Decimal(1),"m2":Decimal(1000000)},
               {"mm3":Decimal(1),"m3":Decimal(1000000000)},
               {"N":Decimal(1),"kN":Decimal(1000)},
               {"Pa":Decimal(1),"kPa":Decimal(1000),"MPa":Decimal(1000000),"bar":Decimal(100000)},
               {"g":Decimal(1),"kg":Decimal(1000)},
               {"s":Decimal(1),"min":Decimal(60),"h":Decimal(3600)},
               {"mL/min":Decimal(1),"L/min":Decimal(1000)},
               {"1":Decimal(1),"percent":Decimal("0.01")},
               {"g/cm3":Decimal(1000),"kg/m3":Decimal(1)}]


class PackageError(ValueError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def strict_json(data: bytes, label="JSON"):
    if len(data) > LIMITS["json"]:
        raise PackageError(f"{label}: JSON resource exceeds inspection limit")
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise PackageError(f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result
    def nonfinite(value):
        raise PackageError(f"{label}: nonfinite number {value}")
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=nonfinite)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise PackageError(f"{label}: invalid UTF-8 JSON: {exc}") from exc


def safe_paths(names):
    seen = set()
    for name in names:
        if not SAFE_PATH.fullmatch(name):
            raise PackageError(f"Unsafe or unsupported package path: {name!r}")
        lower = name.lower()
        if lower in seen:
            raise PackageError(f"Duplicate or case-colliding package path: {name!r}")
        seen.add(lower)
    for name in seen:
        parts = name.split("/")
        if any("/".join(parts[:i]) in seen for i in range(1, len(parts))):
            raise PackageError(f"File/directory prefix conflict: {name!r}")


def read_package(path: Path) -> dict[str, bytes]:
    if path.is_dir():
        entries = sorted(path.rglob("*"))
        if any(p.is_symlink() for p in entries):
            raise PackageError("Symlinks are not allowed in unpacked packages")
        files = [p for p in entries if p.is_file()]
        safe_paths([p.relative_to(path).as_posix() for p in files])
        if len(files) > LIMITS["entries"]:
            raise PackageError("Too many package entries")
        total = 0
        for p in files:
            size = p.stat().st_size
            total += size
            if size > LIMITS["entry"] or total > LIMITS["total"]:
                raise PackageError("Package exceeds expanded resource limits")
        return {p.relative_to(path).as_posix(): p.read_bytes() for p in files}
    try:
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            if len(entries) > LIMITS["entries"]:
                raise PackageError("Too many archive entries")
            safe_paths([e.filename.rstrip("/") for e in entries])
            total = 0
            for e in entries:
                if e.flag_bits & 1:
                    raise PackageError("Encrypted entries are unsupported")
                if stat.S_ISLNK(e.external_attr >> 16):
                    raise PackageError("Archive symlinks are forbidden")
                if e.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
                    raise PackageError("Unsupported ZIP compression method")
                total += e.file_size
                if e.file_size > LIMITS["entry"] or total > LIMITS["total"]:
                    raise PackageError("Archive exceeds expanded resource limits")
                if e.file_size / max(e.compress_size, 1) > LIMITS["ratio"]:
                    raise PackageError("Archive exceeds compression-ratio limit")
            return {e.filename: archive.read(e) for e in entries if not e.is_dir()}
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError) as exc:
        raise PackageError(f"Cannot read OPP ZIP: {exc}") from exc


def schema_runtime():
    schemas = {}
    for path in sorted((ROOT / "schemas/v0").glob("*.schema.json")):
        value = strict_json(path.read_bytes(), path.name)
        Draft202012Validator.check_schema(value)
        schemas[value["$id"]] = value
    registry = Registry().with_resources((key, Resource.from_contents(value)) for key, value in schemas.items())
    return schemas, registry


def convert(value, source_unit, target_unit):
    value = Decimal(value)
    if source_unit == target_unit:
        return value
    for group in UNIT_GROUPS:
        if source_unit in group and target_unit in group:
            return value * group[source_unit] / group[target_unit]
    raise PackageError(f"Unsupported or incompatible units: {source_unit} → {target_unit}")


def at_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def walk(value, path=""):
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from walk(child, path + "/" + key)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from walk(child, path + "/" + str(i))


class Checker:
    def __init__(self, files):
        self.files = files
        self.errors = []
        self.warnings = []
        self.schemas, self.registry = schema_runtime()
        self.docs = {}
        self.resources = {}
        self.design = {}
        self.actual = None
        self.d = {}
        self.a = {}

    def error(self, text):
        if text not in self.errors:
            self.errors.append(text)

    def warn(self, text):
        if text not in self.warnings:
            self.warnings.append(text)

    def validate_schema(self, value, name, label):
        validator = Draft202012Validator(self.schemas[f"urn:opp:schema:{VERSION}:{name}"],
                                         registry=self.registry, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(value), key=lambda e: str(list(e.absolute_path)))
        for error in errors[:30]:
            pointer = "/" + "/".join(map(str, error.absolute_path))
            self.error(f"{label}{pointer}: {error.message}")
        return not errors

    def index(self, collection, label):
        result = {}
        for value in collection:
            key = value["id"]
            if key in result:
                self.error(f"{label}: duplicate ID {key}")
            result[key] = value
        return result

    def document(self, resource_id, name):
        resource = self.resources.get(resource_id)
        if not resource or resource["path"] not in self.files:
            self.error(f"Missing {name} resource {resource_id}")
            return None
        try:
            value = strict_json(self.files[resource["path"]], resource["path"])
        except PackageError as exc:
            self.error(str(exc))
            return None
        if not self.validate_schema(value, name, resource["path"]):
            return None
        self.docs[resource_id] = value
        return value

    def check(self):
        if "manifest.json" not in self.files:
            self.error("Missing root manifest.json")
            return self.report()
        manifest = strict_json(self.files["manifest.json"], "manifest.json")
        if not self.validate_schema(manifest, "manifest", "manifest.json"):
            return self.report()
        self.manifest = manifest
        self.resources = self.index(manifest["resources"], "manifest/resources")
        try:
            safe_paths([r["path"] for r in manifest["resources"]] + ["manifest.json"])
        except PackageError as exc:
            self.error(str(exc))
        expected = {r["path"] for r in manifest["resources"]} | {"manifest.json"}
        for path in sorted(expected - self.files.keys()):
            self.error(f"Missing inventoried file: {path}")
        for path in sorted(self.files.keys() - expected):
            self.error(f"Uninventoried file: {path}")
        for r in manifest["resources"]:
            data = self.files.get(r["path"])
            if data is not None and (len(data) != r["size"] or sha(data) != r["sha256"]):
                self.error(f"Size/SHA-256 mismatch: {r['path']}")
        roots = [("designResourceId","design"),("bindingsResourceId","bindings"),
                 ("asBuiltResourceId","as-built"),("presentationResourceId","presentation")]
        for key, role in roots:
            if key in manifest and self.resources.get(manifest[key], {}).get("role") != role:
                self.error(f"{key} must name a resource with role {role}")
        root_ids = [manifest[key] for key, _ in roots if key in manifest]
        if len(root_ids) != len(set(root_ids)):
            self.error("Root document resources must be distinct")
        if self.errors:
            return self.report()
        self.design = self.document(manifest["designResourceId"], "design")
        self.bindings = self.document(manifest["bindingsResourceId"], "bindings")
        if manifest["packageType"] == "as-built":
            self.actual = self.document(manifest["asBuiltResourceId"], "as-built")
        if "presentationResourceId" in manifest:
            self.presentation = self.document(manifest["presentationResourceId"], "presentation")
        for r in manifest["resources"]:
            if r["role"] == "conversion-report":
                self.document(r["id"], "conversion-report")
        if self.errors:
            return self.report()
        self.d = {key:self.index(value, "design/"+key) for key,value in self.design.items()
                  if isinstance(value,list) and key not in {"extensions","resourcePins"}}
        if self.actual:
            self.a = {key:self.index(value, "actual/"+key) for key,value in self.actual.items()
                      if isinstance(value,list) and key != "extensions"}
        for label, indices in [("design",self.d),("actual",self.a)]:
            ids = [key for index in indices.values() for key in index]
            if len(ids) != len(set(ids)):
                self.error(f"{label}: IDs must be unique across collections")
        self.check_references(self.design, "design")
        if self.actual:
            self.check_references(self.actual, "actual")
        if self.errors:
            return self.report()
        self.check_profiles()
        self.check_quantities(self.design, "design")
        if self.actual:
            self.check_quantities(self.actual, "actual")
        self.check_design()
        self.check_bindings()
        if getattr(self,"presentation",None):
            self.check_references(self.presentation,"presentation")
            if self.presentation["designId"] != self.design["id"]:
                self.error("Presentation designId mismatch")
        if self.actual:
            self.check_actual()
        return self.report()

    def check_references(self, document, label):
        design_refs = {
            "rootDefinitionId":"productDefinitions", "productDefinitionId":"productDefinitions",
            "parentDefinitionId":"productDefinitions", "childDefinitionId":"productDefinitions",
            "stateId":"states", "frameId":"coordinateFrames", "designFrameId":"coordinateFrames",
            "parentFrameId":"coordinateFrames", "representationId":"representations",
            "regionId":"regions", "regionIds":"regions", "targetRegions":"regions",
            "featureId":"features", "featureIds":"features", "connectionId":"connections",
            "materialDefinitionId":"materials", "permittedAlternativeMaterialIds":"materials",
            "adhesiveMaterialId":"materials", "fillerMaterialId":"materials",
            "datumIds":"datums", "datumSystemId":"datumSystems", "requirementId":"requirements",
            "requirementIds":"requirements", "overridesRequirementIds":"requirements",
            "sequenceAfterRequirementIds":"requirements", "verificationId":"verifications",
            "decisionRuleId":"decisionRules", "interpretationId":"interpretations",
            "standardDocumentIds":"documents", "dependsOnDocumentIds":"documents",
            "specificationDocumentIds":"documents", "specificationDocumentId":"documents",
            "methodDocumentId":"documents", "standardDocumentId":"documents",
            "procedureDocumentId":"documents", "gaugeDocumentId":"documents",
            "inspectionDocumentId":"documents", "documentId":"documents", "documentIds":"documents",
            "sequenceOccurrenceIds":"occurrences"}
        actual_refs = {"subjectId":"subjects", "subjectIds":"subjects", "parentSubjectId":"subjects",
                       "equipmentId":"equipment", "equipmentIds":"equipment", "calibrationIds":"calibrations",
                       "materialLotIds":"materialLots", "parentMaterialLotIds":"materialLots",
                       "cellId":"productionCells", "runId":"runs", "observationIds":"observations",
                       "supersedesObservationId":"observations", "supersedesEventId":"productionEvents",
                       "evaluationIds":"evaluations", "productionEventIds":"productionEvents",
                       "deviationId":"deviations", "deviationIds":"deviations"}
        actor_refs = {"actorId","organizationId","supplierActorId","reviewedByActorId",
                      "operatorActorIds","evaluatorActorId","manufacturerActorId"}
        resource_refs = {"resourceId","sourceResourceId","boundaryResourceId","certificateResourceId",
                         "evidenceResourceIds","certificateResourceIds","reportResourceIds","procedureResourceId",
                         "budgetResourceId","settingsResourceId","previewResourceId","designResourceId"}
        actors = dict(self.d["actors"])
        if label == "actual":
            for key,value in self.a["actors"].items():
                if key in actors and value != actors[key]:
                    self.error(f"Ambiguous design/actual actor ID: {key}")
                actors[key] = value
        for pointer,node in walk(document):
            if "/extensions/" in pointer:
                continue
            for field,value in node.items():
                target = None
                if field in design_refs:
                    target = self.d[design_refs[field]]
                elif field in actor_refs:
                    target = actors
                elif field in resource_refs:
                    target = self.resources
                elif field == "approvalIds":
                    target = (self.a if label == "actual" else self.d)["approvals"]
                elif label == "actual" and field in actual_refs:
                    target = self.a[actual_refs[field]]
                elif field == "bindingIds":
                    target = {b["id"]:b for b in self.bindings["bindings"]}
                if target is not None:
                    values = value if isinstance(value,list) else [value]
                    for item in values:
                        if item not in target:
                            self.error(f"{label}{pointer}/{field}: unresolved reference {item}")

    def check_profiles(self):
        profiles = {}
        for p in self.manifest["profiles"]:
            if p["id"] in profiles:
                self.error(f"Duplicate profile: {p['id']}")
            profiles[p["id"]] = p
            if p["required"] and (p["id"] not in KNOWN_PROFILES or p["version"] != VERSION):
                self.warn(f"Unknown required profile/version: {p['id']} {p['version']}")
        needed = {"opp.core"}
        if self.design["representations"]:
            needed.add("opp.geometry.step-part21")
        if any(r["kind"] == "dimension" for r in self.design["requirements"]):
            needed.add("opp.dimensions")
        if any(r["kind"] not in {"dimension","geometric-tolerance"} for r in self.design["requirements"]):
            needed.add("opp.requirements")
        if self.actual:
            needed.add("opp.as-built")
            if self.actual["scans"]: needed.add("opp.scan")
            if self.actual["faiReports"]: needed.add("opp.fai")
        for i in self.design["interpretations"]:
            if i["profileId"] not in profiles or not profiles[i["profileId"]]["required"]:
                self.error(f"Interpretation {i['id']} needs required profile {i['profileId']}")
            expected = {"asme-gdt":"opp.gdt.asme","iso-gps":"opp.gdt.iso"}.get(i["family"])
            if expected and i["profileId"] != expected:
                self.error(f"Interpretation {i['id']} profile does not match its GD&T family")
        for p in needed:
            if p not in profiles or not profiles[p]["required"]:
                self.error(f"Missing required profile: {p}")
        for label, document in [("design",self.design),("actual",self.actual), ("manifest",self.manifest)]:
            if not document: continue
            for pointer,node in walk(document):
                if {"namespace","profileId","required","data"} <= node.keys():
                    p = profiles.get(node["profileId"])
                    if node["required"]:
                        if not p or not p["required"] or p["version"] != node["version"]:
                            self.error(f"{label}{pointer}: required extension needs matching required profile")
                        self.warn(f"Required extension semantics not implemented: {node['namespace']}")
        self.warn("Full engineering profile interpretation is not implemented by this checker")

    def check_quantities(self, document, label):
        for pointer,node in walk(document):
            if "/extensions/" in pointer: continue
            if "unit" in node and ("lower" in node or "upper" in node):
                lower,upper = node.get("lower"),node.get("upper")
                if lower is not None and upper is not None:
                    if Decimal(lower) > Decimal(upper):
                        self.error(f"{label}{pointer}: lower limit exceeds upper limit")
                    if Decimal(lower) == Decimal(upper) and not (node["lowerInclusive"] and node["upperInclusive"]):
                        self.error(f"{label}{pointer}: equal bounds must both be inclusive")
            if "rotation" in node and "translationUnit" in node:
                r = list(map(Decimal,node["rotation"]))
                eps = Decimal("1e-9")
                for row in range(3):
                    for other in range(3):
                        dot = sum(r[3*row+k]*r[3*other+k] for k in range(3))
                        if abs(dot-(1 if row==other else 0)) > eps:
                            self.error(f"{label}{pointer}: rotation is not orthonormal")
                det = r[0]*(r[4]*r[8]-r[5]*r[7])-r[1]*(r[3]*r[8]-r[5]*r[6])+r[2]*(r[3]*r[7]-r[4]*r[6])
                if abs(det-1) > eps:
                    self.error(f"{label}{pointer}: rotation must have determinant +1")
            if {"expanded","coverageFactor","method"} <= node.keys():
                if Decimal(node["expanded"]["value"]) < 0 or Decimal(node["coverageFactor"]) <= 0:
                    self.error(f"{label}{pointer}: invalid uncertainty magnitude/coverage factor")
                if "confidencePercent" in node and not 0 < Decimal(node["confidencePercent"]) <= 100:
                    self.error(f"{label}{pointer}: invalid uncertainty confidence")
            if "startedAt" in node and "endedAt" in node and at_time(node["startedAt"]) > at_time(node["endedAt"]):
                self.error(f"{label}{pointer}: end precedes start")

    def cycles(self, graph, label):
        # Iterative DFS avoids blowing the Python recursion limit on deeply nested assemblies.
        visited, active = set(), set()
        for start in graph:
            if start in visited: continue
            stack = [(start,False)]
            while stack:
                node,leave = stack.pop()
                if leave:
                    active.discard(node); visited.add(node); continue
                if node in active:
                    self.error(f"{label}: cycle at {node}"); return
                if node in visited: continue
                active.add(node); stack.append((node,True))
                stack.extend((child,False) for child in reversed(graph.get(node,[])))

    def path_definition(self, path, label):
        current = self.design["rootDefinitionId"]
        for occurrence_id in path:
            occurrence = self.d["occurrences"].get(occurrence_id)
            if not occurrence or occurrence["parentDefinitionId"] != current:
                self.error(f"{label}: invalid occurrence path at {occurrence_id}")
                return None
            current = occurrence["childDefinitionId"]
        return current

    def subject_scope(self, subject, label):
        product = subject["productDefinitionId"]
        if "occurrencePath" in subject and self.path_definition(subject["occurrencePath"],label) != product:
            self.error(f"{label}: occurrence path resolves to wrong product")
        for key,collection in [("featureId","features"),("regionId","regions")]:
            if key in subject and self.d[collection][subject[key]]["productDefinitionId"] != product:
                self.error(f"{label}: {key} belongs to another product")
        if "connectionId" in subject and self.d["connections"][subject["connectionId"]]["parentDefinitionId"] != product:
            self.error(f"{label}: connection belongs to another product")

    def check_design(self):
        d = self.d
        pins = {}
        for pin in self.design["resourcePins"]:
            resource_id = pin["resourceId"]
            if resource_id in pins:
                self.error(f"Duplicate design resource pin: {resource_id}")
            pins[resource_id] = pin["sha256"]
            if resource_id == self.manifest["designResourceId"]:
                self.error("Design resource cannot pin its own bytes")
            if pin["sha256"] != self.resources[resource_id]["sha256"]:
                self.error(f"Design resource pin does not match inventory: {resource_id}")
        required_pins = {self.manifest["bindingsResourceId"]}
        resource_fields = {"resourceId","sourceResourceId","boundaryResourceId","previewResourceId",
                           "certificateResourceId","evidenceResourceIds","budgetResourceId","settingsResourceId"}
        for document in [self.design,self.bindings]:
            for pointer,node in walk(document):
                if pointer.startswith("/resourcePins/") or "/extensions/" in pointer:
                    continue
                for key,value in node.items():
                    if key in resource_fields:
                        required_pins.update(value if isinstance(value,list) else [value])
        for resource_id in required_pins - pins.keys():
            self.error(f"Design closure resource lacks a hash pin: {resource_id}")
        identities = [(p["namespace"],p["partNumber"],p["revision"]) for p in d["productDefinitions"].values()]
        if len(identities) != len(set(identities)):
            self.error("Duplicate product namespace/part-number/revision identity")
        for collection in ["representations","regions","features","datums","datumSystems"]:
            for value in d[collection].values():
                if d["states"][value["stateId"]]["productDefinitionId"] != value["productDefinitionId"]:
                    self.error(f"{value['id']}: state belongs to another product")
        authorities = set()
        for representation in d["representations"].values():
            if d["coordinateFrames"][representation["frameId"]]["productDefinitionId"] != representation["productDefinitionId"]:
                self.error(f"{representation['id']}: frame belongs to another product")
            if representation["role"] == "nominal-exact":
                key = (representation["productDefinitionId"],representation["stateId"])
                if key in authorities: self.error(f"Competing exact geometry authorities for {key}")
                authorities.add(key)
                if self.resources[representation["resourceId"]]["role"] != "nominal-geometry":
                    self.error(f"{representation['id']}: exact geometry has wrong resource role")
        for region in d["regions"].values():
            representation = d["representations"][region["representationId"]]
            if any(region[k] != representation[k] for k in ["productDefinitionId","stateId"]):
                self.error(f"{region['id']}: representation ownership/state mismatch")
            if region["kind"] in {"trimmed-surface","volume"}:
                self.warn(f"Exact partial-region encoding not implemented: {region['id']}")
        for key,target,fields in [("features","regions",["regionIds"]),("datums","features",["featureIds"]),("datums","regions",["targetRegions"])]:
            for value in d[key].values():
                for field in fields:
                    for child in value.get(field,[]):
                        if any(value[k] != d[target][child][k] for k in ["productDefinitionId","stateId"]):
                            self.error(f"{value['id']}: {field} ownership/state mismatch")
        for system in d["datumSystems"].values():
            for compartment in system["compartments"]:
                if len(compartment["datumIds"]) != len(set(compartment["datumIds"])):
                    self.error(f"{system['id']}: duplicate datum in compartment")
                for datum_id in compartment["datumIds"]:
                    if any(system[k] != d["datums"][datum_id][k] for k in ["productDefinitionId","stateId"]):
                        self.error(f"{system['id']}: datum ownership/state mismatch")
        graph = defaultdict(list)
        for occurrence in d["occurrences"].values():
            parent = d["productDefinitions"][occurrence["parentDefinitionId"]]
            if parent["kind"] not in {"assembly","kit"}:
                self.error(f"{occurrence['id']}: parent must be an assembly or kit")
            graph[parent["id"]].append(occurrence["childDefinitionId"])
        self.cycles(graph,"assembly containment")
        frames = defaultdict(list)
        for frame in d["coordinateFrames"].values():
            if "parentFrameId" in frame:
                parent = d["coordinateFrames"][frame["parentFrameId"]]
                if frame["productDefinitionId"] != parent["productDefinitionId"]:
                    self.error(f"{frame['id']}: parent frame belongs to another product")
                frames[frame["id"]].append(parent["id"])
        self.cycles(frames,"coordinate frames")
        for connection in d["connections"].values():
            for subject in connection["participants"]:
                self.subject_scope(subject,connection["id"])
        overrides = {}
        for r in d["requirements"].values():
            for subject in r["subjects"]:
                self.subject_scope(subject,r["id"])
                if d["states"][r["stateId"]]["productDefinitionId"] != subject["productDefinitionId"]:
                    self.error(f"{r['id']}: requirement state belongs to another subject product")
                for key,target in [("featureId","features"),("regionId","regions")]:
                    if key in subject and d[target][subject[key]]["stateId"] != r["stateId"]:
                        self.error(f"{r['id']}: selected subject has a different state")
            overrides[r["id"]] = r["overridesRequirementIds"]
            for target in r["overridesRequirementIds"]:
                previous = d["requirements"][target]
                if r["stateId"] != previous["stateId"] or r["subjects"] != previous["subjects"] or r["kind"] != previous["kind"]:
                    self.error(f"{r['id']}: override changes subject/state/kind scope")
            if "verificationId" in r and r["id"] not in d["verifications"][r["verificationId"]]["requirementIds"]:
                self.error(f"{r['id']}: verification does not include this requirement")
            if r["kind"] == "dimension":
                spec = r["spec"]
                if "nominal" in spec and "limits" in spec:
                    try: convert(spec["nominal"]["value"],spec["nominal"]["unit"],spec["limits"]["unit"])
                    except PackageError as exc: self.error(f"{r['id']}: {exc}")
                unit = spec.get("limits",spec.get("nominal",{})).get("unit")
                if spec["characteristic"] == "angle" and unit not in {"deg","rad"}:
                    self.error(f"{r['id']}: angular dimension needs angle units")
                if spec["characteristic"] != "angle" and unit not in LENGTH:
                    self.error(f"{r['id']}: linear dimension needs length units")
            if r["kind"] == "geometric-tolerance":
                for segment in r["spec"]["segments"]:
                    if segment["tolerance"]["unit"] not in LENGTH or Decimal(segment["tolerance"]["value"]) < 0:
                        self.error(f"{r['id']}: invalid geometric-tolerance magnitude/unit")
                    if "datumSystemId" in segment:
                        system = d["datumSystems"][segment["datumSystemId"]]
                        if system["stateId"] != r["stateId"]:
                            self.error(f"{r['id']}: datum system uses another state")
                self.warn(f"GD&T engineering interpretation not assessed: {r['id']}")
            if r["kind"] == "unresolved-text":
                self.warn(f"Unresolved normative text: {r['id']}")
        self.cycles(overrides,"requirement overrides")
        document_graph = {}
        for document in d["documents"].values():
            document_graph[document["id"]] = document.get("dependsOnDocumentIds",[])
            if document["role"] in {"normative","procedure"} and document["dependencyStatus"] != "embedded":
                self.warn(f"Normative dependency {document['dependencyStatus']}: {document['id']}")
        self.cycles(document_graph,"document dependencies")
        release = self.design["release"]
        if release["status"] != "released" or release["engineeringCompleteness"] != "author-declared-complete":
            self.warn("Design is not declared a complete engineering release")
        if release["status"] == "released":
            if release["unresolvedItems"] or release["engineeringCompleteness"] != "author-declared-complete":
                self.error("Released design has incomplete/unresolved engineering declaration")
            if not any(d["approvals"][a]["role"] == "release-authority" for a in release["approvalIds"]):
                self.error("Released design lacks release-authority approval")

    def check_bindings(self):
        if self.bindings["designId"] != self.design["id"]:
            self.error("Bindings designId does not match design snapshot")
        bindings = self.index(self.bindings["bindings"],"bindings")
        for region in self.d["regions"].values():
            for binding_id in region.get("bindingIds",[]):
                if bindings[binding_id]["regionId"] != region["id"]:
                    self.error(f"{region['id']}: binding selects another region")
        entities_by_resource = {}
        for binding in bindings.values():
            region = self.d["regions"].get(binding["regionId"])
            representation = self.d["representations"].get(binding["representationId"])
            resource = self.resources.get(binding["resourceId"])
            if not region or not representation or not resource:
                self.error(f"{binding['id']}: unresolved binding ownership/resource"); continue
            if region["representationId"] != representation["id"] or representation["resourceId"] != resource["id"]:
                self.error(f"{binding['id']}: region/representation/resource mismatch")
            if binding["id"] not in region.get("bindingIds",[]):
                self.error(f"{binding['id']}: region does not reference binding")
            if binding["resourceSha256"] != resource["sha256"]:
                self.error(f"{binding['id']}: geometry hash does not match inventory")
            if representation["encoding"] != "step-part21":
                self.error(f"{binding['id']}: representation is not STEP Part 21")
            if resource["id"] not in entities_by_resource:
                try:
                    source = self.files[resource["path"]].decode("utf-8")
                    # Lexical check only. Mask comments/strings so labels inside either cannot satisfy a binding.
                    source = re.sub(r"/\*.*?\*/|'(?:''|[^'])*'", lambda m: " "*len(m.group()), source, flags=re.S)
                    if len(re.findall(r"\bDATA\s*(?:\([^;]*\))?\s*;",source)) != 1:
                        self.error(f"{resource['id']}: binding profile requires one DATA section")
                    labels = re.findall(r"(#\d+)\s*=",source)
                    if len(labels) != len(set(labels)):
                        self.error(f"{resource['id']}: duplicate STEP entity labels")
                    entities_by_resource[resource["id"]] = dict(re.findall(r"(#\d+)\s*=\s*([A-Z][A-Z0-9_]*)\s*\(",source))
                except UnicodeDecodeError:
                    self.error(f"{resource['id']}: STEP text encoding is unsupported"); continue
            for entity in binding["entities"]:
                actual_type = entities_by_resource[resource["id"]].get(entity["label"])
                if actual_type != entity["entityType"]:
                    self.error(f"{binding['id']}: missing or wrong STEP entity {entity['label']} ({entity['entityType']})")

    def applies(self, requirement, subject):
        if requirement["id"] in {x for r in self.d["requirements"].values() for x in r["overridesRequirementIds"]}:
            return False
        return any(s["productDefinitionId"] == subject["productDefinitionId"] and
                   ("occurrencePath" not in s or s["occurrencePath"] == subject["occurrencePath"])
                   for s in requirement["subjects"])

    def check_actual(self):
        d,a = self.d,self.a
        snapshot = self.actual["designSnapshot"]
        if snapshot["designResourceId"] != self.manifest["designResourceId"] or snapshot["designId"] != self.design["id"]:
            self.error("Actual designSnapshot resource/identity mismatch")
        if snapshot["sha256"] != self.resources[self.manifest["designResourceId"]]["sha256"]:
            self.error("Actual designSnapshot SHA-256 mismatch")
        parent_graph = {}
        physical_keys = set()
        for subject in a["subjects"].values():
            if self.path_definition(subject["occurrencePath"],subject["id"]) != subject["productDefinitionId"]:
                self.error(f"{subject['id']}: physical occurrence path resolves to wrong product")
            if "parentSubjectId" in subject:
                parent = a["subjects"][subject["parentSubjectId"]]
                if parent["kind"] != "instance" or d["productDefinitions"][parent["productDefinitionId"]]["kind"] not in {"assembly","kit"}:
                    self.error(f"{subject['id']}: physical parent is not an assembly/kit instance")
                if subject["occurrencePath"][:-1] != parent["occurrencePath"] or not subject["occurrencePath"]:
                    self.error(f"{subject['id']}: physical parent path mismatch")
                parent_graph[subject["id"]] = [parent["id"]]
            if "serialNumber" in subject:
                identity = (subject.get("manufacturerActorId"),subject["productDefinitionId"],subject["serialNumber"])
                if identity in physical_keys: self.error(f"Duplicate physical serial identity: {subject['id']}")
                physical_keys.add(identity)
        self.cycles(parent_graph,"physical containment")
        self.cycles({x["id"]:x["parentMaterialLotIds"] for x in a["materialLots"].values()},"material genealogy")
        self.cycles({x["id"]:[x["supersedesObservationId"]] for x in a["observations"].values() if "supersedesObservationId" in x},"observation supersession")
        self.cycles({x["id"]:[x["supersedesEventId"]] for x in a["productionEvents"].values() if "supersedesEventId" in x},"production supersession")
        for calibration in a["calibrations"].values():
            if at_time(calibration["calibratedAt"]) > at_time(calibration["validUntil"]):
                self.error(f"{calibration['id']}: calibration validity ends before calibration")
        for run in a["runs"].values():
            if run["sampling"]["sampleCount"] > run["sampling"]["populationCount"]:
                self.error(f"{run['id']}: sample count exceeds population")
            if any(a["subjects"][s]["kind"] == "lot" for s in run["subjectIds"]):
                self.warn(f"Lot sample/aggregation and population acceptance not assessed: {run['id']}")
            calibrated = set()
            for calibration_id in run["calibrationIds"]:
                calibration = a["calibrations"][calibration_id]
                calibrated.add(calibration["equipmentId"])
                if calibration["equipmentId"] not in run["equipmentIds"]:
                    self.error(f"{run['id']}: calibration equipment not used in run")
                if calibration["status"] == "withdrawn" or not (at_time(calibration["calibratedAt"]) <= at_time(run["startedAt"]) <= at_time(run["endedAt"]) <= at_time(calibration["validUntil"])):
                    self.error(f"{run['id']}: calibration invalid at run date")
            for equipment_id in run["equipmentIds"]:
                if a["equipment"][equipment_id]["kind"] in {"measurement","test-rig"} and equipment_id not in calibrated:
                    self.error(f"{run['id']}: measurement/test equipment lacks calibration")
        for observation in a["observations"].values():
            requirement = d["requirements"][observation["requirementId"]]
            subject = a["subjects"][observation["subjectId"]]
            run = a["runs"][observation["runId"]]
            if not self.applies(requirement,subject):
                self.error(f"{observation['id']}: requirement does not apply to physical subject")
            if observation["stateId"] != requirement["stateId"]:
                self.error(f"{observation['id']}: measured state differs from requirement state")
            if subject["id"] not in run["subjectIds"]:
                self.error(f"{observation['id']}: run does not include subject")
            if not at_time(run["startedAt"]) <= at_time(observation["observedAt"]) <= at_time(run["endedAt"]):
                self.error(f"{observation['id']}: observation date is outside run")
            pointer = observation["characteristicPath"]
            try:
                if not pointer.startswith("/"): raise KeyError(pointer)
                value = requirement
                for token in pointer[1:].split("/"):
                    token = token.replace("~1","/").replace("~0","~")
                    value = value[int(token)] if isinstance(value,list) else value[token]
            except (KeyError,IndexError,ValueError,TypeError):
                self.error(f"{observation['id']}: characteristicPath does not resolve in requirement")
            if "supersedesObservationId" in observation:
                old = a["observations"][observation["supersedesObservationId"]]
                if any(old[k] != observation[k] for k in ["subjectId","requirementId","stateId"]):
                    self.error(f"{observation['id']}: retest supersedes different subject/characteristic/state")
                if at_time(old["observedAt"]) > at_time(observation["observedAt"]):
                    self.error(f"{observation['id']}: retest predates superseded observation")
        for evaluation in a["evaluations"].values():
            subject = a["subjects"][evaluation["subjectId"]]
            requirement = d["requirements"][evaluation["requirementId"]]
            if not self.applies(requirement,subject):
                self.error(f"{evaluation['id']}: requirement does not apply to evaluation subject")
            observations = [a["observations"][key] for key in evaluation["observationIds"]]
            for observation in observations:
                if any(observation[k] != evaluation[k] for k in ["subjectId","requirementId"]):
                    self.error(f"{evaluation['id']}: observation subject/requirement mismatch")
                if at_time(observation["observedAt"]) > at_time(evaluation["evaluatedAt"]):
                    self.error(f"{evaluation['id']}: evaluation predates observation")
            if evaluation["disposition"] == "accepted" and evaluation["conformance"] != "pass":
                self.error(f"{evaluation['id']}: ordinary acceptance requires reported pass")
            if evaluation["disposition"] == "accepted-under-deviation":
                deviation = a["deviations"][evaluation["deviationId"]]
                if subject["id"] not in deviation["subjectIds"] or requirement["id"] not in deviation["requirementIds"]:
                    self.error(f"{evaluation['id']}: deviation scope mismatch")
                if deviation["disposition"] != "use-as-is":
                    self.error(f"{evaluation['id']}: deviation is not a final use-as-is acceptance")
                if at_time(deviation["approvedAt"]) > at_time(evaluation["evaluatedAt"]) or ("expiresAt" in deviation and at_time(evaluation["evaluatedAt"]) > at_time(deviation["expiresAt"])):
                    self.error(f"{evaluation['id']}: deviation is not effective at evaluation date")
                if any(at_time(a["approvals"][key]["approvedAt"]) > at_time(evaluation["evaluatedAt"]) for key in deviation["approvalIds"]):
                    self.error(f"{evaluation['id']}: referenced deviation approval postdates evaluation")
                if "quantityLimit" in deviation and sum(a["subjects"][key].get("quantity",1) for key in deviation["subjectIds"]) > deviation["quantityLimit"]:
                    self.error(f"{evaluation['id']}: deviation quantity limit exceeded")
            rule = d["decisionRules"][evaluation["decisionRuleId"]]
            if "verificationId" in requirement and d["verifications"][requirement["verificationId"]]["decisionRuleId"] != rule["id"]:
                self.error(f"{evaluation['id']}: evaluation uses wrong verification decision rule")
            if rule["method"] == "report-only" and evaluation["conformance"] in {"pass","fail"}:
                self.error(f"{evaluation['id']}: report-only rule cannot assert conformance")
            self.numeric_evaluation(evaluation,requirement,rule,observations)
        for scan in a["scans"].values():
            run = a["runs"][scan["runId"]]
            if run["kind"] != "scan" or not set(scan["subjectIds"]) <= set(run["subjectIds"]):
                self.error(f"{scan['id']}: scan run scope/kind mismatch")
            if scan["equipmentId"] not in run["equipmentIds"]:
                self.error(f"{scan['id']}: scan equipment not in run")
            if self.resources[scan["resourceId"]]["role"] != "evidence":
                self.error(f"{scan['id']}: actual scan must have evidence resource role")
            if not at_time(run["startedAt"]) <= at_time(scan["capturedAt"]) <= at_time(run["endedAt"]):
                self.error(f"{scan['id']}: scan date is outside run")
            registration = scan["registration"]
            if registration["method"] == "datum-system" and "datumSystemId" not in registration:
                self.error(f"{scan['id']}: datum registration needs datumSystemId")
            frame = d["coordinateFrames"][registration["designFrameId"]]
            if any(a["subjects"][s]["productDefinitionId"] != frame["productDefinitionId"] for s in scan["subjectIds"]):
                self.error(f"{scan['id']}: scan design frame belongs to another product")
            if "datumSystemId" in registration and d["datumSystems"][registration["datumSystemId"]]["productDefinitionId"] != frame["productDefinitionId"]:
                self.error(f"{scan['id']}: registration datum system belongs to another product")
        self.check_fai()

    def numeric_evaluation(self, evaluation, requirement, rule, observations):
        if rule["method"] not in {"simple-limits","guard-band"}: return
        if requirement["kind"] not in {"dimension","surface-texture","performance"}: return
        bounds = requirement["spec"].get("limits")
        if not bounds:
            if evaluation["conformance"] in {"pass","fail"}:
                self.error(f"{evaluation['id']}: basic/reference characteristic has no acceptance limits")
            return
        for observation in observations:
            if observation["value"]["kind"] != "scalar":
                self.error(f"{evaluation['id']}: simple scalar limits require scalar observations"); continue
            q = observation["value"]["quantity"]
            try:
                value = convert(q["value"],q["unit"],bounds["unit"])
                guard = convert(rule["guardBand"]["value"],rule["guardBand"]["unit"],bounds["unit"]) if rule["method"] == "guard-band" else Decimal(0)
                if guard < 0: raise PackageError("Negative guard band")
                low = Decimal(bounds["lower"])+guard if "lower" in bounds else None
                high = Decimal(bounds["upper"])-guard if "upper" in bounds else None
                if low is not None and high is not None and low > high: raise PackageError("Guard band removes acceptance interval")
                passed = ((low is None or (value >= low if bounds["lowerInclusive"] else value > low)) and
                          (high is None or (value <= high if bounds["upperInclusive"] else value < high)))
                if evaluation["conformance"] in {"pass","fail"} and (evaluation["conformance"] == "pass") != passed:
                    self.error(f"{evaluation['id']}: reported conformance disagrees with checked scalar limits")
                if "uncertainty" in observation:
                    uncertainty = observation["uncertainty"]["expanded"]
                    convert(uncertainty["value"],uncertainty["unit"],q["unit"])
                    if "verificationId" in requirement:
                        maximum = self.d["verifications"][requirement["verificationId"]].get("maximumExpandedUncertainty")
                        if maximum and convert(uncertainty["value"],uncertainty["unit"],maximum["unit"]) > Decimal(maximum["value"]):
                            self.error(f"{observation['id']}: uncertainty exceeds verification limit")
                elif "verificationId" in requirement and "maximumExpandedUncertainty" in self.d["verifications"][requirement["verificationId"]]:
                    self.error(f"{observation['id']}: verification requires reported uncertainty")
            except PackageError as exc:
                self.error(f"{evaluation['id']}: {exc}")

    def check_fai(self):
        for fai in self.a["faiReports"].values():
            applicable = {(subject_id,r["id"]) for subject_id in fai["subjectIds"]
                          for r in self.d["requirements"].values() if self.applies(r,self.a["subjects"][subject_id])}
            declared = set(fai["requirementIds"])
            for evaluation_id in fai["evaluationIds"]:
                evaluation = self.a["evaluations"][evaluation_id]
                if evaluation["subjectId"] not in fai["subjectIds"] or evaluation["requirementId"] not in declared:
                    self.error(f"{fai['id']}: evaluation lies outside FAIR scope")
            if fai["type"] == "partial":
                baseline = fai["baseline"]
                if self.resources[baseline["resourceId"]]["sha256"] != baseline["sha256"]:
                    self.error(f"{fai['id']}: baseline hash mismatch")
                if self.resources[baseline["resourceId"]]["role"] != "baseline-as-built":
                    self.error(f"{fai['id']}: baseline needs baseline-as-built resource role")
                self.warn(f"Partial FAIR inherited accountability not implemented: {fai['id']}")
            elif not {r for _,r in applicable} <= declared:
                self.error(f"{fai['id']}: full FAIR omits applicable requirement IDs")
            if fai["status"] == "complete":
                if not fai["approvalIds"]:
                    self.error(f"{fai['id']}: complete FAIR needs approval")
                accepted = {(e["subjectId"],e["requirementId"]) for key in fai["evaluationIds"]
                            for e in [self.a["evaluations"][key]] if e["conformance"] in {"pass","fail"}
                            and e["disposition"] in {"accepted","accepted-under-deviation"}}
                needed = applicable if fai["type"] == "full" else {(s,r) for s,r in applicable if r in declared}
                if not needed <= accepted:
                    self.error(f"{fai['id']}: complete FAIR lacks accepted evaluations for subject/characteristic scope")

    def report(self):
        return {"formatVersion":VERSION, "valid":not self.errors,
                "checked":"archive, inventory, schema and selected graph/numeric invariants",
                "geometryConformance":"not-assessed", "semanticSupport":"partial-prototype",
                "engineeringCompleteness":"not-assessed", "actualAcceptance":"not-assessed",
                "errors":self.errors, "warnings":self.warnings}


def validate_package(path: Path):
    return Checker(read_package(path)).check()
