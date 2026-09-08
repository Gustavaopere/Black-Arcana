# Phase 2Z — Ars Nouveau: Two-Way Portals 2.0.0 checkpoint

Status: `CATALOG COMPLETE TO AVAILABLE EVIDENCE / PRE-CI MAIN SYNC COMPLETE / CI PENDING / EXACT 2.0.0 JAR EXTRACTION + CURRENT-HOST QA DEFERRED`

Execution branch: `docs/magic-catalog-phase2z-two-way-portals`
Base main at phase start: `5b343dbb91ff15a08ca3a09d1e4ca9ac177b3dd2`
Pre-CI reconciled main: `ede7dc310499ec21941504e8e6754d4f7c7f512e`
Pre-CI relation: `0 behind`; exact delta remains confined to eight new files under `wiki/modpack-catalog/**`.
Physical JAR: `ars_two_way_portals-2.0.0.jar`
Physical mod id/version: `ars_two_way_portals` / `2.0.0`
Physical SHA-1: `233846fc30667893c5f36a719da576d5eed43f5c`
Physical CurseForge hash: `683033210`
Exact release file: CurseForge file `8515817`, 1.21.1 NeoForge, uploaded 2026-07-26, 65.8 KB
Public source baseline: `Astrologic-Git/ars-nouveau-two-way-portals@f4b2e2e1fef99284968cfa99fc405ead7f56efbf` — **1.3.4 / Minecraft 1.20.1 Forge**, not exact 2.0.0 source.

## Critical source/release distinction

The publisher links the public GitHub repository as Source, but its current public history/tree exposes only the 1.3.4 Forge 1.20.1 release source. The installed 2.0.0 NeoForge 1.21.1 file is independently verified on CurseForge, but its exact source/bytecode was not available through the permitted retrieval path in this phase.

Therefore:

- exact 2.0.0 claims come only from physical JAR metadata/hash and the publisher's 2.0.0/project description;
- implementation-level formulas/classes/mixins/recipes are labeled **1.3.4 PUBLIC SOURCE BASELINE** unless independently confirmed by exact 2.0.0 evidence;
- source continuity is useful for architecture/deduplication but is not promoted to exact 2.0.0 API compatibility;
- installed runtime remains fail-closed for any detail not confirmed by exact release evidence.

## Exact installed/release facts closed

- physical JAR/mod id/version/hash;
- exact CurseForge 2.0.0 release identity and 1.21.1 NeoForge classification;
- client + server environment and LGPLv3 publisher license;
- two-way permanent linked portal feature;
- matching frame requirement;
- vertical/horizontal and cross-dimension support;
- optional Immersive Portals mode: normal throw uses seamless mode when available; sneaking selects traditional Ars mode according to publisher description;
- regular portal three-second re-entry cooldown;
- Dominion Wand normal/shift rotation modes;
- Portal Nullify Scroll removes one side according to publisher description;
- configured Double-Sided Stable Warp Scroll can be crafted alone to clear coordinates;
- 1.21.1 release note explicitly says old Silk Touch frame replacement was replaced by Ars Nouveau Weave blocks.

## Public 1.3.4 source baseline closed

- 2 registered stack-size-1 items;
- 3 data recipes;
- 7 declared common mixins;
- 1024-block bound for connected portal inspection/removal;
- pending pair transaction keyed by item-entity UUID;
- regular pair id + partner-dimension/coordinate persistence on PortalTile data;
- successful regular player teleport starts a 60-tick cooldown;
- one-endpoint regular nullification semantics;
- ordinary regular frame break removes both connected endpoints when partner level resolves;
- optional Immersive conversion creates provider-owned portal entities and removes underlying Ars portal blocks;
- baseline Immersive frame validation and Dominion Wand hooks;
- LGPL-3.0-or-later gradle metadata + LGPLv3 root license;
- no provider-owned spell/glyph registration observed in the baseline tree.

## Current physical optional-provider concern

The current pack contains Immersive Portals through `Immersive-Aeronautics1.1.4-1.21.1-NeoForge.jar`, exposing top-level mod id `immersive_portals_core` version 6.0.7, plus True Immersion 2.0.4. The 1.3.4 baseline checks mod id `immersive_portals` and imports older `qouteall.imm_ptl` APIs.

Because exact 2.0.0 source/JAR internals were not extracted, Phase 2Z does **not** infer whether 2.0.0 adapted that gate/API to the current Immersive-Aeronautics packaging. Current optional bridge behavior remains runtime/binary QA.

## Release-page editorial conflict

The project page simultaneously:

1. states that on 1.21.1 the Silk Touch frame replacement function was replaced by Ars Nouveau Weave blocks; and
2. retains older general-description prose saying tracked frames can be replaced with Leap, Silk Touch or Break + Extract.

The explicit 1.21.1 note is treated as the stronger release-specific signal. Exact 2.0.0 frame replacement mixins/config are not reconstructed from the older 1.3.4 source.

## Deferred exact-binary/current-host validation

- extract the physical 2.0.0 JAR and inventory NeoForge metadata, mixins, recipes and classes;
- confirm exact 2.0.0 Ars Nouveau dependency range/build host;
- confirm exact optional Immersive mod-id/API gate under current `immersive_portals_core` 6.0.7;
- confirm 2.0.0 replacement of old Silk Touch/Leap/Break mixin paths by Weave-block semantics;
- verify pair creation/rollback when one frame becomes invalid mid-transaction;
- verify save/reload, chunk unload, server restart and unavailable partner dimension behavior;
- verify regular 3-second cooldown exactly once across multi-block portals;
- verify nullify leaves the opposite endpoint with the documented one-way behavior;
- verify ordinary frame break removes intended endpoints without duplicate drops/mutations;
- verify Dominion rotation/gravity flow under installed gravity/Immersive stack;
- validate no force-loading/global-unbounded scans are introduced in the 2.0.0 port;
- client + dedicated-server + full-pack interop.

These are runtime/binary gates, not missing catalog statements that can be safely inferred from the available public baseline.

## Final gate

- pre-CI synchronization complete against `main@ede7dc310499ec21941504e8e6754d4f7c7f512e`;
- branch confirmed 0 commits behind after semantic merge of concurrent Stage 05.13 plan work;
- exact diff confirmed catalog-only under `wiki/modpack-catalog/**`;
- require fresh CI on the exact HEAD produced by this checkpoint update;
- immediately before merge, fetch `main` again and reconcile/revalidate if it advanced;
- keep PR review threads clear;
- merge only with exact expected head SHA and confirm final main SHA.

Phase 2Z is documentation/catalog work only and does not promote any Black Arcana runtime Stage.
