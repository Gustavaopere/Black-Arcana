# Gilded Friendship — Golden Charm

Status: `SOURCE-PINNED 21.3.0 / NO-CHARGE-CONSUMPTION PATH CONFIRMED / RUNTIME QA PENDING`

- Registry item: `ars_additions:golden_charm`
- Default charges: 1000
- Recharge: 5 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:golden_helmet`, `minecraft:golden_chestplate`, `minecraft:golden_leggings`, `minecraft:golden_boots`, `minecraft:gilded_blackstone`

## Behavior

The NeoForge/Curios Piglin-neutrality hooks simply return whether a valid Golden charm with charges is found. The inspected `makesPiglinsNeutral` path does **not** consume charges.

Accordingly, this source checkpoint does not justify describing neutrality as costing one charge per query/tick. The item still has a charge capacity and recharge recipe because all charm types share the common framework.

## Boundary

Piglin-neutrality state remains provider-owned. Do not create a parallel faction-neutrality modifier from item detection.
