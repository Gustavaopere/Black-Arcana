# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation remains implemented but **verification-blocked** on `round-1-foundation` HEAD `3d4b9e24361e5ca3ed8cdcebeeb116abe7361c00`. Its latest retry job completed with `steps=null`, so no Gradle/NeoForge/GameTest/dedicated-server command executed.

Stage 01 Reference Catalog is specification-complete only in `prep/01-reference-catalog` HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`: 53/53 reference rows classified, 32 candidates specified, runtime host baselines pinned and per-candidate host viability/probe routes documented. It is not canonical or frozen.

Stage 02 Arcana Core is implementation-advanced only in `prep/02-arcana-core`. Verification branch `feat/verify-arcana-core-v4` was frozen from clean preparatory SHA `5ce4a5b4ea9dde41538c72cd5a4da6b1c760361e`; its workflow again produced a failed job with `steps=null`, so no repository command executed.

Stage 03 Integration Layer is implementation-advanced on `prep/03-integration-layer`. Iron's, Ars, Malum, Eidolon and RPG adapters/fallback descriptors are present. Ars uses installed-first baseline `5.13.0`; Malum uses discrete typed spirit transactions; Eidolon uses the public 1.21.1 ritual registry with a conditionally loaded non-destructive probe ritual; RPG progression/mastery is reflection-isolated. Verification v2 run `33140112220`, job `98748844646`, again ended with `steps=null` and no job log.

Stage 04 World Safety is implementation-advanced on `prep/04-world-safety` checkpoint `6e1571c3bc1dbf5abe9216815f1875fc95f181b1`. The branch now contains centralized world-effect modes/profiles, cumulative per-cast budgets, no-force-load chunk admission, persistent temporary block rollback with a real Minecraft backend, entity/PvP/boss/protection semantics, protected-destination guards, unit stress tests and GameTests for mutation/restoration/persistence/entity safety. Verification v3 run `33143669024`, job `98759917906`, completed `failure` with `steps=null`; no checkout or repository command executed.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | runner jobs have returned no executable steps |
| 01 Reference Catalog | 🟦 Preparatory complete | HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`; awaiting canonical rebase/review |
| 02 Arcana Core | 🟨 Preparatory advanced | broad core implementation present; real-runner evidence still missing |
| 03 Integration Layer | 🟨 Preparatory advanced | v2 run `33140112220`, job `98748844646`: `steps=null` |
| 04 World Safety | 🟨 Preparatory advanced | checkpoint `6e1571c3...`; v3 run `33143669024`, job `98759917906`: `steps=null` |
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

A workflow failure with no executable steps neither satisfies nor meaningfully fails these gates. `main` therefore remains intentionally unchanged until a runner actually executes them.

## Stage 04 preparatory checkpoint

Implemented on `prep/04-world-safety`:
- global `OFF / COSMETIC / TEMPORARY / LIMITED / FULL` world-effect policy with fail-closed per-spell profiles;
- server overrides can only restrict the global mode/caps, never silently elevate them;
- cumulative bounded work ledger per cast plus the existing bounded per-tick scheduler;
- loaded-chunk admission contracts that intentionally expose no chunk-loading/ticket operation;
- provider-neutral claim/protection adapter registry that fails closed on adapter exceptions;
- server-derived PvP/team/boss/invulnerability facts and explicit boss caps instead of accidental immunity/trivialization;
- protected-destination guard for displacement/teleport style mechanics;
- temporary world-mutation tracker storing dimension, position, owner, cast, original state, replacement state and expiry;
- temporary mutations persisted through global Overworld `SavedData` with defensive restore ceilings;
- real `MinecraftTemporaryBlockBackend` using already-loaded chunks, full BlockState NBT serialization, compare-and-set writes, no block-entity mutation and suppressed drops;
- restoration processor wired to the live server tick with bounded checks and fail-closed backend error handling;
- rollback never overwrites later player/world edits because restoration requires the Black Arcana replacement to still be present;
- unit tests for modes, policies, budgets, chunk guards, protection adapters, temporary mutation overlap/rollback/persistence and scheduler ceilings;
- GameTests for real Minecraft temporary mutation/CAS/block-entity denial, expiry restoration, player-edit preservation, NBT restart round-trip, PvP, alliances, bosses, invulnerability and protected/unloaded destinations;
- architecture audit recorded in `docs/architecture/world-safety-preparatory.md`.

## Stage 04 still open

- execute JUnit/build/GameTest/dedicated-server gates in a real runner;
- perform an actual process restart smoke proving an expired pending mutation is restored from disk rather than only NBT round-trip;
- exercise real chunk unload/reload timing where the harness can guarantee chunk lifecycle without force-loading;
- bind concrete destructive spell implementations to these services as Stage 07 content is implemented;
- rebase/canonicalize only after Stages 00–03 are promoted in order.

## Canonical promotion order

`Stage 00 verified -> merge main -> Stage 01 rebase/review/merge -> Stage 02 rebase/review/verification -> merge main -> Stage 03 rebase/verification -> merge main -> Stage 04 rebase/verification -> merge main`.

No preparatory branch may skip this order, and no task receives ✅ before its actual acceptance gates are met.
