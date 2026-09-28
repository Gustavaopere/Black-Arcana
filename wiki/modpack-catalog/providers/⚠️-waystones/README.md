# Waystones — 21.1.45

Status: `⚠️ PARTIAL / PHYSICAL IDENTITY CLOSED / EXACT-VERSION SOURCE PIN / LOWER_BOUND 3 DISCRETE SUPERNATURAL PLAYER ACTIONS / SETUP-ACTION CLASSIFICATION OPEN / +0 STRICT`

## Current physical authority

- sibling checkpoint: `neoforge-rpg-skilltree@7c9d0e9552e33531d0d6b46b86c9de86d3b233bf`;
- physical row: `#564`;
- JAR: `waystones-neoforge-1.21.1-21.1.45.jar`;
- mod id: `waystones`;
- runtime: `21.1.45`;
- physical SHA-1: `6ec1a176a102212db4f6391886db52ed103c830f`.

The top-of-dossier physical override to 21.1.45 supersedes the older 21.1.44 narrative retained in the sibling dossier.

## Exact-version source checkpoint

Official repository:

`https://github.com/TwelveIterations/Waystones`

Exact source checkpoint:

`TwelveIterations/Waystones@c540cfdbb9c1d790fbff397beea7c83f0c6f035f`

At this revision, `gradle.properties` declares:

- `mod_id = waystones`;
- `version = 21.1.45`;
- `minecraft_version = 1.21.1`;
- `include_neoforge=true`.

The exact 21.1.45 changelog is the multiplayer activation-crash fix. No source-build ↔ physical-JAR byte equality is claimed.

## Semantic metric boundary

Black Arcana counts one provider-owned semantic magic object for one discrete supernatural player action identity.

It does not count:

- item or block totals;
- GUI/menu surfaces;
- destination registries and indexes;
- visibility/ownership state;
- costs, cooldowns or requirements by themselves;
- ordinary recipes or setup processes by themselves;
- worldgen;
- map markers;
- status effects applied as consequences;
- aliases or multiple trigger surfaces for the same provider-native action;
- bridge behavior from Waystones:Sable or JourneyMap integration.

The same Waystones teleport engine exposed by a block, item, menu, portal, plate or inventory button is therefore one causal action identity, not one identity per surface.

## Lower-bound root 1 — Waystone Warp / Teleport

The exact 21.1.45 source exposes one authoritative teleport pipeline through `WaystonesAPI.tryTeleportAsync(...)`.

Player-facing surfaces that converge on this same provider-native teleport include:

- activated Waystone selection;
- Sharestone selection;
- Portstone selection;
- Warp Stone;
- Warp Scroll;
- Bound Scroll;
- Return Scroll;
- inventory-button targets when configured.

Warp Plate and Warp Portal traversal also settle through the same teleport pipeline, but they do not mint additional semantic identities.

The teleport manager validates the context, requirements, source validity and destination before moving entities and emitting provider teleport events.

Semantic contribution: **1**.

## Lower-bound root 2 — Warp Portal Conjuration

`PortalScrollItem` is not merely another direct-warp item.

The exact selection handler special-cases the Portal Scroll menu: it resolves a target context and invokes the menu's post-selection handler **without calling the teleport pipeline**.

That post-selection handler calls `WarpPortalManager.spawnPortal(...)`, which creates and initializes a temporary portal targeting the chosen Waystone.

Entering the resulting portal later invokes the already-counted Waystone teleport root.

Therefore:

- portal creation is a distinct player-invoked supernatural action;
- later portal traversal is a downstream use of the existing teleport identity, not a fourth root.

Semantic contribution: **1**.

## Lower-bound root 3 — Twinbound Link

`TwinboundFeatherItem` implements an explicit synchronized player action:

- both players actively use Twinbound Feathers;
- each must target the other at close range;
- the action progresses while both maintain the interaction;
- completion writes reciprocal persistent link state between the two feathers;
- the linked partner becomes an eligible dynamic Waystones destination while the linked feather is carried.

The interaction also has its own completion feedback and does not itself execute the normal teleport pipeline.

Under the semantic metric this is a discrete ritual-like supernatural player action rather than a passive item property or GUI alias.

Semantic contribution: **1**.

## Current semantic lower bound

`1 Waystone Warp / Teleport + 1 Warp Portal Conjuration + 1 Twinbound Link = 3`.

Current disposition:

**LOWER_BOUND 3 / +0 STRICT**.

## Surfaces deliberately excluded from the lower bound

### Waystone activation

First interaction with an unactivated Waystone writes player discovery/activation state and presents magical feedback.

It may represent a discrete supernatural attunement action, but it also functions as network-discovery/setup state. The current metric excludes ordinary setup/processes by themselves, so activation remains **classification-open** rather than being added speculatively.

### Blank Scroll binding

Using a Blank Scroll on a Waystone converts it into a Bound Scroll carrying that target.

This is a player action, but its current evidence can be read as item preparation/attunement for the already-counted teleport root. It remains **classification-open**.

### Warp Plate shard attunement

A Dormant Shard placed in a Warp Plate is transformed into an Attuned Shard after provider-managed attunement time.

This is infrastructure/setup for Warp Plate targeting and is not added to the semantic count without a stronger action-identity basis.

### Epitaph / Fleeting Memorial

Epitaph is consumed from inventory on player death and spawns a Fleeting Memorial. It is a death-triggered passive proc, not a player-invoked action under the current metric.

### Waystone modifiers

Poison, blindness, slow falling, fire resistance, wither and cure effects applied by configured Waystone modifiers are downstream consequences of a teleport and do not mint independent action roots.

## Reachability / config boundary

The three lower-bound actions exist in exact 21.1.45 source, but deployed server configuration still controls aspects of practical use:

- warp requirements;
- XP costs;
- cooldowns;
- Warp Stone durability;
- inventory-button mode;
- target eligibility;
- permissions and entity deny lists;
- visibility/ownership;
- modifier enablement.

These runtime policy values do not erase the source identities, but deployed reachability remains separate QA and is not inferred here.

## Ownership boundary

Waystones remains authority for:

- Waystone identity and persistent destination state;
- activation/discovery state;
- target selection;
- teleport validation and settlement;
- warp requirements/cost/cooldown policy;
- Warp Plate and Warp Portal state;
- Twinbound destination state.

Waystones:Sable may translate provider teleports through moving/sublevel coordinates but does not mint a second teleport identity.

JourneyMap integrations are presentation/marker surfaces and do not own teleport state.

Black Arcana must not create a parallel Waystones destination registry or bypass provider validation when integrating with these actions.

RPG Skill Tree remains sibling authority only for progression, attributes, Mastery, perks and gates through verified contracts.

## Clean-room / license note

The audited source declares **All Rights Reserved**.

Black Arcana uses the source only for factual interoperability/catalog evidence: version metadata, public type/registry identities, causal action boundaries and observable provider contracts.

No upstream implementation body, text, model, texture, sound or other asset is copied or adapted.

## Closure gate

Promote Waystones beyond `LOWER_BOUND 3 / +0 STRICT` only after:

1. Waystone activation is classified as either semantic action or setup/network state;
2. Blank Scroll binding is classified as either semantic attunement action or item preparation;
3. Warp Plate shard attunement is classified under the same metric;
4. the complete exact 21.1.45 player-action surface is rechecked for any additional independent causal roots;
5. aliases and alternate trigger surfaces remain deduplicated to the provider-native action they settle;
6. deployed config/reachability is captured if strict promotion requires active current-pack eligibility.

Runtime teleport behavior, multiplayer, Sable coordinate transforms, persistence and JourneyMap presentation remain separate QA.

## Result

**⚠️ Partial — exact-version source lower bound 3.**

Countable lower bound:

- **1** Waystone Warp / Teleport root;
- **1** Warp Portal Conjuration root;
- **1** Twinbound Link root.

Explicitly not counted:

- alternate teleport surfaces;
- Waystone activation pending classification;
- Blank Scroll binding pending classification;
- shard attunement pending classification;
- Epitaph death proc;
- modifier status effects;
- worldgen, GUI, destination indexes, markers and bridges.

Strict global delta: **+0** until the remaining action/setup classifications and any required deployed reachability are closed.
