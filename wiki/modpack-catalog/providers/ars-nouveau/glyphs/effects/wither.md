# Ars Nouveau — Wither

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_wither`
- Display name: Wither
- School: Abjuration
- Default tier: 3
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify
- Default Amplify limit: 4
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies vanilla Wither using Ars' potion-effect path. Amplify raises effect level; Time augments modify duration.

## Authority / deduplication

Ars Nouveau owns this generic Wither application. Black Arcana curse/death content must demonstrate a distinct persistent/ritual/hazard contract rather than reskinning the same debuff.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectWither`).
