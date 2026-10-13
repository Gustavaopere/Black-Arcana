# Ars Additions — Locate Structure

Status: `SOURCE-PINNED 21.3.0 / 15/15 BUILT-IN LOCATOR RECIPES / ASYNC LOOKUP / RUNTIME+PERFORMANCE QA PENDING`

- Registry id: `ars_additions:ritual_locate_structure`
- Display name: Locate Structure
- Source class: `RitualLocateStructure`

## Provider-native behavior

The ritual resolves a `LocateStructureRecipe` matching consumed items. It refuses to start without a matching recipe. On start it delegates the search to provider `LocateUtil.locateCenter(...)`, using recipe-defined structure holder, search radius and `skipExisting` behavior.

The exact source-generated set contains **15 built-in locator recipes** covering Pillager Outpost, End City, Jungle Temple, Wilden Den, Ocean Monument, Nether Fortress, Ancient City, Igloo, Bastion, Desert Temple, Trail Ruins, Arcane Library, Stronghold, Trial Chamber and Woodland Mansion. Exact augment sets are cataloged in [`../systems/structure-locator.md`](../systems/structure-locator.md).

Default generated recipe search contract is **50 chunks** with known structures skipped. Datapack recipes may override radius and skip-known behavior.

On success the ritual creates an Ars Additions Wayfinder with:

- provider `WAYFINDER_DATA` naming the located structure where a registry key is available;
- vanilla `LODESTONE_TRACKER` pointing at the located structure-center `GlobalPos` without requiring a lodestone.

On failure it returns consumed items and the ritual item as spawned item entities before finishing.

The ritual itself has an empty tick method; expensive lookup is not implemented as a per-tick world scan in this class.

## Async configuration

The provider locator thread pool has a source-default maximum of **1 thread** and requires a world restart to change. The config intentionally has no upper bound beyond integer range, so representative-performance QA is required before any increase.

## Black Arcana boundary

Structure discovery, recipe matching and Wayfinder state are provider-owned. Black Arcana must not mirror the lookup into a second unbounded search or treat a provider-found position as blanket teleport/world-effect authorization.

Source checkpoint: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4` (`RitualLocateStructure`, `LocateStructureProvider`, `LocateStructureRecipe`, `ExplorationScrollData`, `ServerConfig`).

## Engenharia para perks — execução exata 21.3.0

- **Classe pinada:** [`RitualLocateStructure.java`](https://github.com/Jarva/Ars-Additions/blob/91f102a90dc058cf40e4eac5a67a881e48b856b4/src/main/java/com/github/jarva/arsadditions/common/ritual/RitualLocateStructure.java); commit `91f102a90dc058cf40e4eac5a67a881e48b856b4`, versão de source 21.3.0.
- **Recipe gate:** `canStart` sets `recipe=getRecipe()` from `LocateStructureRegistry.INSTANCE.getRecipes().stream().filter(r->r.value().matches(getConsumedItems())).findFirst()`, then requires present; `canConsumeItem` returns true but **that does not bypass the start-time recipe validation**.
- **Search:** `onStart` validates world/pos/recipe/server. Calls `LocateUtil.locateCenter(serverLevel,locator.getStructureHolder(serverLevel),getPos(),locator.getRadius(),locator.getSkipExisting(), callback)`. `tick()` is empty. The source snippet does not specify synchronous/async executor scheduling; follow `LocateUtil` before asserting thread affinity or timing.
- **Outcomes:** callback null calls `fail`, respawning *consumed item stacks* and the ritual item near brazier, messaging player and marking finished. Success constructs provider `WAYFINDER` with optional `WAYFINDER_DATA` structure name and vanilla `LODESTONE_TRACKER=GlobalPos(serverDimension,locatedPos),false`, dispenses and finishes.
- **Perks:** a located position is not a teleport entitlement nor proof of loaded chunks; don't duplicate structure scans or refund items from an observer. Thread-pool config default 1 must not be raised without work budget and game-thread completion QA.
- **Estado:** ✅ classe versionada e entrada source-audited; ⚠️ diferença host Ars 5.13.1 versus build baseline 5.11.2, config instalada, helpers/callback, runtime e Survival ainda não aprovados; ⛔ nenhuma perk RPG/adaptador Black Arcana foi implementado ou testado. Não duplicar mana, Source, inventário ou resolução do provider.
