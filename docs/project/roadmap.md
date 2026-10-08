# Roadmap

## V0: reviewable architecture (this draft)

Package/identity/authority rules, design and actual schemas, typed requirement families, reusable assembly definitions, geometry bindings, candidate STEP mapping, synthetic examples, a structural/semantic-reference checker, and public project docs.

## V0.2: prove a narrow exchange

1. SME review of quantity, state, datum, tolerance, and decision-rule semantics.
2. Validate block geometry with two independent geometry readers.
3. Import one NIST AP242 semantic-PMI fixture and produce an itemized conversion report.
4. Implement dimensions, a limited ASME GD&T subset, materials, and surface texture end to end.
5. Show requirement selection on exact geometry and a linked measurement result.
6. Test nested assembly reuse, physical serial/lot identity, and unit/placement conversions.

## Viewer baseline

Inspect SFA dependency and redistribution terms; choose a pinned baseline; add OPP package/metadata panels, source-ID lookup, actual overlays, and capability/loss displays. Bundle viewer resources for offline use. Keep SFA's analysis as an independent migration comparison where practical.

## Before a stable V1

Independent exporters/readers must pass public fixtures across supported profiles. Resolve exact partial-face regions, GD&T compounds/modifiers, source PMI conflicts, dependency closure, calibration/uncertainty rules, partial FAIR baselines, redaction, signatures, and process-specific vocabulary.

CAD-native exporters can reuse their STEP geometry pipeline while directly serializing OPP semantics. No file profile should claim more than its publicly tested support.

