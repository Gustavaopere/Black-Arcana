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

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `minecraft:totem_of_undying`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns summon gating, Vex ownership/lifecycle and Summoning Sickness. Black Arcana must not create a parallel ownership ledger or bypass provider summon restrictions when interacting with these entities.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectSummonVex.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonVex.java) do Ars 5.13.1.
- **Admissão e número:** exige `canSummon(shooter)`; `ticks=(int)(20*(GENERIC_INT.get()+EXTEND_TIME.get()*durationMultiplier))`, defaults 15s e 10s; se `ticks<=0`, retorna. Laço **fixo de três** invoca `EntityAllyVex` em posições aleatórias perto do hit.
- **Executor:** cada Vex passa por `finalizeSpawn(...MOB_SUMMONED)`, `setOwner(shooter)`, `setBoundOrigin(blockPos)`, `setLimitedLife(ticks)` e `summonLivingEntity`; caster recebe `SUMMONING_SICKNESS_EFFECT` com mesmos ticks. O código não usa AOE/Split para aumentar contagem neste effect.
- **Perks:** count fixo e lifetime não devem ser extrapolados da quantidade de projéteis/augments de outras magias Ars; agentes autônomos podem causar dano posterior sem recast da origem.
- **Estado:** ✅ classe/método do source pin; ⚠️ scripts de addons, config física e QA Survival pendentes; ⛔ bridge de perks RPG e mutação de `SpellStats` sem validação de causalidade e limites.
