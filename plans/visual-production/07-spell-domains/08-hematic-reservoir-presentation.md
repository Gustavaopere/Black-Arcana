# 07.08 — Hematic Reservoir Presentation

## State

`DEFERRED VISUAL PRODUCTION / RUNTIME PLAN SEPARATE`

Runtime structure, controller state, fluid transactions, binding, persistence and sync fields are authoritative in `plans/07-spell-domains/08-hematic-reservoirs-vampiric-sustenance.md`.

This file owns only the player-facing reservoir/UI/asset requirements extracted from the mixed plan.

## Player-facing form

The Black Arcana reservoir is an original open-basin/cistern multiblock intended to support visually deep pools, reservoirs and lake-like constructions without requiring a wall of individual Create tanks.

“Tinkers-style smeltery/furnace” is conceptual inspiration for the idea of a large constructed multiblock only. Do not copy Tinkers code, assets, block models, text, sounds, recipes, geometry or implementation.

For v1, a “blood lake” is only the appearance of a deliberately formed, bounded Black Arcana reservoir. Natural terrain-wide lakes and arbitrary flood-fill presentation are out of scope.

## Asset surfaces

Visual production may require original:

- Hematic Reservoir Controller model/texture/readability treatment;
- casing and/or glass family when needed for structure readability;
- blood interior/surface rendering driven by controller state;
- icons and inspection/UI treatment for source kind, bound state and reserve state;
- transfer/refill feedback;
- optional VFX, animation and audio after art direction is explicitly scheduled.

Exact texture resolution, palette, model topology, shader choice, particles, animation and sound are intentionally not invented here. Those details are deferred to the visual-production lane and reusable pipeline constraints from `minecraft-mod-factory`.

## Server-derived visual state

The visible blood surface is derived from the authoritative controller's synchronized state. It is not an independent fluid inventory and must never become drainable client/world `FluidState` authority.

Required presentation states include:

- low/high or otherwise readable fill representation derived from current/capacity;
- formed vs invalid reservoir state where the final UI needs it;
- bound/unbound/stale/unloaded source status;
- safe source display kind without exposing provider-internal mutable objects;
- current Hematic Reserve/capacity;
- refill result split into thirst contribution vs reserve contribution when the server permits that information;
- server-authored failure reason for stale/unloaded/unsupported/provider-unavailable sources.

The visual layer must not recompute transfer validity, thirst acceptance, capacity authority or source identity.

## Structure readability

An original casing/glass family is optional, not automatically required. Compatible wall/floor blocks may remain data/tag driven when runtime validation allows them. Visual design should make controller identity and formed-volume/fill state readable without requiring every valid structural block to become a bespoke Black Arcana asset.

Geometry/occlusion choices must not imply structural validity that the server has rejected.

## UI/HUD boundary

Hematic Reserve is a Blood-domain buffer, not a global Black Arcana mana pool. Presentation must not introduce a permanent universal mana bar or imply that unrelated spells consume the reserve.

Sync is event-driven under D023. Do not design the UI around per-tick full reservoir snapshots.

## QA

When this lane resumes, real-client acceptance should verify:

- fill presentation tracks server state and survives reload/reconnect without stale authority;
- invalid/stale/unloaded sources are visually distinguishable without fabricating validity;
- low/high fill and capacity remain readable at supported GUI scales/layouts;
- assembled Create/Vampirism presentation does not duplicate provider-owned resource UI unnecessarily;
- dedicated-server classloading remains unaffected by visual-only classes/assets;
- no visual surface can mutate or debit authoritative fluid state.

Historical mixed source is preserved at `plans/visual-production/_migration-source/07-spell-domains/08-hematic-reservoirs-vampiric-sustenance.pre-extraction.md`.