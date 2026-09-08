# Ars Elemental 0.7.10.1 — rituals

Status: `8/8 RITUAL REGISTRATIONS SOURCE-PINNED / INSTALLED RUNTIME QA PENDING`

All eight entries are registered through Ars `RitualRegistry` by `ArsNouveauRegistry.registerRituals()`.

## `ars_elemental:ritual_attraction`

- Name: Attraction.
- Base radius: 8 blocks.
- Each consumed Earth Essence increases `getRadius()` by one through consumed-item count.
- Every 10 game ticks, pulls entities in the AABB except types in `ars_elemental:attraction_ritual_blacklist`.
- Explicit Source cost: 10.

## `ars_elemental:ritual_detection`

- Name: Detection.
- Progress increments once per 20 ticks server-side.
- At progress >= 15, all `Monster` entities in radius 128 receive Glowing for 12000 ticks and the ritual finishes.
- Explicit Source cost: 250.

## `ars_elemental:ritual_pollination`

- Accelerates nearby Bee pollination progress in radius 15.
- Adds 100 to `successfulPollinatingTicks` when a bee is actively pollinating.
- Uses a persisted backoff field to reduce work when no bees are relevant.
- Explicit Source cost: 10.

## `ars_elemental:ritual_repulsion`

- Radius: 15.
- Default target set excludes players and boss-tagged entity types.
- Consuming Bone changes the predicate to undead-only.
- Applies provider `REPEL` for 200 ticks, carrying the ritual position.
- Persists its backoff field.
- Explicit Source cost: 10.

## `ars_elemental:ritual_squirrels`

- Name: Fast Squirrels.
- Targets Ars Starbuncles.
- Radius 15, doubled to 30 when Gold Block was consumed.
- Refresh interval comes from `SQUIRREL_REFRESH_RATE`; source default is 600 ticks.
- Applies Movement Speed amplifier 1 for 2400 ticks and Jump amplifier 0 for 2400 ticks.
- Explicit Source cost: 150.

## `ars_elemental:ritual_tesla_coil`

- Name: Zapping.
- Every 100 ticks scans AABB inflated by `(5, 3, 5)` around the brazier.
- Without Air Essence it excludes players; with Air Essence it accepts all LivingEntity targets.
- Spawns Ars Nouveau `LightningEntity` at each target with null cause.
- Explicit Source cost: 500.

## `ars_elemental:ritual_archwood_forest`

Extends Ars `ConjureBiomeRitual`.

- Base biome target is Ars Nouveau Archwood Forest.
- Creates grass on the top layer and dirt underneath through `stateForPos`.
- Consuming at most one Archfruit Pod can switch the target biome:
  - Bombegrante -> Blazing Forest;
  - Frostaya -> Cascading Forest;
  - Mendosteen -> Flourishing Forest;
  - Bastion -> Vexing Caves;
  - Flashing Pod -> Flashing Forest.
- Non-default selected biome is persisted in ritual NBT.
- Provider text states radius 7 and Source Gems add +1 radius each; exact inherited superclass cost/limits are not restated without re-auditing the Ars base implementation.

## `ars_elemental:ritual_archwood_forestation`

Extends Ars `FeaturePlacementRitual`.

- Always adds a Bonemeal feature.
- A consumed specific Archwood sapling selects Blazing, Cascading, Vexing, Flourishing or Flashing feature families.
- Selected families place their corresponding tree, thematic resource/plant and Archfruit Pod.
- Without a specific variant it draws from all five Archwood tree families and all five pod families.
- Adds provider `PlaceableLightFeature` after the variant features.
- Provider text states a 7x7 circular area and Source Gem radius augmentation; inherited superclass cost/limits are not inferred here.

## World-safety boundary

The two Archwood rituals are provider-owned world mutation/biome operations. Black Arcana may observe their results for compatibility but must not replay them or claim ownership. Independent Black Arcana world effects continue through `WorldEffectPolicy`.