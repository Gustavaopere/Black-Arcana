# Featherlight — Fall Prevention Charm

Status: `SOURCE-PINNED 21.3.0 / CHARGE-RATE QA PENDING`

- Registry item: `ars_additions:fall_prevention_charm`
- Default charges: 20
- Recharge: 20 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:feather`, `minecraft:phantom_membrane`

## Behavior

During either inventory tick or Curios tick, when `fallDistance > 3.0`, the provider applies Slow Falling for 100 ticks and returns a one-charge consumption.

Unlike several other charm paths, this call does not use `CharmRegistry.every(...)` in the inspected implementation. Continuous falling can therefore revisit the event on repeated ticks; effective drain rate and duplicate inventory/Curios tick behavior require runtime QA.

## Boundary

Black Arcana must not add a second slow-fall effect/charge model merely because the charm is observed. The provider's actual tick/event ordering remains authority.
