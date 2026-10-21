# Ars Nouveau — Summon Steed

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

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

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:leather` ×4.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this temporary mount summon, its ownership and Summoning Sickness. Black Arcana should not duplicate a generic conjured steed or replace the provider lifetime/ownership ledger.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSummonSteed`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectSummonSteed.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonSteed.java) do Ars 5.13.1.
- **Quantidade:** `for (i=0;i<1+Math.round(getAoeMultiplier());i++)` cria `SummonHorse` — contagem derivada de AOE arredondada, não raio geográfico. `ticks=(int)(20*(GENERIC_INT.get()+EXTEND_TIME.get()*durationMultiplier))`, defaults 300s+120s; se ticks<=0 é reajustado a **20 ticks**, ao contrário de summons que retornam sem spawn.
- **Owner/equipamento:** `tameWithName((Player)shooter)`, adiciona `Items.SADDLE`, define UUID owner, `setDropChance(CHEST,0.0F)` e passa por `summonLivingEntity`. Após a invocação aplica `applySummoningSickness(shooter,30*20)` = argumento 600 ticks, **independente do lifetime**. O cast explícito de `shooter` a `Player` pede auditoria do gate `canSummon` para outros casters.
- **Perks:** não tomar controle de mounts ou copy do saddle; se AOE modificado externamente, assegurar caps de entidades, colisão e decompensação de Summoning Sickness com integração real.
- **Estado:** ✅ classe/método do source pin; ⚠️ scripts de addons, config física e QA Survival pendentes; ⛔ bridge de perks RPG e mutação de `SpellStats` sem validação de causalidade e limites.
