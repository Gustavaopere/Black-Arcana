# Resonant Shield — Sonic Boom Protection Charm

Status: `SOURCE-PINNED 21.3.0 / DAMAGE-ORDER QA PENDING`

- Registry item: `ars_additions:sonic_boom_protection_charm`
- Default charges: 3
- Recharge: 1000 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:sculk`, `minecraft:shield`, `minecraft:white_wool`

## Behavior

On `LivingDamageEvent.Pre`, when the source is `DamageTypes.SONIC_BOOM`, the provider sets new damage to zero and consumes one charm charge outside creative mode.

## Boundary

This is a provider-owned damage veto. Black Arcana defensive mechanics must not settle a second prevention/proc chain from the same zeroed provider damage.
