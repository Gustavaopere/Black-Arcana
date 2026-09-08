# Ars Nouveau — Summon Steed

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_summon_steed`
- Display name: Summon Steed
- School: Conjuration
- Default tier: 1
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`), AOE
- Source default duration: 300 s
- Source default Extend Time increment: 120 s

## Provider-native behavior

Summons at least one tamed, saddled `SummonHorse`; AOE increases the number by `1 + round(AOE multiplier)`. The horse is owned by the caster and expires after its lifetime. The caster receives 30 seconds of Summoning Sickness independently of the horse lifetime.

## Authority / deduplication

Ars Nouveau owns this temporary mount summon, its ownership and Summoning Sickness. Black Arcana should not duplicate a generic conjured steed or replace the provider lifetime/ownership ledger.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSummonSteed`).
