# Ars Sable 1.1.2

Status: `EXACT SOURCE-PINNED 1.1.2 / SPATIAL BRIDGE CATALOGED / CURRENT SABLE 2.0.5 RUNTIME QA OPEN`

## Installed identity

Physical modlist authority:

- JAR: `ars_sable-1.21.1-1.1.2.jar`;
- mod id: `ars_sable`;
- version: `1.1.2`;
- SHA-1: `df43ad58fb9ca3b7acf7f62dc97ed75fd6da3da8`;
- CurseForge hash: `2760241931`.

Current physical hosts:

- Ars Nouveau `5.13.1`;
- Sable `2.0.5`, JAR `sable-neoforge-1.21.1-2.0.5.jar`, SHA-1 `05f666e973d32baaaf405acb9bbed6615b909971`.

## Exact source checkpoint

Official source: `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba`.

The commit is explicitly `1.1.2`. Its source declares:

- Minecraft `1.21.1`, runtime range `[1.20.6,1.21.2)`;
- NeoForge build `21.1.219`, runtime range `[21,)`;
- Ars Nouveau build `5.11.7.1354`, runtime range `[5.11.7,)`;
- Sable build `1.2.2`, runtime range `[1.0,)`;
- LGPLv3;
- mixin config `ars_sable.mixins.json`.

The current pack is inside the declared open dependency ranges, but the Sable runtime has moved from build target `1.2.2` to `2.0.5`. Because Ars Sable directly mixes into both Ars and Sable internals, loader acceptance is not evidence of binary/behavioral compatibility.

## Provider role

Ars Sable is a **spatial compatibility bridge**, not an independent magic provider. It adapts Ars Nouveau systems to Sable sublevels/physical spaces by projecting positions, tracking moved targets and reconnecting Ars-owned systems after assembly/disassembly.

Exact 1.1.2 source registers DeferredRegisters for blocks, block entities and items but leaves `onBlockItemsRegistry()` empty and contains no gameplay block/item registration. No provider-owned spell, glyph, ritual, mana pool, Source pool or physics engine is registered.

## Major adapted surfaces

- Source Jar / Ars SourceManager visibility from moving sublevels;
- Storage/Crafting Lectern position tracking and item-handler cache rebinding;
- Bookwyrm and selected Ars automation entity tracking/pathfinding;
- Mob Jar;
- Planarium / dimension-boundary links;
- Ars Warp Portal, Warp Scroll and Stable Warp Scroll destination projection;
- flying items and follow projectiles;
- scrying/camera tracking;
- particles and BlockPos helpers;
- client rendering for Arcane Pedestal, Mob Jar and Planarium;
- Sable assembly/sublevel lifecycle.

## Authority boundary

- Ars Nouveau remains authority for spells, Source, Source Jars, Storage Lectern, portals/warp semantics, Planarium and Ars entities.
- Sable remains authority for sublevels, physical-space containment/projection and assembly lifecycle.
- Ars Sable owns only the adapter/tracking metadata needed to preserve those systems across Sable geometry.
- Black Arcana must not create a second Source balance, second spatial projection ledger, second warp settlement or second moving-storage address map for these provider systems.
- BA-owned spatial magic remains server-authoritative and independently subject to Stage 07.04 destination validation and `WorldEffectPolicy` where world mutation occurs.

## Current-host gate

Sable `2.0.5` is substantially newer than the exact build target `1.2.2`. All direct Sable helper/event/mixin assumptions are runtime QA gates. Missing/changed hooks must fail closed; thematic similarity does not create a safe adapter contract.
