# Ars Additions 21.3.0 — Worldgen and magical structures

Status: `SOURCE-PINNED / STRUCTURE SETS+LOOT+PROCESSORS AUDITED / RUNTIME PACK-WORLDGEN QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

The exact pin contains three enabled-by-default structure families: Arcane Library, Nexus Tower and Ruined Warp Portals. All are independently guarded by Ars Additions common-config conditions.

## Arcane Library

- structure id: `ars_additions:arcane_library`;
- config default: enabled;
- random-spread spacing: **50 chunks**;
- separation: **25 chunks**;
- surface jigsaw, size 1, max distance from center 80;
- structure-level monster spawn overrides: Wilden Guardian, Wilden Stalker and Wilden Hunter, each weight 5 and count range 5–10;
- template: one large `arcane_library.nbt`.

Processor behavior source-pinned in `ProcessorDatagen`:

- Ars runes in the structure are transformed to charged, non-temporary state with the Ars fake-player UUID;
- Warp Nexus blocks are generated with `requires_source=false` and an embedded Nexus Warp Scroll;
- Source Jars receive generated source fill/state values.

Chest loot table:

- Codex Entry ×1–4;
- one pool selecting one Ars pod type (Bombegranate, Frostaya, Bastion or Mendosteen), count ×1–8.

## Nexus Tower

- structure id: `ars_additions:nexus_tower`;
- config default: enabled;
- random-spread spacing: **80 chunks**;
- separation: **20 chunks**;
- surface jigsaw, size 1, max distance from center 80;
- eight shipped tower templates: four color variants (blue, green, purple, red), each with filled and `_empty` variants.

Processor behavior includes randomized block ageing/material substitution, optional Starbuncle/Scribes-block helper state, and the same provider Warp Nexus transformation to `requires_source=false` with an embedded Nexus Warp Scroll.

Chest loot table matches the Arcane Library's Codex Entry + Ars pod pools.

## Ruined Warp Portals

Structure ids:

- `ars_additions:ruined_portal`;
- `ars_additions:ruined_portal_large`.

Config default: enabled.

Shared random-spread set:

- spacing: **40 chunks**;
- separation: **15 chunks**;
- exclusion zone: **10 chunks** from the vanilla `minecraft:ruined_portals` structure set;
- equal weight between normal and large Ars Additions variants.

Shipped NBT templates:

- small: 4 colors × normal/horizontal = 8;
- large: 4 colors × normal/horizontal = 8;
- total ruined-portal templates: 16.

Chest loot:

- one Explorer's Warp Scroll configured through the addon exploration-scroll loot function with search radius 100 and skip-existing-chunks enabled;
- Sourcestone ×4–64;
- Codex Entry ×1–4.

## Worldgen authority boundary

These structures may ship preconfigured Ars/Ars Additions block state that would not be obtainable by normal player configuration, notably free-source Warp Nexus instances and charged runes. Black Arcana must not interpret structure-placed state as permission to bypass its own world safety/resource policies.

Worldgen placement and structure location are provider/datapack authority. Black Arcana does not rewrite provider structure state or use provider structure lookup as an implicit force-load/displacement primitive.
