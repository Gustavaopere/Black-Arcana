# Ars Nouveau — Freeze

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_freeze`
- Display name: Freeze
- School: Elemental Water
- Default tier: 1
- Default mana cost: 15
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify, AOE, Pierce, Sensitive
- Default Sensitive limit: 1
- Source config default Slow duration: 10 s
- Source config default Extend Time increment: 5 s

## Provider-native behavior

On living targets, Freeze applies vanilla Slowness. On blocks it can convert water to Ice (or Frosted Ice with Sensitive), lava to Obsidian/Cobblestone, extinguish fire, upgrade Ice to Packed Ice and Packed Ice to Blue Ice. AOE/Pierce expand the affected block set.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:water_essence` + `minecraft:snow_block` ×2.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this fluid/ice conversion and slowing primitive. Independent Black Arcana freezing/world mutation must remain `WorldEffectPolicy`-controlled and must not replay Ars conversions.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFreeze`).
