# Ars Nouveau — Glide

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_glide`
- Display name: Glide
- School: Elemental Air
- Default tier: 3
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source config default duration: 180 s
- Source config default Extend Time increment: 120 s

## Provider-native behavior

Applies Ars' Glide effect, allowing elytra-like flight behavior. The source also exposes `canGlide`, which treats either the Glide effect or Ars' Gliding Perk as sufficient for provider gliding eligibility.

## Authority / deduplication

Ars Nouveau already owns temporary elytra-like gliding and a perk-based alternative path. Black Arcana mobility/familiar content should not add a generic duplicate glide buff or take over Ars' glide eligibility state.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectGlide`).
