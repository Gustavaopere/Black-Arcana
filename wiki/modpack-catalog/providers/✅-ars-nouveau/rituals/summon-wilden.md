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

Ritual progress increments every 20 ticks and the ritual finishes once the provider's progress condition is met after its periodic summon work.

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
