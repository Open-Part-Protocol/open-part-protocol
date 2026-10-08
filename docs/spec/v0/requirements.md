# Engineering requirements

Every requirement has an ID, typed `kind`, readable name, one or more explicit subjects, product `stateId`, `interpretationId`, criticality, typed `spec`, and explicit override IDs. A characteristic number is a presentation/FAIR label, not the permanent identifier.

A requirement applies to the declared geometry/feature/occurrence **in the declared state** under the declared rules. Information about a preferred process is not a requirement unless the engineer explicitly prescribes it. All records in `requirements` are normative; informal suggestions belong in reference documents or optional extensions.

## Typed families in V0

| Kind | Structured information |
| --- | --- |
| `dimension` | Characteristic (size/location/angle), nominal, absolute inclusive/exclusive limits, basic/reference/toleranced mode, direction/frame, related subjects, display precision. |
| `geometric-tolerance` | Ordered segments with characteristic, tolerance zone/value, datum-system reference, modifiers, offsets, projected zone, maximum tolerance, and relationship. |
| `material` | Required material definition, explicit alternatives, substitution approval rule. |
| `surface-texture` | Ra/Rq/Rz/Rt or areal parameters, limits, cutoff/evaluation length, filter, lay, method. |
| `coating` | Layer stack, processes/materials, thickness ranges, specifications, exclusions, dimensional basis, color/gloss. |
| `heat-treatment` | Process, temperature/time ranges, hardness/case depth, specification, required sequence. |
| `edge-condition` | Deburr/chamfer/radius/keep-sharp, size limits, maximum burr, exclusions. |
| `thread` | Exact designation/standard, handedness, pitch, engagement, gauge specification. |
| `process-constraint` | Process family and named controls using range, allowed values, boolean, direction/frame, or exact document-clause criteria. |
| `weld` / `bond` / `fastener` | Joint/process/filler/repair constraints; adhesive/bondline/cure; torque/preload/lubrication/sequence. |
| `performance` | Measured characteristic, bounds, explicit loading/environmental conditions, and test procedure. |
| `cleanliness` | Typed criterion and procedure. |
| `marking` | Required identity fields, literal content, method, size/depth; subject identifies location. No executable templating. |
| `packaging` | Required protection, preservation/handling conditions, procedure. |
| `certification` | Required certificate/report/declaration type, governing documents, issuer qualifications. |
| `unresolved-text` | Preserved normative text requiring human interpretation; blocks fully structured support. |

The schema prevents one family's fields being accidentally accepted as another family's core meaning. The breadth of this table is a data-design proposal; specialized semantics are [experimental profiles](profiles.md) until reviewed and independently tested.

## Dimensions and GD&T

Absolute limits are independent of nominal values and display rounding. Basic and reference dimensions do not carry manufacturing acceptance limits. Size and location are distinct engineering concepts; a location needs its related subjects and orientation. An adapter must preserve whether a measure refers to inside/outside/center, a derived axis, or a physical face; unsupported conventions require a profile or a conversion exception.

GD&T does not become fully defined by a symbol and a decimal. The interpretation family and exact standard editions, controlled feature, zone geometry, ordered datum compartments/modifiers, material requirements, and state all matter. ASME/ISO semantics must never be switched silently. Datum A|B|C is different from A|C|B and from A|B(M)|C. See the [CAx-IF PMI practice](https://www.mbx-if.org/home/wp-content/uploads/2024/06/rec_pracs_pmi_v41.pdf), §6.9.

The V0 schema can express segments and several common modifiers. Datum-target degrees of freedom, fully specified complex profile-zone constructions, specialized feature-pattern rules, and all possible compound GD&T combinations still need specialist profiles. Schema acceptance of a combination is not evidence that the combination is physically meaningful or implemented.

## Defaults, overrides, and exclusions

V0 deliberately has no implicit title-block defaults or automatic “tightest tolerance wins” rule. A released package materializes general obligations onto explicit subjects/characteristics. `overridesRequirementIds` identifies the exact superseded obligation; the override must have compatible subject/state scope. Override cycles are invalid. Readers show the effective requirement and its source chain.

Coating/masking exclusions identify subjects explicitly. Before/after coating dimensions refer to different states as needed. A masking region that selects part of a face needs an exact boundary, not an approximate preview. [Geometry bindings](geometry-bindings.md) explain the current partial-region limit.

## Verification

`Verification` lists the requirement IDs it covers, method constraints, decision rule, coverage (every instance/sample/first article/lot), equipment kinds, environmental conditions, optional procedure, and maximum expanded uncertainty.

`DecisionRule` selects simple inclusive/exclusive limits, a stated guard band, manual review, or report-only. Guard band narrows acceptance bounds; it does not alter design limits. A report-only result cannot assert conformance. General uncertainty-based risk rules, sampling-plan statistics, and complex GD&T evaluation remain separate profile work.

