# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Stage 00 Foundation remains implemented but **verification-blocked** on `round-1-foundation` HEAD `3d4b9e24361e5ca3ed8cdcebeeb116abe7361c00`. The fresh post-incident workflow run `33126490920` again terminated without executable job steps; therefore no Gradle/NeoForge/GameTest/dedicated-server command executed.

Stage 01 Reference Catalog is specification-complete only in `prep/01-reference-catalog` HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`: 53/53 reference rows classified, 32 candidates specified, runtime host baselines pinned and per-candidate host viability/probe routes documented. It is not canonical or frozen.

Stage 02 Arcana Core is advancing only in `prep/02-arcana-core`. The branch now includes the real NeoForge 1.21.1 networking/reload/persistence bridges, bounded protocol invariants and a channel/charge execution hook that converges on the canonical cast engine, but remains preparatory until Stages 00 and 01 are promoted in order.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | HEAD `3d4b9e24361e5ca3ed8cdcebeeb116abe7361c00`; fresh hosted job still received no executable steps |
| 01 Reference Catalog | 🟦 Preparatory complete | HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`; awaiting canonical rebase/review |
| 02 Arcana Core | 🟨 Preparatory advanced | Runtime, SavedData, payload registration, strict datapack metadata reload, event-driven sync, canonical channel release and dedicated GameTest sources implemented; runtime verification still blocked |
| 03 Integration Layer | ⬜ Not started | Iron's, Ars, Eidolon, Malum, RPG adapters |
| 04 World Safety | ⬜ Not started | Destruction policy, rollback, budgets |
| 05 Casting & UX | ⬜ Not started | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`00-foundation`

## Foundation gate

Required before `main` moves:
1. Gradle unit tests execute.
2. NeoForge build and JAR inspection pass.
3. GameTest server executes successfully.
4. Dedicated-server smoke reaches normal startup and Black Arcana load marker.

The current Actions failures do not satisfy or fail those gates because the jobs report no executable steps. `main` therefore remains intentionally unchanged.

## Stage 02 preparatory checkpoint

Implemented on `prep/02-arcana-core`:
- unique cast identity, server-owned canonical spell/loadout validation and bounded replay protection;
- transactional/composite costs with flat/percent-of-max models and explicit creative/admin policy;
- channel lifecycle integrated into `ArcanaServerRuntime`: server-owned begin/cancel/release, bounded channel duration, preserved loadout identity and exactly-once release through the same `ArcanaCastEngine` as immediate casts;
- shared/persistent cooldowns, charge pools, bounded UI snapshots, snapshot/restore and orphan-group pruning;
- server-fact targeting with bounded multi-target resolution, a real SELF/ENTITY Minecraft adapter and no chunk force-loading;
- bounded follow-up work scheduler;
- canonical spell registry plus atomically replaceable presentation metadata catalog;
- per-server runtime lifecycle and Overworld `SavedData` persistence with defensive restore ceilings;
- NeoForge 1.21.1 payload registration and bounded C2S/S2C codecs;
- centralized protocol string/list ceilings, with duplicate cooldown/presentation snapshot keys rejected at the protocol boundary;
- server ingress rate limiting and canonical request construction;
- strict datapack reload listener under `data/<namespace>/black_arcana/spells/*.json`, with datapack identifiers constrained to the same bounds as network synchronization;
- presentation/cooldown sync on login, metadata reload and successful cast only;
- dedicated GameTest source for the no-optional-mod core path and cooldown denial on immediate recast;
- dedicated GameTest source for NBT round-trip of persistent cooldown and loadout state.

Detailed implementation/pending audit: `docs/architecture/arcana-core-preparatory.md`.

## Stage 02 still open

- execute all JUnit, packet codec, GameTest and dedicated-server gates in a real runner;
- add real Minecraft bridges for ray/block/cone/sphere/cylinder/projectile/linked targets as required by content;
- bind actual expensive world/effect producers to the bounded scheduler;
- prove persistence across actual restart/death/logout/dimension changes;
- add explicit ID rename migration for cooldown/charge groups when a real rename exists;
- extend the authoritative data schema with balance parameters only after Stage 08 defines the canonical bounded model;
- run malformed/spam transport-level tests where the dedicated harness supports them.

## Canonical promotion order

`Stage 00 verified -> merge main -> Stage 01 rebase/review/merge -> Stage 02 rebase/review/verification -> merge main`.

No preparatory branch may skip this order, and no task receives ✅ before its actual acceptance gates are met.
