# Ars Nouveau — Summon Decoy

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_summon_decoy`
- Display name: Summon Decoy
- School: Conjuration
- Default tier: 3
- Default mana cost: 200
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source default duration: 30 s
- Source default Extend Time increment: 15 s

## Provider-native behavior

Summons an `EntityDummy` decoy and redirects nearby `Mob` targets within an inflated 20×10×20 search volume to attack the decoy. The spell applies a minimal Summoning Sickness duration after creation.

## Authority / deduplication

Ars Nouveau owns this aggro-decoy primitive. Black Arcana illusion/control content should not clone the same temporary taunt dummy without a materially different contract.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSummonDecoy`).
