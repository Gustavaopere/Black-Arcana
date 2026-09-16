# Long Stride

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:long_stride`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Crafting:** disabled
- **Looting:** disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 12`
- `manaCostPerLevel = -1` (irrelevant to the one-level registry range)
- `castTime = 1200 ticks = 60 s`
- effective cast time deliberately ignores cast-time reduction
- provider mobility effect refresh: every `5 ticks`
- level-1 movement bonus displayed by this spell: `10%`

## Provider behavior

Long Stride continuously refreshes the provider's `LONG_STRIDE_MOBILITY` effect while channelled. The public guide associates it with the Explorer's Cane and describes faster travel, treating water/lava as traversable surfaces and stepping over moderate obstacles.

The exact movement/surface hooks live in the provider effect/event layer rather than the spell class; this sheet does not invent those internals beyond the source-backed guide behavior.

## Acquisition

The spell is item-only in source: crafting and looting are both disabled. Registered presence does not imply survival-scroll availability.

## Causality

Continuous effect refresh is provider maintenance for one sustained cast. It must not generate per-tick RPG Mastery or Black Arcana hazard/proc chains.

## Deduplication

Occupies the **item-bound sustained exploration mobility / terrain-traversal channel** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT CHANNEL+COST+EFFECT REFRESH / SURFACE-TRAVERSAL EVENT INTERNALS + ITEM ACQUISITION + RUNTIME QA PENDING`