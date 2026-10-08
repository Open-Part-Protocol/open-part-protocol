# Design and assemblies

`Design` is the complete resolved graph for a design snapshot. Its entry point is `rootDefinitionId`; each product definition declares identity, revision, name, product kind, and manufactured/purchased supply. `resourcePins` binds that JSON to its exact geometry, bindings, and referenced resources, so the design hash identifies the full engineering snapshot. All graph collections are explicit arrays, even when empty. The exact structural contract is [the design schema](../../../schemas/v0/design.schema.json).

## Object families

| Collection | Meaning and important fields |
| --- | --- |
| `productDefinitions` | Exact `(namespace, partNumber, revision)`, `kind`, `supply`; purchased items require supplier/part identity. |
| `states` | Product-specific finished/uncoated/coated/free/restrained/flat/formed/intermediate conditions. |
| `coordinateFrames` | Product coordinates and optional parent-frame rigid transforms. |
| `representations` | Product/state/frame, resource, encoding, source AP/schema/edition, authority role, geometric validation properties. |
| `regions` / `features` | Exact selected geometry and engineering subjects built from those regions. |
| `occurrences` | A reusable child definition in a parent definition with a rigid placement. |
| `connections` | Joints/interfaces with occurrence-scoped participants. |
| `materials` | Grade, family, condition, form, specification documents, and required property ranges. |
| `datums` / `datumSystems` | Datum features/targets and ordered reference compartments with modifiers. |
| `requirements` | Typed obligations, subjects, states, interpretation, criticality, and explicit overrides. |
| `verifications` / `decisionRules` | Characteristic coverage, inspection/test constraints, conditions, uncertainty, and decision rule. |
| `documents` / `interpretations` | Exact dependencies and applicable semantic rules. |
| `actors` / `approvals` | Design/release provenance and reported authorization. |

## States and representations

The nominal finished shape must not be confused with tooling-compensated, flat, restrained, or intermediate geometry. Each representation and requirement references a declared state of its product. Multiple representations are allowed, but there must be a unique authoritative exact representation for a product/state unless a future multi-body profile explicitly partitions that authority.

Manufactured parts intended for exact manufacture require exact nominal geometry. Purchased items may expose an interface/envelope and exact supplier identity. Consumables need no solid. An assembly can be entirely defined by component geometry plus occurrences; it need not duplicate a flattened assembly STEP file.

## Reusable definitions, distinct occurrences

Each physical use has its own occurrence. Two identical bolts use one definition and two occurrences. Repeated subassemblies reuse a definition; they do not duplicate its descendants in the design graph.

```text
pair-assy A
├── occ-left  → module-assy A
│   └── occ-block → block A
└── occ-right → module-assy A
    └── occ-block → block A
```

The block's two uses have paths `[occ-left, occ-block]` and `[occ-right, occ-block]`. `occ-block` alone cannot identify one physical block. Paths MUST form a valid root-to-descendant traversal. Definition-level requirements apply to every matching physical use. An occurrence-scoped requirement additionally declares its path. V0 has no wildcard occurrence paths or unresolved option expressions.

An occurrence is one discrete child use. Repeated count is represented by distinct occurrences; bulk consumable quantity belongs in a later explicit consumption profile. Assembly component count is derived from occurrences and does not represent purchasing quantity.

Parent definitions must be assemblies or kits. Recursive containment is forbidden. Connections attach to exact participants; an interface's weld/torque/bond requirement must not be an unscoped note. Occurrence placements use the [common transform convention](common-types.md).

## Requirement scope and release

Features/regions, datums, representations, and states MUST resolve to the same owning product. Related subjects of a dimension or connection may name other products using explicit occurrence context. Requirements on interfaces across products apply in the parent assembly state.

`release.status` is working/review/released. `engineeringCompleteness` is not-assessed/incomplete/author-declared-complete. A released design requires release-authority approval, no unresolved normative items, and separately reported capability/dependency completeness. It still requires engineering review; schema validity is insufficient.
