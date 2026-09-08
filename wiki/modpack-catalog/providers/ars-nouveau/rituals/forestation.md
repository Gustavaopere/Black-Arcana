# Forestation

Status: `SOURCE-PINNED 5.13.1 / FEATURE-PLACEMENT RITUAL`

- Registry id: `ars_nouveau:ritual_forestation`
- Class: `ForestationRitual`
- Base check radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native feature modes

Forestation inherits Ars Nouveau's `FeaturePlacementRitual`, which constructs a shuffled bounded target-position list for each feature and processes features sequentially, returning after each successful placement.

### Default forest

- Oak/Birch random tree feature;
- provider bonemeal feature.

### Taiga modifier

Exactly one Brown Mushroom selects the taiga family, including:

- Spruce trees;
- conversion of dirt/grass to Podzol;
- fern/large fern placement;
- Brown Mushroom placement;
- grass placement;
- rare Sweet Berry Bush placement with randomized vanilla age.

### Jungle modifier

Exactly one Glow Berries item selects the jungle family, including:

- big Jungle trees;
- normal Jungle trees;
- cocoa placement;
- grass, melon and fern placement.

Brown Mushroom and Glow Berries are mutually exclusive variant selectors. Source Gem-tag items remain separately accepted as radius augments.

## Bounded placement model

`FeaturePlacementRitual` starts at radius 7, builds positions inside the radius, shuffles them, checks minimum separation per feature and advances feature-by-feature. It returns after a successful `onPlace`, rather than executing every candidate in one tick.

## Authority / Black Arcana boundary

Terrain vegetation conversion, feature probabilities, placement order and radius modifiers remain Ars Nouveau authority. Black Arcana must not replay generated trees/plants or treat each feature as an independent ritual completion.

Independent Black Arcana environmental creation remains bounded and subject to `WorldEffectPolicy` where it mutates the world.

## QA

Source structure is pinned to 5.13.1. The base helper does not itself prove every protection/claim integration for every `IPlaceableFeature`; representative full-pack world-safety QA remains required.