# Hexalia 1.3.7 — Nature's Ritual catalog

## Estado

`SOURCE-PINNED 1.3.7 / PLAYER-FACING RECIPES 23/23 / CURRENT LIFECYCLE AUDITED / SOUL-SUMMONING PATH AUDITED / PHYSICAL JAR HASH KNOWN / SOURCE-BUILD BYTE EQUALITY UNPROVEN`

Physical artifact: `hexalia-neoforge-1.3.7.jar` / SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`.

Exact current source pin: `AstralyaStudios/Hexalia@1230d32056f155e58ee1139c105a93eeea42fa05`.

The generated 1.3.7 data set contains exactly **23** `hexalia:natures_ritual` recipe JSONs. The previous 1.3.6 catalog contained 19 player-facing recipes plus a debug recipe; current 1.3.7 data contains the 19 retained player recipes plus four new player-facing identities and no `debug_natures_ritual` recipe.

## Semantic delta from 1.3.6

Added in the current 1.3.7 source surface:

1. `hexalia:cinderhew_from_ritual_table`;
2. `hexalia:heartseed_from_ritual_table`;
3. `hexalia:summon_cacofey`;
4. `hexalia:summon_silk_moth`.

No previously counted Nature's Ritual identity was removed.

## Current provider-native ritual contract

Nature's Ritual is a discrete Hexalia provider action. It is not an Iron's spell or Black Arcana cast.

### Admission

A player starts the ritual by interacting with a Ritual Table while holding `hexalia:hex_focus` in either hand. The table must contain the recipe center ingredient.

Current 1.3.7 source scans **all non-empty Ritual Braziers in a horizontal radius of 8 blocks** around the table. Available braziers are sorted deterministically by distance to the table and then block position. Recipe offerings are matched against this pool without a fixed cardinal layout.

Every selected brazier must have `RitualBrazierBlock.SALTED=true` at admission. If any selected brazier is unsalted, the ritual does not start.

### Crop requirement

The provider reads `naturesRitualCropRequirement`; NeoForge config constrains it to `0..32`. When nonzero, fully grown vanilla/Hexalia-tagged crops are collected within horizontal radius 8. On ordinary successful completion the selected crops are reset to age 0 rather than removed.

### Offering settlement and duration

Duration is:

`40 ticks × number of selected offering braziers`.

Offerings are consumed sequentially. When an offering is consumed, that brazier's salted state is reset to false. If the center input disappears or a still-required selected brazier/item disappears, the ritual cancels.

Current recipe durations therefore range from 80 ticks for 2-offering node rituals up to 320 ticks for the 8-offering Cacofey summoning ritual.

### Soul-gated summoning

`summon_cacofey` and `summon_silk_moth` set `requires_soul=true` and use entity results rather than item outputs.

After all offerings are processed, these rituals enter `AWAITING_SOUL` instead of settling immediately. `NaturesRitualSoulEvents` accepts a non-player living-entity death only when:

- the level is server-side;
- the killer/source entity is a player;
- the killing weapon is `hexalia:athame`;
- an awaiting Ritual Table is within radius 8.

The nearest deterministic candidate table captures the soul. A **50-tick** manifestation phase follows. On success the provider creates and adds the configured entity result to the world; for both current summon recipes the count is 1.

This entire soul-capture/manifestation sequence remains Hexalia-owned and must not be reimplemented or double-settled by Black Arcana.

## Player-facing recipe inventory — 23/23

| Recipe ID | Center input | Offerings | Result | Offerings / base processing | Soul? |
|---|---|---|---|---:|---|
| `hexalia:fire_node_from_ritual_table` | `minecraft:amethyst_shard` | coal; sunflower | `hexalia:fire_node` | 2 / 80 ticks | no |
| `hexalia:air_node_from_ritual_table` | `minecraft:amethyst_shard` | feather; dandelion | `hexalia:air_node` | 2 / 80 ticks | no |
| `hexalia:water_node_from_ritual_table` | `minecraft:amethyst_shard` | lily pad; ink sac | `hexalia:water_node` | 2 / 80 ticks | no |
| `hexalia:earth_node_from_ritual_table` | `minecraft:amethyst_shard` | clay ball; brown mushroom | `hexalia:earth_node` | 2 / 80 ticks | no |
| `hexalia:astrylis_from_ritual_table` | `minecraft:lily_of_the_valley` | celestial crystal; earth node; bone meal; glowstone dust | `hexalia:astrylis` | 4 / 160 ticks | no |
| `hexalia:kelpweave_blade_from_ritual_table` | `hexalia:ancient_seed` | water node; wooden sword; kelp; siren paste | `hexalia:kelpweave_blade` | 4 / 160 ticks | no |
| `hexalia:rootshaper_from_ritual_table` | `hexalia:ancient_seed` | earth node; wooden pickaxe; wooden shovel; dream paste | `hexalia:rootshaper` | 4 / 160 ticks | no |
| `hexalia:sage_pendant_from_ritual_table` | `hexalia:celestial_crystal` | gold nugget; book; experience bottle; spirit powder | `hexalia:sage_pendant` | 4 / 160 ticks | no |
| `hexalia:bloomwrap_hat_from_ritual_table` | leather helmet | pink tulip; silk fiber; mandrake; rooted dirt | `hexalia:bloomwrap_hat` | 4 / 160 ticks | no |
| `hexalia:bloomwrap_robes_from_ritual_table` | leather chestplate | moss block; earth node; silk fiber; iron nugget | `hexalia:bloomwrap_robes` | 4 / 160 ticks | no |
| `hexalia:bloomwrap_leggings_from_ritual_table` | leather leggings | peony; spirit bloom; silk fiber; honeycomb | `hexalia:bloomwrap_leggings` | 4 / 160 ticks | no |
| `hexalia:bloomwrap_boots_from_ritual_table` | leather boots | dandelion; air node; silk fiber; sugar | `hexalia:bloomwrap_boots` | 4 / 160 ticks | no |
| `hexalia:grimshade_from_ritual_table` | azure bluet | ghost powder; wither rose; bone; black dye | `hexalia:grimshade` | 4 / 160 ticks | no |
| `hexalia:rabbage_seeds_from_ritual_table` | beetroot seeds | dream paste; iron nugget; sweet berries; poppy | `hexalia:rabbage_seeds` | 4 / 160 ticks | no |
| `hexalia:nautilite_from_ritual_table` | kelp | siren paste; water node; nautilus shell; prismarine crystals | `hexalia:nautilite` | 4 / 160 ticks | no |
| `hexalia:windsong_from_ritual_table` | oxeye daisy | air node; ghost powder; feather; phantom membrane | `hexalia:windsong` | 4 / 160 ticks | no |
| `hexalia:lourdes_from_ritual_table` | blue orchid | air node; honeycomb; glistering melon slice; dream paste | `hexalia:lourdes` | 4 / 160 ticks | no |
| `hexalia:aegiflora_from_ritual_table` | dandelion | gunpowder; ghost powder; lotus blossom; moss block | `hexalia:aegiflora` | 4 / 160 ticks | no |
| `hexalia:morphora_from_ritual_table` | poppy | dream paste; spirit powder; earth node; tree resin | `hexalia:morphora` | 4 / 160 ticks | no |
| `hexalia:cinderhew_from_ritual_table` | `hexalia:ancient_seed` | wooden axe; fire node; blaze powder; tree resin; charcoal; flint | `hexalia:cinderhew` | 6 / 240 ticks | no |
| `hexalia:heartseed_from_ritual_table` | golden apple | fragrant nectar; amethyst shard; spirit powder; lotus flower; honeycomb; poppy | `hexalia:heartseed` | 6 / 240 ticks | no |
| `hexalia:summon_silk_moth` | `hexalia:fragrant_nectar` | string; white wool; spirit powder; celestial bloom; glowstone dust; witchweed | entity `hexalia:silk_moth` ×1 | 6 / 240 ticks + 50-tick manifestation after soul | yes |
| `hexalia:summon_cacofey` | `hexalia:galeberries_cookie` | spirit powder; tree resin; jungle sapling; cocoa beans; melon slice; wheat seeds; moss block; brown mushroom | entity `hexalia:cacofey` ×1 | 8 / 320 ticks + 50-tick manifestation after soul | yes |

## Count disposition

All 23 recipes are provider-owned player-facing ritual identities. The two entity manifestations remain one identity each; soul capture, particles, offering transfers, crops reset, summoned entity behavior and other downstream consequences are not separately counted.

Together with Hexalia's unchanged six Celestial Infusions, the current semantic Hexalia surface is **29** discrete magic actions.

## Authority boundary

Hexalia owns recipe admission, offering consumption, salt settlement, crop costs, ritual state/persistence, soul capture and result settlement. A future Black Arcana integration may observe a deduplicated provider completion only through a verified boundary; it must not run a parallel ritual transaction.
