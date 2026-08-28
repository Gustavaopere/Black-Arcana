# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation remains implemented but **verification-blocked** on `round-1-foundation` HEAD `3d4b9e24361e5ca3ed8cdcebeeb116abe7361c00`. Its latest retry job completed with `steps=null`, so no Gradle/NeoForge/GameTest/dedicated-server command executed.

Stage 01 Reference Catalog is specification-complete only in `prep/01-reference-catalog` HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`: 53/53 reference rows classified, 32 candidates specified, runtime host baselines pinned and per-candidate host viability/probe routes documented. It is not canonical or frozen.

Stage 02 Arcana Core is implementation-advanced only in `prep/02-arcana-core`. Verification branch `feat/verify-arcana-core-v4` was frozen from clean preparatory SHA `5ce4a5b4ea9dde41538c72cd5a4da6b1c760361e`; its workflow again produced a failed job with `steps=null`, so no repository command executed.

Stage 03 Integration Layer is implementation-advanced on `prep/03-integration-layer`. Iron's, Ars, Malum, Eidolon and RPG adapters/fallback descriptors are present. Ars uses installed-first baseline `5.13.0`; Malum uses discrete typed spirit transactions; Eidolon uses the public 1.21.1 ritual registry with a conditionally loaded non-destructive probe ritual; RPG progression/mastery is reflection-isolated. Source-level tests cover resource transactions, synthetic cast/cooldown behavior, Eidolon descriptor/recipe contracts and unavailable-provider semantics.

Verification v2 froze source checkpoint `e545db4d345eb69633a393b08b14431f06913298` into `feat/verify-integration-layer-v2`; marker commit `faa20ed876295b92e7d25ce3e6ceea17bd66f28b` triggered workflow run `33140112220`. Job `98748844646` completed `failure` with `steps=null`, and the job-log endpoint returned no log blob. The workflow therefore failed before checkout or any repository command executed.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | runner jobs have returned no executable steps |
| 01 Reference Catalog | 🟦 Preparatory complete | HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`; awaiting canonical rebase/review |
| 02 Arcana Core | 🟨 Preparatory advanced | broad core implementation present; real-runner evidence still missing |
| 03 Integration Layer | 🟨 Preparatory advanced | v2 run `33140112220`, job `98748844646`: `steps=null`; source checkpoint remains preparatory |
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

A workflow failure with no executable steps neither satisfies nor meaningfully fails these gates. `main` therefore remains intentionally unchanged until a runner actually executes them.

## Stage 03 preparatory checkpoint

Implemented on `prep/03-integration-layer`:
- optional provider loading is gated by NeoForge mod presence and provider-specific entrypoints;
- missing providers are explicit `MISSING_MOD` descriptors rather than absent registry entries;
- API/linkage failures become `API_INCOMPATIBLE` and advertise no capabilities;
- Iron's integration uses its addon-facing API classifier;
- Ars mana transactions and synthetic spell acceptance path use installed-first baseline `5.13.0`;
- Malum spirits are bounded discrete inventory resources with rollback protection;
- Eidolon `RITUAL_HOST` is backed by public `Ritual`/`RitualRegistry` API and a conditional `ritual_brazier` probe recipe;
- Eidolon descriptor classloading is provider-free; the binary registry probe stays in the optional bootstrap path;
- RPG progression/mastery bridge probes the private project's exact binary method surface and uses dynamic mastery lane `black_arcana:casting`;
- optional dependencies are metadata-optional and ordered `AFTER`;
- preparatory audit is recorded in `docs/architecture/integration-layer-preparatory.md`.

## Stage 03 still open

- execute JUnit/build/GameTest/dedicated-server gates in a real runner;
- boot representative installed-provider profiles for Iron's, Ars, Eidolon and Malum;
- rebase/canonicalize only after Stages 00, 01 and 02 are promoted in order.

## Canonical promotion order

`Stage 00 verified -> merge main -> Stage 01 rebase/review/merge -> Stage 02 rebase/review/verification -> merge main -> Stage 03 rebase/verification -> merge main`.

No preparatory branch may skip this order, and no task receives ✅ before its actual acceptance gates are met.
