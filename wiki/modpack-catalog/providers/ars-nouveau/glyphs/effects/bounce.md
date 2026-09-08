# Ars Nouveau — Bounce

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_bounce`
- Display name: Bounce
- School: Abjuration
- Default tier: 1
- Default mana cost: 50
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies Ars' Bounce effect, causing targets to bounce upward after falling. Provider documentation states that amplification preserves additional forward-facing motion on each bounce.

## Authority / deduplication

Ars Nouveau owns this bounce/mobility status. Black Arcana should not add a generic duplicate bounce buff or take over provider motion-state interpretation.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectBounce`).
