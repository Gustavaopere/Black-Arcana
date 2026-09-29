# Waystones 21.1.45 — exact-version semantic closure

Checkpoint: 2026-09-29

Evidence class:

`EXACT_PHYSICAL_IDENTITY / EXACT_VERSION_SOURCE / COMPLETE SOURCE ACTION-SURFACE RECONCILIATION / COUNTED_SOURCE_PINNED 3 / +3 STRICT`

## Authority

- sibling: `neoforge-rpg-skilltree@82d0d551f34d20363201f5b71f0ad91a141cbe56`;
- physical row: `#564`;
- JAR: `waystones-neoforge-1.21.1-21.1.45.jar`;
- runtime: `21.1.45`;
- physical SHA-1: `6ec1a176a102212db4f6391886db52ed103c830f`;
- official source: `TwelveIterations/Waystones@c540cfdbb9c1d790fbff397beea7c83f0c6f035f`.

The source checkpoint declares Waystones 21.1.45 for Minecraft 1.21.1 with NeoForge included. Physical/source byte equality is not claimed.

## Counted roots

1. **Waystone Warp / Teleport** — all direct-warp items, Waystone/Sharestone/Portstone selection, inventory button, Warp Plate traversal and Warp Portal traversal converge on the provider teleport settlement pipeline. Count once.
2. **Warp Portal Conjuration** — Portal Scroll target selection spawns a target-bound Warp Portal instead of directly teleporting. Later traversal is the existing teleport root.
3. **Twinbound Link** — synchronized two-player Feather use persists reciprocal link state and creates a dynamic partner destination. Independent from teleport execution.

Denominator: **3**.

## Setup classifications closed at +0

### Activation

Exact `WaystoneBlock.handleActivation(...)` and `PlayerWaystoneManager.activateWaystone(...)` show that first-use activation records discovery/ownership/visibility state, fires the activation event, syncs state and emits feedback. It does not settle a teleport or produce a separate independent supernatural effect.

Player placement also calls the same activation path automatically for the placer.

Disposition: **`EXCLUDED_SETUP_DISCOVERY`**.

### Blank Scroll binding

Exact `BlankScrollItem.useOn(...)` creates a Bound Scroll and writes the clicked Waystone identity through `WaystonesAPI.setBoundWaystone(...)`.

The Bound Scroll later resolves the target and executes the already-counted teleport pipeline.

Disposition: **`EXCLUDED_ITEM_PREPARATION`**.

### Warp Plate shard attunement

Exact `WarpPlateBlock.useItemOn(...)` only inserts a shard. Exact `WarpPlateBlockEntity.serverTick()/attuneShard()` performs the later conversion from Dormant Shard to Attuned Shard, binds the plate Waystone and ejects the prepared shard.

Disposition: **`EXCLUDED_AUTOMATED_INFRA_PREPARATION`**.

## Complete action-surface recheck

The exact source tree was enumerated across current provider item/block interaction classes.

Current direct item action families:

- scroll family;
- Warp Stone;
- Twinbound Feather;
- Blank Scroll.

Current block action families:

- regular Waystone activation/selection;
- Sharestone selection;
- Portstone selection;
- Warp Plate shard insertion/ejection/settings/traversal;
- Warp Portal traversal;
- edit/settings management inherited from the Waystone block base.

Fleeting Memorial exposes no independent activation action. Shard items, Warp Dust and Epitaph expose no independent player-use cast family.

All positive action paths reconcile to the three counted roots; all remaining surfaces are setup, management, passive, infrastructure or aliases.

## Reachability

Exact generated recipes provide normal provider-native acquisition for Waystone, Warp Stone, Portal Scroll and Twinbound Feather, plus supporting scroll/shard items.

Exact config source exposes cost/cooldown/durability/warp-requirement/worldgen/modifier policy but no provider registration switch that removes the three action identities. External/deployed policy can still change practical conditions and remains runtime QA.

## Exclusions

- Epitaph/Fleeting Memorial death proc: passive;
- teleport modifier effects: downstream consequences;
- GUI/list/index/sorting/group/visibility state: management;
- map integrations: presentation;
- Sable bridge: coordinate transformation;
- recipes/items themselves: containers/acquisition, not extra action roots.

## Clean-room

Waystones source is All Rights Reserved. This closure retains only factual version/registry/resource identities, public method-level causal relationships and semantic classification. No implementation body, localization prose, assets or provider code are copied into Black Arcana runtime.

## Result

- exact physical identity: closed;
- exact-version source line: closed;
- complete source player-action denominator: **3**;
- setup classifications: closed at **+0**;
- source-level acquisition: closed;
- semantic state: **`COUNTED_SOURCE_PINNED`**;
- strict contribution: **+3**;
- provider catalog status: **✅**;
- assembled runtime QA: separate.