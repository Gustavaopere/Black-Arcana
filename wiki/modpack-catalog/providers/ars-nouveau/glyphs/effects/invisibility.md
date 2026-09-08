# Ars Nouveau — Invisibility

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_invisibility`
- Display name: Invisibility
- School: Abjuration
- Default tier: 2
- Default mana cost: 30
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies vanilla Invisibility to a living target using Ars' potion-effect timing path.

## Authority / deduplication

Ars Nouveau already owns generic temporary invisibility. Black Arcana should only add concealment magic when it has a materially different forbidden-magic contract rather than duplicating this buff.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectInvisibility`).
