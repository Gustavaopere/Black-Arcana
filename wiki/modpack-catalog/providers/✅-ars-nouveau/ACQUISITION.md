# Ars Nouveau 5.13.1 — Spell-Part Acquisition

State: `85/85 SOURCE-PINNED RECIPE SURFACE / STARTER DEFAULTS IDENTIFIED / RUNTIME+CONFIG QA PENDING`

Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

Primary source: core `GlyphRecipeProvider` from the exact 5.13.1 release checkpoint. This is the provider datagen that emits the glyph-learning recipes shipped by the mod.

## Learning contract

A generated Glyph recipe produces the provider Glyph item for a spell part. Using that Glyph server-side records knowledge through the Ars player capability, synchronizes it, updates the mana glyph-count bonus when applicable, and consumes the item in survival.

Recipe XP is derived from the spell part's **default tier** in the 5.13.1 datagen:

- Tier I → **27 XP**;
- Tier II → **55 XP**;
- Tier III → **160 XP**.

This recipe XP comes from `defaultTier()` at datagen time. Runtime config can change a glyph's configured tier/cost/starter flag, so customized runtime behavior must still be QA'd against the actual pack configs.

## Default starter spell parts

The exact 5.13.1 source defaults these five parts to `starter=true`:

- `ars_nouveau:glyph_projectile`;
- `ars_nouveau:glyph_touch`;
- `ars_nouveau:glyph_self`;
- `ars_nouveau:glyph_break`;
- `ars_nouveau:glyph_harm`.

When they remain configured as starters, the player is considered to know them without consuming a Glyph item. The recipes still exist in generated data; the runtime `Glyph` item path rejects learning a spell part already considered a starter. Server config can change the starter flags.

## Forms / Methods — 5/5

| Spell part | Recipe ingredients |
|---|---|
| `ars_nouveau:glyph_projectile` | `minecraft:fletching_table` + `minecraft:arrow` |
| `ars_nouveau:glyph_touch` | `#minecraft:buttons` |
| `ars_nouveau:glyph_self` | `#minecraft:wooden_pressure_plates` + `minecraft:iron_chestplate` |
| `ars_nouveau:glyph_pantomime` | `#c:glass_blocks` ×8 |
| `ars_nouveau:glyph_underfoot` | `minecraft:iron_boots` + `#minecraft:wooden_pressure_plates` |

## Augments — 13/13

| Spell part | Recipe ingredients |
|---|---|
| `ars_nouveau:glyph_accelerate` | `minecraft:powered_rail` + `minecraft:sugar` + `minecraft:clock` |
| `ars_nouveau:glyph_decelerate` | `minecraft:soul_sand` + `minecraft:cobweb` + `minecraft:clock` |
| `ars_nouveau:glyph_split` | `ars_nouveau:relay_splitter` + `ars_nouveau:wilden_spike` + `minecraft:stonecutter` |
| `ars_nouveau:glyph_amplify` | `minecraft:diamond_pickaxe` |
| `ars_nouveau:glyph_aoe` | `minecraft:firework_star` |
| `ars_nouveau:glyph_extend_time` | `minecraft:clock` + `#c:storage_blocks/redstone` |
| `ars_nouveau:glyph_pierce` | `minecraft:arrow` + `ars_nouveau:wilden_spike` |
| `ars_nouveau:glyph_dampen` | `minecraft:nether_brick` |
| `ars_nouveau:glyph_extract` | `minecraft:emerald` |
| `ars_nouveau:glyph_fortune` | `minecraft:rabbit_foot` |
| `ars_nouveau:glyph_duration_down` | `minecraft:clock` + `minecraft:glowstone_dust` |
| `ars_nouveau:glyph_sensitive` | `minecraft:scaffolding` + `minecraft:poppy` + `minecraft:water_bucket` |
| `ars_nouveau:glyph_randomize` | `minecraft:pink_carpet` ×2 |

## Effects — 67/67

| Spell part | Recipe ingredients |
|---|---|
| `ars_nouveau:glyph_break` | `minecraft:iron_pickaxe` |
| `ars_nouveau:glyph_harm` | `ars_nouveau:earth_essence` + `minecraft:iron_sword` ×3 |
| `ars_nouveau:glyph_ignite` | `minecraft:flint_and_steel` + `#minecraft:coals` ×3 |
| `ars_nouveau:glyph_phantom_block` | `#c:glass_blocks` ×8 |
| `ars_nouveau:glyph_heal` | `ars_nouveau:abjuration_essence` + `minecraft:glistering_melon_slice` ×4 + `minecraft:golden_apple` |
| `ars_nouveau:glyph_grow` | `ars_nouveau:earth_essence` + `minecraft:bone_block` ×5 + `#c:seeds` ×3 |
| `ars_nouveau:glyph_gust` | `ars_nouveau:air_essence` + `minecraft:piston` ×3 |
| `ars_nouveau:glyph_light` | `minecraft:lantern` + `minecraft:torch` |
| `ars_nouveau:glyph_dispel` | `ars_nouveau:abjuration_essence` + `minecraft:milk_bucket` ×3 |
| `ars_nouveau:glyph_launch` | `ars_nouveau:air_essence` + `minecraft:rabbit_hide` ×3 |
| `ars_nouveau:glyph_pull` | `minecraft:fishing_rod` |
| `ars_nouveau:glyph_blink` | `ars_nouveau:manipulation_essence` + `#c:ender_pearls` ×4 |
| `ars_nouveau:glyph_explosion` | `ars_nouveau:fire_essence` + `minecraft:tnt` ×3 + `minecraft:fire_charge` |
| `ars_nouveau:glyph_lightning` | `ars_nouveau:air_essence` + `minecraft:lightning_rod` ×3 + `minecraft:heart_of_the_sea` |
| `ars_nouveau:glyph_slowfall` | `ars_nouveau:air_essence` + `ars_nouveau:wilden_wing` + `minecraft:feather` ×3 + `#c:rods/blaze` + `#c:crops/nether_wart` |
| `ars_nouveau:glyph_fangs` | `ars_nouveau:conjuration_essence` + `minecraft:prismarine_shard` ×2 + `minecraft:totem_of_undying` |
| `ars_nouveau:glyph_summon_vex` | `ars_nouveau:conjuration_essence` + `minecraft:totem_of_undying` |
| `ars_nouveau:glyph_ender_inventory` | `ars_nouveau:manipulation_essence` + `minecraft:ender_chest` |
| `ars_nouveau:glyph_harvest` | `ars_nouveau:earth_essence` + `minecraft:iron_hoe` |
| `ars_nouveau:glyph_fell` | `ars_nouveau:earth_essence` + `minecraft:diamond_axe` |
| `ars_nouveau:glyph_pickup` | `minecraft:hopper` ×2 |
| `ars_nouveau:glyph_interact` | `ars_nouveau:manipulation_essence` + `minecraft:lever` + `#minecraft:wooden_pressure_plates` + `#minecraft:buttons` |
| `ars_nouveau:glyph_place_block` | `ars_nouveau:manipulation_essence` + `minecraft:dispenser` |
| `ars_nouveau:glyph_snare` | `ars_nouveau:earth_essence` + `minecraft:cobweb` ×4 |
| `ars_nouveau:glyph_smelt` | `ars_nouveau:fire_essence` + `minecraft:blast_furnace` ×4 + `#c:rods/blaze` |
| `ars_nouveau:glyph_leap` | `ars_nouveau:air_essence` + `ars_nouveau:wilden_wing` ×3 |
| `ars_nouveau:glyph_delay` | `ars_nouveau:manipulation_essence` + `minecraft:repeater` + `minecraft:clock` |
| `ars_nouveau:glyph_redstone_signal` | `ars_nouveau:manipulation_essence` + `#c:storage_blocks/redstone` ×3 |
| `ars_nouveau:glyph_intangible` | `ars_nouveau:manipulation_essence` + `minecraft:phantom_membrane` ×3 + `#c:ender_pearls` ×2 |
| `ars_nouveau:glyph_invisibility` | `ars_nouveau:abjuration_essence` + `minecraft:fermented_spider_eye` + `#c:rods/blaze` |
| `ars_nouveau:glyph_wither` | `ars_nouveau:abjuration_essence` + `minecraft:wither_skeleton_skull` ×3 |
| `ars_nouveau:glyph_exchange` | `ars_nouveau:manipulation_essence` + `minecraft:emerald_block` + `#c:ender_pearls` ×2 |
| `ars_nouveau:glyph_craft` | `minecraft:crafting_table` |
| `ars_nouveau:glyph_flare` | `ars_nouveau:fire_essence` + `minecraft:flint_and_steel` ×2 + `minecraft:fire_charge` ×2 + `minecraft:blaze_rod` |
| `ars_nouveau:glyph_cold_snap` | `ars_nouveau:water_essence` + `minecraft:powder_snow_bucket` + `minecraft:ice` |
| `ars_nouveau:glyph_conjure_water` | `ars_nouveau:water_essence` + `minecraft:water_bucket` |
| `ars_nouveau:glyph_gravity` | `ars_nouveau:air_essence` + `minecraft:anvil` ×2 + `#c:feathers` ×3 |
| `ars_nouveau:glyph_cut` | `ars_nouveau:manipulation_essence` + `minecraft:shears` + `minecraft:iron_sword` |
| `ars_nouveau:glyph_crush` | `ars_nouveau:earth_essence` + `minecraft:grindstone` + `minecraft:piston` |
| `ars_nouveau:glyph_summon_wolves` | `ars_nouveau:conjuration_essence` + `minecraft:bone` ×3 + `ars_nouveau:wilden_wing` ×4 |
| `ars_nouveau:glyph_summon_steed` | `minecraft:leather` ×4 |
| `ars_nouveau:glyph_summon_decoy` | `ars_nouveau:conjuration_essence` + `minecraft:armor_stand` ×4 |
| `ars_nouveau:glyph_hex` | `ars_nouveau:abjuration_essence` + `minecraft:fermented_spider_eye` + `minecraft:blaze_rod` ×3 + `minecraft:wither_rose` |
| `ars_nouveau:glyph_glide` | `ars_nouveau:air_essence` + `minecraft:elytra` + `#c:gems/diamond` ×3 |
| `ars_nouveau:glyph_rune` | `ars_nouveau:manipulation_essence` + `ars_nouveau:runic_chalk` + `minecraft:tripwire_hook` |
| `ars_nouveau:glyph_freeze` | `ars_nouveau:water_essence` + `minecraft:snow_block` ×2 |
| `ars_nouveau:glyph_name` | `ars_nouveau:manipulation_essence` + `minecraft:name_tag` |
| `ars_nouveau:glyph_summon_undead` | `ars_nouveau:conjuration_essence` + `minecraft:bone` + `minecraft:wither_skeleton_skull` |
| `ars_nouveau:glyph_firework` | `ars_nouveau:fire_essence` + `minecraft:firework_rocket` ×2 + `minecraft:firework_star` |
| `ars_nouveau:glyph_toss` | `ars_nouveau:manipulation_essence` + `minecraft:dropper` |
| `ars_nouveau:glyph_bounce` | `ars_nouveau:abjuration_essence` + `#c:slime_balls` ×3 |
| `ars_nouveau:glyph_wind_shear` | `ars_nouveau:air_essence` + `minecraft:iron_sword` ×3 |
| `ars_nouveau:glyph_evaporate` | `ars_nouveau:manipulation_essence` + `minecraft:sponge` ×3 |
| `ars_nouveau:glyph_linger` | `ars_nouveau:manipulation_essence` + `minecraft:dragon_breath` + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2 |
| `ars_nouveau:glyph_sense_magic` | `ars_nouveau:abjuration_essence` + `ars_nouveau:dowsing_rod` + `ars_nouveau:starbuncle_shards` |
| `ars_nouveau:glyph_infuse` | `ars_nouveau:abjuration_essence` + `minecraft:glass_bottle` + `#c:rods/blaze` |
| `ars_nouveau:glyph_rotate` | `ars_nouveau:manipulation_essence` |
| `ars_nouveau:glyph_wall` | `ars_nouveau:manipulation_essence` + `minecraft:dragon_breath` + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2 |
| `ars_nouveau:glyph_animate_block` | `ars_nouveau:conjuration_essence` + `#c:obsidians` ×3 |
| `ars_nouveau:glyph_burst` | `ars_nouveau:manipulation_essence` + `minecraft:tnt` ×5 + `minecraft:firework_star` |
| `ars_nouveau:glyph_orbit` | `minecraft:compass` + `minecraft:ender_eye` + `#c:rods/blaze` |
| `ars_nouveau:reset` | `minecraft:target` |
| `ars_nouveau:wololo` | `ars_nouveau:abjuration_essence` + `#c:dyes` ×3 |
| `ars_nouveau:rewind` | `ars_nouveau:manipulation_essence` + `minecraft:clock` ×3 |
| `ars_nouveau:glyph_bubble` | `#c:feathers` ×3 + `minecraft:water_bucket` + `#minecraft:boats` + `ars_nouveau:water_essence` |
| `ars_nouveau:glyph_wind_burst` | `minecraft:wind_charge` ×4 + `ars_nouveau:air_essence` |
| `ars_nouveau:glyph_prestidigitation` | `ars_nouveau:conjuration_essence` |

## Important interpretation notes

- These are **provider-native generated recipes**. Do not replace them with generic crafting in Black Arcana.
- The XP cost is part of the glyph acquisition recipe; it is not RPG Skill Tree XP authority.
- Starter status and glyph enable/tier/cost fields are configurable. Exact live pack config still requires runtime/config QA.
- Addon glyph recipes belong to their addon namespaces and must be catalogued on their respective provider pages rather than folded into these 85 core entries.
