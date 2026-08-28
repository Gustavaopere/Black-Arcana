# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Stage 00 Foundation remains implemented but **verification-blocked** on `round-1-foundation` HEAD `3d4b9e24361e5ca3ed8cdcebeeb116abe7361c00`. Workflow run `33126490920` was retried again in this session; the retry created job `98730674669`, which again completed `failure` with `steps=null`. Therefore no Gradle/NeoForge/GameTest/dedicated-server command executed.

Stage 01 Reference Catalog is specification-complete only in `prep/01-reference-catalog` HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`: 53/53 reference rows classified, 32 candidates specified, runtime host baselines pinned and per-candidate host viability/probe routes documented. It is not canonical or frozen.

Stage 02 Arcana Core is implementation-advanced only in `prep/02-arcana-core`. Verification branch `feat/verify-arcana-core-v4` was frozen from clean preparatory SHA `5ce4a5b4ea9dde41538c72cd5a4da6b1c760361e`. Workflow run `33135172255` created job `98733413416`, which again completed `failure` with `steps=null`; no repository step executed. Stage 02 therefore remains preparatory despite its broad implementation coverage.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | HEAD `3d4b9e24361e5ca3ed8cdcebeeb116abe7361c00`; retry job `98730674669` still received no executable steps |
| 01 Reference Catalog | 🟦 Preparatory complete | HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`; awaiting canonical rebase/review |
| 02 Arcana Core | 🟨 Preparatory advanced | v4 verification run `33135172255`, job `98733413416`: `steps=null`; remaining closure is real-runner evidence plus restart/logout/chunk-boundary/transport tests |
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
- validated cooldown/charge group rename migrations applied after restore and before pruning, with conservative collision semantics;
- server-fact targeting for SELF, ENTITY, PROJECTILE, BLOCK, RAY, SPHERE, CONE, CYLINDER and LINKED, with typed target references, explicit geometry, loaded-chunk preflight and server-owned linked sets;
- bounded follow-up work scheduler connected to the real server tick plus `ScheduledArcanaEffect` admission/failure behavior;
- canonical spell registry plus atomically replaceable presentation metadata catalog;
- per-server runtime lifecycle and Overworld `SavedData` persistence with defensive restore ceilings;
- NeoForge 1.21.1 payload registration and bounded C2S/S2C codecs;
- centralized protocol string/list ceilings, with duplicate cooldown/presentation snapshot keys rejected at the protocol boundary;
- server ingress rate limiting and canonical request construction;
- strict datapack reload listener under `data/<namespace>/black_arcana/spells/*.json`, with datapack identifiers constrained to the same bounds as network synchronization;
- presentation/cooldown sync on login, metadata reload and successful cast only;
- JUnit source for target geometry, linked-target normalization, migration order, dimension invariance, overflow boundaries and all four packet codec round-trips;
- GameTest source for the no-optional-mod core path and cooldown denial on immediate recast;
- GameTest source for NBT round-trip of persistent cooldown and loadout state;
- real Minecraft GameTest source for loaded entity targeting, range rejection and LOS rejection through `ServerEntityTargetSelector`;
- real Minecraft GameTest source for scoreboard-team friendly-fire policy and player death without cooldown reset.

Detailed implementation/pending audit: `docs/architecture/arcana-core-preparatory.md`.

## Stage 02 still open

- execute all JUnit, packet codec, GameTest and dedicated-server gates in a real runner;
- add dedicated chunk-boundary targeting GameTest where chunk lifecycle can be controlled without force-loading;
- prove persistence across actual server restart and logout; death is now GameTest-covered and dimension invariance is unit-covered;
- bind each future expensive content/world effect to the live bounded scheduler as that content is implemented;
- run malformed/spam transport-level tests where the dedicated harness permits packet injection;
- extend the authoritative data schema with balance parameters only after Stage 08 defines the canonical bounded model.

## Canonical promotion order

`Stage 00 verified -> merge main -> Stage 01 rebase/review/merge -> Stage 02 rebase/review/verification -> merge main`.

No preparatory branch may skip this order, and no task receives ✅ before its actual acceptance gates are met.
