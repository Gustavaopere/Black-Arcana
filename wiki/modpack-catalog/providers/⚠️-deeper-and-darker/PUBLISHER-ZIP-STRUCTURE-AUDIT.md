# Deeper and Darker 1.4.1 — publisher ZIP structure audit

Status: `PUBLISHER ZIP STRUCTURE VERIFIED / NO DUPLICATE NAMES OR LOCAL OFFSETS / NO OVERLAP-SPAN VIOLATIONS / NO ZIPFILE READ ERRORS / #632 STRUCTURAL WORKAROUND RATIONALE SUPERSEDED / PHYSICAL ARTIFACT STILL UNMATCHED`

## Scope

This checkpoint records the successful NON-MERGE structural audit **#635** for the official Deeper and Darker 1.4.1 publisher artifact.

It follows NON-MERGE **#632**, which tested 61 effective-content-identical full repacks and found **0/61** matches to the physical SHA-1/fingerprint. The #632 workflow used an Info-ZIP extraction boundary after its Python 3.12 path reported overlapping ZIP entries during direct per-entry reading.

PR #635 was created specifically to determine whether that overlap explanation is reproducible on the independently verified publisher artifact.

This audit is limited to the base provider **Deeper and Darker** / `deeperdarker`. The separate **Deeper and Darker: Spellbooks** / `darkermagic` addon is out of scope.

## Fixed identities

Official publisher artifact:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- byte size: **3,906,057**.

Physical target:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- CurseForge-style fingerprint: **1917446721**.

## Execution evidence

NON-MERGE PR: **#635**

Successful audit:

- workflow run: **37261688172**;
- audit HEAD: `966700ad38b650c07739dd784827105c52f39729`;
- job: `zip-structure-audit` — **SUCCESS**;
- text-only evidence artifact: **11324932365**;
- artifact digest: `sha256:c18bfe979ccddb34688a551b6ce0aeaad9839185d6039e29608b37fa32a76b58`.

The workflow re-downloaded and verified the official v1.4.1 artifact before structural analysis.

## Measured publisher ZIP structure

Measured values:

- total file size: **3,906,057**;
- EOCD offset: **3,906,035**;
- central-directory offset: **3,596,362**;
- central-directory size: **309,673**;
- CPython-style archive prefix/concatenation adjustment: **0**;
- central-directory entries: **2,900**;
- unique entry names: **2,900**;
- duplicate entry names: **0**;
- duplicate local-header offsets: **0**;
- CPython-style compressed-data span overlap violations: **0**;
- full-entry `zipfile` read errors: **0**;
- `ZipFile.testzip()`: **NONE**;
- local-header / central-directory metadata mismatches: **0**;
- minimum margin from compressed-data end to the next local-header or central-directory bound: **0**.

Disposition:

`NO_REPRODUCIBLE_ZIP_OVERLAP_OR_READ_ERROR_ON_VERIFIED_PUBLISHER_ARTIFACT`

## Correction to #632 interpretation

The measured result of #632 remains valid:

- 61 effective-content-identical Info-ZIP/JDK full-repack candidates were generated;
- all accepted candidates matched the publisher extracted path/content boundary used by that workflow;
- **0/61** candidates matched physical SHA-1 `83f7edd0...` or physical fingerprint **1917446721**.

What #635 supersedes is only the explanatory rationale that the verified publisher artifact itself necessarily contains an overlapping ZIP layout that prevents direct Python `zipfile` per-entry reads.

The dedicated structural audit did **not** reproduce:

- duplicate names;
- duplicate local-header offsets;
- compressed-data span overlaps;
- direct full-entry read errors;
- `testzip()` corruption;
- local-vs-central metadata inconsistencies.

Therefore Black Arcana no longer treats “publisher ZIP overlap” as an established structural property of official File 8201775.

## What remains valid from #632

The bounded no-op conclusion remains:

> none of the 61 tested ordinary content-identical full-repack/recompression candidates reproduces the physical SHA-1/fingerprint.

That conclusion does not depend on the discarded overlap explanation.

The #632 candidate matrix still cannot establish:

- every possible serializer/repacker;
- every possible metadata-preserving archive-update algorithm;
- every possible low-level ZIP layout;
- whether the physical artifact contains semantic file-content changes;
- whether the physical artifact derives from one of the retained NeoVitae compatibility JARs.

## Relationship to the other Deeper candidate audits

The currently documented bounded negative matrices are:

- **#604** — 57 mixin-config repack candidates; **0/57** exact physical SHA-1 matches;
- **#622** — 80 expanded NeoVitae patch/repack candidates; **0/80** physical SHA-1/fingerprint matches;
- **#632** — 61 content-identical ordinary full repacks; **0/61** physical SHA-1/fingerprint matches;
- **#635** — publisher ZIP structural reconnaissance; no candidate generated, but the alleged publisher-overlap condition is not reproduced.

These are complementary bounded tests, not one exhaustive search space.

## Catalog consequence

No semantic promotion follows.

Current state remains:

- public/source supernatural baseline: **3 roots**;
- exact-current physical roots: **UNKNOWN**;
- strict semantic contribution: **+0**;
- provider state: **⚠️ partial / conditioned**.

The public/source roots remain:

1. Otherside Portal Activation;
2. Sonorous Staff Sonic Boom;
3. Soul Elytra Boost.

## Remaining closure requirement

Promotion to `✅ Catalogado` still requires an exact bridge to the installed bytes, such as:

- authorized raw-byte inspection of the physical canonical JAR;
- raw-byte hash/fingerprint of a retained generated compatibility JAR followed by exact comparison;
- or another artifact proven identical to physical SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88` / fingerprint **1917446721**.

Until then, Black Arcana remains fail-closed.
