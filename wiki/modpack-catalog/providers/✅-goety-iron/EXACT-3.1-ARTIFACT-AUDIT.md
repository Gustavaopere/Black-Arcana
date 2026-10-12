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

## Exact recipe path→outcome re-audit — 2026-10-11

A lacuna histórica de paths/outcomes foi encerrada com reauditoria textual do **JAR SHA-1 hash-matched** no [workflow #38186445480](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38186445480) (commit de auditoria NON-MERGE `474f17eda068883629b9017eaf5c6f37ae980e0e`). A [matriz preservada](RITUAL-INVENTORY-EXACT-3.1.md) contém **14/14 paths, recipe type, subtype, result IDs, outcome IDs e condições no topo**: 10 conversões/summons `goety:convert_complete_tamed`, 2 crafting outcomes não-Focus `goety:craft` e 2 crafting Focus-acquisition `goety:craft`. Foram produzidas [12 fichas não-Focus](RITUAL-CARDS-3.1.md), permanecendo **+0 identidades novas** e **14** no ledger. `goety:jei_dummy/none` nos campos de resultado de conversão é **placeholder**, não outcome adicional. Nenhum runtime foi verificado no pack nem material proprietário redistribuído.

## Evidence chain

NON-MERGE PR #205. Structural `34704435612 / 10301537361`; semantic `34704813857 / 10301716793`; registration gate `34705555893 / 10301284496`.

Clean-room: the evidence branch never commits the JAR and durable docs retain no implementation bodies/assets. The CurseForge MIT vs Modrinth ARR discrepancy remains unresolved; the stricter posture controls.
