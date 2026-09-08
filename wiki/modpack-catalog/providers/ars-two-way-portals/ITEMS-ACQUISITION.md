# Ars Two-Way Portals — items and acquisition

Status: `2.0.0 ITEM NAMES/FEATURES RELEASE-CONFIRMED / RECIPES FROM 1.3.4 PUBLIC BASELINE`

## Items

The public baseline registers exactly two stack-size-1 items, matching the two named items documented by the 2.0.0 project:

1. `ars_two_way_portals:double_sided_stable_warp_scroll`
2. `ars_two_way_portals:portal_nullify_scroll`

The Double-Sided item extends Ars `StableWarpScroll` in the baseline rather than implementing a parallel teleport primitive.

## Baseline recipes — 3

### Double-Sided Stable Warp Scroll

Type: `ars_nouveau:enchanting_apparatus`

- reagent: `ars_nouveau:stable_warp_scroll`;
- pedestal: `ars_nouveau:stable_warp_scroll`;
- output: `ars_two_way_portals:double_sided_stable_warp_scroll`;
- `keepNbtOfReagent: true`;
- `sourceCost: 0`.

The exact 2.0.0 project description independently says to combine two Stabilized Warp Scrolls in an Enchanting Apparatus, so the acquisition shape is release-corroborated even though exact 2.0.0 JSON was not extracted.

### Portal Nullify Scroll

Baseline apparatus recipe:

- reagent: `ars_nouveau:stable_warp_scroll`;
- pedestal: `minecraft:obsidian`;
- output: `ars_two_way_portals:portal_nullify_scroll`;
- `keepNbtOfReagent: false`;
- `sourceCost: 0`.

The publisher page independently describes the nullify scroll as crafted from obsidian + stabilized warp scroll in the apparatus.

### Reset configured Double-Sided Scroll

Baseline shapeless recipe takes one Double-Sided Stable Warp Scroll and returns the same item. The exact project page says crafting a configured scroll by itself clears saved coordinates.

## Authority

Ars apparatus/crafting and Ars Stable Warp Scroll data remain provider-native. Black Arcana must not add a second unlock/cost transaction around these recipes or rewrite the provider scroll's destination data in a BA-owned persistence ledger.
