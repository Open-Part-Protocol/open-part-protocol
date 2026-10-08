# Open Part Protocol

**One file for what a part should be. One related file for what was actually built.**

Open Part Protocol (OPP) is a proposed free, open, community-governed exchange standard for mechanical parts and assemblies. An `.opp` file combines exact geometry, readable engineering requirements, assembly structure, and supporting records in an offline package.

The name is also a nod to Naughty by Nature's “O.P.P.”

**Status: V0 working draft — `0.1.0-draft.1`, October 7, 2026.** This repository contains a proposed specification, JSON Schemas, examples, a package checker, and an interoperability plan. It is an engineering discussion baseline, not an approved standard or a production CAD converter.

## Two core record types

| Record | Answers | Contents |
| --- | --- | --- |
| **Design** | What should this part or assembly be? | Released nominal geometry, identity/revision, materials, dimensions, GD&T, surface/process requirements, component occurrences, verification requirements, and interpretation rules. |
| **As-built** | What was this physical part, lot, or assembly actually like? | The exact embedded design snapshot, physical identities, production history, material genealogy, scans, measurements, tests, equipment/calibration, FAIR records, deviations, and approvals. |

Both use `.opp`. The manifest declares `packageType: "design"` or `"as-built"`. A product is separately a `part`, `assembly`, `kit`, or `consumable`; these are product kinds, not additional core exchange record types.

```text
Design .opp                         As-built .opp
  manifest.json                       manifest.json
  design/design.json                  design/design.json  ← exact snapshot
  design/bindings.json                 design/bindings.json
  geometry/block.step                 geometry/block.step
                                      actual/as-built.json
                                      evidence/scan.ply
                                      evidence/test.csv
                                      evidence/calibration.txt
```

OPP owns the structured engineering meaning. STEP initially supplies exact geometry and a migration path from established CAD export pipelines. Requirements can be read without a CAD kernel. Presentation is generated from the same meaning; a PDF or a preview does not become a competing source of authority.

## Start here

- [Documentation guide](docs/README.md) — paths for engineers, implementers, and contributors.
- [Project charter](docs/project/charter.md) — purpose, scope, and open governance.
- [V0 overview](docs/spec/v0/README.md) — specification status and object model.
- [Design model](docs/spec/v0/design.md) and [as-built model](docs/spec/v0/as-built.md).
- [STEP mappings](docs/interoperability/step-mapping.md) and [NIST SFA assessment](docs/interoperability/nist-sfa.md).
- [Schemas](schemas/v0/README.md), [examples](examples/README.md), and [roadmap](docs/project/roadmap.md).
- [OPP Viewer](https://github.com/Open-Part-Protocol/opp-viewer) — the independent native Rust prototype for Linux, Windows, and macOS.

## Try the draft

Python 3.11 or later is required for the reference package checker.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/build_examples.py
.venv/bin/python tools/validate.py examples/packages/block-design.opp
.venv/bin/python tools/validate.py examples/packages/block-as-built.opp
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/check_docs.py
```

The checker verifies package safety, inventory/hash consistency, JSON Schema, and selected cross-record invariants. Its successful result **does not certify geometric validity, complete GD&T interpretation, a build-ready engineering release, or AS9102 compliance**. See [conformance](docs/spec/v0/conformance.md) for the precise boundary.

## What is in this repository?

| Directory | Purpose |
| --- | --- |
| `docs/project/` | Charter, governance proposal, roadmap, terminology, and draft decisions. |
| `docs/spec/v0/` | Package format, common types, design/as-built semantics, bindings, profiles, and conformance. |
| `docs/interoperability/` | STEP/AP242 migration, QIF/FAI crosswalks, sources, and viewer plan. |
| `schemas/v0/` | Offline-resolvable JSON Schema 2020-12 definitions. |
| `mappings/v0/` | Machine-readable candidate STEP crosswalk, with evidence and maturity per row. |
| `examples/` | Unpacked source packages and generated `.opp` archives. All production data is synthetic. |
| `tools/`, `tests/` | A small reference checker, package builder, and conformance regression cases. |
| `rfcs/`, `.github/` | Public proposal process and GitHub contribution templates/checks. |

## Open by design

The original specification, schemas, examples, and tools in this repository are licensed under [Apache 2.0](LICENSE). No membership, paid document, proprietary service, or commercial CAD system is required to implement OPP itself. Third-party standards retain their own terms; references are not copies of those standards.

Siemens/NX, Boeing, NIST, CAD/CAM/metrology vendors, manufacturers, and independent engineers are prospective advisory participants. No affiliation, endorsement, participation, or implemented vendor support is claimed. See [governance](docs/project/governance.md).

