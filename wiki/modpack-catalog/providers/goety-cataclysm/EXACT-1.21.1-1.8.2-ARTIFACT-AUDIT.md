# Goety Cataclysm 1.21.1-1.8.2 — exact artifact audit

Status: `EXACT HASH-MATCHED / COUNTED_EXACT / COMPONENT #60 CANDIDATE UNTIL MERGE`

Physical SHA-1 and publisher artifact SHA-1 are identical: `4e3052a082200371b36e1a88fdce05e294d82757` (CurseForge `1224214 / 8518940`).

## Exact semantic facts

- 28 addon-owned Focus holders with provider-owned spell surfaces.
- all 28 have packaged acquisition recipes: 24 ritual, 4 ordinary crafting.
- 48 packaged `goety:ritual` recipes.
- 24 rituals are Focus acquisition only and are deduplicated against their Focus identities.
- 24 non-Focus rituals remain; all have distinct outcomes and no mod-loaded condition.
- non-Focus outcome classes: 10 conversion, 13 summon/thrall, 1 fabricator.
- neither the 28 Focus identities nor the 24 non-Focus outcomes duplicates the exact Goety 3.1.4 semantic inventory already counted in Phase 2BH.
- Registration initializer: 0 branches, 0 config references; no enable/disable-like config field was found by the narrow gate scan.

Semantic disposition: **+52 = 28 Focus + 24 non-Focus rituals**.

## Evidence chain

NON-MERGE PR #206. Structural `34704449593 / 10301367858`; semantic `34704823100 / 10301168646`; registration gate `34705567753 / 10301603762`.

Clean-room: the evidence branch never commits the JAR and durable docs retain no implementation bodies/assets. ARR is preserved. Older 1.20 public source is not treated as exact 1.21.1 implementation authority.
