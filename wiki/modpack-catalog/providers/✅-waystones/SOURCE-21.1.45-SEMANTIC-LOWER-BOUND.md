> **HISTORICAL / SUPERSEDED.** This lower-bound checkpoint is preserved for provenance only. The complete semantic closure is now [SOURCE-21.1.45-SEMANTIC-CLOSURE.md](SOURCE-21.1.45-SEMANTIC-CLOSURE.md), which classifies the remaining setup surfaces at +0 and closes Waystones 21.1.45 at three `COUNTED_SOURCE_PINNED` actions.

# Waystones 21.1.45 — exact-source semantic lower bound

Checkpoint: 2026-09-28

## Evidence class

`EXACT_PHYSICAL_IDENTITY / EXACT_VERSION_SOURCE / LOWER_BOUND 3 PLAYER ACTIONS / SETUP-ACTION CLASSIFICATION OPEN / +0 STRICT`

## Physical authority

Sibling physical row #564 at
`neoforge-rpg-skilltree@7c9d0e9552e33531d0d6b46b86c9de86d3b233bf`:

- JAR: `waystones-neoforge-1.21.1-21.1.45.jar`;
- mod id: `waystones`;
- runtime: `21.1.45`;
- SHA-1: `6ec1a176a102212db4f6391886db52ed103c830f`;
- category includes `Magic`.

Category membership is not used as semantic-count evidence.

## Exact source pin

`TwelveIterations/Waystones@c540cfdbb9c1d790fbff397beea7c83f0c6f035f`

Exact metadata at this revision:

- mod id `waystones`;
- version `21.1.45`;
- Minecraft `1.21.1`;
- NeoForge included;
- license declared All Rights Reserved.

The 21.1.45 changelog contains the multiplayer activation-crash fix.

No byte-equivalence claim is made between this source checkout and the installed publisher JAR.

## Metric used

A countable object must be one provider-owned discrete supernatural player action.

The audit deduplicates different items, blocks and GUIs when they ultimately invoke the same provider-native causal action.

Infrastructure/state such as menus, target indexes, worldgen, markers, costs, cooldowns, status effects and bridge transformations does not create a separate semantic root.

## Root 1 — Waystone Warp / Teleport

Exact 21.1.45 source centralizes actual teleport settlement through `WaystonesAPI.tryTeleportAsync(...)` / the provider teleport manager.

Positive player-invoked entry surfaces include:

- regular Waystone selection after activation;
- Sharestone selection;
- Portstone selection;
- Warp Stone selection;
- Warp Scroll selection;
- Bound Scroll direct target;
- Return Scroll direct target;
- configured inventory-button target or selection.

Additional non-identical trigger surfaces include Warp Plate collision and Warp Portal traversal, but they terminate in the same provider teleport pipeline.

The teleport manager performs provider validation and requirement settlement before moving the entity/entities.

### Deduplication rule

The following are **not** separate semantic roots:

- Warp Stone teleport;
- Warp Scroll teleport;
- Bound Scroll teleport;
- Return Scroll teleport;
- Waystone GUI teleport;
- Sharestone teleport;
- Portstone teleport;
- inventory-button teleport;
- Warp Plate teleport;
- Warp Portal traversal.

They are physical/input surfaces of one provider-owned teleport identity.

Subtotal: **1**.

## Root 2 — Warp Portal Conjuration

`PortalScrollItem` opens a dedicated target-selection flow.

The server selection handler recognizes the Portal Scroll menu as a special case. Instead of executing `tryTeleportAsync(...)`, it resolves the target context and directly invokes the menu's post-selection action.

The Portal Scroll post-selection action calls the provider portal manager to spawn and initialize a temporary Warp Portal aimed at that target.

This establishes a separate causal action:

**conjure a target-bound Warp Portal**.

The portal's later entity traversal is settled by the already-counted teleport root and contributes +0 additional roots.

Subtotal: **1**.

## Root 3 — Twinbound Link

`TwinboundFeatherItem` provides a distinct cooperative player action.

At exact source:

- using the feather begins a held action;
- a valid target must be another player;
- both players must simultaneously use Twinbound Feathers while mutually targeting each other;
- progress accumulates only while the synchronized interaction remains valid;
- completion persists reciprocal link identifiers on both feathers;
- linked carried feathers create dynamic partner destinations for Waystones targeting.

This action changes persistent provider state and is independent of the later teleport settlement.

It is treated as a ritual-like supernatural player action under the canonical metric.

Subtotal: **1**.

## Lower-bound arithmetic

`1 provider teleport + 1 portal conjuration + 1 twinbound link = 3`.

Disposition:

**LOWER_BOUND 3 / +0 STRICT**.

## Exact source surfaces excluded or left open

### Waystone activation — OPEN CLASSIFICATION

Regular Waystone first-use calls the provider activation path, records player activation/discovery, provides feedback and later enables selection.

This is a real player-triggered state transition, but its semantic status is ambiguous between supernatural attunement and network/discovery setup.

It is excluded from the lower bound until that distinction is closed.

### Blank Scroll binding — OPEN CLASSIFICATION

Using a Blank Scroll on a Waystone creates a Bound Scroll carrying that Waystone target.

The action is real and explicit, but it may be item preparation for the already-counted teleport rather than an independent semantic magical action.

Excluded pending classification.

### Warp Plate shard attunement — OPEN CLASSIFICATION

Warp Plate processing can turn an inserted Dormant Shard into an Attuned Shard bound to the plate.

This currently reads as targeting/setup infrastructure and is excluded pending final classification.

### Epitaph / Fleeting Memorial — EXCLUDED PASSIVE PROC

Epitaph processing occurs on player death. The handler consumes the item and spawns the memorial without a discrete player-invoked cast/action at that moment.

Contribution: **+0**.

### Waystone modifier effects — EXCLUDED DOWNSTREAM EFFECTS

Configured modifier effects are applied as consequences of provider teleport settlement.

Contribution: **+0**.

### UI / registry / worldgen / bridge state — EXCLUDED INFRASTRUCTURE

- Waystone destination registries/indexes;
- visibility and ownership metadata;
- menu/list construction;
- worldgen;
- JourneyMap/Dynmap/BlueMap markers;
- Waystones:Sable coordinate transformation;
- cooldown/cost bookkeeping.

Contribution: **+0**.

## Reachability boundary

Exact source proves the three positive action identities, but effective pack policy is still server-configurable.

The inspected source exposes configurable warp requirements, costs, cooldowns, durability, inventory-button mode, teleport deny lists, visibility and modifier policy.

No deployed config values are inferred from source defaults.

## Source-version closure

Repository history directly contains:

- version commit for 21.1.44;
- subsequent changes;
- exact commit `c540cfdb...` setting version 21.1.45.

A direct compare from the 21.1.44 version commit to the 21.1.45 version commit changes only the changelog, `PlayerWaystoneManager`, and version metadata. This gives a bounded exact 21.1.45 source line for the semantics audited here.

## Clean-room / license

The exact source license is **All Rights Reserved**.

The audit retains only factual identities, version metadata, behavior-level causal relationships and provider authority boundaries required for cataloging/interoperability.

No source implementation body or asset is reused.

## Result

- physical 21.1.45 identity: **closed**;
- exact-version source checkpoint: **closed**;
- Waystone Warp / Teleport root: **1**;
- Warp Portal Conjuration root: **1**;
- Twinbound Link root: **1**;
- semantic lower bound: **3**;
- activation/binding/attunement classification: **open**;
- Epitaph passive proc: **excluded**;
- modifier effects: **excluded downstream consequences**;
- strict contribution: **+0**;
- status: **⚠️**.