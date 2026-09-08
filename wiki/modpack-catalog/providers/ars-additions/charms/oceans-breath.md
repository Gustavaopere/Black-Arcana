# Ocean's Breath — Water Breathing Charm

Status: `SOURCE-PINNED 21.3.0 / DESCRIPTION-PATH NUANCE / RUNTIME QA PENDING`

- Registry item: `ars_additions:water_breathing_charm`
- Default charges: 1000
- Recharge: 5 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:pufferfish`, `minecraft:ink_sac`, `minecraft:kelp`

## Behavior

The executable path is damage interception rather than proactive air restoration. On `LivingDamageEvent.Pre`, when the source is vanilla drowning damage, the provider sets new damage to zero and consumes `(int) originalDamage` charges outside creative mode.

The provider display description says it enables underwater breathing; Phase 2Q records the executable contract precisely as drowning-damage prevention and does not invent an air-supply mutation not present in this class.

## Boundary

Do not duplicate drowning prevention or convert this provider protection into a Black Arcana aquatic-resistance state.
