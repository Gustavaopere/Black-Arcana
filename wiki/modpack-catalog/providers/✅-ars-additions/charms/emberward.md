# Emberward — Fire Resistance Charm

Status: `SOURCE-PINNED 21.3.0 / RUNTIME EVENT-ORDER QA PENDING`

- Registry item: `ars_additions:fire_resistance_charm`
- Default charges: 1000
- Recharge: 5 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:magma_cream`, `minecraft:lava_bucket`, `minecraft:flint_and_steel`

## Behavior

On `LivingDamageEvent.Pre`, when the damage source is in `DamageTypeTags.IS_FIRE`, the provider sets new damage to zero. Charge consumption is throttled by a provider cooldown to at most once per 20 ticks for this charm/entity key; when the cooldown permits, it consumes `(int) originalDamage` charges.

Because the cast to `int` can truncate fractional damage, the catalog does not equate prevented damage exactly to charges consumed in every case.

## Boundary

Fire-damage prevention and charge settlement are provider-owned. Black Arcana must not zero the same damage again or settle a second defensive proc from the prevented event.
