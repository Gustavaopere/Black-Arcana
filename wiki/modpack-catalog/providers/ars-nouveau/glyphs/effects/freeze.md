# Ars Nouveau — Freeze

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

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

## Authority / deduplication

Ars Nouveau owns this fluid/ice conversion and slowing primitive. Independent Black Arcana freezing/world mutation must remain `WorldEffectPolicy`-controlled and must not replay Ars conversions.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFreeze`).
