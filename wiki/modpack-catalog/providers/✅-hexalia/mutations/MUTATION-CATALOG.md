# Hexalia 1.3.6 — Mutation catalog

## Estado

`SOURCE-PINNED 1.3.6 / MUTATION RECIPES 21/21 / MORPHORA EXECUTION PATH AUDITED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Source authority:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

Hexalia has a real provider recipe type `hexalia:mutation`. This is the transformation authority consumed by Morphora/Mutavis and must not be represented as a generic Black Arcana transmutation registry.

## Execution model

The exact Morphora 1.3.6 path:

- uses a hard-coded horizontal mutation radius `3` around Morphora;
- scans the same Y level only;
- ignores Morphora's own position;
- skips air and blocks whose default item is empty;
- queries the provider's `hexalia:mutation` recipe type using the target block's default item;
- destroys a matched target block with drops disabled;
- applies the recipe's `MutationOutput`;
- consumes one Mutavis for the overall activation only if at least one target converted, unless creative.

This means one activation can convert multiple matching blocks while consuming a single Mutavis.

## Recipe inventory — 21/21

### Vanilla/material transmutations — 11

| Recipe ID | Input | Output |
|---|---|---|
| `hexalia:andesite_from_mutation` | `minecraft:granite` | `minecraft:andesite` |
| `hexalia:blackstone_from_mutation` | `minecraft:netherrack` | `minecraft:blackstone` |
| `hexalia:blue_ice_from_mutation` | `minecraft:ice` | `minecraft:blue_ice` |
| `hexalia:diorite_from_mutation` | `minecraft:andesite` | `minecraft:diorite` |
| `hexalia:granite_from_mutation` | `minecraft:diorite` | `minecraft:granite` |
| `hexalia:mud_from_mutation` | `minecraft:clay` | `minecraft:mud` |
| `hexalia:packed_ice_from_mutation` | `minecraft:snow_block` | `minecraft:packed_ice` |
| `hexalia:podzol_from_mutation` | `minecraft:rooted_dirt` | `minecraft:podzol` |
| `hexalia:red_sand_from_mutation` | `minecraft:sand` | `minecraft:red_sand` |
| `hexalia:rooted_dirt_from_mutation` | `minecraft:dirt` | `minecraft:rooted_dirt` |
| `hexalia:tuff_from_mutation` | `minecraft:dripstone_block` | `minecraft:tuff` |

### Hexalia-content mutations — 10

| Recipe ID | Input | Output |
|---|---|---|
| `hexalia:celestial_bloom_from_mutation` | Hexalia `TULIPS` item tag | `hexalia:celestial_bloom` |
| `hexalia:dreamshroom_from_mutation` | `minecraft:brown_mushroom` | `hexalia:dreamshroom` |
| `hexalia:ghost_fern_from_mutation` | `minecraft:fern` | `hexalia:ghost_fern` |
| `hexalia:lotus_flower_from_mutation` | `minecraft:lily_pad` | `hexalia:lotus_flower` |
| `hexalia:siren_kelp_from_mutation` | `minecraft:kelp` | `hexalia:siren_kelp` |
| `hexalia:spirit_bloom_from_mutation` | `minecraft:blue_orchid` | `hexalia:spirit_bloom` |
| `hexalia:witchweed_from_mutation` | `minecraft:azure_bluet` | `hexalia:witchweed` |
| `hexalia:saltsprout_from_mutation` | `minecraft:cactus` | `hexalia:saltsprout` |
| `hexalia:cottonwood_sapling_from_mutation` | `minecraft:oak_sapling` | `hexalia:cottonwood_sapling` |
| `hexalia:willow_sapling_from_mutation` | `minecraft:birch_sapling` | `hexalia:willow_sapling` |

## Radius/config discrepancy

`HexaliaCommonConfig.Values` exposes `morphoraRadius`, with:

- default: `6`;
- sanitized range: `1..32`.

However the exact `MorphoraBlock` activation path uses:

`private static final int MUTATION_RADIUS = 3`

and does not consult `HexaliaConfig.morphoraRadius()` in the audited path.

Therefore the catalog deliberately records:

`SOURCE EXECUTION RADIUS 3 / CONFIG DEFAULT 6 APPEARS DISCONNECTED FROM THIS PATH / INSTALLED RUNTIME QA REQUIRED`.

Do not silently substitute the configured value for the executed source constant.

## World-effect authority

Mutation destroys/replaces world blocks under Hexalia authority. Black Arcana must not:

- re-run the replacement through a second transmutation pipeline;
- generate duplicate drops;
- charge a second resource;
- award repeated mastery for every scan tick;
- infer a Black Arcana cast from every mutated block.

For a future **Black Arcana-owned** mutation, `WorldEffectPolicy` remains mandatory. That policy does not retroactively become authority over Hexalia's native mutation settlement.

## Deduplication

Hexalia already occupies bounded area material/block mutation through a prepared provider item/plant loop. Any proposed Black Arcana transmutation mechanic must demonstrate a real semantic delta — for example typed binding, transactional external-resource routing, spell-domain law, or another independently justified contract — rather than merely adding a second block A→B recipe system.
