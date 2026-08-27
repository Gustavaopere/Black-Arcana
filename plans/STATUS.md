# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Stage 00 Foundation remains implemented but **verification-blocked** on `round-1-foundation` HEAD `e843d35789a7a30be16da8348e7daf06f604cdea`. Repeated Linux and macOS GitHub-hosted jobs have terminated with no assigned runner and zero steps, so no Gradle/NeoForge/GameTest command has executed remotely.

Stage 01 Reference Catalog is specification-complete only in `prep/01-reference-catalog` HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`: 53/53 reference rows classified, 32 candidates specified, runtime host baselines pinned and per-candidate host viability/probe routes documented. It is not canonical or frozen.

Stage 02 Arcana Core is now advancing only in `prep/02-arcana-core`. Pure Black Arcana infrastructure that does not require optional magic mods is being prepared while the canonical gate is blocked. This does not change the merge order.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | 🟨 Verification blocked | HEAD `e843d35789a7a30be16da8348e7daf06f604cdea`; hosted jobs still receive no runner/steps |
| 01 Reference Catalog | 🟦 Preparatory complete | HEAD `d2450eeb972758dbd5b3880553461c86fd79d301`; awaiting canonical rebase/review |
| 02 Arcana Core | 🟨 Preparatory implementation | Pure-Java cast/replay/cost/cooldown/target/runtime/registry/network contracts implemented; NeoForge/SavedData/runtime gates still open |
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

The current Actions failures do not satisfy or fail those gates because the jobs report no runner and no steps.

## Stage 02 preparatory checkpoint

Implemented on `prep/02-arcana-core`:
- `ArcanaCastId`, canonical request validation seam and bounded replay protection;
- composite transactional cost provider with reverse rollback;
- shared/persistent cooldown model and snapshot/restore;
- server-fact target policy with absolute range/target caps;
- bounded follow-up work scheduler;
- canonical compiled spell registry with spoof protection;
- atomic schema-v1 metadata catalog;
- versioned/bounded cast-result/cooldown/presentation payload contracts;
- bounded ingress rate limiting.

Detailed implementation/pending audit: `docs/architecture/arcana-core-preparatory.md`.

## Stage 02 still open

- actual loadout resolution and charge/channel lifecycle;
- percent-of-max costs and creative/admin payment policy;
- Minecraft target collection/raycast/area adapters;
- SavedData cooldown persistence and canonical persistent clock;
- charge pools;
- NeoForge payload registration/codecs/handlers;
- datapack reload listener/codec bridge;
- real Gradle, GameTest and dedicated-server execution.

## Canonical promotion order

`Stage 00 verified -> merge main -> Stage 01 rebase/review/merge -> Stage 02 rebase/review/verification -> merge main`.

No preparatory branch may skip this order, and no task receives ✅ before its actual acceptance gates are met.