# NIST STEP File Analyzer assessment

Research baseline: [usnistgov/SFA](https://github.com/usnistgov/SFA) commit `72375d17c09cf7072c30d9393b5c08b7aa272285` (September 14, 2026), inspected October 7, 2026. No fork or SFA code has been added to this repository.

## Useful baseline

SFA analyzes STEP entities/attributes, semantic and graphic PMI, validation properties, and basic syntax; its viewer covers parts/assemblies and several PMI/geometry types. These are useful comparison inputs for OPP migration. [SFA README](https://github.com/usnistgov/SFA/blob/72375d17c09cf7072c30d9393b5c08b7aa272285/README.md).

The current implementation is Tcl-based. Its source build guide specifies freeWrap 6.51, additional Tcl packages, and installed IFCsvr/stp2x3d dependencies. The NIST service page documents Windows/Excel requirements and an internet-connected browser viewer. [Source build guide](https://github.com/usnistgov/SFA/blob/72375d17c09cf7072c30d9393b5c08b7aa272285/source/README.md), [NIST service page](https://www.nist.gov/services-resources/software/step-file-analyzer-and-viewer).

## Source modules reviewed for OPP planning

| Module | Relevance |
| --- | --- |
| `sfa-dimtol.tcl` | Dimensional characteristic/value/qualifier traversal; inspected source. |
| `sfa-geotol.tcl` | Tolerance/modifier/datum-system processing; inspected source. |
| `sfa-valprop.tcl` | Validation-property relationships; inspected source. |
| `sfa-part.tcl` | B-rep to X3D invocation and geometry workflow; inspected source. |
| `sfa-grafpmi.tcl`, `sfa-grafx3d.tcl` | Candidate presentation/view integration points; inventory reviewed, detailed modification analysis pending. |
| `sfa-uuid.tcl`, `sfa-geom.tcl`, `sfa-step.tcl` | Candidate persistent-ID/binding/source-entity services; inventory reviewed, detailed analysis pending. |

The source module inventory is documented in [SFA's build guide](https://github.com/usnistgov/SFA/blob/72375d17c09cf7072c30d9393b5c08b7aa272285/source/README.md). This assessment uses source names and behavior as references and copies no Tcl implementation.

## Proposed fork scope

Add a package loader, inventory/snapshot checks, OPP metadata/requirement panels, requirement-to-source-geometry selection, instance/lot/run selectors, actual overlays, and clear support/loss states. Keep the nominal STEP resource unchanged. Route OPP semantics through a separate model layer rather than encoding them into spreadsheet cells.

Before distributing a fork, review NIST's [terms](https://www.nist.gov/copyrights-disclaimers) and each bundled dependency's terms; acknowledge NIST where reused. Confirm available APIs and whether stp2x3d exposes a source-entity-to-rendered-geometry map. A renderable model alone is insufficient to bind engineering requirements reliably.

For the offline requirement, bundle all viewer assets and remove automatic remote asset requests. Test the whole package on a disconnected machine. An adapter may need to replace platform-specific dependencies for a cross-platform OPP viewer. The first [OPP Viewer](https://github.com/Open-Part-Protocol/opp-viewer) instead uses an independent native Rust implementation. The unused SFA fork is archived as a reference, and SFA remains a comparison tool rather than an application dependency. Verified engineering-to-render bindings remain open implementation work.
