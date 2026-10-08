# Documentation guide

OPP V0 is a proposed exchange format. Start with the concepts, then follow the relevant implementation path.

| Reader | Suggested order |
| --- | --- |
| Engineer or manufacturer | [Charter](project/charter.md) → [design](spec/v0/design.md) → [requirements](spec/v0/requirements.md) → [as-built](spec/v0/as-built.md) → [examples](../examples/README.md). |
| CAD/CAM/metrology implementer | [V0 overview](spec/v0/README.md) → [package](spec/v0/package.md) → [common types](spec/v0/common-types.md) → [bindings](spec/v0/geometry-bindings.md) → [STEP mapping](interoperability/step-mapping.md) → [conformance](spec/v0/conformance.md). |
| Viewer developer | [NIST SFA assessment](interoperability/nist-sfa.md) → [viewer architecture](interoperability/viewer-plan.md) → [profiles](spec/v0/profiles.md). |
| Contributor/advisor | [Governance](project/governance.md) → [draft decisions](project/decisions.md) → [roadmap](project/roadmap.md) → [contributing](../CONTRIBUTING.md). |

## V0 specification

1. [Overview and authority](spec/v0/README.md)
2. [Package format](spec/v0/package.md)
3. [Common types and identity](spec/v0/common-types.md)
4. [Design and nested assemblies](spec/v0/design.md)
5. [Engineering requirements](spec/v0/requirements.md)
6. [Geometry bindings](spec/v0/geometry-bindings.md)
7. [As-built and evidence](spec/v0/as-built.md)
8. [Capabilities and process profiles](spec/v0/profiles.md)
9. [Conformance and validation](spec/v0/conformance.md)

The [serialized field dictionary](spec/v0/data-dictionary.md) lists every V0 type and field directly from the schema.

## Interoperability and research

- [STEP/AP242 crosswalk and migration rules](interoperability/step-mapping.md)
- [QIF and AS9102-style FAIR crosswalk](interoperability/quality-mapping.md)
- [NIST SFA source assessment](interoperability/nist-sfa.md)
- [First viewer implementation plan](interoperability/viewer-plan.md)
- [Primary-source register](interoperability/sources.md)

The prose specifies intended semantics. Schemas specify serialized structure. A disagreement is a draft defect to resolve; neither allows silently overriding engineering intent. `MUST`, `SHOULD`, and `MAY` express requirements of the **proposed** draft, not an established certification regime.
