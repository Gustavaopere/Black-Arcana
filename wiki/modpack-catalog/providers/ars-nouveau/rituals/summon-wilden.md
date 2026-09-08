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