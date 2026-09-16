# Conjure Island: Desert

Status: `SOURCE-PINNED 5.13.1 / BIOME-WORLDGEN RITUAL`

- Registry id: `ars_nouveau:ritual_conjure_island_desert`
- Class: `ConjureDesertRitual`
- Base radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Source cost: `50` per provider Source request
- Source request cadence: every `5` successful placements
- Placement budget: at most one successful block placement per ritual tick
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

The ritual inherits `ConjureBiomeRitual` and defaults to Desert biome output.

### Desert mode

- top island layer: Sand;
- deeper generated layers: Sandstone.

### Badlands modifier

If a terracotta-tag item is consumed, the provider switches the biome to Badlands and creates a depth-dependent material profile:

- depth 1: Red Sand;
- depth 2: Orange Terracotta;
- depth 3–4: Red Terracotta;
- deeper layer: Terracotta.

Only one terracotta variant selector is accepted. Source Gem-tag inputs remain radius modifiers.

Every successful placed block also invokes the provider biome-change helper. The shared helper requests 50 Source every five successful placements.

## Authority / Black Arcana boundary

Terrain generation, biome conversion, Source accounting and persistent tracker state are Ars Nouveau authority. Black Arcana must not duplicate blocks or biome changes.

Independent Black Arcana terrain/biome mechanics remain subject to `WorldEffectPolicy` and bounded scheduling.

## QA

Source behavior is pinned to 5.13.1. As with the Plains variant, direct protection/claim preflight is not explicit in this helper path and therefore requires runtime validation.