# T.O Magic n' Extras 4.4.0.1 — expanded surgical repack lineage audit

Status: `164 BOUNDED SURGICAL CANDIDATES / 0 PHYSICAL SHA-1 MATCHES / 0 PHYSICAL FINGERPRINT MATCHES / 0 RETAINED FIXED-SIZE MATCHES / NEGATIVE LINEAGE EVIDENCE ONLY`

## Purpose

This checkpoint expands the earlier PR #474 one-entry repack test around the retained August `fixed-keyloot` artifact.

It tests a bounded family in which exact publisher File `6342780` is modified only by replacing:

`com/gametechbc/traveloptics/loot/TOLootModifiers.class`

with the corresponding class bytes from public patch File `8861368`.

The audit is archive/hash/size evidence only. It does not parse or decompile the replacement implementation and does not redistribute transformed JARs.

## Fixed inputs

Publisher File `6342780`:

- SHA-1: `3808493ce45cdfeb6408e85578adecf13df698e8`;
- bytes: **18,393,445**;
- CurseForge fingerprint: **1868150654**.

Public patch File `8861368`:

- SHA-1: `680fa679d8ea2419a79571f455436367222f6f9d`.

Current physical target:

- SHA-1: `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- CurseForge fingerprint: **4254006126**.

Retained Project Library candidate metadata:

- `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar`;
- recorded bytes: **18,393,641**.

The workflow independently validates its CurseForge fingerprint implementation against publisher fingerprint **1868150654** before measuring candidates.

## Bounded matrix

Temporary NON-MERGE PR **#648** generated **164** candidates from the publisher archive using the public patch replacement class.

Archive strategies:

- Info-ZIP delete + add;
- Info-ZIP direct update;
- JDK `jar uf`.

Info-ZIP dimensions:

- default extra-field handling and `-X`;
- compression levels **0–9**;
- four bounded replacement-member timestamps:
  - publisher member timestamp;
  - public patch member timestamp;
  - retained Library creation timestamp interpreted as UTC wall-clock;
  - the same retained instant interpreted as UTC-03 wall-clock.

The four JDK `jar uf` candidates vary the same timestamp modes.

For each candidate the workflow records archive size, SHA-1, CurseForge fingerprint, target-member compression metadata, ZIP integrity and content-delta diagnostics.

## Successful run

- PR: **#648** — temporary / NON-MERGE;
- workflow run: **37317446376**;
- audit job: **111787652542** — `SUCCESS`;
- audited head: `42469067f01cdc9157d704e2ee7be08c8e70067a`;
- text-only artifact: **11348308934**;
- artifact digest: `sha256:811beda99b541c7018dbabafe39ecc1100868b3d8558015bc6e2f9ef0637dcd9`.

PR #648 was closed without merge after evidence capture.

The ordinary Black Arcana CI on the temporary PR separately failed because the Iron's Spellbooks API dependency download from `code.redspace.io` timed out. That network failure is independent of the dedicated audit workflow, which completed successfully.

## Measured result

Across **164** candidates:

- exact physical SHA-1 `7b74816e...` matches: **0 / 164**;
- physical CurseForge fingerprint `4254006126` matches: **0 / 164**;
- retained `fixed-keyloot.jar` size **18,393,641** matches: **0 / 164**.

The closest reported size family contains eight level-1/default-extra candidates at:

- **18,393,560 bytes**;
- delta from retained `fixed-keyloot.jar`: **-81 bytes**;
- replacement-member compressed size: **983 bytes**;
- reported changed-content entry count: **1**.

Those eight candidates use both Info-ZIP strategies across the four tested timestamp modes. Their SHA-1 values and CurseForge fingerprints all differ from the current physical target.

The next closest reported family begins at:

- **18,393,544 bytes**;
- delta: **-97 bytes**;
- replacement-member compressed size: **967 bytes**;
- reported changed-content entry count: **1**.

## Interpretation

This excludes the **exact 164 archive outputs** in the tested surgical family as identities for either:

- the current physical `7b74816e... / 4254006126` artifact; or
- the retained Aug-17 `fixed-keyloot.jar` by exact recorded size.

It also strengthens the earlier #474 result because the bounded search now varies compression level, extra-field handling and plausible replacement timestamps instead of testing only a handful of common reconstruction methods.

It does **not** establish:

- how the retained `fixed-keyloot.jar` was generated;
- that the retained candidate differs semantically from the public patch class;
- which archive serializer/options were actually used;
- that the current physical artifact changes only `TOLootModifiers.class`;
- byte identity or ancestry between the retained candidate and current `7b74816e...`;
- exact-current spell-registry equality;
- exact-current loot-codec object identity;
- Blackout survival acquisition.

## Catalog consequence

No provider promotion follows.

Traveloptics remains:

`⚠️ partial / conditioned / OTHER_VERIFIED / strict +0`.

Gate 1 is narrowed by additional **negative lineage evidence**, but exact-current bytes/content provenance remains open.
