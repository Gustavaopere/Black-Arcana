# Summon Wilden

Status: `SOURCE-PINNED 5.13.1 / COMBAT-SUMMON RITUAL`

- Registry id: `ars_nouveau:ritual_wilden_summon`
- Class: `RitualWildenSummoning`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native modes

### Standard mode

Without the full boss modifier set, every server interval where `gameTime % 60 == 0` the ritual chooses one of three Wilden types at random and summons it near the brazier:

- Wilden Stalker;
- Wilden Guardian;
- Wilden Hunter.

Ritual progress increments every 20 ticks and the ritual finishes when its 20-tick progress threshold is observed during the 60-tick work cycle; that threshold is not a count of summoned mobs.

### Chimera mode

Boss mode is active only when the ritual consumed all three provider Wilden drops:

- Wilden Horn;
- Wilden Wing;
- Wilden Spike.

Once the boss progress threshold is reached on the ritual's 60-tick work interval, it summons a `WildenChimera` above the brazier.

The source then scans the bounded block volume around the ritual. For each candidate it requires NeoForge `canEntityGrief`, non-negative destroy speed and provider harvest-level eligibility before invoking Ars' safe destroy helper through its fake player.

## Authority / Black Arcana boundary

Wilden entity creation, boss admission, drop modifiers and terrain destruction remain Ars Nouveau authority. Black Arcana must not summon duplicate entities, duplicate progression settlement or replay the Chimera's preparation destruction.

This provider world destruction is **not** permission for Black Arcana to bypass `WorldEffectPolicy`; independent Black Arcana destructive mechanics remain governed by D007.

## QA

Exact source logic is pinned to 5.13.1. Effective mob-griefing/protection integration and full-pack boss behavior remain runtime QA.

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`RitualWildenSummoning.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualWildenSummoning.java) no Ars 5.13.1.
- **Duas cadências:** `incrementProgress` quando `gameTime%20==0`; spawn é processado quando `gameTime%60==0` no `ServerLevel`. Modo normal sorteia `WildenStalker`, `WildenGuardian` ou `WildenHunter` e sempre faz spawn nesse intervalo até `progress>=15` após a criação.
- **Boss:** apenas quando consumiu **todos** `WILDEN_HORN`, `WILDEN_WING`, `WILDEN_SPIKE`, `isBossSpawn()` vale true; no work tick com progress>=8 instancia `WildenChimera` e percorre grade de blocos em torno do brazier (`x,z=-5..5`, `y=+1..+5`). Para cada bloco verifica `EventHooks.canEntityGrief(serverLevel,chimera)`, destroy speed>=0, harvest level 4 e chama `destroyBlockSafelyWithoutSound(...,fakePlayer)`. Não há `destroyRespectsClaim` explícito nesse trecho; proteção depende do helper/integrations.
- **Perks:** risco de mundo é elevado no boss mode; item de boss não habilita controle de world effects Black Arcana, e spawn/destruição/loot não podem ser reexecutados por observadores RPG. Verificar mobGriefing, claims e limites de processamento no runtime exato.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.

## Certificação técnica estática — Wilden mobs / Chimera e world safety (2026-10-25)

**✅ STATIC_TECHNICAL_CATALOG_ONLY · ⛔ mutating_hook=NOT_VERIFIED · ⚠️ physical_qa=NOT_TESTED.** Registry ars_nouveau:ritual_wilden_summon ↔ classe RitualWildenSummoning comprovados pela auditoria binária de IDs do JAR 5.13.1 SHA-1 02782d071ee5fab3b5c4b8ced67b7e1748277dfd; igualdade de método não provada. Fonte baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157: [RitualWildenSummoning.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualWildenSummoning.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java), [AbstractRitual.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ritual/AbstractRitual.java).

- **Relógios e vida:** WildenChimera.spawnPhaseParticles é VFX no tick da classe. incrementProgress() ocorre em gameTime%20==0 **sem verificação explícita de server-side nesse ramo**, mas o bloco que instancia mobs exige gameTime%60==0 e getWorld() instanceof ServerLevel. Portanto getProgress()>=15 e getProgress()>=8 são **contagens de incrementos de 20 ticks**, não de criaturas geradas; a conclusão é testada no tick de trabalho a cada 60.
- **Modo normal:** quando !isBossSpawn(), rand.nextInt(3) escolhe WildenStalker, WildenGuardian ou WildenHunter; spawn em getPos().above().east(rand.nextInt(3)-rand.nextInt(6)).north(rand.nextInt(3)-rand.nextInt(6)), com deslocamentos por eixo entre -5 e +2, não círculo uniforme garantido. Depois do summon, se getProgress()>=15 chama setFinished(). O método summon chama Mob.level.addFreshEntity(mob) **sem verificar o resultado**. Nenhuma conversão para familiar BA, death perk ou cooldown de spell demonstrada.
- **Gating da Chimera:** isBossSpawn() só quando didConsumeItem(ItemsRegistry.WILDEN_HORN), didConsumeItem(ItemsRegistry.WILDEN_WING) **e** didConsumeItem(ItemsRegistry.WILDEN_SPIKE). canConsumeItem aceita stack na WILDEN_DROP_TAG e **não limita duplicatas pela própria classe**; qualquer subconjunto sem as três partes segue a invocação comum. Com trio completo, no work tick com getProgress()>=8 instancia uma WildenChimera em getPos().above(), percorre candidatos e finaliza.
- **Volume geométrico destrutivo:** BlockPos.betweenClosed(getPos().east(5).north(5).above(),getPos().west(5).south(5).above(5)) cobre **11×11×5 = 605 candidatos** (X/Z ±5, Y +1..+5). Para cada posição, EventHooks.canEntityGrief(serverLevel,chimera) é consultado; o trecho exige destroy speed>=0 e SpellUtil.isCorrectHarvestLevel(4,...). Passados os gates, chama BlockUtil.destroyBlockSafelyWithoutSound(serverLevel,b,true,fakePlayer), que por sua vez publica BlockEvent.BreakEvent e pode falhar. O ritual não verifica o retorno do helper; portanto **605 candidatos não significam 605 blocos destruídos**, nem drop garantido. A cada tick de boss podem existir até 605 chamadas ao gate grief, mas não é benchmark de performance.
- **Claims e segurança:** O ramo não chama diretamente destroyRespectsClaim, embora BlockUtil.destroyBlockSafelyWithoutSound efetue preflight de BlockEvent.BreakEvent com ANFakePlayer. EventHooks.canEntityGrief não é prova de claims gerais; mundo protegido, gamerules, mobs modded e cancels precisam de QA. WorldEffectPolicy permanece para as mutações **próprias** do Black Arcana, sem autorizar/bloquear automaticamente o ritual do Ars.
- **Custo e integração:** RitualWildenSummoning herda AbstractRitual.getSourceCost()=0, mas isso **não equivale a ritual grátis** devido a ingredientes/ativação. Específico do provider, o ritual não expõe DamageType, raio de projétil ou API de scaling confiável para perk. RPG Skill Tree é sibling de progresso/Mastery/gates, não executor de spawn, terreno ou Source do Ars. Sem hook seguro e budget por bloco/mob, perks de multiplicar Chimera, alterar terreno, loot e contagem de mobs ficam fail-closed.

**PENDENTE QA física:** mobs efetivamente admitidos por addFreshEntity, classfile/side de progress, vanilla mobGriefing, WorldGuard/claims e BreakEvent, bloco com tile, chunks, dimension reload, inputs duplicados, loot, performance, mobs/skills de addons. mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED. Stage 06.05 e Stage 09 permanecem inalterados.
