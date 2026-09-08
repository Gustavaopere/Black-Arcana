# Snowstride — Powdered Snow Walk Charm

Status: `SOURCE-PINNED 21.3.0 / QUERY-FREQUENCY QA PENDING`

- Registry item: `ars_additions:powdered_snow_walk_charm`
- Default charges: 1000
- Recharge: 5 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:leather_boots`, `minecraft:powder_snow_bucket`

## Behavior

Both powdered-snow walking hooks delegate to `canWalkOnPowderedSnow`. When a valid charm is found, the provider returns true and uses `CharmRegistry.every(...)` to consume at most one charge per 20 ticks for this charm/entity key.

Charge use depends on how often the engine/provider queries this hook, so representative runtime cadence remains QA.

## Boundary

Traversal permission and charge cadence are provider-owned. Black Arcana must not grant an independent snow-walk state based solely on inventory observation.
