# Ars Additions 21.3.0 — Exact Registry Inventory

Status: `SOURCE-PINNED 21.3.0 / REGISTRY COUNTS NORMALIZED / RUNTIME QA PENDING`

Exact source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

This inventory follows the actual DeferredRegister/custom-registry setup at the exact pin rather than older documentation counts.

## Blocks and items

### Blocks — 35

`AddonBlockRegistry` registers exactly **35 blocks**, all through `registerBlockAndItem`, therefore all 35 also have block-item registrations.

Functional/stateful blocks:

1. `enchanting_wixie_cauldron`
2. `ender_source_jar`
3. `source_spawner`
4. `warp_nexus`

Decorative/utility families:

- 6 cracked/decorative Sourcestone variants;
- 4 chains;
- 6 Magelight Lanterns;
- 4 normal lanterns;
- 4 walls;
- 2 buttons;
- 2 doors;
- 2 trapdoors;
- 1 Magebloom carpet.

Count: `4 + 6 + 4 + 6 + 4 + 4 + 2 + 2 + 2 + 1 = 35`.

### Direct non-block items — 26

`AddonItemRegistry` registers 14 explicit items plus all 12 `CharmType` values:

Explicit 14:

1. `warp_index`
2. `stabilized_warp_index`
3. `codex_entry`
4. `lost_codex_entry`
5. `ancient_codex_entry`
6. `unstable_reliquary`
7. `exploration_warp_scroll`
8. `nexus_warp_scroll`
9. `xp_jar`
10. `handy_haversack`
11. `advanced_dominion_wand`
12. `wayfinder`
13. `imbued_spell_parchment`
14. `memory_crystal`

Dynamic charms: 12/12, cataloged under [`charms/`](charms/README.md).

### Total item registry entries — 61

- 35 block items;
- 26 direct items;
- total: **61**.

This corrects an intermediate documentation decomposition of `34 block items + 27 items`. The **total 61** was right, but the exact 21.3.0 source decomposition is **35 + 26**.

## Block entities — 5

The exact `AddonBlockRegistry` contains five `registerTile(...)` calls:

1. `enchanting_wixie_cauldron`
2. `ender_source_jar`
3. `source_spawner`
4. `warp_nexus`
5. `magelight_lantern`

The one Magelight Lantern block-entity type is valid for the six Magelight Lantern block variants.

No additional block-entity DeferredRegister was found in the exact setup. Older counts such as 13 block entities are not promoted to this checkpoint.

## Custom entity types — 0

`AddonSetup` does not register an EntityType DeferredRegister, and the exact source search exposes no addon EntityType registration surface. References to external/vanilla entity types in Source Spawner recipes are not provider-owned entity registrations.

## Ars-facing magic registries

- Glyphs: **3** — Retaliate, Mark, Recall.
- Rituals: **2** — Arcane Permanence, Locate Structure.
- Perks: **1** — Reach.
- Mob effects: **1** — `marked`.

## Recipes — 5 serializers / 5 types

`AddonRecipeRegistry` registers the same five ids as both recipe type and serializer:

1. `source_spawner`
2. `locate_structure`
3. `charm_charging`
4. `bulk_scribing`
5. `imbue_scroll`

Older `4 serializers / 6 recipe types` counts are not valid for this exact pin.

## Data components — 11

1. `haversack_data`
2. `charm_data`
3. `advanced_dominion_data`
4. `wayfinder_data`
5. `mark_data`
6. `warp_bind_data`
7. `exploration_scroll_data`
8. `structure_lookup_data`
9. `override_perks`
10. `xp_jar_remainder`
11. `memory_crystal_data`

All except `structure_lookup_data` are explicitly network-synchronized in their component builder at this pin; all 11 are persistent.

## NeoForge attachments — 4

1. `single_item_handler` — serializable one-slot `ItemStackHandler`;
2. `warp_nexus_inventory` — serializable nine-slot handler, `copyOnDeath()`;
3. `particle_color` — serialized Ars `ParticleColor`;
4. `local_weather_status` — serialized `WeatherStatus`.

## Custom codec registries

### MarkData — 4

- `entity`
- `location`
- `empty`
- `broken`

### Tag/NBT modifiers — 4

- `remove_guaranteed_drops`
- `remove_tag`
- `set_tag`
- `append_tag`

These are provider codec/data surfaces and are not generic Black Arcana mutation authority.

## Other registered surfaces

- Loot item functions: **1** — `exploration_scroll`.
- NeoForge condition codecs: **1** — `config`.
- Painting variants: **1** — `snoozebuncle` (32×32).
- Advancement criterion triggers: **3** — `find_ruined_portal`, `create_ruined_portal`, `wixie_enchanting_apparatus`.
- Creative tabs: **1** — `general`.

The source uses vanilla `LootItemCondition` values inside its exploration-scroll loot function codec, but does not register a separate provider loot-condition type in `AddonSetup`.

## Authority consequence

Registry presence establishes provider-owned identity only. Black Arcana must not mirror persistent components/attachments, duplicate recipe settlement or infer gameplay authority from decorative registrations. Stateful systems are audited separately and remain provider-owned unless a real integration seam is later proven.
