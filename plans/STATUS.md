# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. Branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline. All 53 observable reference rows and 32 candidate specifications are frozen inputs for later content stages.

Stage 02 Arcana Core is ✅ complete, verified and merged. Canonical branch run `33169091342` and post-merge run `33169344809` both passed the full pipeline. The five Stage 02 tasks are frozen contracts.

Stage 03 Integration Layer is ✅ complete, verified and merged at `359dff669bdb9fe45c4db326668057ff4e28f725`. Canonical branch run `33170777944` and post-merge run `33171003791` both passed unit tests, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke. Its six task files are frozen.

Stage 04 World Safety is now the canonical active stage. Its stacked preparatory implementation has already passed the full pipeline at `212ee9d00fa24f574ba7b7cdb98dc59df83e1a12` via run `33170234798`, but it must be reapplied onto this latest canonical `main` before merge.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | branch + post-merge full CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; canonical full CI green |
| 02 Arcana Core | ✅ Complete | branch `33169091342` + post-merge `33169344809` green |
| 03 Integration Layer | ✅ Complete | merged at `359dff66...`; branch `33170777944` + post-merge `33171003791` green |
| 04 World Safety | 🟨 Active | preparatory SHA `212ee9d...` full-green in `33170234798`; canonical reapplication starts now |
| 05 Casting & UX | ⬜ Not started canonically | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`04-world-safety`

## Frozen predecessors

Stages 00, 01, 02 and 03 may only change through explicit follow-up decisions recorded in `DECISIONS.md`.

Stage 03 frozen outputs include:
- fail-closed optional provider discovery and capability reporting;
- transactional Iron's mana, Ars mana and Malum spirit resource adapters;
- public Eidolon ritual-host bridge with a non-destructive integration probe;
- reflection-isolated RPG progression/mastery adapter with post-success mastery awards;
- optional dependency metadata and provider-specific classloading boundaries;
- no provider absence/API mismatch may silently make a required cost or progression gate free.

## Immediate next actions

1. Create `feat/04-world-safety` from latest `main`.
2. Reapply only Stage 04 world-policy, rollback, budget, protection, persistence and GameTest changes from `prep/04-world-safety`.
3. Preserve all frozen Stage 03 integration contracts and current CI/build fixes.
4. Run full canonical CI.
5. If green, merge Stage 04, run post-merge CI, mark its four tasks ✅ and activate Stage 05.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- No Stage 04 task receives ✅ until canonical implementation passes its acceptance gates and merge.
- Destructive effects must route through Black Arcana world-effect policy and bounded runtime work.
- No world effect may force-load arbitrary chunks.
- Client input/presentation never becomes authoritative gameplay state.
