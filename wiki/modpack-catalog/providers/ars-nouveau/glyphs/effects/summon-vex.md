# Summon Vex

- Registry ID: `ars_nouveau:glyph_summon_vex`
- Source class: `EffectSummonVex`
- School: Conjuration
- Default tier: **3**
- Default mana: **150**
- Default summon duration: **15 seconds**, Extend Time contribution **10 seconds** per provider duration unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

If the provider summon gate allows the caster, the effect spawns **three** allied Ars Vex entities near the resolved position. Each is owned by the caster, receives limited life for the computed duration and participates in the provider summon pipeline. The caster receives Ars Nouveau Summoning Sickness for the same computed lifetime.

Compatible augments: Extend Time, Reduce Time through Ars Nouveau's common summon-augment set.

## Boundary

Ars Nouveau owns summon gating, Vex ownership/lifecycle and Summoning Sickness. Black Arcana must not create a parallel ownership ledger or bypass provider summon restrictions when interacting with these entities.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.