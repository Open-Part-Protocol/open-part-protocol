# Geometry bindings

Bindings connect engineering regions to entities in an **immutable exact geometry payload**.

```text
requirement → feature / region → representation → resource + SHA-256 → STEP #entity
```

`Binding` contains `id`, `regionId`, `representationId`, `resourceId`, `resourceSha256`, `encoding: "step-part21"`, and one or more `{label, entityType}` references. The region lists the binding IDs that select it. The manifest, representation, region, and binding must agree on the resource and product state.

One feature can comprise multiple regions and faces. Source `SHAPE_ASPECT`/`GEOMETRIC_ITEM_SPECIFIC_USAGE` relationships help translate PMI geometry associations; OPP bindings remain direct, inspectable references to exact entities. See [CAx-IF PMI practice](https://www.mbx-if.org/home/wp-content/uploads/2024/06/rec_pracs_pmi_v41.pdf), §5.1 and §6.1.

## Immutability and import healing

Entity labels are not stable across STEP export, renumbering, or healing. Reserializing geometry requires new hashes and new bindings. A geometry adapter must preserve a source-entity → imported-topology map. If a face splits/merges or cannot be mapped reliably, report affected regions and requirements; do not attach them by visual proximity.

The reference checker confirms labels and declared simple entity types exist in the exact resource. It does not parse EXPRESS schemas, traverse complex STEP entities, load a kernel, validate face meaning, or prove topological correctness. Multi-DATA-section Part 21 files need a future section-qualified locator profile; this draft's binding profile assumes a single DATA section with globally unique labels.

## Exact partial regions

`whole-representation` and `entity-set` selections are the initial interoperable targets. `trimmed-surface` and `volume` contain a `boundaryResourceId` and source bindings, but their exact boundary encoding is reserved for a separate profile. The current checker reports them as unsupported for complete geometry binding. A GLB triangle selection or a loose bounding box cannot silently substitute for an exact masking boundary.

## Assembly placement

Bind component geometry in component coordinates. Occurrence paths and accumulated placements locate it within an assembly. A flattened assembly representation may be retained as a derived preview/source, but must not compete with authoritative component definitions and occurrences.

