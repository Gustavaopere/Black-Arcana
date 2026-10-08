# Deeper and Darker 1.4.1 — Python zipfile content-identical repack audit

Status: `22 PYTHON ZIPFILE CONTENT-IDENTICAL REPACKS TESTED / 0 PHYSICAL SHA-1 OR FINGERPRINT MATCHES / 0 RETAINED LOCAL-SIZE MATCHES / 4 PUBLISHER-SIZE-ONLY MATCHES / BOUNDED PYTHON-ZIPFILE FAMILY RULED OUT / FAIL-CLOSED`

## Scope

This checkpoint records the successful NON-MERGE audit **#640** for the base provider **Deeper and Darker** / `deeperdarker`.

It fills a specific gap left by NON-MERGE **#632**. That earlier PR originally described a Python `zipfile` family but its final measured **61-candidate** result contained only Info-ZIP and JDK rebuilds.

Follow-up NON-MERGE **#635** then established that a freshly re-downloaded and verified publisher artifact can be fully read by Python `zipfile` without duplicate names, local-offset duplication, overlap-span violations, per-entry read errors, `testzip()` corruption or local-vs-central metadata mismatches.

That made a direct bounded Python-`zipfile` rewrite experiment technically justified.

The separate **Deeper and Darker: Spellbooks** / `darkermagic` addon is out of scope.

## Fixed identities

Official publisher Deeper and Darker 1.4.1:

- filename: `deeperdarker-neoforge-1.21.1-1.4.1.jar`;
- SHA-1: `b6094adde68bd4b909bc75c64901e1f3fb99ad8f`;
- SHA-256: `eee3f51222b0bcc714def002ff089ac9e131d3cae4575b542fd0a7dd101fe0af`;
- byte size: **3,906,057**;
- CurseForge-style fingerprint: **1323964125**.

Current physical target:

- SHA-1: `83f7edd0a8516b2767c2cda7a3b2402f9e290d88`;
- CurseForge-style fingerprint: **1917446721**.

Retained local compatibility artifact sizes:

- first generated Deeper compatibility JAR: **3,906,052 bytes**;
- generated `v2` Deeper compatibility JAR: **3,906,044 bytes**.

## Execution evidence

NON-MERGE PR: **#640**

Successful audit:

- workflow run: **37263427789**;
- audit HEAD: `ceece176c8ee950ab4e85bd3c35b4f96411956a9`;
- job: `python-zipfile-repack-audit` — **SUCCESS**;
- text-only evidence artifact: **11325760264**;
- artifact digest: `sha256:3a5bfbddaaeb767f29d93ffad4c620f4653e6604cc00bbfde8c53293599a0366`.

The workflow re-downloaded and verified the official publisher bytes before candidate generation.

Measured publisher fingerprint validation:

- computed: **1323964125**;
- expected: **1323964125**.

Result:

`CURSEFORGE_FINGERPRINT_IMPLEMENTATION_VALIDATED`

## Candidate boundary

The workflow generated **22** candidates in publisher entry order.

Two bounded `ZipInfo` strategies were tested:

1. **copy-info** — shallow-copy each publisher `ZipInfo` record before rewriting the entry;
2. **rebuild-info** — construct a new `ZipInfo` while preserving the public metadata fields used by the bounded workflow.

For each strategy:

- Python default DEFLATE behavior;
- explicit DEFLATE levels **0–9**.

Every candidate was required to preserve the publisher entry manifest:

- entry filename;
- directory/non-directory identity;
- compression method;
- uncompressed file size;
- non-directory file-content SHA-256;
- publisher entry order.

A candidate failing that manifest check would terminate the workflow rather than be counted.

## Result

Measured candidates:

**22**

Exact physical identity gate:

- SHA-1 or physical fingerprint matches: **0 / 22**.

Retained local-size matches:

- **3,906,052 bytes**: **0 / 22**;
- **3,906,044 bytes**: **0 / 22**.

Publisher total-size matches:

- **3,906,057 bytes**: **4 / 22**.

The four publisher-size candidates are:

- `python-copy-info-level-default.jar`;
- `python-copy-info-level-6.jar`;
- `python-rebuild-info-level-default.jar`;
- `python-rebuild-info-level-6.jar`.

All four collapse to the same measured bytes:

- size: **3,906,057**;
- SHA-1: `eb6f9fbc5adfc4e12de9e6b2462370da74572acc`;
- CurseForge-style fingerprint: **824150764**.

They match only the publisher's **total byte size**. They match neither:

- publisher SHA-1 `b6094add...` / fingerprint **1323964125**; nor
- physical SHA-1 `83f7edd0...` / fingerprint **1917446721**.

Size equality is not treated as byte identity.

Disposition:

`NO_PHYSICAL_MATCH_IN_22-CANDIDATE_PYTHON_ZIPFILE_CONTENT_IDENTICAL_REPACK_FAMILY`

## Interpretation

This audit rules out the following bounded hypothesis:

> the physical `83f7edd0...` JAR is one of these 22 ordinary Python-`zipfile` full rewrites of the verified publisher entry/content set under the two tested `ZipInfo` strategies and default/0–9 DEFLATE settings.

It does **not** prove:

- that every Python version/zlib build produces the same serialization;
- that every possible `ZipInfo` field policy has been tested;
- that every append/update/in-place ZIP strategy has been tested;
- that every archive serializer has been tested;
- that physical semantic file contents necessarily differ;
- that either retained local compatibility JAR is or is not the deployed artifact.

The negative result is bounded to the explicitly enumerated 22-candidate family.

## Relationship to prior bounded audits

The documented negative matrices now include:

- **#604** — 57 bounded mixin-config repack candidates; **0/57** exact physical SHA-1 matches;
- **#622** — 80 expanded NeoVitae patch/repack candidates; **0/80** physical SHA-1/fingerprint matches;
- **#632** — 61 Info-ZIP/JDK content-identical full repacks; **0/61** physical SHA-1/fingerprint matches;
- **#635** — structural publisher ZIP audit; no candidate generated, but no reproducible publisher overlap/read-error condition;
- **#640** — 22 Python-`zipfile` content-identical full rewrites; **0/22** physical SHA-1/fingerprint matches.

These matrices test overlapping but non-exhaustive bounded hypotheses and are not arithmetically combined into a claim of exhaustive coverage.

## Clean-room boundary

- publisher bytes were downloaded only at CI runtime;
- candidate JARs existed only inside the runner workspace;
- publisher/candidate JARs were deleted before artifact upload;
- the uploaded artifact contains only text hashes/metadata.

No third-party JAR bytes are committed or distributed by Black Arcana.

## Catalog consequence

No semantic promotion follows.

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

Until then, Black Arcana remains fail-closed.
