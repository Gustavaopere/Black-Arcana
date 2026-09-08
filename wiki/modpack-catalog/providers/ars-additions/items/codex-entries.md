# Codex Entry / Lost Codex Entry / Ancient Codex Entry

Status: `SOURCE-PINNED 21.3.0 / GLYPH-LEARNING SEMANTICS AUDITED / ACQUISITION PARTIAL`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

## Registry ids

- `ars_additions:codex_entry` — Tier I
- `ars_additions:lost_codex_entry` — Tier II
- `ars_additions:ancient_codex_entry` — Tier III

## Provider-native learning behavior

Use is server-side and obtains the Ars Nouveau player capability. The item builds the candidate set from the provider Glyph Registry and filters out:

- glyphs disabled by Ars config;
- glyphs tagged by Ars Additions as forgotten-knowledge exclusions;
- default starting spells;
- glyphs the player already knows;
- glyphs outside the Codex Entry's tier.

One eligible glyph is chosen randomly and unlocked through `IPlayerCap.unlockGlyph`, after which the Ars capability is synchronized.

The Codex Entry is consumed after use.

If no eligible glyph remains, no duplicate unlock is fabricated. Instead the provider awards vanilla experience:

- Tier I Codex Entry: **55 XP points**;
- Tier II Lost Codex Entry: **160 XP points**;
- Tier III Ancient Codex Entry: **480 XP points**.

These fallback values are vanilla XP, not Ars recipe XP, RPG Skill Tree XP, Mastery or Black Arcana progression.

## Acquisition evidence

`AddonSetup` adds the normal Codex Entry to Ars Nouveau `DungeonLootTables.BASIC_LOOT`.

The exact Ars Additions ruined-portal chest table also contains **1–4 normal Codex Entries** in a guaranteed one-roll pool for that table.

The current exact-source pass did not prove a recipe/loot injection for Lost Codex Entry or Ancient Codex Entry. Their registry/runtime semantics are confirmed, but acquisition remains `UNPROVEN IN CURRENT SOURCE PASS` rather than inferred from names or tier.

## Authority / deduplication

Glyph learning remains Ars Nouveau player-capability authority. Black Arcana and RPG Skill Tree must not maintain a parallel learned-glyph ledger, award duplicate progression for the same unlock or reinterpret fallback vanilla XP as Mastery.
