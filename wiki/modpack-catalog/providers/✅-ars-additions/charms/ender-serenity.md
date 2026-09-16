# Ender Serenity — Ender Mask Charm

Status: `SOURCE-PINNED 21.3.0 / QUERY-FREQUENCY QA PENDING`

- Registry item: `ars_additions:ender_mask_charm`
- Default charges: 100
- Recharge: 10 Source per missing charge
- Apparatus reagent: `minecraft:glass_bottle`
- Pedestals: `minecraft:pumpkin`, `minecraft:chorus_fruit`

## Behavior

The Curios/NeoForge Ender-mask hooks delegate to provider logic. The charm returns an enabled mask state when the wearer's view vector is sufficiently aligned with the Enderman and line of sight exists. Charge consumption is throttled to one charge per 20 ticks by `CharmRegistry.every(...)` when the predicate is evaluated true.

The exact source uses `Items.PUMPKIN` as its Apparatus pedestal item; this page deliberately does not substitute Carved Pumpkin by analogy.

## Boundary

Enderman-neutrality masking and its charge cadence are provider-owned. Query frequency is engine/provider driven and remains runtime QA.
