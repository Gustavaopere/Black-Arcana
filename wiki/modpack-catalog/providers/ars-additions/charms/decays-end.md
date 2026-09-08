# Decay's End — Wither Protection Charm

Status: `SOURCE-PINNED 21.3.0 / EFFECT-ORDER QA PENDING`

- Registry item: `ars_additions:wither_protection_charm`
- Default charges: 10
- Recharge: 100 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:wither_rose`, `minecraft:wither_skeleton_skull`, `minecraft:milk_bucket`

## Behavior

On `MobEffectEvent.Applicable`, when the candidate effect is vanilla Wither, the provider sets the result to `DO_NOT_APPLY`. Charge consumption is throttled by `CharmRegistry.every(...)` to one charge per 20 ticks for this charm/entity key.

Repeated Wither-application attempts inside the cooldown window can still be vetoed while the consumer returns zero additional charge for that interval.

## Boundary

Ars Additions owns this effect-admission veto. Black Arcana must not interpret a rejected Wither application as its own cleanse/resistance proc.
