# Conjure Island: Plains

Status: `SOURCE-PINNED 5.13.1 / BIOME-WORLDGEN RITUAL`

- Registry id: `ars_nouveau:ritual_conjure_island_plains`
- Class: `ConjurePlainsRitual`
- Base radius: `7`
- Radius augmentation: `+1` per consumed Source Gem-tag item count
- Source cost: `50` per provider Source request
- Source request cadence: every `5` successfully placed blocks
- Placement budget: at most one successful block placement per ritual tick
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

The ritual inherits `ConjureBiomeRitual`. On start it builds a Manhattan tracker centered three blocks below the ritual and increases radius by consumed Source Gems.

For eligible positions inside the spherical radius, the ritual places:

- Grass Block at ritual Y−1;
- Dirt at the other generated island layers.

Each successful placement also calls Ars Nouveau's biome-change helper for the ritual biome. The default biome is Plains.

If one Frostaya Pod is consumed, the ritual switches biome output to Snowy Plains while preserving the same island block construction rules.

The generation loop is bounded: each ritual tick searches up to `radius` candidate tracker positions but returns immediately after the first successful placement. Every five successful placements, it resets the local counter and marks the ritual as needing Source.

## Authority / Black Arcana boundary

Block placement, biome mutation, Source-gem radius augmentation, Source debit and tracker persistence are Ars Nouveau authority. Black Arcana must not duplicate island blocks/biome changes or replace this with an unbounded worldgen operation.

Independent Black Arcana terrain/biome mutation remains subject to `WorldEffectPolicy` and explicit bounded-work contracts.

## QA

Source behavior is pinned to 5.13.1. Protection/claim interaction is not explicitly visible in `ConjureBiomeRitual`'s placement path and therefore requires full-pack runtime QA rather than inference.