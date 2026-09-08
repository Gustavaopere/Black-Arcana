# Ars Nouveau — Snare

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_snare`
- Display name: Snare
- School: Elemental Earth
- Default tier: 1
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source default base duration: 8 s
- Source default Extend Time increment: 1 s

## Provider-native behavior

Snare applies Ars' Snare mob effect to living targets, immediately zeroes their motion, and supports duration adjustment through Time augments. When used on an Ars `EnchantedFallingBlock`, it attempts to ground/place the block and propagates block-shaping spell behavior.

## Authority / deduplication

Ars Nouveau owns this immobilization/status effect and its block-shaping interaction. Black Arcana should not double-apply movement suppression or replay block settlement when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSnare`).
