# Ars Two-Way Portals — pair lifecycle and teleport semantics

Status: `2.0.0 FEATURE CONTRACT RELEASE-CONFIRMED / INTERNAL FORMULAS FROM 1.3.4 BASELINE`

## Exact release-level contract

The 2.0.0 publisher page establishes:

- two matching Source Stone frames become one permanent linked pair;
- vertical/horizontal and cross-dimension pairs are supported;
- regular Ars mode has a three-second re-entry cooldown;
- ordinary tracked-frame break removes the linked endpoints;
- Portal Nullify intentionally removes only one side;
- optional Immersive mode can replace regular Ars portal rendering/engine behavior.

## Public 1.3.4 baseline transaction

The old implementation wraps Ars `StableWarpScroll.onEntityItemUpdate` rather than replacing it.

### Before Ars portal creation

For the provider scroll the baseline:

1. validates server level and Ars WarpScroll data;
2. resolves the recorded dimension;
3. rejects invalid/mismatched frame geometry;
4. rejects pairing the same dimension+position to itself;
5. records an ephemeral `PendingPair` keyed by thrown `ItemEntity` UUID;
6. remembers endpoints, rotation, throw direction, display name, original stack count and whether the optional Immersive path was selected.

### After Ars portal creation

Only when Ars reports portal creation and the scroll count decreased does the baseline continue:

1. resolve both ServerLevels;
2. construct a reverse Ars Stable Warp Scroll;
3. ask Ars `PortalBlock.trySpawnPortal` to create the return endpoint;
4. inspect both connected portal geometries;
5. either convert to Immersive Portals or tag/point both Ars portals at each other.

This is one causal provider transaction around Ars portal creation. A BA observer must not execute a second return portal or second teleport.

## Bounded topology baseline

Connected portal inspection/cleanup uses flood fill with `MAX_PORTAL_BLOCKS = 1024`. Geometry calculation derives a bounded AABB, axis/facing/orientation and a collision-checked preferred/alternate exit.

The 1024 bound belongs to the old provider baseline. Black Arcana's own world/spatial effects retain their own stricter budgets and `WorldEffectPolicy` requirements.

## Baseline regular pair persistence

Each Ars `PortalTile` is tagged with provider persistent data:

- pair id;
- partner dimension;
- partner X/Y/Z.

No separate global SavedData pair database was identified in the 1.3.4 source. Ordinary frame break finds a linked neighboring PortalTile, removes the local connected portal region and then removes the partner region if that dimension resolves.

Because exact 2.0.0 source is unavailable, this persistence shape is not asserted as current implementation.

## Anti-reentry baseline

`PortalCooldown` stores `ars_two_way_portals:cooldown_until` only on `ServerPlayer` persistent data. A successful `PortalTile.teleportEntityTo` result begins a 60-tick cooldown. PortalTile tick drops queued entities whose cooldown is active, and a queued teleport attempt returns null while active.

The exact 2.0.0 publisher page independently confirms the user-facing duration as three seconds. Exact 2.0.0 implementation/storage remains binary QA.

## Nullification baseline

A thrown Portal Nullify Scroll scans a small swept AABB around its own ItemEntity path. For regular provider portals, the first matching linked endpoint is removed locally; the baseline does not delete the opposite endpoint through `nullifyEndpoint`. Optional Immersive behavior delegates to its integration.

## Fail-closed lifecycle questions

Do not infer from the baseline:

- 2.0.0 exact persistent keys/schema;
- exact unload/restart repair behavior;
- force-loading behavior;
- exact NeoForge event ordering;
- exact current-host protection integration;
- exact handling when the partner dimension/chunk is unavailable.

Those require the physical 2.0.0 binary/current runtime.
