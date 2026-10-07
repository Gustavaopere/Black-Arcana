# Waystones — 21.1.45

Status: `✅ CATALOGED / CURRENT PHYSICAL 21.1.45 / COUNTED_SOURCE_PINNED / EXACT SEMANTIC DENOMINATOR 3 / +3 STRICT / RUNTIME QA SEPARATE`

## Current physical authority

Current sibling physical authority at `neoforge-rpg-skilltree@1bb7c7d6e2e6878248b0c178bdae55e84697acd2` records:

- physical row: `#564`;
- JAR: `waystones-neoforge-1.21.1-21.1.45.jar`;
- mod id: `waystones`;
- runtime: `21.1.45`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `6ec1a176a102212db4f6391886db52ed103c830f`.

The older 21.1.44 narrative retained by the sibling dossier is superseded by its current physical override to 21.1.45.

## Exact-version source pin

Official repository:

`TwelveIterations/Waystones`

Exact source checkpoint:

`c540cfdbb9c1d790fbff397beea7c83f0c6f035f`

At this revision `gradle.properties` declares:

- `mod_id = waystones`;
- `version = 21.1.45`;
- `minecraft_version = 1.21.1`;
- `include_neoforge=true`.

The source license is All Rights Reserved. No physical-JAR ↔ source-build byte equality is claimed, so the semantic state is `COUNTED_SOURCE_PINNED`, not `COUNTED_EXACT`.

## Semantic metric

Black Arcana counts one provider-owned semantic magic object for one discrete supernatural player action identity.

Aliases and alternate trigger surfaces are deduplicated when they settle through the same provider-native causal action. Setup/discovery state, item preparation, automated infrastructure processing, GUI/management state, passive procs and downstream consequences are excluded unless they form an independent supernatural player action.

## Fichas por ação

As **3 identidades semânticas** fechadas para Waystones 21.1.45 estão materializadas em fichas individuais em [`ACTION-CARDS-21.1.45.md`](ACTION-CARDS-21.1.45.md). A camada de cards preserva `COUNTED_SOURCE_PINNED 3 / +3 strict` e não altera runtime QA.

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Exact current semantic inventory

### 1. Waystone Warp / Teleport

Waystones centralizes teleport settlement through its provider teleport pipeline ending in `WaystonesAPI.tryTeleportAsync(...)`.

The following player-facing surfaces are aliases of that same causal action and therefore count once:

- activated Waystone selection;
- Sharestone selection;
- Portstone selection;
- Warp Stone;
- Warp Scroll;
- Bound Scroll;
- Return Scroll;
- configured inventory-button selection;
- Warp Plate traversal;
- Warp Portal traversal.

Semantic contribution: **1**.

### 2. Warp Portal Conjuration

`PortalScrollItem` opens a target-selection flow whose post-selection action calls `WarpPortalManager.spawnPortal(...)` instead of directly executing the teleport pipeline.

Portal creation is therefore a distinct player-invoked supernatural action. Later traversal of the created portal reuses the already-counted teleport root.

Semantic contribution: **1**.

### 3. Twinbound Link

`TwinboundFeatherItem` implements a synchronized two-player held interaction. Both players use Twinbound Feathers while mutually targeting each other; completion persists reciprocal link state, and a carried linked feather exposes the partner as a dynamic Waystones destination.

This is a distinct cooperative ritual-like supernatural action and does not itself execute the normal teleport root.

Semantic contribution: **1**.

## Previously open setup surfaces — closed at +0

### Waystone activation — `EXCLUDED_SETUP_DISCOVERY`

First interaction with an unactivated regular Waystone records activation/discovery state, initializes ownership/visibility where applicable, emits the provider activation event and presents feedback.

It does not execute teleport, create a separate magical effect target, or expose an action independent from preparing/discovering the transport network. Player-placed Waystones are also activated for the placer during placement.

Under the canonical metric this is provider network/discovery setup, not a fourth semantic magic action.

### Blank Scroll binding — `EXCLUDED_ITEM_PREPARATION`

`BlankScrollItem.useOn(...)` consumes a Blank Scroll on a Waystone and creates a Bound Scroll carrying that Waystone identity through `WaystonesAPI.setBoundWaystone(...)`.

The prepared Bound Scroll later invokes the already-counted teleport root. Binding therefore prepares an invocation item and does not create an independent magical action outcome.

### Warp Plate shard attunement — `EXCLUDED_AUTOMATED_INFRA_PREPARATION`

A player may insert a Dormant Shard into a Warp Plate, but the actual conversion is provider-managed server-tick processing: after the attunement timer completes, the plate creates an Attuned Shard, binds it to the plate Waystone and ejects it.

This is automated target/infrastructure preparation for Warp Plate routing, not an independent player cast/action.

## Complete current player-action surface recheck

The exact 21.1.45 source tree was rechecked across provider item and block interaction surfaces.

`ModItems` registers the current item set. Direct use/action methods are confined to:

- the scroll family;
- Warp Stone;
- Twinbound Feather;
- Blank Scroll binding.

Shard items, Warp Dust and Epitaph do not expose a separate player-use cast family. Block interaction surfaces are confined to Waystone/Sharestone/Portstone selection or activation, Warp Plate setup/traversal/settings, Warp Portal traversal, and ordinary edit/management state. Fleeting Memorial exposes no independent activation action.

After deduplicating transport aliases and applying the setup/preparation exclusions above, no additional semantic root remains.

Therefore the exact source-pinned denominator is:

`1 teleport + 1 portal conjuration + 1 twinbound link = 3`.

## Source-level reachability

The exact 21.1.45 generated data includes normal crafting routes for the core surfaces used by all three counted roots, including:

- `waystones:waystone`;
- `waystones:warp_stone`;
- `waystones:portal_scroll`;
- `waystones:twinbound_feather`;
- supporting scroll/shard recipes.

The provider config exposes costs, cooldowns, durability, warp requirements, inventory-button policy, worldgen and modifier policy, but no global registration/enable toggle that removes the three counted action identities from the provider.

This is sufficient for catalog-level source reachability. Exact deployed values, multiplayer behavior and server policy remain runtime QA and are not inferred.

## Explicit exclusions

The following contribute **+0** additional semantic identities:

- alternate teleport surfaces listed above;
- Waystone activation/discovery;
- Blank Scroll binding;
- Warp Plate shard attunement;
- Epitaph → Fleeting Memorial death-triggered passive proc;
- Waystone modifier status effects;
- edit/settings/group/sorting/visibility management;
- destination registries/indexes;
- costs, cooldowns and requirements;
- worldgen and map markers;
- JourneyMap/Dynmap/BlueMap presentation;
- Waystones:Sable coordinate transformation/bridge behavior.

## Authority boundary

Waystones remains authority for destination state, activation/discovery state, teleport validation and settlement, warp requirements/cost/cooldown policy, Warp Plate/Portal state and Twinbound destination state.

Black Arcana must not create a parallel Waystones destination registry, bypass provider teleport validation, duplicate provider costs/cooldowns or reinterpret setup state as a second execution path.

RPG Skill Tree remains sibling authority only for progression, attributes, Mastery, perks and gates through real contracts.

## Runtime QA remains separate

Catalog closure does not assert assembled-pack PASS. Remaining runtime/integration QA includes:

- client + dedicated-server behavior with physical 21.1.45;
- persistence of destinations/activation/Twinbound state;
- multiplayer target selection and portal lifecycle;
- effective deployed warp requirements/costs/cooldowns;
- Warp Plate timing and single-use shard consumption;
- Sable coordinate transforms;
- map integrations and permission/deny-list behavior.

## Result

**✅ Cataloged — `COUNTED_SOURCE_PINNED`.**

Current semantic inventory: **3** discrete provider-owned supernatural player actions.

Strict global semantic delta: **+3**.