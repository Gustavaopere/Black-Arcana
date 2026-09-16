# Flowering

Status: `SOURCE-PINNED 5.13.1 / FEATURE-PLACEMENT RITUAL`

- Registry id: `ars_nouveau:ritual_flowering`
- Class: `FloweringRitual`
- Base check radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native modes

Flowering inherits `FeaturePlacementRitual`, using its bounded shuffled-position/feature-by-feature placement model.

### Default mode

It registers:

- a randomized flower-placement feature drawn from 16 vanilla flower blocks;
- a bonemeal feature.

### Desert modifier

If a sand-tag item has been consumed, it switches to:

- sparse Cactus placement;
- Dead Bush placement.

Only one sand variant selector is accepted. Source Gems remain separately accepted to enlarge the feature radius.

## Authority / Black Arcana boundary

Feature selection, probabilities, radius and world placement remain Ars Nouveau authority. Black Arcana must not replay flowers/cactus/bonemeal operations or award progression per placed block.

Independent Black Arcana environmental mutation remains bounded and subject to project world-safety policy.

## QA

Source behavior is pinned to 5.13.1. Protection/claim compatibility for every feature implementation remains full-pack runtime QA.