# Ars Nouveau — Burst

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_burst`
- Display name: Burst
- Default tier: 3
- Default mana cost: 500
- Compatible augments: AOE, Sensitive, Dampen
- Default Sensitive limit: 1
- Per-spell occurrence limit: exactly 1
- Default invalid combinations: Linger, Wall
- School: no explicit school override in the inspected class; do not infer one

## Provider-native behavior

Burst resolves the remaining spell across a spherical target set and then cancels the original context. Radius is `int(AOE multiplier) + 3` for entity targeting or `+1` with Sensitive block targeting. Dampen changes the filled sphere into a shell. Each eligible target receives a cloned child context/new resolver. Burst is registered in `EffectReset.RESET_LIMITS`.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:tnt` ×5 + `minecraft:firework_star`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Burst is an Ars spell-composition fan-out runtime. Black Arcana must not route those child executions through a parallel Black Arcana cast pipeline or duplicate resource/effect settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectBurst`).

## Engenharia de perks — evidência de execução individual

- **Classe versionada:** [`EffectBurst.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBurst.java) no Ars Nouveau 5.13.1.
- **Raio efetivo:** `radius=(int)getAoeMultiplier()+(isSensitive()?1:3)`. A geometria de `Dampen` vira casca esférica com condição `distance<=radius+0.5 && distance>=radius-0.5`; sem Dampen usa esfera preenchida até `radius+0.5`. O source não demonstra clamp positivo; bounds e custos de varredura requerem QA.
- **Alvos:** Sensitive percorre `BlockPos.withinManhattan(center,radius,radius,radius)` e filtra pela esfera; sem Sensitive percorre `world.getEntities(null,new AABB(center).inflate(radius,...))`, incluindo `LivingEntity` ou whitelist `BURST_WHITELIST`.
- **Causalidade:** cada alvo recebe `resolver.getNewResolver(spellContext.clone().makeChildContext())`, que resolve as partes seguintes. Depois cancela parent. `PER_SPELL_LIMIT=1`, Sensitive limit 1, invalid combos Linger e Wall. **Perks:** não transformar cada child resolver em cast/custo/Mastery autônomo; limite de alvos exige budget.
- **Status:** ✅ code pin/identidade; ⚠️ downstream, config e Survival pendentes; mutação por RPG perk só pode ocorrer via [eventos reais](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e adapter validado, não por inferência temática.
