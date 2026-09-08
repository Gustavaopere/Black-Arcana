# Darkvision — Night Vision Charm

Status: `SOURCE-PINNED 21.3.0 / TICK-ORDER QA PENDING`

- Registry item: `ars_additions:night_vision_charm`
- Default charges: 20
- Recharge: 10 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:lantern`, `minecraft:torch`

## Behavior

During inventory/Curios tick, the provider calculates raw brightness. When brightness is below 5 and Night Vision is absent or has at most 200 ticks remaining, it applies Night Vision for 600 ticks and consumes one charge outside creative mode.

This creates provider-native refresh behavior rather than a permanent attribute.

## Boundary

Black Arcana vision/divination systems must not duplicate this vanilla Night Vision refresh or infer magical-detection authority from it.
