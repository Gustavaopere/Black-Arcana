# Locate Structure recipe system

Status: `SOURCE-PINNED 21.3.0 / 15/15 GENERATED LOCATOR RECIPES / ASYNC SEARCH AUTHORITY AUDITED / RUNTIME+PERFORMANCE QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Custom recipe type: `ars_additions:locate_structure`.

This recipe system determines which consumed augment set can drive the Ars Additions Locate Structure ritual. It is not normal crafting: vanilla `Recipe.matches/assemble` deliberately return false/empty, while `RitualLocateStructure` queries the provider recipe registry and calls the recipe's dedicated item-list matcher.

## Source-generated recipe inventory — 15/15

1. Pillager Outpost — Emerald
2. End City — Purpur Block
3. Jungle Temple — Mossy Cobblestone
4. Wilden Den — Ars Source Gem
5. Ocean Monument — `#minecraft:fishes`
6. Nether Fortress — Nether Brick
7. Ancient City — Deepslate Bricks
8. Igloo — Ice
9. Bastion — Polished Blackstone Bricks
10. Desert Temple — Sandstone
11. Trail Ruins — `#minecraft:terracotta`
12. Arcane Library — Ars Apprentice Spell Book
13. Stronghold — Ender Eye ×12
14. Trial Chamber — Ominous Bottle
15. Woodland Mansion — Brown Mushroom + Red Mushroom

Recipes may target either a structure registry key or a structure tag. All source-generated entries use the `ExplorationScrollData` defaults unless datapack authors override them:

- search radius: **50 chunks**;
- skip known structures: **true**.

## Ritual execution

`RitualLocateStructure` refuses to start without one matching locator recipe. On start it performs provider async location through `LocateUtil.locateCenter` and the configured recipe structure holder/radius/skip-known values.

On success the ritual emits a Wayfinder carrying:

- provider `wayfinder_data` naming the resolved structure when a key is available;
- vanilla `LODESTONE_TRACKER` containing the structure-center `GlobalPos`.

On lookup failure, consumed augment items and the ritual tablet are returned as item entities and the ritual ends.

## Threading / performance

The provider's locator executor defaults to one worker thread. Search completion schedules gameplay mutation back onto the Minecraft server thread. This avoids implementing the expensive structure lookup as a per-tick ritual scan, but actual structure-locate cost remains a representative-world performance QA surface.

## Extensibility

Because these are datapack recipes backed by `ResourceOrTag`, additional structure targets/augment sets may be supplied by datapacks. The 15/15 count above is the exact built-in set for source pin 21.3.0, not a universal ceiling.

## Black Arcana boundary

Provider-found structure positions do not grant Black Arcana teleport, chunk-load or world-effect authority. Black Arcana must not mirror this async locator into a second search pipeline or interpret Wayfinder state as permission to bypass loaded-chunk/safe-target policies.
