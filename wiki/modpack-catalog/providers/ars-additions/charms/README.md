# Ars Additions 21.3.0 — Charms

Status: `12/12 SOURCE-PINNED / ACQUISITION+RECHARGE AUDITED / RUNTIME STACKING QA PENDING`

Exact source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

`CharmRegistry.CharmType` defines exactly 12 charms. Each item is created with its full configured charge count in `CHARM_DATA`.

## Lookup / activation contract

For a `Player`, provider `PlayerInvUtil` searches in this order:

1. main hand;
2. off-hand;
3. Curios inventory;
4. the player's normal inventory.

Therefore a charm does not need to be treated as a Curios-only equipped effect. Bridges must not apply a second effect merely because the same provider item is found in another inventory surface.

## Acquisition

Every charm is generated as an Ars Enchanting Apparatus recipe with `minecraft:glass_bottle` as reagent and the charm-specific pedestal ingredients listed on its page. The datagen does not explicitly set a Source cost for these charm-crafting recipes; this catalog does not invent one.

## Recharging

`CharmChargingProvider` generates one Imbuement Chamber recharge recipe per charm. It accepts that same partially discharged charm, rejects a charm with zero damage/full charges, and restores all charges.

Recharge Source cost is:

`missing charges × costPerCharge`

The table below lists source-default charge capacity and recharge cost from the exact enum.

| Registry item | Display name | Charges | Source / missing charge | Full recharge from empty |
|---|---|---:|---:|---:|
| `ars_additions:fire_resistance_charm` | Emberward | 1000 | 5 | 5000 |
| `ars_additions:undying_charm` | Second Wind | 1 | 2000 | 2000 |
| `ars_additions:dispel_protection_charm` | Unyielding Magic | 3 | 1000 | 3000 |
| `ars_additions:fall_prevention_charm` | Featherlight | 20 | 20 | 400 |
| `ars_additions:water_breathing_charm` | Ocean's Breath | 1000 | 5 | 5000 |
| `ars_additions:ender_mask_charm` | Ender Serenity | 100 | 10 | 1000 |
| `ars_additions:void_protection_charm` | Void's Salvation | 1 | 2000 | 2000 |
| `ars_additions:sonic_boom_protection_charm` | Resonant Shield | 3 | 1000 | 3000 |
| `ars_additions:wither_protection_charm` | Decay's End | 10 | 100 | 1000 |
| `ars_additions:golden_charm` | Gilded Friendship | 1000 | 5 | 5000 |
| `ars_additions:night_vision_charm` | Darkvision | 20 | 10 | 200 |
| `ars_additions:powdered_snow_walk_charm` | Snowstride | 1000 | 5 | 5000 |

## Authority / deduplication

Charge state, event interception, effect cancellation, teleport fallback and recharge Source cost are Ars Additions/Ars-owned. Black Arcana must not maintain a mirror charge ledger, replay prevented damage/effects or charge a second resource for provider charm activation.
