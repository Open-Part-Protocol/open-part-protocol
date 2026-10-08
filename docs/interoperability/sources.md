# Primary-source register

Reviewed October 7, 2026. External sources inform interoperability; OPP's proposed semantics are original project design, not an endorsement or reproduction of those standards.

| ID | Primary source | Used for |
| --- | --- | --- |
| `nist-sfa` | [NIST SFA repository](https://github.com/usnistgov/SFA), inspected commit `72375d17c09cf7072c30d9393b5c08b7aa272285` (September 14, 2026); [source build guide](https://github.com/usnistgov/SFA/blob/72375d17c09cf7072c30d9393b5c08b7aa272285/source/README.md). | Source modules, analysis/viewer behavior, build/dependency assessment. |
| `nist-sfa-service` | [NIST STEP File Analyzer and Viewer](https://www.nist.gov/services-resources/software/step-file-analyzer-and-viewer). | Semantic versus graphic PMI, supported uses, documented platform requirements. |
| `nist-terms` | [NIST copyrights and disclaimers](https://www.nist.gov/copyrights-disclaimers). | Attribution and terms to check before any reuse. |
| `cax-pmi-4.1` | [CAx-IF PMI Representation and Presentation v4.1, June 20, 2024](https://www.mbx-if.org/home/wp-content/uploads/2024/06/rec_pracs_pmi_v41.pdf). | Dimension/zone/datum/entity associations and source notation conventions. |
| `cax-current` | [Current CAx recommended practices](https://www.mbx-if.org/home/cax/recpractices/). | Exact practice versions; product structure, validation, persistent IDs, tessellation, styling. |
| `cax-qif-cross-domain-1.0` | [CAx-IF/DMSC Cross-Domain Exchange v1.0, January 29, 2026](https://www.mbx-if.org/home/wp-content/uploads/2026/02/rec_prac_cross-domain_exchange_v10.pdf). | AP242 edition 4/QIF 3.0 traceability and persistent IDs; §§5–6 and Annex B. |
| `iso-ap242-2025` | [ISO Update, September 2025](https://www.iso.org/files/live/sites/isoorg/files/news/magazine/ISOupdate/EN/2025/ISOupdate_September_2025.pdf), p.17. | Publication metadata for ISO 10303-242:2025; not access to its complete normative text. |
| `occt-step` | [Open CASCADE STEP translator documentation](https://occt3d.com/dev/doc/overview/html/occt_user_guides__step.html). | Assembly transformation chains, XDE attributes, geometry healing and implementation limits. |
| `qif` | [DMSC QIF](https://qifstandards.org/) and [ISO 23952:2020 catalog](https://www.iso.org/standard/77461.html). | Quality information scope: model, plans, resources, actual results, statistics. |
| `iaqg-fai` | [IAQG SCMH Make / First Article Inspection](https://scmh.iaqg.org/scmh-make/) and [IAQG 2022 SCMH communication pack](https://scmh.iaqg.org/wp-content/uploads/2022/07/SCMH-Communication-Pack-6JUL2022.pdf). | FAI guidance and broad accountability form families. Revision-C guidance requires edition-specific review. |
| `sae-as9102c` | [SAE AS9102C catalog](https://www.sae.org/standards/content/as9102c/). | Edition identifier; this research did not retrieve the complete paid normative standard. |
| `rfc8785` | [IETF RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html). | Candidate future signature input canonicalization; not implemented in V0. |

## Mapping evidence levels

`documented-chain` means a cited public implementation practice documents the relevant source construct. `candidate` means a mapping needs edition-specific schema/fixture review. Neither means a converter exists. `no-v0-mapping` means content is preserved or requires a future adapter/profile.

The machine-readable registry records these distinctions per row. OPP does not claim arbitrary AP242 round trips are lossless. A future adapter must identify the exact EXPRESS schema, AP edition, serialization, and recommended-practice revisions it actually supports.
