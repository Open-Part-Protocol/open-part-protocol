# Package format

An `.opp` file is a ZIP archive with a root `manifest.json`, encoded as UTF-8 JSON. ZIP stored/deflate methods are supported. ZIP64 is allowed within local resource limits. Archives are standalone; nested packages, encrypted entries, spanning, symbolic links, executable code, and external resource fetching are not V0 mechanisms.

## Manifest

`format` is `OPP`; `formatVersion` is the exact draft version. `packageId` is a UUID URN and identifies this immutable exchange snapshot. `packageType` is `design` or `as-built`. `createdAt` has an explicit UTC offset. `generator` identifies the writing tool.

`designResourceId` and `bindingsResourceId` resolve through `resources`. As-built additionally requires `asBuiltResourceId`. `presentationResourceId` is optional. Each `profiles` entry specifies an exact ID/version and whether its understanding is required for the exchange.

Every resource entry has `id`, `path`, `mediaType`, `role`, exact uncompressed `size`, and lowercase SHA-256 of its **raw bytes**. Roles distinguish design, actual, nominal geometry, source, evidence, documents, previews, bindings, presentation, baseline actual records, and conversion reports. A source STEP file may supply nominal geometry while its original PMI remains source content.

Every archive file except `manifest.json` MUST appear exactly once in the inventory. Every inventory item MUST exist. The manifest is not included in its own hash inventory, avoiding recursion. Bare hashes establish consistency, not trusted authorship: an attacker able to replace files can also replace the manifest. V0 does not define signature bytes or claim authenticated release approval.

## JSON rules

Use UTF-8 without a byte-order mark. Duplicate object keys, nonfinite numbers, and unknown core fields are errors. Object order and whitespace have no engineering significance, but changing them changes a raw-byte resource hash. Engineering quantities use decimal strings. Extension content is declarative JSON.

Schemas are loaded locally by exact `$id`; a reader MUST NOT dereference schema URLs from a package. Industry-standard dependencies and external identifiers also do not authorize automatic downloads.

## Safe paths and resource limits

V0 restricts resource paths to ASCII letters, digits, `_`, `-`, `/`, and a final filename extension. Reject absolute paths, empty segments, `.`/`..`, backslashes, drive prefixes, duplicate paths including ASCII case collisions, and file/directory-prefix conflicts. The manifest itself cannot be a resource path. Readers need not extract the package to inspect it.

The reference checker defaults to 10,000 entries, 256 MiB per entry, 1 GiB total expanded bytes, 100 MiB of parsed JSON per document, and 200:1 maximum compression ratio. These are **implementation limits**, not maximum permitted scan sizes for the standard. Reject over-limit files with a clear resource-limit result; production scan/CT tools may adopt larger explicit limits with bounded streaming.

## Design closure in as-built

The included design, bindings, exact geometry, and referenced required resources MUST retain their exact bytes and resource IDs. `Design.resourcePins` pins the bindings and every resource referenced by the design/bindings. The design cannot pin its own bytes. `designSnapshot.sha256` pins the design JSON, so it transitively identifies the complete pinned design closure. The as-built inventory must agree with every design pin. A new package ID does not create a new design revision.

A design snapshot includes all definitions, states, and exact versions needed to resolve the selected configuration. Normative product-specific documents should be embedded. Recipient-supplied or missing normative dependencies MUST be reported; they block the strongest self-contained profile even if the package is structurally valid.

## Media identifiers

`.opp` and `application/vnd.openpartprotocol+zip` are **proposed, unregistered** identifiers. `model/step` is the proposed inventory media type for STEP resources in this draft; dispatch depends on declared encoding and the resource header, not solely on a media string. V0 does not assign a new ZIP magic number.
