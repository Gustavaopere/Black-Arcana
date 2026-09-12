# Phase 2AB — Ars Sable 1.1.2 checkpoint

Status: `SOURCE CATALOG COMPLETE / CURRENT-HOST RUNTIME QA DEFERRED / CI NOT YET STARTED`

Execution branch: `docs/magic-catalog-phase2ab-ars-sable`
Base main at phase start: `ede7dc310499ec21941504e8e6754d4f7c7f512e`
Physical JAR: `ars_sable-1.21.1-1.1.2.jar`
Physical mod id/version: `ars_sable` / `1.1.2`
Physical SHA-1: `df43ad58fb9ca3b7acf7f62dc97ed75fd6da3da8`
Physical CurseForge hash: `2760241931`
Physical Sable host: `sable-neoforge-1.21.1-2.0.5.jar`, mod id `sable`, version `2.0.5`, SHA-1 `05f666e973d32baaaf405acb9bbed6615b909971`
Exact source: `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba`

## Exact catalog closed

- exact physical identities/hashes for Ars Sable and current Sable host;
- exact official source pin matching version 1.1.2;
- dependency ranges and build pins;
- exact classification as spatial infrastructure bridge rather than spell/content provider;
- no gameplay block/item/spell/glyph/ritual registration in exact source;
- 24 common + 5 client mixins;
- network registrar protocol `2` with zero provider-owned payload registrations;
- Source Jar and Ars SourceManager position bridge;
- persistent Storage Lectern spatial tracking/rebinding;
- Warp Portal same/cross-dimension projection and client position consistency;
- Warp/Stable Warp target tracking;
- Planarium assembly persistence;
- selected Ars entity/logistics/pathfinding adapters;
- Mob Jar, camera/scrying and render boundaries;
- four upstream GameTest classes inventoried;
- 1.1.2 changelog fixes recorded;
- clean-room provenance and Black Arcana authority consequences.

## Current-host risk

Exact build target uses Sable `1.2.2`; physical pack uses Sable `2.0.5`. Although metadata accepts `[1.0,)`, the provider has 29 direct mixin points plus Sable API/event/helper dependencies. Current-host compatibility remains unproven until runtime validation.

Ars Nouveau also moved from build `5.11.7.1354` to physical `5.13.1`; all Ars mixin targets remain part of the runtime gate.

## Deferred validation

- client + dedicated-server startup;
- all mixin applications;
- Source exactly-once behavior through movement/reload;
- storage handler/cache/tracking lifecycle;
- Warp/Stable Warp/Portal + unloaded target;
- Planarium assembly/disassembly/restart;
- Bookwyrm/Whirlisprig/Wixie/pathfinding;
- projectiles/flying items/Mob Jar;
- scrying/camera/render;
- save/reload/chunk unload/restart;
- interop with other Sable compatibility mods in the physical pack.

## Merge protocol

Before merge:

1. re-fetch `main`;
2. reconcile semantically if it advanced;
3. verify diff remains catalog-only;
4. run fresh CI on reconciled exact HEAD;
5. require clear review threads;
6. merge only with exact expected head SHA;
7. confirm final `main` SHA.

Phase 2AB is documentation/catalog work only and does not promote any Black Arcana runtime Stage.
