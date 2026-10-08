# V0 serialized field dictionary

Generated from [common.schema.json](../../../schemas/v0/common.schema.json). Do not edit this dictionary by hand; run `tools/generate_dictionary.py`.

This lists every serialized field in the V0 types. **Required** means unconditionally required; conditional requirements and interpretation rules remain in the schema and [specification](README.md). Array entries can have inline object fields whose complete constraints are in the schema.

Quantity, range, transform, requirement, and identity semantics are described in [common types](common-types.md), [requirements](requirements.md), [design](design.md), and [as-built](as-built.md).

## Id

string; controlled grammar in schema.

## Decimal

string; controlled grammar in schema.

## Quantity

| Field | Required | Serialized type |
| --- | --- | --- |
| `value` | yes | string; controlled grammar in schema |
| `unit` | yes | `1` / `mm` / `cm` / `m` / `um` / `in` / `mm2` / `m2` / `mm3` / `m3` / `deg` / `rad` / `s` / `min` / `h` / `kg` / `g` / `N` / `kN` / `N.m` / `N/mm` / `Pa` / `kPa` / `MPa` / `bar` / `K` / `Cel` / `mL/min` / `L/min` / `percent` / `HRC` / `HRB` / `HV` / `HBW` / `ShoreA` / `ShoreD` / `Ohm` / `V` / `A` / `W` / `Hz` / `g/cm3` / `kg/m3` |

## Range

| Field | Required | Serialized type |
| --- | --- | --- |
| `lower` | no / conditional | string; controlled grammar in schema |
| `upper` | no / conditional | string; controlled grammar in schema |
| `unit` | yes | `1` / `mm` / `cm` / `m` / `um` / `in` / `mm2` / `m2` / `mm3` / `m3` / `deg` / `rad` / `s` / `min` / `h` / `kg` / `g` / `N` / `kN` / `N.m` / `N/mm` / `Pa` / `kPa` / `MPa` / `bar` / `K` / `Cel` / `mL/min` / `L/min` / `percent` / `HRC` / `HRB` / `HV` / `HBW` / `ShoreA` / `ShoreD` / `Ohm` / `V` / `A` / `W` / `Hz` / `g/cm3` / `kg/m3` |
| `lowerInclusive` | yes | boolean |
| `upperInclusive` | yes | boolean |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## Vector3

array of string; controlled grammar in schema; 3–3 entries.

## Rotation3

array of string; controlled grammar in schema; 9–9 entries.

## Transform

| Field | Required | Serialized type |
| --- | --- | --- |
| `translation` | yes | Vector3 |
| `translationUnit` | yes | `mm` / `cm` / `m` / `um` / `in` |
| `rotation` | yes | Rotation3 |

## ExternalIdentifier

| Field | Required | Serialized type |
| --- | --- | --- |
| `authority` | yes | string (uri) |
| `value` | yes | string |
| `kind` | yes | `cad-persistent-id` / `uuid` / `supplier-id` / `customer-id` / `qif-id` / `other` |

## Extension

| Field | Required | Serialized type |
| --- | --- | --- |
| `namespace` | yes | string (uri) |
| `version` | yes | string |
| `required` | yes | boolean |
| `profileId` | yes | string; controlled grammar in schema |
| `data` | yes | inline object; see schema |

## Actor

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `kind` | yes | `organization` / `person` / `software` |
| `name` | yes | string |
| `organizationId` | no / conditional | string; controlled grammar in schema |
| `address` | no / conditional | string |
| `supplierCode` | no / conditional | string |
| `softwareVersion` | no / conditional | string |
| `externalIdentifiers` | no / conditional | array of ExternalIdentifier |

## Approval

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `actorId` | yes | string; controlled grammar in schema |
| `organizationId` | no / conditional | string; controlled grammar in schema |
| `role` | yes | `designer` / `release-authority` / `inspector` / `quality-authority` / `customer` / `reviewer` |
| `approvedAt` | yes | string (date-time) |
| `statement` | yes | string |
| `evidenceResourceIds` | no / conditional | array of string; controlled grammar in schema |

## Provenance

| Field | Required | Serialized type |
| --- | --- | --- |
| `method` | yes | `native-cad` / `import` / `manual` / `ai-extracted` |
| `sourceResourceId` | no / conditional | string; controlled grammar in schema |
| `sourceEntityRefs` | no / conditional | array of string; controlled grammar in schema |
| `sourceObjectId` | no / conditional | string |
| `tool` | no / conditional | string |
| `toolVersion` | no / conditional | string |
| `recordedAt` | no / conditional | string (date-time) |
| `reviewedByActorId` | no / conditional | string; controlled grammar in schema |
| `confidence` | no / conditional | number |

## Profile

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `version` | yes | string |
| `required` | yes | boolean |

## Resource

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `path` | yes | string; controlled grammar in schema |
| `mediaType` | yes | string |
| `role` | yes | `design` / `as-built` / `bindings` / `presentation` / `nominal-geometry` / `source` / `evidence` / `document` / `preview` / `conversion-report` / `baseline-as-built` |
| `size` | yes | integer |
| `sha256` | yes | string; controlled grammar in schema |

## Manifest

| Field | Required | Serialized type |
| --- | --- | --- |
| `format` | yes | `OPP` |
| `formatVersion` | yes | `0.1.0-draft.1` |
| `packageId` | yes | string; controlled grammar in schema |
| `packageType` | yes | `design` / `as-built` |
| `createdAt` | yes | string (date-time) |
| `generator` | yes | inline object; see schema |
| `designResourceId` | yes | string; controlled grammar in schema |
| `bindingsResourceId` | yes | string; controlled grammar in schema |
| `asBuiltResourceId` | no / conditional | string; controlled grammar in schema |
| `presentationResourceId` | no / conditional | string; controlled grammar in schema |
| `profiles` | yes | array of Profile |
| `resources` | yes | array of Resource |
| `extensions` | no / conditional | array of Extension |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## StandardReference

| Field | Required | Serialized type |
| --- | --- | --- |
| `publisher` | yes | string |
| `number` | yes | string |
| `edition` | yes | string |
| `clause` | no / conditional | string |
| `uri` | no / conditional | string (uri) |

## Document

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `title` | yes | string |
| `role` | yes | `normative` / `informative` / `procedure` / `certificate` |
| `dependencyStatus` | yes | `embedded` / `recipient-supplied` / `missing` |
| `resourceId` | no / conditional | string; controlled grammar in schema |
| `standard` | no / conditional | StandardReference |
| `dependsOnDocumentIds` | no / conditional | array of string; controlled grammar in schema |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## Interpretation

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `family` | yes | `asme-gdt` / `iso-gps` / `opp-explicit` / `customer` |
| `profileId` | yes | string; controlled grammar in schema |
| `standardDocumentIds` | yes | array of string; controlled grammar in schema |
| `description` | yes | string |

## ProductDefinition

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `namespace` | yes | string (uri) |
| `partNumber` | yes | string |
| `revision` | yes | string |
| `name` | yes | string |
| `description` | no / conditional | string |
| `kind` | yes | `part` / `assembly` / `kit` / `consumable` |
| `supply` | yes | `manufactured` / `purchased` |
| `externalIdentifiers` | no / conditional | array of ExternalIdentifier |
| `supplierActorId` | no / conditional | string; controlled grammar in schema |
| `supplierPartNumber` | no / conditional | string |
| `extensions` | no / conditional | array of Extension |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## State

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `kind` | yes | `finished` / `uncoated` / `coated` / `free` / `restrained` / `flat` / `formed` / `intermediate` / `custom` |
| `description` | no / conditional | string |
| `conditions` | no / conditional | array of Condition |

## Condition

| Field | Required | Serialized type |
| --- | --- | --- |
| `name` | yes | string |
| `quantity` | no / conditional | Quantity |
| `text` | no / conditional | string |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## CoordinateFrame

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `unit` | yes | `mm` / `cm` / `m` / `um` / `in` |
| `parentFrameId` | no / conditional | string; controlled grammar in schema |
| `transform` | no / conditional | Transform |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## Representation

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `stateId` | yes | string; controlled grammar in schema |
| `resourceId` | yes | string; controlled grammar in schema |
| `frameId` | yes | string; controlled grammar in schema |
| `role` | yes | `nominal-exact` / `nominal-envelope` / `derived-preview` / `source` |
| `encoding` | yes | `step-part21` / `step-ap242-xml` / `glb` / `x3d` / `ply` / `other` |
| `applicationProtocol` | no / conditional | string |
| `schemaIdentifier` | no / conditional | string |
| `edition` | no / conditional | string |
| `validationProperties` | no / conditional | array of inline object; see schema |

## Region

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `stateId` | yes | string; controlled grammar in schema |
| `representationId` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `kind` | yes | `whole-representation` / `entity-set` / `trimmed-surface` / `volume` |
| `bindingIds` | no / conditional | array of string; controlled grammar in schema |
| `boundaryResourceId` | no / conditional | string; controlled grammar in schema |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## Feature

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `stateId` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `kind` | yes | `surface` / `plane-pair` / `bore` / `hole` / `hole-pattern` / `thread` / `slot` / `edge` / `body` / `interface` / `custom` |
| `regionIds` | yes | array of string; controlled grammar in schema |
| `externalIdentifiers` | no / conditional | array of ExternalIdentifier |

## Subject

| Field | Required | Serialized type |
| --- | --- | --- |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `featureId` | no / conditional | string; controlled grammar in schema |
| `regionId` | no / conditional | string; controlled grammar in schema |
| `occurrencePath` | no / conditional | array of string; controlled grammar in schema |
| `connectionId` | no / conditional | string; controlled grammar in schema |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## Occurrence

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `parentDefinitionId` | yes | string; controlled grammar in schema |
| `childDefinitionId` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `transform` | yes | Transform |
| `externalIdentifiers` | no / conditional | array of ExternalIdentifier |

## Connection

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `parentDefinitionId` | yes | string; controlled grammar in schema |
| `kind` | yes | `weld` / `braze` / `bond` / `fastener` / `fit` / `contact` / `electrical` / `other` |
| `name` | yes | string |
| `participants` | yes | array of Subject |

## MaterialDefinition

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `family` | yes | `metal` / `polymer` / `ceramic` / `composite` / `elastomer` / `adhesive` / `coating` / `other` |
| `grade` | no / conditional | string |
| `condition` | no / conditional | string |
| `productForm` | no / conditional | string |
| `specificationDocumentIds` | yes | array of string; controlled grammar in schema |
| `properties` | no / conditional | array of inline object; see schema |

## Datum

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `stateId` | yes | string; controlled grammar in schema |
| `label` | yes | string |
| `featureIds` | yes | array of string; controlled grammar in schema |
| `targetRegions` | no / conditional | array of string; controlled grammar in schema |
| `description` | no / conditional | string |

## DatumSystem

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `stateId` | yes | string; controlled grammar in schema |
| `compartments` | yes | array of inline object; see schema |

## DimensionSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `characteristic` | yes | `length` / `width` / `height` / `diameter` / `radius` / `thickness` / `distance` / `angle` / `curve-length` / `spherical-diameter` / `spherical-radius` |
| `mode` | yes | `toleranced` / `basic` / `reference` |
| `nominal` | no / conditional | Quantity |
| `limits` | no / conditional | Range |
| `direction` | no / conditional | Vector3 |
| `frameId` | no / conditional | string; controlled grammar in schema |
| `relatedSubjects` | no / conditional | array of Subject |
| `displayDecimals` | no / conditional | integer |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## GdtSegment

| Field | Required | Serialized type |
| --- | --- | --- |
| `characteristic` | yes | `flatness` / `straightness` / `circularity` / `cylindricity` / `parallelism` / `perpendicularity` / `angularity` / `position` / `profile-line` / `profile-surface` / `circular-runout` / `total-runout` |
| `tolerance` | yes | Quantity |
| `zone` | yes | `two-planes` / `cylinder` / `sphere` / `line` / `radial` / `profile` |
| `datumSystemId` | no / conditional | string; controlled grammar in schema |
| `modifiers` | yes | array of `maximum-material` / `least-material` / `regardless-material` / `free-state` / `tangent-plane` / `all-around` / `all-over` / `common-zone` / `translation` / `basic` |
| `zoneOffset` | no / conditional | Quantity |
| `projectedLength` | no / conditional | Quantity |
| `maximumTolerance` | no / conditional | Quantity |

## GdtSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `segments` | yes | array of GdtSegment |
| `relationship` | yes | `independent` / `composite` / `simultaneous` |

## MaterialSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `materialDefinitionId` | yes | string; controlled grammar in schema |
| `permittedAlternativeMaterialIds` | yes | array of string; controlled grammar in schema |
| `substitutionRequiresApproval` | yes | boolean |

## TextureSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `parameter` | yes | `Ra` / `Rq` / `Rz` / `Rt` / `Sa` / `Sq` / `Sz` |
| `limits` | yes | Range |
| `cutoff` | no / conditional | Quantity |
| `evaluationLength` | no / conditional | Quantity |
| `lay` | no / conditional | string |
| `filter` | no / conditional | string |
| `methodDocumentId` | no / conditional | string; controlled grammar in schema |

## CoatingSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `layers` | yes | array of inline object; see schema |
| `excludedSubjects` | yes | array of Subject |
| `dimensionBasis` | yes | `before-coating` / `after-coating` |
| `color` | no / conditional | string |
| `gloss` | no / conditional | Range |

## HeatTreatmentSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `process` | yes | string |
| `temperature` | no / conditional | Range |
| `duration` | no / conditional | Range |
| `hardness` | no / conditional | Range |
| `caseDepth` | no / conditional | Range |
| `specificationDocumentId` | no / conditional | string; controlled grammar in schema |
| `sequenceAfterRequirementIds` | no / conditional | array of string; controlled grammar in schema |

## EdgeSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `operation` | yes | `deburr` / `chamfer` / `radius` / `keep-sharp` |
| `size` | no / conditional | Range |
| `maximumBurrHeight` | no / conditional | Quantity |
| `excludedSubjects` | yes | array of Subject |

## ThreadSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `standardDocumentId` | yes | string; controlled grammar in schema |
| `designation` | yes | string |
| `handedness` | yes | `right` / `left` |
| `pitch` | no / conditional | Quantity |
| `engagementLength` | no / conditional | Range |
| `gaugeDocumentId` | no / conditional | string; controlled grammar in schema |

## Criterion

| Field | Required | Serialized type |
| --- | --- | --- |
| `type` | yes | `range` / `allowed-values` / `boolean` / `direction` / `document-clause` |
| `limits` | no / conditional | Range |
| `values` | no / conditional | array of string |
| `value` | no / conditional | boolean |
| `direction` | no / conditional | Vector3 |
| `frameId` | no / conditional | string; controlled grammar in schema |
| `documentId` | no / conditional | string; controlled grammar in schema |
| `clause` | no / conditional | string |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## ProcessConstraintSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `processFamily` | yes | `machining` / `molding` / `additive` / `casting` / `forging` / `forming` / `cutting` / `joining` / `composites` / `powder` / `extrusion` / `other` |
| `prescribedProcess` | no / conditional | string |
| `controls` | yes | array of inline object; see schema |

## WeldSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `jointType` | yes | string |
| `process` | yes | string |
| `size` | no / conditional | Range |
| `fillerMaterialId` | no / conditional | string; controlled grammar in schema |
| `procedureDocumentId` | no / conditional | string; controlled grammar in schema |
| `inspectionDocumentId` | no / conditional | string; controlled grammar in schema |
| `repairAllowed` | yes | boolean |

## BondSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `adhesiveMaterialId` | yes | string; controlled grammar in schema |
| `bondlineThickness` | yes | Range |
| `cureConditions` | yes | array of Condition |
| `procedureDocumentId` | no / conditional | string; controlled grammar in schema |

## FastenerSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `torque` | no / conditional | Range |
| `preload` | no / conditional | Range |
| `lubrication` | no / conditional | string |
| `sequenceOccurrenceIds` | no / conditional | array of string; controlled grammar in schema |
| `procedureDocumentId` | no / conditional | string; controlled grammar in schema |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## PerformanceSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `characteristic` | yes | string |
| `limits` | yes | Range |
| `conditions` | yes | array of Condition |
| `procedureDocumentId` | no / conditional | string; controlled grammar in schema |

## CleanlinessSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `characteristic` | yes | string |
| `criterion` | yes | Criterion |
| `procedureDocumentId` | no / conditional | string; controlled grammar in schema |

## MarkingSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `fields` | yes | array of `part-number` / `revision` / `serial-number` / `lot-number` / `company` / `custom` |
| `method` | yes | string |
| `literalText` | no / conditional | string |
| `height` | no / conditional | Range |
| `depth` | no / conditional | Range |

## PackagingSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `protection` | yes | array of `corrosion` / `moisture` / `esd` / `surface` / `cleanliness` / `restraint` |
| `conditions` | yes | array of Condition |
| `procedureDocumentId` | no / conditional | string; controlled grammar in schema |

## CertificationSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `deliverable` | yes | `material-certificate` / `test-report` / `conformity-declaration` / `process-certificate` / `ndt-report` / `substance-declaration` / `other` |
| `specificationDocumentIds` | yes | array of string; controlled grammar in schema |
| `issuerQualifications` | yes | array of string |

## TextSpec

| Field | Required | Serialized type |
| --- | --- | --- |
| `text` | yes | string |
| `documentIds` | yes | array of string; controlled grammar in schema |

## Requirement

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `kind` | yes | `dimension` / `geometric-tolerance` / `material` / `surface-texture` / `coating` / `heat-treatment` / `edge-condition` / `thread` / `process-constraint` / `weld` / `bond` / `fastener` / `performance` / `cleanliness` / `marking` / `packaging` / `certification` / `unresolved-text` |
| `name` | yes | string |
| `subjects` | yes | array of Subject |
| `stateId` | yes | string; controlled grammar in schema |
| `interpretationId` | yes | string; controlled grammar in schema |
| `criticality` | yes | `normal` / `key` / `critical` / `safety` |
| `characteristicNumber` | no / conditional | string |
| `spec` | yes | inline object; see schema |
| `verificationId` | no / conditional | string; controlled grammar in schema |
| `overridesRequirementIds` | yes | array of string; controlled grammar in schema |
| `provenance` | no / conditional | Provenance |
| `extensions` | no / conditional | array of Extension |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## DecisionRule

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `method` | yes | `simple-limits` / `guard-band` / `manual` / `report-only` |
| `guardBand` | no / conditional | Quantity |
| `description` | yes | string |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## Verification

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `requirementIds` | yes | array of string; controlled grammar in schema |
| `method` | yes | `dimensional` / `visual` / `material-review` / `process-review` / `ndt` / `performance-test` / `document-review` / `other` |
| `decisionRuleId` | yes | string; controlled grammar in schema |
| `procedureDocumentId` | no / conditional | string; controlled grammar in schema |
| `maximumExpandedUncertainty` | no / conditional | Quantity |
| `coverage` | yes | `every-instance` / `sample` / `first-article` / `lot` |
| `requiredEquipmentKinds` | yes | array of string |
| `conditions` | yes | array of Condition |

## Release

| Field | Required | Serialized type |
| --- | --- | --- |
| `status` | yes | `working` / `review` / `released` |
| `engineeringCompleteness` | yes | `not-assessed` / `incomplete` / `author-declared-complete` |
| `approvalIds` | yes | array of string; controlled grammar in schema |
| `unresolvedItems` | yes | array of string |

## ResourcePin

| Field | Required | Serialized type |
| --- | --- | --- |
| `resourceId` | yes | string; controlled grammar in schema |
| `sha256` | yes | string; controlled grammar in schema |

## Design

| Field | Required | Serialized type |
| --- | --- | --- |
| `schemaVersion` | yes | `0.1.0-draft.1` |
| `id` | yes | string; controlled grammar in schema |
| `rootDefinitionId` | yes | string; controlled grammar in schema |
| `release` | yes | Release |
| `resourcePins` | yes | array of ResourcePin |
| `productDefinitions` | yes | array of ProductDefinition |
| `states` | yes | array of State |
| `coordinateFrames` | yes | array of CoordinateFrame |
| `representations` | yes | array of Representation |
| `regions` | yes | array of Region |
| `features` | yes | array of Feature |
| `occurrences` | yes | array of Occurrence |
| `connections` | yes | array of Connection |
| `materials` | yes | array of MaterialDefinition |
| `datums` | yes | array of Datum |
| `datumSystems` | yes | array of DatumSystem |
| `requirements` | yes | array of Requirement |
| `verifications` | yes | array of Verification |
| `decisionRules` | yes | array of DecisionRule |
| `documents` | yes | array of Document |
| `interpretations` | yes | array of Interpretation |
| `actors` | yes | array of Actor |
| `approvals` | yes | array of Approval |
| `extensions` | no / conditional | array of Extension |

## EntityRef

| Field | Required | Serialized type |
| --- | --- | --- |
| `label` | yes | string; controlled grammar in schema |
| `entityType` | yes | string; controlled grammar in schema |

## Binding

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `regionId` | yes | string; controlled grammar in schema |
| `representationId` | yes | string; controlled grammar in schema |
| `resourceId` | yes | string; controlled grammar in schema |
| `resourceSha256` | yes | string; controlled grammar in schema |
| `encoding` | yes | `step-part21` |
| `entities` | yes | array of EntityRef |
| `externalIdentifiers` | no / conditional | array of ExternalIdentifier |

## Bindings

| Field | Required | Serialized type |
| --- | --- | --- |
| `schemaVersion` | yes | `0.1.0-draft.1` |
| `designId` | yes | string; controlled grammar in schema |
| `bindings` | yes | array of Binding |

## DesignSnapshot

| Field | Required | Serialized type |
| --- | --- | --- |
| `designId` | yes | string; controlled grammar in schema |
| `designResourceId` | yes | string; controlled grammar in schema |
| `sha256` | yes | string; controlled grammar in schema |
| `sourcePackageId` | no / conditional | string; controlled grammar in schema |

## PhysicalSubject

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `kind` | yes | `instance` / `lot` |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `occurrencePath` | yes | array of string; controlled grammar in schema |
| `parentSubjectId` | no / conditional | string; controlled grammar in schema |
| `serialNumber` | no / conditional | string |
| `lotNumber` | no / conditional | string |
| `quantity` | no / conditional | integer |
| `manufacturedAt` | no / conditional | string (date-time) |
| `manufacturerActorId` | no / conditional | string; controlled grammar in schema |
| `externalIdentifiers` | no / conditional | array of ExternalIdentifier |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## ProductionCell

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `organizationId` | yes | string; controlled grammar in schema |
| `site` | yes | string |
| `line` | no / conditional | string |

## Equipment

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `kind` | yes | `measurement` / `production-machine` / `test-rig` / `fixture` |
| `manufacturer` | yes | string |
| `model` | yes | string |
| `serialNumber` | yes | string |
| `organizationId` | yes | string; controlled grammar in schema |
| `softwareVersion` | no / conditional | string |
| `firmwareVersion` | no / conditional | string |
| `resolutions` | yes | array of Quantity |
| `operatingRanges` | yes | array of Range |

## Uncertainty

| Field | Required | Serialized type |
| --- | --- | --- |
| `expanded` | yes | Quantity |
| `coverageFactor` | yes | string; controlled grammar in schema |
| `confidencePercent` | no / conditional | string; controlled grammar in schema |
| `method` | yes | string |
| `budgetResourceId` | no / conditional | string; controlled grammar in schema |

## Calibration

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `equipmentId` | yes | string; controlled grammar in schema |
| `calibratedAt` | yes | string (date-time) |
| `validUntil` | yes | string (date-time) |
| `organizationId` | yes | string; controlled grammar in schema |
| `certificateResourceId` | yes | string; controlled grammar in schema |
| `traceability` | yes | array of string |
| `uncertainty` | no / conditional | Uncertainty |
| `status` | yes | `valid` / `expired` / `withdrawn` |

## MaterialLot

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `materialDefinitionId` | yes | string; controlled grammar in schema |
| `lotNumber` | yes | string |
| `heatNumber` | no / conditional | string |
| `batchNumber` | no / conditional | string |
| `supplierActorId` | yes | string; controlled grammar in schema |
| `certificateResourceIds` | yes | array of string; controlled grammar in schema |
| `subjectIds` | yes | array of string; controlled grammar in schema |
| `parentMaterialLotIds` | yes | array of string; controlled grammar in schema |

## ProductionEvent

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `subjectIds` | yes | array of string; controlled grammar in schema |
| `processFamily` | yes | string |
| `name` | yes | string |
| `startedAt` | yes | string (date-time) |
| `endedAt` | yes | string (date-time) |
| `organizationId` | yes | string; controlled grammar in schema |
| `operatorActorIds` | yes | array of string; controlled grammar in schema |
| `cellId` | no / conditional | string; controlled grammar in schema |
| `equipmentIds` | yes | array of string; controlled grammar in schema |
| `materialLotIds` | yes | array of string; controlled grammar in schema |
| `procedureResourceId` | no / conditional | string; controlled grammar in schema |
| `parameters` | yes | array of Condition |
| `evidenceResourceIds` | yes | array of string; controlled grammar in schema |
| `supersedesEventId` | no / conditional | string; controlled grammar in schema |

## Run

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `kind` | yes | `inspection` / `test` / `scan` / `material-review` / `document-review` |
| `subjectIds` | yes | array of string; controlled grammar in schema |
| `startedAt` | yes | string (date-time) |
| `endedAt` | yes | string (date-time) |
| `organizationId` | yes | string; controlled grammar in schema |
| `operatorActorIds` | yes | array of string; controlled grammar in schema |
| `equipmentIds` | yes | array of string; controlled grammar in schema |
| `calibrationIds` | yes | array of string; controlled grammar in schema |
| `method` | yes | string |
| `procedureResourceId` | no / conditional | string; controlled grammar in schema |
| `conditions` | yes | array of Condition |
| `sampling` | yes | inline object; see schema |

## ObservedValue

| Field | Required | Serialized type |
| --- | --- | --- |
| `kind` | yes | `scalar` / `boolean` / `text` / `vector` / `resource` |
| `quantity` | no / conditional | Quantity |
| `boolean` | no / conditional | boolean |
| `text` | no / conditional | string |
| `vector` | no / conditional | Vector3 |
| `unit` | no / conditional | `1` / `mm` / `cm` / `m` / `um` / `in` / `mm2` / `m2` / `mm3` / `m3` / `deg` / `rad` / `s` / `min` / `h` / `kg` / `g` / `N` / `kN` / `N.m` / `N/mm` / `Pa` / `kPa` / `MPa` / `bar` / `K` / `Cel` / `mL/min` / `L/min` / `percent` / `HRC` / `HRB` / `HV` / `HBW` / `ShoreA` / `ShoreD` / `Ohm` / `V` / `A` / `W` / `Hz` / `g/cm3` / `kg/m3` |
| `resourceId` | no / conditional | string; controlled grammar in schema |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## Observation

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `subjectId` | yes | string; controlled grammar in schema |
| `requirementId` | yes | string; controlled grammar in schema |
| `stateId` | yes | string; controlled grammar in schema |
| `runId` | yes | string; controlled grammar in schema |
| `observedAt` | yes | string (date-time) |
| `characteristicPath` | yes | string |
| `value` | yes | ObservedValue |
| `uncertainty` | no / conditional | Uncertainty |
| `evidenceResourceIds` | yes | array of string; controlled grammar in schema |
| `supersedesObservationId` | no / conditional | string; controlled grammar in schema |

## Evaluation

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `subjectId` | yes | string; controlled grammar in schema |
| `requirementId` | yes | string; controlled grammar in schema |
| `observationIds` | yes | array of string; controlled grammar in schema |
| `decisionRuleId` | yes | string; controlled grammar in schema |
| `evaluatedAt` | yes | string (date-time) |
| `evaluatorActorId` | yes | string; controlled grammar in schema |
| `conformance` | yes | `pass` / `fail` / `indeterminate` / `not-inspected` |
| `disposition` | yes | `accepted` / `rejected` / `pending` / `accepted-under-deviation` |
| `deviationId` | no / conditional | string; controlled grammar in schema |
| `rationale` | yes | string |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## Scan

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `subjectIds` | yes | array of string; controlled grammar in schema |
| `runId` | yes | string; controlled grammar in schema |
| `resourceId` | yes | string; controlled grammar in schema |
| `dataClass` | yes | `point-cloud` / `mesh` / `ct-volume` |
| `capturedAt` | yes | string (date-time) |
| `equipmentId` | yes | string; controlled grammar in schema |
| `unit` | yes | `mm` / `cm` / `m` / `um` / `in` |
| `registration` | yes | inline object; see schema |
| `uncertainty` | no / conditional | Uncertainty |
| `description` | yes | string |

## Deviation

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `subjectIds` | yes | array of string; controlled grammar in schema |
| `requirementIds` | yes | array of string; controlled grammar in schema |
| `description` | yes | string |
| `disposition` | yes | `use-as-is` / `rework` / `repair` / `scrap` |
| `approvalIds` | yes | array of string; controlled grammar in schema |
| `approvedAt` | yes | string (date-time) |
| `expiresAt` | no / conditional | string (date-time) |
| `quantityLimit` | no / conditional | integer |
| `evidenceResourceIds` | yes | array of string; controlled grammar in schema |

## Fai

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `type` | yes | `full` / `partial` |
| `status` | yes | `incomplete` / `complete` |
| `subjectIds` | yes | array of string; controlled grammar in schema |
| `requirementIds` | yes | array of string; controlled grammar in schema |
| `evaluationIds` | yes | array of string; controlled grammar in schema |
| `materialLotIds` | yes | array of string; controlled grammar in schema |
| `productionEventIds` | yes | array of string; controlled grammar in schema |
| `deviationIds` | yes | array of string; controlled grammar in schema |
| `approvalIds` | yes | array of string; controlled grammar in schema |
| `reportResourceIds` | yes | array of string; controlled grammar in schema |
| `reason` | no / conditional | string |
| `baseline` | no / conditional | inline object; see schema |

Conditional/cross-field structural constraints apply; inspect this type in the common schema.

## AsBuilt

| Field | Required | Serialized type |
| --- | --- | --- |
| `schemaVersion` | yes | `0.1.0-draft.1` |
| `id` | yes | string; controlled grammar in schema |
| `designSnapshot` | yes | DesignSnapshot |
| `recordedAt` | yes | string (date-time) |
| `recordStatus` | yes | `working` / `review` / `closed` |
| `supersedesRecord` | no / conditional | inline object; see schema |
| `subjects` | yes | array of PhysicalSubject |
| `actors` | yes | array of Actor |
| `productionCells` | yes | array of ProductionCell |
| `equipment` | yes | array of Equipment |
| `calibrations` | yes | array of Calibration |
| `materialLots` | yes | array of MaterialLot |
| `productionEvents` | yes | array of ProductionEvent |
| `runs` | yes | array of Run |
| `observations` | yes | array of Observation |
| `evaluations` | yes | array of Evaluation |
| `scans` | yes | array of Scan |
| `deviations` | yes | array of Deviation |
| `faiReports` | yes | array of Fai |
| `approvals` | yes | array of Approval |
| `extensions` | no / conditional | array of Extension |

## View

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `name` | yes | string |
| `productDefinitionId` | yes | string; controlled grammar in schema |
| `stateId` | yes | string; controlled grammar in schema |
| `frameId` | yes | string; controlled grammar in schema |
| `camera` | yes | inline object; see schema |
| `requirementIds` | yes | array of string; controlled grammar in schema |
| `previewResourceId` | no / conditional | string; controlled grammar in schema |

## Presentation

| Field | Required | Serialized type |
| --- | --- | --- |
| `schemaVersion` | yes | `0.1.0-draft.1` |
| `designId` | yes | string; controlled grammar in schema |
| `views` | yes | array of View |

## ConversionItem

| Field | Required | Serialized type |
| --- | --- | --- |
| `id` | yes | string; controlled grammar in schema |
| `sourceResourceId` | yes | string; controlled grammar in schema |
| `sourceEntityRefs` | yes | array of string; controlled grammar in schema |
| `targetObjectIds` | yes | array of string; controlled grammar in schema |
| `mappingId` | yes | string; controlled grammar in schema |
| `outcome` | yes | `translated` / `preserved-only` / `unsupported` / `ambiguous` / `conflict` / `omitted` |
| `severity` | yes | `information` / `warning` / `error` |
| `reason` | yes | string |

## ConversionReport

| Field | Required | Serialized type |
| --- | --- | --- |
| `schemaVersion` | yes | `0.1.0-draft.1` |
| `id` | yes | string; controlled grammar in schema |
| `converter` | yes | inline object; see schema |
| `sourceSchema` | yes | string |
| `sourceEdition` | yes | string |
| `recommendedPracticeVersions` | yes | array of string |
| `items` | yes | array of ConversionItem |
| `unresolvedNormativeCount` | yes | integer |
| `reviewRequired` | yes | boolean |

