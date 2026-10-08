#!/usr/bin/env python3
"""Rebuild deterministic synthetic fixture inventories and .opp archives."""
import argparse
import io
import sys
import zipfile
from pathlib import Path
from opp import ROOT, PackageError, json_bytes, sha, strict_json, validate_package, walk


def archive_bytes(files):
    target = io.BytesIO()
    with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in ["manifest.json",*sorted(set(files)-{"manifest.json"})]:
            entry = zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry,files[name],compresslevel=9)
    return target.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true",help="Check freshness without modifying files")
    args = parser.parse_args()
    failures = []
    for folder in sorted((ROOT/"examples/unpacked").iterdir()):
        if not folder.is_dir(): continue
        files = {p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob("*") if p.is_file()}
        manifest = strict_json(files["manifest.json"])
        design_resource = next(r for r in manifest["resources"] if r["id"] == manifest["designResourceId"])
        design = strict_json(files[design_resource["path"]])
        design.pop("resourcePins",None)
        needed = {manifest["bindingsResourceId"]}
        fields = {"resourceId","sourceResourceId","boundaryResourceId","previewResourceId",
                  "certificateResourceId","evidenceResourceIds","budgetResourceId","settingsResourceId"}
        for _,node in walk(design):
            for key,value in node.items():
                if key in fields:
                    needed.update(value if isinstance(value,list) else [value])
        resource_by_id = {r["id"]:r for r in manifest["resources"]}
        design["resourcePins"] = [{"resourceId":key,"sha256":sha(files[resource_by_id[key]["path"]])} for key in sorted(needed)]
        files[design_resource["path"]] = json_bytes(design)
        if manifest["packageType"] == "as-built":
            actual_resource = next(r for r in manifest["resources"] if r["id"] == manifest["asBuiltResourceId"])
            actual = strict_json(files[actual_resource["path"]])
            actual["designSnapshot"]["sha256"] = sha(files[design_resource["path"]])
            files[actual_resource["path"]] = json_bytes(actual)
        for resource in manifest["resources"]:
            data = files[resource["path"]]
            resource["sha256"],resource["size"] = sha(data),len(data)
        files["manifest.json"] = json_bytes(manifest)
        # Check in-memory generated contents before writing any package.
        from opp import Checker
        report = Checker(files).check()
        if not report["valid"]:
            failures.append(f"{folder.name}: " + "; ".join(report["errors"]))
            continue
        archive = archive_bytes(files)
        destination = ROOT/"examples/packages"/(folder.name+".opp")
        if args.check:
            stale = [name for name,data in files.items() if (folder/name).read_bytes() != data]
            if stale or not destination.is_file() or destination.read_bytes() != archive:
                failures.append(f"{folder.name}: generated inventory/archive is stale")
        else:
            for name,data in files.items(): (folder/name).write_bytes(data)
            destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_bytes(archive)
            print(f"Built {destination.relative_to(ROOT)}")
    for failure in failures: print(failure,file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
