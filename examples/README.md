# Synthetic OPP examples

All design, operator/company, equipment, certificate, production, scan, and measured data is **synthetic**. These files illustrate serialization and relationships; they are not production releases, traceable measurements, or approved FAIRs.

| Archive | Demonstrates |
| --- | --- |
| [block-design.opp](packages/block-design.opp) | A 40×20×10 mm block, face bindings, dimensions, material, flatness, texture, marking, proof-test requirement, and explicit interpretation dependencies. |
| [block-as-built.opp](packages/block-as-built.opp) | Exact embedded design; serial/lot, cell/date/operator/company, calibration, dimensions, raw test CSV, sparse scan, and a failed width accepted under a synthetic concession. |
| [assembly-design.opp](packages/assembly-design.opp) | Two uses of a reusable module definition containing the same block definition; occurrence placements and paths. |
| [assembly-as-built.opp](packages/assembly-as-built.opp) | Distinct physical assembly/module/block identities and characteristic results for both reused paths. |
| [lot-as-built.opp](packages/lot-as-built.opp) | An explicit lot population and sample scope; incomplete FAIR/marking accountability, without individual serial claims. |

Review the [unpacked design](unpacked/block-design/design/design.json) and [unpacked actual record](unpacked/block-as-built/actual/as-built.json) alongside the schemas. These text files are the reviewable sources; `tools/build_examples.py` regenerates inventories/hashes and deterministic ZIP archives.

The STEP payload is original synthetic AP203-style planar B-rep. Its geometry has not been independently kernel/EXPRESS-validated. OPP semantics are manually authored; there is no AP242 PMI conversion demonstrated here. The sparse PLY contains corner points and cannot establish full surface compliance. The procedure and certificates explicitly describe their synthetic status.

Designs are marked `review` / `incomplete`. ASME interpretation is a declared recipient-supplied dependency. Those limitations are expected checker warnings. A synthetic FAIR marked complete means modeled accountability pairs have reported accepted results; it does not certify the design or actual acceptance.

```sh
.venv/bin/python tools/build_examples.py --check
.venv/bin/python tools/validate.py examples/packages/block-as-built.opp
.venv/bin/python tools/validate.py examples/unpacked/assembly-as-built
```

