# Common types and identity

## Identifiers and revision

Object IDs are readable lowercase package-local strings (`req-block-height`, `occ-module-left`). The schema permits letters/digits separated by `-`, `.`, or `_`. Design IDs are unique across all design collections; actual IDs are unique across all actual collections. Resource IDs are unique in the manifest. Typed references declare their domain; a resource ID is not interchangeable with a requirement ID.

A released definition's external identity is `(namespace, partNumber, revision)`. The exact design JSON hash identifies its immutable snapshot. Across packages, qualify local objects by `(designSnapshot.sha256, objectId)`; actual identity uses `(asBuiltResource.sha256, actualObjectId)`. Physical serials and lots are additionally qualified by manufacturer/definition. Do not equate two serial strings from different organizations.

Preserve source CAD/STEP/QIF persistent identifiers in `externalIdentifiers` with `authority`, `kind`, and `value`. A STEP `#123` is only a locator in exact hashed bytes. UUIDs help trace continuity but do not prove unchanged geometry. Cross-revision mapping needs explicit exporter evidence, not matching names.

## Quantities and bounds

`Quantity = { "value": "20.010", "unit": "mm" }`.

The decimal grammar is `-?(0|[1-9][0-9]*)(\.[0-9]+)?`: no exponent, leading `+`, leading zeros, NaN, or infinity. Negative zero is numerically zero. Display decimals are separate metadata. Never infer an engineering tolerance from serialized precision.

`Range` has `unit`, at least one of `lower`/`upper`, and explicit `lowerInclusive`/`upperInclusive`. Limits are **absolute values**, not deviations. `lower <= upper`; equal endpoints require both inclusive. A nominal may lie outside a unilaterally offset tolerance range. Convert STEP offset tolerances explicitly; see [the crosswalk](../../interoperability/step-mapping.md).

The V0 unit enumeration is in `Quantity`/`Range` in [the common schema](../../../schemas/v0/common.schema.json). It covers length/area/volume, angle, time, mass, force, torque, stiffness, pressure, temperature, flow, percentage, hardness scales, electrical quantities, power/frequency, and density. Its ASCII spellings are a draft controlled vocabulary, **not a claim of full UCUM conformance**. Hardness scales are distinct empirical measurement scales. `percent` is 0–100 and `1` is a dimensionless fraction.

All compared quantities MUST have compatible dimensions. Length conversions use exact decimal scale factors (`in = 25.4 mm`, `um = 0.001 mm`). Celsius is affine relative to kelvin; a temperature difference must not be treated as an absolute temperature. Different hardness scales cannot be silently converted. The reference checker supports only selected conversions and reports its limits.

## Coordinates

Frames are right-handed Cartesian frames with explicit length units. `Transform` contains a 3×3 row-major rotation and a translation vector with its own length unit. Use column vectors: `p_parent = R × p_child + t`, after converting child, translation, and parent coordinates to the same length unit. Rotations are dimensionless, orthonormal, and have determinant +1. Scale, shear, and reflection are forbidden; an opposite-hand manufactured part has a separate definition.

Frame and assembly containment graphs MUST be acyclic. A parent frame is in the same product definition. The reference checker uses a numerical tolerance of `1e-9` when checking rotations; adapter geometry tolerances are separate.

## Documents, actors, and provenance

Documents name their role, exact standard publisher/number/edition/clause where applicable, dependency status, and optional embedded resource. A missing normative document cannot be hidden as an informative link. Interpretation objects declare a profile and the standard document IDs it relies on; ASME and ISO GPS are different interpretation families.

Actors are organizations, people, or software. Approvals record an actor, role, timestamp, statement, and evidence; they are reported assertions until authenticated by an external trust mechanism. Production/inspection records can use an operator identifier in place of a personal name if the parties agree on that identifier.

Provenance records native CAD/import/manual/AI extraction, source references, tool/version, and review. Extraction confidence is separate from engineering authority. AI-inferred requirements need engineering review before release.

## Extensions

Extensions require `namespace`, exact `version`, `profileId`, `required`, and declarative `data`. Required unknown extensions block semantic support. Optional unknown extensions may be preserved but not interpreted. Core typed requirements must not be displaced into private arbitrary properties to claim core interoperability.

