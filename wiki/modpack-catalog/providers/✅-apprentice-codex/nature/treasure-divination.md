# Treasure Divination

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:treasure_divination`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 400`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 600 ticks / 30 s`
- scan interval constant: **20 ticks**
- maximum search range: **32 blocks**
- maximum detectable target count before overload: **64**

Search range:

`max(0, min(32, floor(spellPower / 100)))`

## Bounded server scan

Only a `ServerPlayer` performs the scan. At each scan interval the provider:

1. computes the bounded cube around the player;
2. iterates only chunk coordinates intersecting that cube;
3. calls `getChunkNow(...)`, therefore **never synchronously loading an unloaded chunk**;
4. skips empty chunk sections;
5. checks only blocks tagged `TREASURE_DIVINATION_TARGETS`;
6. asks the Lootr compatibility bridge whether an already-opened target should be ignored;
7. counts detectable targets and aborts immediately if the count exceeds 64;
8. keeps the nearest result using **Manhattan distance**.

If overload/noise is detected, the spell tells the player the area is too noisy and cancels the channel.

### Source-comment discrepancy

The executable constant is `SEARCH_INTERVAL_TICKS = 20`, i.e. one second at 20 TPS. An inline developer comment later says the loaded area is scanned "every 2 seconds". The catalog treats the executable 20-tick constant as source behavior and records the comment mismatch for runtime QA instead of silently reconciling it.

## What it does

Provider guide semantics: focus mana to learn how far away the nearest valuable-looking target is. The spell intentionally does not promise that every detected object is actually valuable, and its detectable target set is provider/tag controlled.

## Performance/authority

This is a useful positive reference for Black Arcana Divination: bounded range, loaded-chunk-only access, periodic—not per-tick—scanning and an overload ceiling. Black Arcana must not launch a second treasure scan after observing this provider cast.

## Deduplication

Direct Divination overlap. One scan result/message is part of one continuous provider cast, not a separate magical action per found block.

## Confidence

`SOURCE-PINNED SCAN LOOP / TAG CONTENT + LOOTR EXACT PACK BEHAVIOR + 20-TICK VS COMMENT RUNTIME QA PENDING`