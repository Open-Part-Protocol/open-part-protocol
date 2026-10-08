# Project charter

Open Part Protocol defines a self-contained exchange file for the released design and the recorded realization of a mechanical part or assembly, exchanged between independent parties for manufacturing, review, quoting, inspection, and acceptance.

The specification and implementation materials must be freely accessible, publicly developed, and royalty-free to implement. Community governance must permit effective participation without paid membership. No company, geometry kernel, proprietary portal, or hosting service owns the meaning of an OPP file.

## Principles

- Human-readable structured semantics with exact, machine-resolvable references.
- Offline operation and explicit dependencies.
- Exact nominal geometry, initially reusing STEP B-rep.
- One authority for each engineering fact; explicit source, derived, nominal, and measured roles.
- Honest migration: loss and unsupported content remain visible.
- Stable characteristic identity from design through actual evidence.
- Simple metadata access without a CAD kernel.
- Public versioning, review, issue tracking, fixtures, and interoperability results.
- Vendor-neutral extension mechanisms and independent implementations.

## Scope

V0 defines design and as-built package types; parts, assemblies, kits, and consumables; fixed released configurations; typed engineering requirements; nominal geometry binding; actual physical identity and genealogy; production/inspection/test evidence; approvals and dispositions.

Design contains prescribed outcomes and explicitly prescribed processes. Supplier-chosen operation settings belong to actual production records. An as-built package embeds the exact design snapshot and adds evidence without rewriting it.

Editable CAD feature history, toolpath generation, full PLM workflows, purchasing quantities/prices, machine control, and a new GD&T interpretation system are outside V0. Service history may be preserved as evidence, but V0 does not define a complete lifecycle event ontology.

## Success criteria

A recipient can discover the product, release, material, requirements, and assembly structure without STEP parsing; open geometry with reliable bindings; identify unsupported requirements; and connect each physical item and observation to its exact design basis.

Build-to-print completeness requires engineering release review. A JSON validator cannot establish that no necessary engineering requirement was omitted.

