# Hexalia 1.3.6 — Nature's Ritual catalog

## Estado

`SOURCE-PINNED 1.3.6 / PLAYER-FACING RECIPES 19/19 / DEBUG RECIPE EXCLUDED / RITUAL LIFECYCLE AUDITED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Source pin:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

The exact source/data generation path exposes **20** Nature's Ritual recipe definitions, of which one is explicitly `debug_natures_ritual`. This catalog therefore records **19 player-facing recipes**.

Because the installed physical file is named 1.3.6 but its runtime metadata reports 1.3.5, this is a complete inventory of the pinned public 1.3.6 source surface, not a claim of exact installed-JAR runtime equivalence.

## Provider-native ritual contract

Nature's Ritual is not a spellbook cast.

### Start interaction

A player starts a valid ritual with a `hexalia:hex_focus` in main hand or offhand while interacting with the Ritual Table.

The table holds exactly one central input item. Up to four Ritual Braziers are discovered at:

- north 2 blocks;
- south 2 blocks;
- east 2 blocks;
- west 2 blocks.

Recipe brazier ingredients are matched without assuming orientation/order.

### Salt requirement

Every brazier actually used by the matched recipe must have `RitualBrazierBlock.SALTED=true` when the ritual starts. If any required used brazier is unsalted, the ritual does not start.

During processing, each used brazier ingredient is removed and that brazier's salted state is reset to false.

### Crop requirement

The 1.3.6 source default is:

- `naturesRitualCropRequirement = 8`;
- sanitized configuration range: `0..32`.

When the requirement is nonzero, the provider searches an 8-block horizontal radius around the table for fully grown blocks in vanilla/Hexalia crop tags. On successful completion, the selected grown crops are reset to age `0`; they are not deleted by this path.

### Duration

Transformation duration is:

`40 ticks × number of used braziers`.

Therefore the current recipe set has:

- 2-brazier node recipes: `80 ticks = 4 s`;
- 4-brazier recipes: `160 ticks = 8 s`.

If the table input disappears or a still-required brazier item disappears during transformation, the ritual cancels.

## Player-facing recipe inventory — 19/19

The **central input** is placed on the Ritual Table. The remaining listed ingredients are placed in salted Ritual Braziers.

| Recipe ID | Central input | Brazier ingredients | Output | Braziers / duration |
|---|---|---|---|---:|
| `hexalia:fire_node_from_ritual_table` | `minecraft:amethyst_shard` | `minecraft:coal`, `minecraft:sunflower` | `hexalia:fire_node` | 2 / 80 ticks |
| `hexalia:air_node_from_ritual_table` | `minecraft:amethyst_shard` | `minecraft:feather`, `minecraft:dandelion` | `hexalia:air_node` | 2 / 80 ticks |
| `hexalia:water_node_from_ritual_table` | `minecraft:amethyst_shard` | `minecraft:lily_pad`, `minecraft:ink_sac` | `hexalia:water_node` | 2 / 80 ticks |
| `hexalia:earth_node_from_ritual_table` | `minecraft:amethyst_shard` | `minecraft:clay_ball`, `minecraft:brown_mushroom` | `hexalia:earth_node` | 2 / 80 ticks |
| `hexalia:astrylis_from_ritual_table` | `minecraft:lily_of_the_valley` | `hexalia:celestial_crystal`, `hexalia:earth_node`, `minecraft:bone_meal`, `minecraft:glowstone_dust` | `hexalia:astrylis` | 4 / 160 ticks |
| `hexalia:kelpweave_blade_from_ritual_table` | `hexalia:ancient_seed` | `hexalia:water_node`, `minecraft:wooden_sword`, `minecraft:kelp`, `hexalia:siren_paste` | `hexalia:kelpweave_blade` | 4 / 160 ticks |
| `hexalia:rootshaper_from_ritual_table` | `hexalia:ancient_seed` | `hexalia:earth_node`, `minecraft:wooden_pickaxe`, `minecraft:wooden_shovel`, `hexalia:dream_paste` | `hexalia:rootshaper` | 4 / 160 ticks |
| `hexalia:sage_pendant_from_ritual_table` | `hexalia:celestial_crystal` | `minecraft:gold_nugget`, `minecraft:book`, `minecraft:experience_bottle`, `hexalia:spirit_powder` | `hexalia:sage_pendant` | 4 / 160 ticks |
| `hexalia:bloomwrap_hat_from_ritual_table` | `minecraft:leather_helmet` | `minecraft:pink_tulip`, `hexalia:silk_fiber`, `hexalia:mandrake`, `minecraft:rooted_dirt` | `hexalia:bloomwrap_hat` | 4 / 160 ticks |
| `hexalia:bloomwrap_robes_from_ritual_table` | `minecraft:leather_chestplate` | `minecraft:moss_block`, `hexalia:earth_node`, `hexalia:silk_fiber`, `minecraft:iron_nugget` | `hexalia:bloomwrap_robes` | 4 / 160 ticks |
| `hexalia:bloomwrap_leggings_from_ritual_table` | `minecraft:leather_leggings` | `minecraft:peony`, `hexalia:spirit_bloom`, `hexalia:silk_fiber`, `minecraft:honeycomb` | `hexalia:bloomwrap_leggings` | 4 / 160 ticks |
| `hexalia:bloomwrap_boots_from_ritual_table` | `minecraft:leather_boots` | `minecraft:dandelion`, `hexalia:air_node`, `hexalia:silk_fiber`, `minecraft:sugar` | `hexalia:bloomwrap_boots` | 4 / 160 ticks |
| `hexalia:grimshade_from_ritual_table` | `minecraft:azure_bluet` | `hexalia:ghost_powder`, `minecraft:wither_rose`, `minecraft:bone`, `minecraft:black_dye` | `hexalia:grimshade` | 4 / 160 ticks |
| `hexalia:rabbage_seeds_from_ritual_table` | `minecraft:beetroot_seeds` | `hexalia:dream_paste`, `minecraft:iron_nugget`, `minecraft:sweet_berries`, `minecraft:poppy` | `hexalia:rabbage_seeds` | 4 / 160 ticks |
| `hexalia:nautilite_from_ritual_table` | `minecraft:kelp` | `hexalia:siren_paste`, `hexalia:water_node`, `minecraft:nautilus_shell`, `minecraft:prismarine_crystals` | `hexalia:nautilite` | 4 / 160 ticks |
| `hexalia:windsong_from_ritual_table` | `minecraft:oxeye_daisy` | `hexalia:air_node`, `hexalia:ghost_powder`, `minecraft:feather`, `minecraft:phantom_membrane` | `hexalia:windsong` | 4 / 160 ticks |
| `hexalia:lourdes_from_ritual_table` | `minecraft:blue_orchid` | `hexalia:air_node`, `minecraft:honeycomb`, `minecraft:glistering_melon_slice`, `hexalia:dream_paste` | `hexalia:lourdes` | 4 / 160 ticks |
| `hexalia:aegiflora_from_ritual_table` | `minecraft:dandelion` | `minecraft:gunpowder`, `hexalia:ghost_powder`, `hexalia:lotus_blossom`, `minecraft:moss_block` | `hexalia:aegiflora` | 4 / 160 ticks |
| `hexalia:morphora_from_ritual_table` | `minecraft:poppy` | `hexalia:dream_paste`, `hexalia:spirit_powder`, `hexalia:earth_node`, `hexalia:tree_resin` | `hexalia:morphora` | 4 / 160 ticks |

## Excluded debug recipe

The source also generates:

`hexalia:debug_natures_ritual`

with Diamond central input, Echo Shard + Emerald braziers and Nether Star output.

It is explicitly named `debug_natures_ritual` and is **excluded from the 19-player-facing count**. It must not be used as survival progression evidence without separate proof that the provider intentionally exposes it as normal gameplay.

## Deduplication consequences

This inventory proves that Hexalia already owns provider-native preparation for:

- four elemental nodes;
- magical plants with persistent/area behavior;
- ritual-created combat/tools/equipment;
- Bloomwrap armor progression;
- Sage Pendant;
- Kelpweave Blade and Rootshaper;
- Rabbage Seeds.

A future Black Arcana ritual is not novel merely because it places ingredients around an altar/table or uses crops/nature as admission. Its identity must come from Black Arcana's own transactional casting, hazards, spell domains, world-safety and provider-bridge contracts.

## Authority and progression

The **ritual completion** is the natural discrete provider event. Intermediate 40-tick brazier transfers, crop scanning and persistent output effects are not independent casts/mastery events.

If RPG Skill Tree consumes a future provider milestone, it must bind to a deduplicated completion event with causal player ownership; periodic table ticks or nearby mature crops are not valid mastery sources.
