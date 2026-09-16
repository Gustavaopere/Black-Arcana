# Ars Nouveau — Hex

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

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

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:fermented_spider_eye` + `minecraft:blaze_rod` ×3 + `minecraft:wither_rose`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau already owns this conditional vulnerability/healing/mana-suppression curse. Black Arcana curse content must be mechanically distinct and must not double-apply Hex's provider-local amplification or mana/healing penalties.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectHex`).
