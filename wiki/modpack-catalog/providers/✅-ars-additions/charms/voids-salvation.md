# Void's Salvation — Void Protection Charm

Status: `SOURCE-PINNED 21.3.0 / TELEPORT SAFETY QA PENDING`

- Registry item: `ars_additions:void_protection_charm`
- Default charges: 1
- Recharge: 2000 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: Ars Nouveau `stable_warp_scroll`, `minecraft:end_stone_bricks`

## Provider-native checkpointing

While ticking, when the entity is on ground and the block below is a redstone conductor, the charm stores the current `GlobalPos` in vanilla `DataComponents.LODESTONE_TRACKER`. This checkpoint update consumes no charge.

## Void rescue

On `LivingDamageEvent.Pre` for `DamageTypes.FELL_OUT_OF_WORLD`, the provider:

- sets new damage to zero;
- reads the stored lodestone tracker;
- on server side, teleports to the stored dimension/position when a target exists;
- resets fall distance;
- consumes one charge outside creative mode.

## Boundary

The stored provider checkpoint is not a Black Arcana teleport authorization. Black Arcana must not mirror it or bypass its own loaded-target, dimension, protection and world-safety rules. Missing/unavailable target-dimension behavior requires runtime QA.
