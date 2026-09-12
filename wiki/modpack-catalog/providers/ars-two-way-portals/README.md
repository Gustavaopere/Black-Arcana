# Ars Nouveau: Two-Way Portals 2.0.0

Status: `EXACT RELEASE CATALOGED / PUBLIC SOURCE IS 1.3.4 BASELINE / 2.0.0 BINARY QA OPEN`

## Installed identity

- mod id: `ars_two_way_portals`;
- JAR: `ars_two_way_portals-2.0.0.jar`;
- version: `2.0.0`;
- physical SHA-1: `233846fc30667893c5f36a719da576d5eed43f5c`;
- physical CurseForge hash: `683033210`;
- CurseForge exact file: `8515817`, NeoForge 1.21.1, 2026-07-26;
- publisher license: LGPLv3.

## Evidence tiers

### Tier A — exact installed/release evidence

The physical modlist plus publisher file/project page establish the installed identity and the documented 2.0.0 feature surface.

### Tier B — public source baseline only

`Astrologic-Git/ars-nouveau-two-way-portals@f4b2e2e1fef99284968cfa99fc405ead7f56efbf` is explicitly release source for **1.3.4 on Minecraft 1.20.1 Forge**. It is useful to understand provider architecture but is not an exact source pin for the installed 2.0.0 NeoForge port.

## Provider role and authority

Ars Nouveau owns Stable Warp Scrolls, PortalBlock/PortalTile and its warp primitives. Two-Way Portals adds pair-specific behavior around those primitives. When its optional seamless mode is active, Immersive Portals owns the actual portal entity/engine semantics.

Black Arcana must not:

- create a second pair registry for the same provider portals;
- perform another teleport after provider settlement;
- own the provider cooldown;
- replay endpoint destruction/nullification;
- bind a BA integration to 1.3.4 mixin internals as though they were a stable 2.0.0 API;
- weaken BA `WorldEffectPolicy` because another provider mutates portal frames.

## Exact 2.0.0/project-described features

- Double-Sided Stable Warp Scroll creates permanent linked two-way portals from matching Source Stone frames.
- Vertical and horizontal frames are supported, including cross-dimension links.
- Optional Immersive Portals mode: normal throw creates seamless mode when available; sneaking creates regular Ars portal mode according to the publisher description.
- Regular portals have a three-second re-entry cooldown.
- Dominion Wand can rotate symmetrical portal pairs; normal/shift interaction controls gravity transformation according to the publisher page.
- Portal Nullify Scroll destroys one side of a two-way portal rather than the whole pair.
- Ordinary tracked-frame break removes the linked pair according to the publisher description.
- Crafting a configured Double-Sided Stable Warp Scroll alone clears its stored coordinates.
- 1.21.1-specific note: old Silk Touch frame replacement is replaced by Ars Nouveau Weave blocks.

The project page still contains older generic text mentioning Leap/Silk Touch/Break+Extract replacement; that conflict is recorded and not resolved by guessing implementation details.

## Public 1.3.4 baseline inventory

- exactly 2 stack-size-1 provider items;
- 3 provider recipes;
- 7 common mixins;
- bounded connected-portal traversal (`MAX_PORTAL_BLOCKS = 1024`);
- ephemeral pending pair transaction keyed by thrown item entity UUID;
- regular pair identity stored on Ars PortalTile persistent data;
- 60-tick successful-player teleport cooldown;
- one-endpoint nullification;
- ordinary pair teardown;
- optional Immersive conversion/frame validation/rotation hooks.

See the provider subdocuments for the strict exact-release vs baseline distinction.

## Current optional-provider mismatch requiring QA

Physical modlist contains Immersive Portals via `Immersive-Aeronautics1.1.4-1.21.1-NeoForge.jar`, top-level mod id `immersive_portals_core`, version 6.0.7. The old public baseline checks `immersive_portals` and targets older `qouteall.imm_ptl` APIs. The installed 2.0.0 port may have adapted this, but without exact binary/source inspection Phase 2Z does not assert it.

## Classification

This provider contributes **portal infrastructure/items**, not a new spell school and not provider-owned production glyphs in the public baseline. It remains magic-relevant because it materially changes Ars warp behavior and directly overlaps Black Arcana Space & Displacement design space.
