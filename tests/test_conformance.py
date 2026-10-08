"""Regression cases for exchange risks; these do not certify engineering semantics."""
import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from opp import Checker, PackageError, VERSION, json_bytes, read_package, sha, strict_json, validate_package
from build_examples import archive_bytes
from jsonschema import Draft202012Validator


class ExchangeChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = {p.name:read_package(p) for p in (ROOT/"examples/unpacked").iterdir() if p.is_dir()}

    def files(self,name="block-as-built"):
        return dict(self.fixtures[name])

    def edit(self,files,path,change):
        document = strict_json(files[path])
        change(document)
        files[path] = json_bytes(document)
        self.rehash(files)

    def rehash(self,files):
        manifest = strict_json(files["manifest.json"])
        for resource in manifest["resources"]:
            data = files[resource["path"]]
            resource["sha256"],resource["size"] = sha(data),len(data)
        files["manifest.json"] = json_bytes(manifest)

    def reject(self,files,fragment):
        report = Checker(files).check()
        self.assertFalse(report["valid"],report)
        self.assertTrue(any(fragment in error for error in report["errors"]),report["errors"])

    def test_examples_check_without_claiming_engineering_certification(self):
        for name in self.fixtures:
            with self.subTest(name=name):
                report = validate_package(ROOT/"examples/packages"/(name+".opp"))
                self.assertTrue(report["valid"],report["errors"])
                self.assertEqual(report["geometryConformance"],"not-assessed")
                self.assertEqual(report["actualAcceptance"],"not-assessed")
                self.assertTrue(report["warnings"])

    def test_as_built_copies_the_exact_design_closure(self):
        for design,actual in [("block-design","block-as-built"),("block-design","lot-as-built"),("assembly-design","assembly-as-built")]:
            for path,data in self.fixtures[design].items():
                if path != "manifest.json":
                    self.assertEqual(data,self.fixtures[actual][path],f"{actual}: {path}")

    def test_archives_are_deterministic_and_match_sources(self):
        for name,files in self.fixtures.items():
            self.assertEqual(archive_bytes(files),(ROOT/"examples/packages"/(name+".opp")).read_bytes())

    def test_corrupted_raw_evidence_is_detected(self):
        files=self.files();files["evidence/test.csv"]+=b"2000,0.1\n"
        self.reject(files,"SHA-256 mismatch")

    def test_design_snapshot_hash_cannot_be_changed_independently(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["designSnapshot"].update(sha256="0"*64))
        self.reject(files,"designSnapshot SHA-256")

    def test_geometry_cannot_be_swapped_while_retaining_the_same_design_hash(self):
        files=self.files()
        files["geometry/block.step"]+=b"\n/* new geometry serialization */\n"
        digest=sha(files["geometry/block.step"])
        self.edit(files,"design/bindings.json",lambda d:[b.update(resourceSha256=digest) for b in d["bindings"]])
        self.reject(files,"Design resource pin does not match inventory")

    def test_design_hash_must_cover_its_binding_resource(self):
        files=self.files("block-design")
        self.edit(files,"design/design.json",lambda d:d.update(resourcePins=[p for p in d["resourcePins"] if p["resourceId"]!="res-bindings"]))
        self.reject(files,"Design closure resource lacks a hash pin: res-bindings")

    def test_zip_traversal_is_rejected_before_resource_loading(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/"bad.opp"
            with zipfile.ZipFile(path,"w") as archive:archive.writestr("../outside.txt","no")
            with self.assertRaisesRegex(PackageError,"Unsafe"):read_package(path)

    def test_case_colliding_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/"bad.opp"
            with zipfile.ZipFile(path,"w") as archive:
                archive.writestr("data.json","{}");archive.writestr("DATA.json","{}")
            with self.assertRaisesRegex(PackageError,"case-colliding"):read_package(path)

    def test_duplicate_json_keys_are_not_silently_overwritten(self):
        with self.assertRaisesRegex(PackageError,"duplicate JSON key"):
            strict_json(b'{"value":"pass","value":"fail"}')

    def test_reflection_cannot_make_an_opposite_hand_part(self):
        files=self.files("assembly-design")
        self.edit(files,"design/design.json",lambda d:d["occurrences"][0]["transform"]["rotation"].__setitem__(0,"-1"))
        self.reject(files,"determinant +1")

    def test_recursive_product_containment_is_rejected(self):
        files=self.files("assembly-design")
        self.edit(files,"design/design.json",lambda d:d["occurrences"][2].update(childDefinitionId="def-pair-a"))
        self.reject(files,"assembly containment: cycle")

    def test_state_is_bound_to_the_correct_product(self):
        files=self.files("assembly-design")
        self.edit(files,"design/design.json",lambda d:d["regions"][0].update(stateId="state-module-finished"))
        self.reject(files,"state belongs to another product")

    def test_reused_subassembly_needs_full_occurrence_context(self):
        files=self.files("assembly-as-built")
        self.edit(files,"actual/as-built.json",lambda d:d["subjects"][-1].update(occurrencePath=["occ-block"]))
        self.reject(files,"invalid occurrence path")

    def test_distinct_physical_parts_cannot_share_serial_identity(self):
        files=self.files("assembly-as-built")
        self.edit(files,"actual/as-built.json",lambda d:d["subjects"][-1].update(serialNumber=d["subjects"][-2]["serialNumber"]))
        self.reject(files,"Duplicate physical serial identity")

    def test_binding_must_resolve_to_an_entity_of_the_declared_type(self):
        files=self.files("block-design")
        self.edit(files,"design/bindings.json",lambda d:d["bindings"][0]["entities"][0].update(label="#999999"))
        self.reject(files,"missing or wrong STEP entity")

    def test_comments_cannot_spoof_step_entity_binding(self):
        files=self.files("block-design")
        files["geometry/block.step"]+=b"\n/* #999999=ADVANCED_FACE('spoof'); */\n"
        digest=sha(files["geometry/block.step"])
        def change(d):
            for b in d["bindings"]:b["resourceSha256"]=digest
            d["bindings"][0]["entities"][0]["label"]="#999999"
        self.edit(files,"design/bindings.json",change)
        self.reject(files,"missing or wrong STEP entity")

    def test_measurement_units_must_match_the_characteristic(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["observations"][0]["value"]["quantity"].update(unit="N"))
        self.reject(files,"incompatible units")

    def test_unilateral_offsets_do_not_force_nominal_inside_limits(self):
        files=self.files("block-design")
        self.edit(files,"design/design.json",lambda d:d["requirements"][1]["spec"].update(nominal={"value":"19.000","unit":"mm"}))
        report=Checker(files).check()
        self.assertTrue(report["valid"],report["errors"])

    def test_failed_width_does_not_become_a_pass_under_concession(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["evaluations"][1].update(conformance="pass"))
        self.reject(files,"reported conformance disagrees")

    def test_concession_cannot_apply_to_another_characteristic(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["deviations"][0].update(requirementIds=["req-height"]))
        self.reject(files,"deviation scope mismatch")

    def test_rework_authorization_is_not_final_use_as_is_acceptance(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["deviations"][0].update(disposition="rework"))
        self.reject(files,"not a final use-as-is")

    def test_calibration_must_be_valid_at_measurement_date(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["calibrations"][0].update(validUntil="2026-09-01T00:00:00Z"))
        self.reject(files,"calibration invalid at run date")

    def test_observation_must_be_inside_the_declared_run(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["observations"][0].update(observedAt="2026-09-01T00:00:00Z"))
        self.reject(files,"observation date is outside run")

    def test_evaluation_cannot_use_other_physical_parts_result(self):
        files=self.files("assembly-as-built")
        def change(d):
            target=next(e for e in d["evaluations"] if e["id"]=="right-evaluation-length")
            target["observationIds"]=["left-observation-length"]
        self.edit(files,"actual/as-built.json",change)
        self.reject(files,"observation subject/requirement mismatch")

    def test_complete_fair_cannot_omit_an_accounted_characteristic_result(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["faiReports"][0]["evaluationIds"].pop())
        self.reject(files,"complete FAIR lacks accepted evaluations")

    def test_negative_uncertainty_is_rejected(self):
        files=self.files()
        self.edit(files,"actual/as-built.json",lambda d:d["observations"][0]["uncertainty"]["expanded"].update(value="-0.001"))
        self.reject(files,"invalid uncertainty")

    def test_gdt_family_cannot_be_silently_switched(self):
        files=self.files("block-design")
        self.edit(files,"design/design.json",lambda d:d["interpretations"][1].update(profileId="opp.requirements"))
        self.reject(files,"profile does not match its GD&T family")

    def test_missing_normative_dependencies_remain_visible(self):
        report=Checker(self.files("block-design")).check()
        self.assertTrue(any("Normative dependency recipient-supplied" in warning for warning in report["warnings"]))

    def test_lot_sampling_does_not_claim_population_acceptance(self):
        report=Checker(self.files("lot-as-built")).check()
        self.assertTrue(any("population acceptance not assessed" in warning for warning in report["warnings"]))
        actual=strict_json(self.fixtures["lot-as-built"]["actual/as-built.json"])
        self.assertEqual(actual["faiReports"][0]["status"],"incomplete")

    def test_strict_cli_rejects_incomplete_semantic_claims(self):
        process=subprocess.run([sys.executable,str(ROOT/"tools/validate.py"),str(ROOT/"examples/packages/block-design.opp"),"--strict"],capture_output=True,text=True)
        self.assertEqual(process.returncode,1)
        self.assertTrue(json.loads(process.stdout)["valid"])

    def test_mapping_register_is_structured_and_does_not_claim_an_importer(self):
        mapping=json.loads((ROOT/"mappings/v0/step-crosswalk.json").read_text())
        schema=json.loads((ROOT/"mappings/v0/step-crosswalk.schema.json").read_text())
        Draft202012Validator(schema).validate(mapping)
        ids=[row["id"] for row in mapping["mappings"]]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(all(row["implementation"]=="not-implemented" for row in mapping["mappings"]))


if __name__ == "__main__":unittest.main()
