# Ars Nouveau — Summon Decoy

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

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

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `minecraft:armor_stand` ×4.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this aggro-decoy primitive. Black Arcana illusion/control content should not clone the same temporary taunt dummy without a materially different contract.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSummonDecoy`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectSummonDecoy.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonDecoy.java) do Ars 5.13.1.
- **Spawn e duração:** somente com `canSummon(shooter)`, cria `EntityDummy` em posição do hit +1Y; `ticksLeft=(int)(20*(GENERIC_INT.get()+durationMultiplier*EXTEND_TIME.get()))`, defaults 30s e 15s. `summonLivingEntity` efetiva o lifecycle.
- **Atração:** após invocar, percorre `world.getEntitiesOfClass(Mob.class,dummy.boundingBox.inflate(20,10,20))` e faz `mob.setTarget(dummy)` — é uma caixa de busca 40×20×40 de expansão ao redor do próprio dummy, **não** comprovadamente um raio de 20 nem seleção exclusiva de hostis.
- **Summoning Sickness:** chama `applySummoningSickness(shooter,1)` (parâmetro 1 passado ao helper, não 1 segundo garantido). **Perks:** controle de aggro, lifecycle, HP do dummy e target retargeting exigem classe `EntityDummy`/helpers e auditoria PvP/addons; não repetir taunt por RPG.
- **Estado:** ✅ classe/método do source pin; ⚠️ scripts de addons, config física e QA Survival pendentes; ⛔ bridge de perks RPG e mutação de `SpellStats` sem validação de causalidade e limites.
