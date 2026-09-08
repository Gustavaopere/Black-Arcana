# Phase 2Q — Ars Additions 21.3.0 checkpoint

State: `IN PROGRESS`

## Base

Phase 2Q starts from `main@f9c3854bc7e5b2f1bd051434080f13ae3c7d5e5d`, the Phase 2P Ars Nouveau merge. Exact-SHA post-merge workflow `34184788813` completed green across unit tests, diff sanity, NeoForge build, JAR verification, Foundation GameTests, dedicated-server smoke and main artifact publication before Phase 2Q work began.

Concurrent work was checked before provider selection. No existing Ars Additions catalog branch was found and no open magic-catalog PR owns this provider; current Stage 07.07 runtime work remains separate and is not modified by this documentation stream.

## Exact installed provider

- JAR: `ars_additions-1.21.1-21.3.0.jar`;
- mod id: `ars_additions`;
- runtime metadata: `1.21.1-21.3.0`;
- physical SHA-1: `ce2440b606acb20b79a42bf7c6c24d163c93241f`;
- CurseForge project/file: `974408` / `7646325`.

## Source/provenance checkpoint

Factual source audit is pinned to `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`, whose `version` file is exactly `21.3.0`. Root license is GNU LGPL v3. No upstream code or assets are copied/adapted into Black Arcana.

The publisher's version-labelled source checkpoint and CurseForge release share version/date, but physical-JAR↔commit byte equivalence is not claimed without stronger artifact provenance.

## First closed registry surfaces

- Ars spell parts: 3/3 identified and individually source-cataloged;
- rituals: 2/2 identified and individually source-cataloged;
- perks: 1/1 identified;
- mob effects: 1/1 registry identity identified.

## Remaining Phase 2Q work

- granular charm 12/12 behavior/acquisition;
- exact item/block registry normalization;
- recipes, data components, attachments and tag modifiers;
- Warp Nexus/Index, Ender Source Jar, Source Spawner, Wixie Enchanting, Haversack/Wayfinder/Memory Crystal and related stateful systems;
- acquisition/worldgen/structure/config surfaces;
- capability-matrix and provider-queue delta;
- root provenance/third-party overlay as appropriate;
- final branch synchronization, CI and merge gate.

No Black Arcana runtime Stage is changed by this checkpoint.
