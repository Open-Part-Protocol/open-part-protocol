# Conformance and validation

Conformance results are independent. A single green “valid” badge must not imply manufacturing acceptance.

| Layer | Question | Reference checker |
| --- | --- | --- |
| Archive safety/integrity | Can the package be opened within limits; do resources and hashes agree? | Implemented for the V0 ZIP subset. |
| Serialization | Do manifest and semantic JSON conform to the exact schemas? | JSON Schema 2020-12, locally resolved. |
| Graph consistency | Do IDs, ownership/state, occurrence paths, transforms, snapshots, actual links, and selected coverage rules agree? | Selected invariants implemented and regression-tested. |
| Geometry | Is the STEP valid under its EXPRESS schema, nominal shape valid, and binding semantically correct? | Not assessed; simple label/type existence only. |
| Semantic support | Does a reader implement all required engineering rules and extensions? | Profile needs reported; no complete GD&T/process support claimed. |
| Engineering completeness | Has an authorized engineer specified and released a sufficient build-to-print definition? | Author declarations shown; not certified. |
| Actual acceptance | Are observations trustworthy, decision rules correct, calibration suitable, and disposition authorized? | Selected reference/numeric checks; no certification. |

## Implemented invariants

The checker validates unique IDs, typed references, product/state consistency, acyclic definition/frame/actual containment and supersession graphs, rigid transforms, geometry-resource/hash/entity references, document dependencies, exact embedded design hash, physical occurrence paths, run/equipment/calibration relationships, timestamps, scalar unit/range comparisons for simple dimension/performance/texture limits, evaluation/observation scope, concession scope, and selected full-FAIR completeness rules.

Declared support is intentionally narrower than the prose. It does not evaluate arbitrary compound requirements, all GD&T constraints, parameter interactions, sampling statistics, standard-specific surface-texture rules, certificate authenticity, or proprietary process qualifications. Partial FAIR baseline contents are structurally preserved and hashed; full edition-specific inherited accountability remains unimplemented and is reported as such.

## Results and exit codes

`tools/validate.py` returns a JSON report. `valid: true` means the implemented package/schema/reference checks passed. `geometryConformance`, `engineeringCompleteness`, and `actualAcceptance` remain `not-assessed`; warnings identify normative dependencies, experimental content, and required extensions.

Exit 0 means implemented checks passed; exit 1 means a checked invariant failed; exit 2 means the checker/runtime could not inspect the input. `--strict` additionally rejects known incomplete/unsupported semantic or dependency claims; it still cannot certify engineering or geometric completeness. The synthetic examples intentionally use review-state designs and report their limitations.

## Before claims of interoperability

Publish exporter/reader versions, exact AP242 schemas and recommended-practice revisions, passed public fixtures, information-loss reports, geometry/binding comparisons, and required profiles. Test independent implementations and round trips without silently healing authority conflicts.

Use NIST SFA as a STEP analysis reference and the NIST PMI fixtures as future interoperability inputs, subject to their terms. [The interoperability plan](../../interoperability/viewer-plan.md) separates proposed work from implemented capabilities.

