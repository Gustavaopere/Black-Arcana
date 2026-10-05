# T.O Magic n' Extras — expanded surgical-repack exclusion checkpoint

Status: `164 BOUNDED ONE-CLASS REPACK VARIANTS EXCLUDED / NO SHA-1 MATCH / NO CURSEFORGE-FINGERPRINT MATCH / NO RETAINED FIXED-KEYLOOT SIZE MATCH / CURRENT PHYSICAL STILL UNIDENTIFIED`

## Purpose

This checkpoint expands the earlier PR #474 negative lineage test for the current physical Traveloptics artifact.

It asks a deliberately narrow question:

> Can the current physical SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`, or the retained Aug-17 `fixed-keyloot.jar` size, be reproduced by a broader matrix of straightforward one-class repacks that replace only `TOLootModifiers.class` in publisher File `6342780` with the corresponding class from public patch File `8861368`?

The answer for the tested matrix is **no**.

This is negative lineage evidence. It does not identify the installed bytes or prove what the retained Aug-17 candidate contains.

## Authority

Temporary NON-MERGE clean-room audit PR **#648**:

- audit HEAD: `42469067f01cdc9157d704e2ee7be08c8e70067a`;
- workflow: **Traveloptics Expanded Surgical Repack Clean-room Audit**;
- run: `37317446376` — **SUCCESS**;
- text-only artifact: `11348308934`;
- artifact digest: `sha256:811beda99b541c7018dbabafe39ecc1100868b3d8558015bc6e2f9ef0637dcd9`.

Inputs were hard-fingerprinted public artifacts:

- publisher File `6342780` SHA-1 `3808493ce45cdfeb6408e85578adecf13df698e8`;
- public patch File `8861368` SHA-1 `680fa679d8ea2419a79571f455436367222f6f9d`;
- current physical target SHA-1 `7b74816e89cc15dd0b5a31d9ea1e456024e8fae4`;
- current physical CurseForge fingerprint `4254006126`;
- retained Aug-17 `traveloptics-4.4.0.1-1.21.1-fixed-keyloot.jar` size: **18,393,641 bytes**.

No transformed JAR was retained or merged. The audit retained archive/hash/size/ZIP metadata only and did not parse or decompile class implementation.

## Matrix

The bounded matrix generated **164** candidates using the public patch's already-known replacement member:

`com/gametechbc/traveloptics/loot/TOLootModifiers.class`

Tested archive-production variables:

- Info-ZIP delete + add;
- Info-ZIP direct update;
- default extra fields versus `-X`;
- compression levels **0–9**;
- replacement-member timestamps from:
  - publisher member;
  - public patch member;
  - retained Library timestamp represented as UTC wall-clock;
  - the same retained instant represented as UTC-03/Brazil wall-clock;
- JDK `jar uf` for each timestamp mode.

Each candidate was checked for:

- SHA-1;
- CurseForge fingerprint;
- archive size;
- target-member compression metadata;
- ZIP integrity;
- content delta versus publisher File `6342780`.

## Result

Across all **164** candidates:

- exact current SHA-1 matches: **0**;
- current CurseForge fingerprint matches: **0**;
- retained Aug-17 `fixed-keyloot.jar` size matches: **0**.

The closest tested candidates to the retained **18,393,641-byte** `fixed-keyloot.jar` were **18,393,560 bytes**, still **81 bytes smaller**, and had different SHA-1 and CurseForge fingerprints.

The summary's closest candidates each retained a one-entry content delta relative to the publisher artifact; none became byte-identical to either target.

## What this excludes

Within the exact tested matrix, Black Arcana may now reject the hypothesis that either:

1. current physical `7b74816e...`; or
2. the retained Aug-17 18,393,641-byte `fixed-keyloot.jar`

is byte-identical to one of these 164 straightforward repacks of publisher File `6342780` using only the known public-patch `TOLootModifiers.class`.

This materially expands PR #474's earlier exclusion surface.

## What this does not establish

This checkpoint does **not** prove:

- that the current physical artifact changes more than one ZIP entry;
- that its `TOLootModifiers.class` differs from the public patch class;
- that the Aug-17 `fixed-keyloot.jar` is unrelated to the later installed replacement;
- how either local artifact was built;
- which ZIP implementation/options were actually used;
- provenance/author of the replacement;
- exact-current 33/33 registry equality;
- exact-current mechanics/stat equality;
- exact-current loot-modifier serializer object identity;
- Blackout survival acquisition.

Other archive strategies, metadata layouts, content deltas or independently compiled repair classes were not enumerated and remain possible.

## Gate consequence

Gate 1 remains **open for provenance/content delta**, but the candidate space is narrower.

Current disposition remains:

`OTHER_VERIFIED / CURRENT PHYSICAL CONTENT UNMATERIALIZED / STRICT +0`

The next useful evidence is still one of:

- exact bytes for SHA-1 `7b74816e...`;
- an authoritative checksum/content manifest for those exact bytes;
- a reproducible build/provenance record that cryptographically resolves to `7b74816e...`;
- equivalent exact-current content attestation.

Repeating additional arbitrary repack permutations without a new clue is not promoted as a closure strategy.
