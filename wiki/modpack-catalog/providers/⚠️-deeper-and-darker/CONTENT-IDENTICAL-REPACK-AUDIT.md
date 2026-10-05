# Deeper and Darker 1.4.1 — content-identical full-repack audit

Status: `61 EFFECTIVE-CONTENT-IDENTICAL REPACKS TESTED / 0 PHYSICAL SHA-1 OR FINGERPRINT MATCHES / BOUNDED FULL-REPACK-ONLY FAMILY RULED OUT / PHYSICAL DELTA STILL UNKNOWN / FAIL-CLOSED`

## Scope

This checkpoint records the successful NON-MERGE audit **#632** for the base provider **Deeper and Darker** / `deeperdarker`.

The hypothesis under test was narrower than the NeoVitae patch-reproduction audits:

> the physical JAR may differ from official File 8201775 only because the ZIP/JAR archive was reserialized or recompressed, while every effective extracted file path and file byte remains identical to the publisher artifact.

No semantic/content mutation was permitted in an accepted candidate.

The separate **Deeper and Darker: Spellbooks** / `darkermagic` addon is out of scope.

## Fixed identities

Official publisher Deeper and Darker 1.4.1:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- byte size: **3,906,057**;
- CurseForge fingerprint: **1323964125**.

Current physical pack target:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- mod id: `deeperdarker`;
- runtime: `1.4.1`;
- physical SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- physical CurseForge-style fingerprint: **1917446721**.

## Execution evidence

NON-MERGE PR: **#632**

Successful audit:

- workflow run: **37258315752**;
- audit HEAD: `107f69e3748c5d106764dc2d42963fa3891f7e3c`;
- job: `noop-repack-audit` — **SUCCESS**;
- text-only evidence artifact: **11323109979**;
- artifact digest: `sha256:ad12bf549e67b785180662ac58860c090c99b87411448fd5399891f9e82c267f`.

The workflow first re-downloaded the official release and verified all fixed publisher measurements before generating candidates.

Measured fingerprint validation:

- computed publisher fingerprint: **1323964125**;
- expected publisher fingerprint: **1323964125**.

Result:

`CURSEFORGE_FINGERPRINT_IMPLEMENTATION_VALIDATED`

## Effective-content boundary

The #632 workflow used standard Info-ZIP extraction as its **effective extracted file-tree boundary** after its own Python 3.12 direct-read path reported overlapping ZIP entries.

A dedicated follow-up structural audit in NON-MERGE **#635** did **not** reproduce that overlap condition on an independently re-downloaded and verified publisher artifact: it found **0** duplicate names, **0** duplicate local-header offsets, **0** CPython-style span-overlap violations, **0** full-entry `zipfile` read errors, `ZipFile.testzip() == NONE`, and **0** local-header/central-directory mismatches.

Therefore the overlap explanation is superseded. The #632 extracted-tree comparison remains a valid operational equivalence boundary for the 61 candidates it actually measured; only the reason for selecting that boundary is corrected.

A candidate was retained only if:

- its extracted non-directory path set matched the publisher effective tree; and
- every extracted file content SHA-256 matched the corresponding publisher-extracted file.

Accordingly, all **61** measured candidates were effective-content-identical under that boundary.

This is an operational extracted-tree equivalence test. It is not a claim that all low-level ZIP records, timestamps, extra fields, central-directory ordering or every possible archive serializer were identical.

See [`PUBLISHER-ZIP-STRUCTURE-AUDIT.md`](PUBLISHER-ZIP-STRUCTURE-AUDIT.md).

## Bounded full-repack matrix

The successful run measured **61** effective-content-identical candidates:

### Info-ZIP publisher-derived file-order rebuild

- publisher-derived file order;
- extra attributes retained or stripped with `-X`;
- DEFLATE levels **0–9**.

Candidates: **20**.

### Info-ZIP sorted file-order rebuild

- sorted file order;
- extra attributes retained or stripped with `-X`;
- DEFLATE levels **0–9**.

Candidates: **20**.

### Info-ZIP recursive rebuild

- recursive rebuild;
- extra attributes retained or stripped with `-X`;
- DEFLATE levels **0–9**.

Candidates: **20**.

### JDK `jar` rebuild

- full rebuild using `jar --no-manifest`.

Candidates: **1**.

Total:

**61 candidates**.

## Result

Physical target matches by exact SHA-1 or validated CurseForge fingerprint:

**0 / 61**

Disposition:

`NO_PHYSICAL_MATCH_IN_61-CANDIDATE_CONTENT_IDENTICAL_REPACK_FAMILY`

The workflow also reports that none of the 61 candidates reproduced the publisher archive byte size **3,906,057** exactly.

The decisive acceptance gate is still hash/fingerprint equality, not size.

## Interpretation

This audit rules out a useful bounded hypothesis:

> the physical `83f7edd0...` artifact is one of the tested ordinary full-repack/recompression forms of the publisher effective file tree, with no extracted file-content changes.

It does **not** prove:

- that every possible ZIP/JAR serializer or archive-update strategy has been tested;
- that the physical artifact necessarily changes semantic code/content;
- that the physical artifact necessarily changes any of the three public/source supernatural action roots;
- that every untested low-level archive metadata/serialization form cannot explain the mismatch;
- that the retained NeoVitae compatibility JARs are or are not the deployed artifact.

The negative result is therefore bounded to the enumerated no-op full-repack family.

## Relationship to the NeoVitae candidate audits

The evidence now excludes several distinct bounded explanations without establishing the physical bytes:

- NON-MERGE **#604**: **57** mixin-config candidate repacks, **0/57** exact physical SHA-1 matches;
- NON-MERGE **#622**: **80** expanded NeoVitae patch/repack candidates, **0/80** physical SHA-1 or fingerprint matches;
- NON-MERGE **#632**: **61** effective-content-identical full repacks, **0/61** physical SHA-1 or fingerprint matches.

These matrices test different hypotheses and are not arithmetically merged into one exhaustive search space.

Together they strengthen the conclusion that the exact deployed transformation remains unidentified.

## Catalog consequence

No semantic or structural promotion follows.

Current state remains:

- public/source supernatural baseline: **3 roots**;
- exact-current physical roots: **UNKNOWN**;
- strict semantic contribution: **+0**;
- provider state: **⚠️ partial / conditioned**.

The established public/source roots remain:

1. Otherside Portal Activation;
2. Sonorous Staff Sonic Boom;
3. Soul Elytra Boost.

## Remaining closure requirement

Promotion to `✅ Catalogado` still requires an exact bridge to the installed bytes, such as:

- authorized raw-byte inspection of the physical canonical JAR;
- raw-byte hash/fingerprint of either retained generated compatibility JAR followed by exact comparison;
- or another exact artifact proven identical to physical SHA-1 `83f7edd0a8516b2767c2cda7a3b2402f9e290d88` / fingerprint **1917446721**.

Until then, Black Arcana remains fail-closed and does not project the public/source three-root denominator into the strict exact-current numerator.
