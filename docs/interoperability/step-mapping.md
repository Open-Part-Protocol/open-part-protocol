# STEP interoperability and V0 crosswalk

The initial path is **retain exact STEP geometry, translate supported semantics into OPP, preserve the source, and report every unsupported or conflicting item**. AP242 is an engineering information model; Part 21 is a serialization. A `.step` suffix alone identifies neither the AP nor its edition.

The [machine-readable crosswalk](../../mappings/v0/step-crosswalk.json) is a candidate implementation register. It records target paths, source entity families, evidence, loss conditions, and status. No STEP semantic importer/exporter is implemented in this first draft.

## Protocol and encoding strategy

| Input | V0 strategy |
| --- | --- |
| AP242 MIM, Part 21 | Primary semantic migration target. Pin exact schema/edition; inspect semantic PMI separately from graphics. |
| AP242 domain-model XML (`.stpx`) | Product-structure translation needs a distinct adapter and XML vocabulary mapping; do not reuse Part 21 locators. |
| AP203 / AP214 | Reuse geometry/assembly paths where supported; preserve annotations and missing semantics explicitly. Do not infer release completeness. |
| AP209 | Preserve analysis models/results as evidence until an analysis profile defines their meaning. |
| AP238 | Preserve manufacturing-plan/toolpath source records; required design constraints need explicit OPP requirements. |
| AP239 | Candidate future source for physical/lifecycle traceability; no claimed V0 actual mapping. |
| STEP edition-3 external references/anchors | Resolve required resources into package closure; keep original persistent IDs. Section-qualified bindings need a separate profile. |

## Core source relationships

| OPP target | STEP source constructs | Translation rule |
| --- | --- | --- |
| Product identity and revision | `PRODUCT`, `PRODUCT_DEFINITION_FORMATION`, `PRODUCT_DEFINITION` | Preserve part identity and exact formation/revision; don't call `PRODUCT_DEFINITION.id` the revision without inspecting its context. |
| Nominal representation | `PRODUCT_DEFINITION_SHAPE`, `SHAPE_DEFINITION_REPRESENTATION`, `ADVANCED_BREP_SHAPE_REPRESENTATION`, solid/topology entities | Preserve original geometry bytes; locate product and shape, record units/state, and keep topology identifiers. |
| Assembly occurrence | `NEXT_ASSEMBLY_USAGE_OCCURRENCE` | Reusable child definition plus distinct use; retain source occurrence identity. |
| Placement | `CONTEXT_DEPENDENT_SHAPE_REPRESENTATION`, `SHAPE_REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION`, `ITEM_DEFINED_TRANSFORMATION` | Resolve transform direction, frame units, and nested composition before emitting OPP placement. |
| Feature/region binding | `SHAPE_ASPECT`, `GEOMETRIC_ITEM_SPECIFIC_USAGE`, `ITEM_IDENTIFIED_REPRESENTATION_USAGE` | Retain complete associations and entity sets, not one guessed face. |
| Size/location/angle | `DIMENSIONAL_SIZE`, `DIMENSIONAL_LOCATION`, angular subtypes and characteristic representations | Preserve characteristic convention, orientation, nominal and limits, not only displayed text. |
| GD&T | `GEOMETRIC_TOLERANCE` subtypes, datum-reference and zone structures | Preserve characteristic/zone, modifiers and datum ordering; unsupported compound constructs remain unresolved. |
| Datums | `DATUM`, `DATUM_FEATURE`, target constructs, `DATUM_SYSTEM` and ordered compartments | Preserve physical datum features, targets, compartment order/common datum groups and modifiers. |
| Presentation | Annotation/draughting constructs and camera models | Derived/source visualization, not automatically a semantic requirement. |
| Validation properties | Property-definition and measure-representation chains | Preserve area/volume/centroid and original comparison tolerances for adapter checks. |

Assembly chain evidence: [Open CASCADE's translator documentation](https://occt3d.com/dev/doc/overview/html/occt_user_guides__step.html), “Assembly structure.” Dimension and datum association evidence: [CAx-IF PMI v4.1](https://www.mbx-if.org/home/wp-content/uploads/2024/06/rec_pracs_pmi_v41.pdf), §§5–6. The registry gives more specific pointers per mapping.

## Offset tolerances must be normalized correctly

Under CAx-IF's plus/minus representation, tolerance values are offsets from nominal, including cases where both offsets have the same sign. The value-range form instead uses named absolute limits. [CAx-IF PMI v4.1](https://www.mbx-if.org/home/wp-content/uploads/2024/06/rec_pracs_pmi_v41.pdf), §§5.2.3–5.2.4.

```text
STEP nominal 20.000 mm, lower offset +0.010 mm, upper offset +0.025 mm
OPP nominal 20.000 mm, absolute lower 20.010 mm, absolute upper 20.025 mm
```

An OPP nominal is not required to be inside its acceptance interval. Tolerance-class designations require edition-specific evaluation; never fabricate numeric limits from an incomplete fit string. Preserve the source designation and report a required interpretation profile until resolved.

## Persistent identity and downstream quality

Preserve original CAD/STEP persistent IDs as external identifiers and issue OPP characteristic IDs explicitly. The 2026 [CAx-IF/DMSC cross-domain practice](https://www.mbx-if.org/home/wp-content/uploads/2026/02/rec_prac_cross-domain_exchange_v10.pdf) describes AP242 edition 4 → QIF 3.0 traceability using persistent IDs. It informs OPP's design/result linkage; it is not evidence of a universal OPP mapping or feedback implementation.

## Loss and authority

A converter must emit an item per source engineering item: translated, preserved-only, unsupported, ambiguous, conflict, or intentionally omitted, with source resource/entity IDs, target IDs, mapping ID, severity, and reason. Graphic-only normative annotations and free-text notes do not count as translated engineering meaning. Store them and report the gap.

When imported STEP PMI disagrees with canonical OPP requirements, report a conflict and require engineering resolution. Geometry healing must return a source-topology map. Converting units or rewriting STEP entities requires new bindings/hashes. No nearest-face or nearest-text heuristic can quietly establish authority.

## CAD vendor adoption

1. Existing STEP export supplies exact geometry; a plug-in exports OPP metadata and reviewed requirements from the native API.
2. An AP242 importer bridges installed workflows with explicit loss reporting.
3. Native `.opp` exporters create IDs/bindings directly and declare tested capability profiles.
4. Independent CAD/CAM/metrology readers test the same public fixtures and publish exact-version support.

The synthetic examples use original AP203-style block geometry with manually authored OPP semantics. They do not demonstrate AP242 PMI conversion. The first AP242 fixture/import comparison is a [roadmap task](../project/roadmap.md).

