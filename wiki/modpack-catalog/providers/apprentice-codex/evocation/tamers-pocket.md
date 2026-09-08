# Tamer's Pocket

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:tamers_pocket`
- **Iron's school:** Evocation
- **Levels:** 1
- **Minimum rarity:** Uncommon
- **Cast type:** Long
- **Cooldown:** 4 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `castTime = 20 ticks`
- interaction range: **8 blocks**
- stored-pet count is read from provider capability state `TAMERS_POCKET_STATE`

## Provider lifecycle

Pre-cast is server-player-only and locks one of three provider modes into serializable cast data: withdraw a looked-at owned pet, withdraw nearby owned pets as an area operation, or deploy stored pets to prevalidated positions. The cast then executes against those locked UUIDs/positions.

The exact source stores multiple pets; this is not a one-pet pocket. Entity serialization, ownership checks and deployment safety remain provider-owned.

## Causality and progression

Withdrawing several pets in one area cast remains one player cast. Stored pets do not become Black Arcana familiars merely because they are persisted by this spell. A future Binding integration must preserve each provider pet identity and avoid a second summon/storage lifecycle.

## Deduplication

Occupies the **owner-pet withdrawal, persistent pocket storage and later safe redeployment** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CONFIG+RANGE+MULTI-PET MODES+SERVER-LOCKED CAST DATA / STORAGE LIMIT+ENTITY SERIALIZATION+DEPLOYMENT SAFETY DETAILS REQUIRE FULL CLASS/STATE AUDIT`