# Goety Iron 3.1 — exact artifact audit

Status: `EXACT HASH-MATCHED / COUNTED_EXACT / COMPONENT #59`

Physical SHA-1 and publisher artifact SHA-1 are identical: `c8529867e798661ed01fb2948abda23735888fc6` (CurseForge `1367643 / 8662179`).

## Exact semantic facts

- 2 addon-owned Focus holders: `FIERY_FOCUS`, `TARNISHED_FOCUS`.
- Both are Goety Focus surfaces backed by addon-owned summon-spell identities.
- 14 packaged `goety:ritual` recipes.
- 2 rituals are Focus acquisition only and are deduplicated against their Focus identities.
- 12 non-Focus rituals remain; all 12 have distinct outcomes and no mod-loaded condition.
- None of the 2 Focus IDs or 12 non-Focus outcomes duplicates the exact Goety 3.1.4 semantic inventory already counted in Phase 2BH.
- Registration initializer: 0 branches, 0 config references; no enable/disable-like config field was found by the narrow gate scan.

Semantic disposition: **+14 = 2 Focus + 12 non-Focus rituals**.

## Evidence chain

NON-MERGE PR #205. Structural `34704435612 / 10301537361`; semantic `34704813857 / 10301716793`; registration gate `34705555893 / 10301284496`.

Clean-room: the evidence branch never commits the JAR and durable docs retain no implementation bodies/assets. The CurseForge MIT vs Modrinth ARR discrepancy remains unresolved; the stricter posture controls.
