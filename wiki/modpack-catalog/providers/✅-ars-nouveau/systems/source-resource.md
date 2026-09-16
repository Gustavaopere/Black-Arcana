# Ars Nouveau — Source

State: `SOURCE-PINNED 5.13.1 / PROVIDER AUTHORITY VERIFIED / TILE-SPECIFIC CAPACITIES NOT NORMALIZED HERE`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

## Resource identity

**Source is not player mana.** Ars exposes `ISourceTile` as the generic contract for blocks/tiles that hold or transfer Source. The interface includes:

- transfer rate;
- whether the tile can accept/provide Source;
- current and maximum Source;
- set/add/remove Source;
- simulated add/remove overloads for compatible implementations.

The interface comments explicitly retain default simulation fallbacks for addon compatibility, so an integration must not assume every third-party Source tile implements simulation identically.

## Usage surface

Source is consumed or routed by Ars world/crafting/automation systems. The ritual pages in this catalog record ritual-specific Source requirements where verified. Player spell casting uses Ars **player mana** instead and must not be conflated with Source.

## Integration constraints

- Ars owns Source quantity, storage and transfer semantics.
- Black Arcana must not create a duplicate Source ledger.
- A Black Arcana ritual may consume Ars Source only through a verified provider adapter with transactional semantics compatible with Black Arcana D017; `ISourceTile` alone does not prove atomic multi-resource reservation.
- Because the interface's simulation methods have addon-compatibility fallbacks, using `simulate=true` as if it were universally side-effect-free requires exact provider/runtime verification.
- RPG Skill Tree does not become authority for Source merely because it can gate progression.

## Catalog scope

This page records the resource contract. Individual Source-generating machines, relays and automation blocks are provider content and may receive separate catalog entries when they create a unique magical capability relevant to Black Arcana deduplication; they are not silently converted into spells.