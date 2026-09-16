# Ars Elemental 0.7.10.1 — rituals

Status: `8/8 RITUAL REGISTRATIONS + INHERITED DEFAULTS SOURCE-PINNED / INSTALLED RUNTIME QA PENDING`

Source checkpoints:

- Ars Elemental: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`
- Ars Nouveau 5.13.1 ritual bases: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

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

Extends exact Ars Nouveau 5.13.1 `ConjureBiomeRitual`.

Provider-specific behavior:

- base biome target is Ars Nouveau Archwood Forest;
- grass is placed at `ritualY - 1`, dirt at the other generated layers;
- at most one consumed Archfruit Pod changes the target biome:
  - Bombegrante -> Blazing Forest;
  - Frostaya -> Cascading Forest;
  - Mendosteen -> Flourishing Forest;
  - Bastion -> Vexing Caves;
  - Flashing Pod -> Flashing Forest;
- non-default selected biome is persisted in ritual NBT.

Inherited exact behavior:

- base radius: 7;
- each consumed Ars Source Gem adds its stack count to the radius;
- tracker is initialized around `getPos().below(3)` with the resolved radius;
- each successful placement also calls Ars `RitualUtil.changeBiome` for that position;
- `blocksBeforeSourceNeeded = 5`;
- after five successful block placements the ritual marks itself as needing Source;
- `getSourceCost()` returns 50;
- tracker and radius are persisted by the base ritual.

This means the source contract is **50 Ars Source per five successful placement steps**, not a Black Arcana cost and not a one-time 50-Source total inferred from the tablet description.

## `ars_elemental:ritual_archwood_forestation`

Extends exact Ars Nouveau 5.13.1 `FeaturePlacementRitual`.

Provider-specific behavior:

- always adds a Bonemeal feature;
- a consumed specific Archwood sapling selects Blazing, Cascading, Vexing, Flourishing or Flashing feature families;
- selected families place their corresponding tree, thematic resource/plant and Archfruit Pod;
- without a specific variant it draws from all five Archwood tree families and all five pod families;
- adds provider `PlaceableLightFeature` after the variant features.

Inherited exact behavior:

- base `checkRadius`: 7;
- each consumed Ars Source Gem increases `checkRadius` by its stack count;
- target positions are generated within the radius, shuffled, and processed feature-by-feature;
- the tick loop returns after one successful feature placement, or advances until the ritual finishes;
- `featureIndex`, `positionIndex` and `checkRadius` are persisted;
- the base class does not override `getSourceCost()`; exact `AbstractRitual.getSourceCost()` therefore supplies **0**.

The Source Gems here are radius augment inputs. The inherited source path does not establish an ongoing positive Source pull for this ritual at this pin.

## World-safety boundary

The two Archwood rituals are provider-owned world mutation/biome operations. Black Arcana may observe their results for compatibility but must not replay them or claim ownership. Independent Black Arcana destructive effects continue through `WorldEffectPolicy`.
