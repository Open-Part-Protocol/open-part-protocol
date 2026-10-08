# Quality, QIF, and AS9102-style records

OPP's actual model separates physical identity, raw observations, engineering evaluation, and acceptance. Quality adapters preserve exact design characteristic identifiers and actual scope; they must not rebuild identity from balloon numbers or rounded report text.

## QIF conceptual crosswalk

QIF covers model/PMI, plans, resources, results, and statistics. [DMSC QIF](https://qifstandards.org/), [ISO 23952:2020](https://www.iso.org/standard/77461.html).

| OPP | QIF area to map | Status |
| --- | --- | --- |
| Requirements/features/datums | Model and characteristic definitions/nominals | Candidate; exact element/type mapping pending. |
| Verification/decision rules | Plans/rules and characteristic-to-plan relationships | Candidate; sampling/risk semantics need explicit review. |
| Equipment/calibration | Resources, measurement-device identity and capabilities | Candidate; preserve certificates/uncertainty without inventing equivalence. |
| Physical subjects/runs/observations | Actual part/inspection/characteristic result records | Candidate; preserve actual instance, timestamps, units, uncertainty and source IDs. |
| Evaluation/disposition | Result status plus approval/deviation relationships | Candidate; check differences between conformance and business acceptance. |
| Statistics and scan/field data | Statistics and linked evidence resources | Preserve; no full numerical-field/statistical mapping in V0. |

These are conceptual targets, not QIF XPaths or a lossless adapter. The [2026 cross-domain practice](https://www.mbx-if.org/home/wp-content/uploads/2026/02/rec_prac_cross-domain_exchange_v10.pdf), §§5–6, provides a concrete persistent-ID research baseline. Review QIF 3.0 schemas and industrial result fixtures before claiming XML-level mappings.

## AS9102-style accountability

The three form families group part-number accountability, product/material/process accountability, and characteristic accountability/verification/compatibility. [IAQG SCMH communication pack](https://scmh.iaqg.org/wp-content/uploads/2022/07/SCMH-Communication-Pack-6JUL2022.pdf), section 3.2; [current IAQG FAI guidance entry point](https://scmh.iaqg.org/scmh-make/).

| Accountability group | OPP fields |
| --- | --- |
| Part identity/configuration | Design namespace/part/revision, physical serial/lot, actual assembly subject tree, `faiReports.type`, pinned partial baseline/reason. |
| Materials/special processes/tests | `materialLots`, supplier/company identities, certificates, `productionEvents`, procedures, equipment, actual test runs, raw evidence. |
| Characteristic verification | Requirement IDs/characteristic numbers, requirement state/interpretation, observations, equipment/calibration, reported evaluations, deviations and approvals. |
| Broader digital evidence | Raw 3D scans, CT references, performance curves, process logs, uncertainty budgets, retest history, genealogy. |

V0 has no official AS9102 form-number/field-number implementation and makes no AS9102C compliance claim. A future `opp.fai.as9102c` profile needs the complete applicable standard, customer requirements, field-level mappings, signatures/approval semantics, partial-FAI rules, and validated examples. Referencing a purchased standard does not make OPP itself a paid standard.

Preserve nonconformances even when accepted under an authorized concession. An actual record's FAIR completion statement is reported evidence, not certification by the package checker.

