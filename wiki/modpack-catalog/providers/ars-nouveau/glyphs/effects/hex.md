# Ars Nouveau — Hex

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_hex`
- Display name: Hex
- School: Abjuration
- Default tier: 3
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), Amplify
- Default Amplify limit: 4
- Source default duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

Applies Ars' `Hex` effect. Provider documentation states that Hex increases damage taken while the target is poisoned, withered, burning or frozen, and halves Mana Regeneration and healing while active. Amplify increases effect level; Time augments adjust duration.

## Authority / deduplication

Ars Nouveau already owns this conditional vulnerability/healing/mana-suppression curse. Black Arcana curse content must be mechanically distinct and must not double-apply Hex's provider-local amplification or mana/healing penalties.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectHex`).
