#!/usr/bin/env python3
"""Inspect an .opp archive or unpacked package without extracting or fetching."""
import argparse
import json
import sys
from pathlib import Path
from opp import PackageError, validate_package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--strict", action="store_true", help="Reject reported completeness/support warnings")
    args = parser.parse_args()
    try:
        report = validate_package(args.path)
    except PackageError as exc:
        print(json.dumps({"valid":False,"errors":[str(exc)]},indent=2))
        return 1
    except (OSError, RecursionError) as exc:
        print(json.dumps({"valid":False,"inspectionError":str(exc)},indent=2))
        return 2
    print(json.dumps(report,indent=2))
    return 1 if not report["valid"] or (args.strict and report["warnings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
