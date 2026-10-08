# V0 draft decisions

These decisions establish a reviewable first draft. They can change through public RFCs.

| Decision | Rationale | Follow-up |
| --- | --- | --- |
| Name: Open Part Protocol; extension: `.opp` | Explicit project choice, with the musical nod. | Check extension/MIME/name conflicts before ecosystem registration. |
| ZIP + UTF-8 JSON; one serialization | Familiar tooling and readable metadata. | Test archive interoperability and resource limits. |
| Two package types: design / as-built | Separates specification from physical evidence. | Test lot and nested physical assembly examples. |
| As-built embeds design closure byte-for-byte | Recipient can work offline and verify exact design basis. | Evaluate large-package storage costs after correctness. |
| STEP initially provides exact geometry | Reuses CAD export investment. | AP242 entity-level fixtures and adapter tests. |
| Requirement semantics are canonical OPP | Predictable direct consumption. | Resolve duplicated source PMI through conversion reports. |
| Decimal strings for engineering quantities | Preserves intended decimal limits. | Confirm unit vocabulary and decision-rule precision. |
| Local readable IDs; exact snapshot pins cross-package identity | Avoids opaque IDs in everyday authoring. | Preserve CAD persistent UUIDs as external identifiers. |
| Occurrence paths identify reused subassemblies | A local component ID is insufficient when a subassembly repeats. | Expand fixtures for occurrence-scoped requirements. |
| Actual compliance and acceptance are different | A concession does not make a failed measurement pass. | Quality review of approval and disposition rules. |
| Hash raw resource bytes; no V0 signature wire format | Can be implemented now without inventing cryptography. | Separate signature RFC using established canonicalization/signature standards. |
| Free text and experimental typed families stay visible | Honest broad coverage without fake machine understanding. | Mature individual process/GD&T profiles with SMEs. |

## Questions for founding review

- Which narrowly defined GD&T profile and standards editions should reach interoperable status first?
- Should the first reference viewer extend SFA directly or use it as an external comparison tool?
- What exact treatment of purchased specification dependencies meets the build-to-print profile?
- Which machining, molding, additive, casting, forging, forming, and joining profile needs the first worked industrial dataset?
- Should normative prose eventually use a separate permissive documentation license?
- What resource-limit classes are practical for CT data and large as-built scans?

