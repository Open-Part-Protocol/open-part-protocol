# As-built and evidence

An as-built package contains all design information needed for the selected product plus additional actual data. `AsBuilt.designSnapshot` pins the embedded design resource ID, design object ID, and SHA-256. Its design closure is copied byte-for-byte, including bindings and nominal geometry. See [the as-built schema](../../../schemas/v0/as-built.schema.json).

## Physical identity and actual configuration

`subjects` are `instance` or `lot` records. An instance can carry a serial number, lot association, manufacture date, manufacturer, and external identity. A lot requires its lot number and explicit population count; it does not pretend to be one serialized item.

Every subject names its exact design product and an occurrence path from the design root. Nested physical assemblies additionally reference `parentSubjectId`. Two reused occurrences must never collapse into one physical identity. An assembly's actual BOM is the set of recorded physical subjects and their containment, not a mutated design BOM.

V0 records only the included physical scope. Unrecorded children, substituted components, untracked lot members, and unresolved genealogy must remain visible; an assembly identity alone cannot certify all descendants. Alternative installed parts require explicit approved deviation and a suitable design/profile before a complete actual-configuration claim.

## Actual collections

| Collection | Data captured |
| --- | --- |
| `actors` | Companies, operators/inspectors, quality approvers, software identity. |
| `productionCells` | Organization, site, line, and named production cell. |
| `equipment` | Machine, measurement equipment, fixture/test rig; manufacturer/model/serial, software/firmware, resolution and ranges. |
| `calibrations` | Equipment, calibration date and validity, calibration organization, certificate, traceability statements, uncertainty/status. |
| `materialLots` | Material definition, supplier lot/heat/batch, certificates, affected subjects, feedstock/parent-lot genealogy. |
| `productionEvents` | Subject scope, process, start/end dates, company, operators, cell/machines, materials, actual settings, procedures/evidence, supersession. |
| `runs` | Inspection/test/scan/material/document review; date range, operators/company, equipment/calibration, method, conditions, sampling population/sample count. |
| `observations` | Stable design characteristic link, physical subject/state/run, observation date, typed value, uncertainty, evidence, retest supersession. |
| `evaluations` | Requirement, subject, observations, decision rule, evaluator/date, reported conformance, disposition, deviation, rationale. |
| `scans` | Point cloud/mesh/CT resource, unit, capture date, subject/equipment/run, registration to a design frame, uncertainty and processing metadata. |
| `deviations` | Affected subjects/requirements, approved disposition, date/expiry/quantity scope, approval/evidence IDs. |
| `faiReports` | Full/partial FAIR scope, characteristic accountability, evaluation/material/process/deviation/approval links, optional rendered report, pinned partial baseline. |
| `approvals` | Reported inspection/quality/customer acceptance statements and evidence. |

## Measurements and performance

Scalar values use `Quantity`; boolean/text/vector/resource values are explicitly discriminated. `characteristicPath` locates the measured part of a compound requirement using a JSON Pointer into that requirement. A time series can be a CSV or other evidence resource whose column meanings/units are declared in a procedure or supported evidence profile. Never infer units from a filename.

Observation, production, and test dates are distinct. Runs identify actual temperature/loading, sample scope, measurement equipment, and calibration used. Expanded uncertainty includes a coverage factor and method; optional budget data is another hashed resource. Equipment validity is evaluated at the run/observation date, not the date the package was opened.

Lot observations represent their explicitly stated sample/lot scope. A sampled pass is not evidence that every lot member was individually measured. Sample identities or aggregation semantics need an inspection profile before automated population acceptance.

## Scans and registration

Nominal geometry and actual scans are separate resource roles. A scan never replaces design geometry. `registration` records datum-system/best-fit/fiducial/none, a design frame, and the transform `p_design = R × p_scan + t` with declared scan/translation/design units. Datum-system registration requires its datum-system ID. Best-fit registration must not be silently used to establish datum-based GD&T compliance.

CT segmentation, meshing, filtering, alignment settings, coordinate provenance, uncertainty, and derived deviation maps should be retained as evidence or explicit extensions. The initial scan profile does not standardize every scanner's binary format.

## Conformance versus acceptance

`conformance` is pass/fail/indeterminate/not-inspected. `disposition` is accepted/rejected/pending/accepted-under-deviation. A failed result accepted under a concession remains **fail**. Approved rework is not final acceptance; new measurements must demonstrate the post-rework condition.

Retests link `supersedesObservationId`; events can link `supersedesEventId`. A later actual snapshot can pin `supersedesRecord`. Preserve earlier records and do not overwrite inconvenient measurements. The reference checker checks supersession cycles, but cannot establish the authenticity or authority of approval statements.

## FAIR scope

A full FAIR accounts for applicable requirements of its declared physical subjects. A partial FAIR includes the reason and a hashed baseline actual resource; unchanged-characteristic accountability cannot be inferred from a revision label alone. Missing, indeterminate, rejected, or unapproved results prevent a `complete` report. An accepted-under-deviation result needs an approved in-scope deviation.

FAIR fields are modeled to support AS9102-style accountability and broader quality evidence. This draft does not reproduce official forms or assert AS9102C compliance. The [quality crosswalk](../../interoperability/quality-mapping.md) identifies future edition-specific validation work.

