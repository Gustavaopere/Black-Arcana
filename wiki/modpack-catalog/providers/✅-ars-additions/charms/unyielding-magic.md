# Unyielding Magic — Dispel Protection Charm

Status: `SOURCE-PINNED 21.3.0 / ARS EVENT-ORDER QA PENDING`

- Registry item: `ars_additions:dispel_protection_charm`
- Default charges: 3
- Recharge: 1000 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:milk_bucket`, `minecraft:shield`, `minecraft:spider_eye`, `minecraft:wither_rose`

## Behavior

On Ars Nouveau `DispelEvent.Pre`, when the ray trace resolves to a living entity and the dispel shooter is not that target, the provider cancels the dispel and consumes one charge outside creative mode.

## Boundary

Ars Additions owns this veto of the Ars dispel event. Black Arcana must not infer generic dispel immunity outside the event contract or cancel the same provider dispel twice.
