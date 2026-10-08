# Capabilities and process profiles

A package lists exact profile IDs/versions and whether understanding them is required. A reader returns its support per profile. Unknown required semantics prevent complete interpretation, even if metadata and geometry can be shown safely. Profile declarations describe the file's needs, not a claim that this checker implements those engineering rules.

## Initial proposed profiles

| ID | Purpose | Draft maturity |
| --- | --- | --- |
| `opp.core` | Inventory, identity, product graph, explicit units/authority. | Structural prototype implemented. |
| `opp.geometry.step-part21` | Single-section exact STEP payload and entity-set bindings. | Label/hash checks implemented; kernel conformance pending. |
| `opp.dimensions` | Explicit nominal and absolute dimension bounds. | Selected numeric/reference checks implemented. |
| `opp.gdt.asme` / `opp.gdt.iso` | Declared interpretation of GD&T. | Experimental; full semantic implementation pending. |
| `opp.requirements` | Material, surface, performance, and other typed requirement families. | Serialization proposed; individual engineering semantics pending. |
| `opp.as-built` | Physical subjects, genealogy, actual evidence, disposition. | Structural/reference prototype implemented. |
| `opp.scan` | Unit/registration/evidence identity. | Metadata proposed; scan geometry validation pending. |
| `opp.fai` | Full/partial accountability and baseline records. | Selected coverage checks implemented; AS9102 profile pending. |

All above use `0.1.0-draft.1`. New exact-boundary, signatures, process, sampling, or evidence profiles need their own RFCs and versioned conformance cases. A `build-to-print` designation is a future aggregate claim, not currently granted by this repository.

## Process-family coverage design

These are proposed vocabulary domains for `process-constraint.controls`; control names are not yet a stable registry. Each control must carry a typed criterion and applicable region/state. Independent companies should not invent incompatible spellings and then claim interoperability.

| Family | Design constraints | Useful actual records |
| --- | --- | --- |
| Machining/grinding/EDM | Stock allowance, thread completion, tool marks, edge/burr, recast layer, post-treatment size. | Machine/cell, operator, operation dates, tool/fixture IDs, final dimensions and surface measurements. |
| Molding/overmolding | Resin/condition, regrind, color, gate/parting/ejector regions, draft, flash/sink/warp, insert and adhesion. | Resin batch/drying, mold/cavity, press/cell, shot/date, actual temperatures/pressures, appearance and dimensional results. |
| Additive | Process/feedstock, orientation/support-contact restrictions, lattice/material assignment, powder removal, density/defects, coupons, postprocessing. | Machine/build ID, powder genealogy/reuse, build date/operator, settings, oxygen/thermal logs, CT/scans, coupon/test links. |
| Casting | As-cast/finished states, allowances, wall/core shift, porosity/soundness zones, repair permissions, leak/NDT criteria. | Heat/melt/pour/lot, mold/cell, treatment, repair history, radiography/CT/leak/coupon evidence. |
| Forging | Grain flow/orientation, reduction, allowance, flash/die match, defect/heat-treatment criteria. | Billet heat, die/press, operation temperatures/date, treatment and mechanical/NDT evidence. |
| Stamping/drawing/bending | Sheet/thickness/grain, flat/formed geometry, bend/thinning/springback, burr side, cosmetic zones. | Coil/heat, die/press/cell, setup/lot/date, formed scans, thickness and bend measurements. |
| Cutting | Stock/contour intent, bevel/taper, edge quality, dross/HAZ, pierce/tab restrictions. | Sheet/heat/lot, machine/cell/date, cut quality and dimensional evidence. |
| Joining | Joint/weld/braze/bond, material/procedure qualifications, torque/preload/cure, distortion/inspection. | Installed physical components, filler/adhesive batch, welder/operator, torque/cure logs, NDT and proof/leak tests. |
| Composites | Layup materials/orientations/boundaries, cores, cure, bondlines, void/delamination zones. | Ply/batch/roll genealogy, layup operator/date, cure equipment/log, ultrasonic/CT/trim inspection. |
| Powder/MIM/ceramics/elastomers/extrusion | Green/sintered states, density/shrinkage, binder removal, durometer, compression set, seam/straightness. | Feedstock/batch, process/cell/date, thermal history, scans and material/performance tests. |

Detailed layup/lattice topology, CT field semantics, arbitrary graded material fields, exact thermal cycles, and complete sampling statistics are reserved extension/profile work. V0 provides linked evidence and explicit unsupported status rather than pretending a generic object is universally understood.

