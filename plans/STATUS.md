# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. Branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline. All 53 observable reference rows and 32 candidate specifications are frozen inputs for later content stages.

Stage 02 Arcana Core is ✅ complete, verified and merged. Canonical branch run `33169091342` and post-merge run `33169344809` both passed the full pipeline. The five Stage 02 tasks are frozen contracts.

Stage 03 Integration Layer is ✅ complete, verified and merged at `359dff669bdb9fe45c4db326668057ff4e28f725`. Canonical branch run `33170777944` and post-merge run `33171003791` both passed unit tests, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke. Its six task files are frozen.

Stage 04 World Safety is ✅ complete, verified and merged at `b5a515335544cee5273ff67d033c68bacf98b05a`. Canonical branch run `33171942536` and post-merge main run `33172216821` both passed unit tests, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 05 Casting & UX is now the canonical active stage.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | branch + post-merge full CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; canonical full CI green |
| 02 Arcana Core | ✅ Complete | branch `33169091342` + post-merge `33169344809` green |
| 03 Integration Layer | ✅ Complete | merged at `359dff66...`; branch `33170777944` + post-merge `33171003791` green |
| 04 World Safety | ✅ Complete | merged at `b5a51533...`; branch `33171942536` + post-merge `33172216821` green |
| 05 Casting & UX | 🟨 Active | Direct cast, loadouts, radial selection, contextual HUD and accessibility |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`05-casting-ux`

## Frozen predecessors

Stages 00, 01, 02, 03 and 04 may only change through explicit follow-up decisions recorded in `DECISIONS.md`.

Stage 04 frozen outputs include:
- central `WorldEffectPolicy` modes `OFF`, `COSMETIC`, `TEMPORARY`, `LIMITED` and `FULL`;
- fail-closed per-spell world-effect profiles and overrides that can only restrict the global ceiling;
- bounded world-effect admission, chunk and work budgets with no arbitrary chunk force-loading;
- transactional temporary block mutation with compare-and-set restoration and persisted rollback state;
- Minecraft backend using loaded-chunk checks, full BlockState serialization and block-entity refusal by default;
- server-derived PvP, team, invulnerability and boss facts with boss-specific caps rather than blanket immunity;
- fail-closed protection-adapter registry and protected-destination guard;
- unit/GameTest coverage for policy modes, budgets, rollback, restart persistence, PvP/allies/bosses/protected destinations and external edits.

## Immediate next actions

1. Create `feat/05-casting-ux` from latest `main`.
2. Implement configurable client input and server-validated loadout selection without introducing a parallel cast path.
3. Build a client-only radial selector with explicit selection separate from cast execution.
4. Add contextual cooldown/cost/channel/denial feedback with no permanent resource HUD by default.
5. Add accessibility/client preferences that only reduce presentation and never alter authoritative gameplay state.
6. Run full canonical CI and manual/client UX matrix before Stage 05 receives ✅.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- No Stage 05 task receives ✅ until canonical implementation passes its acceptance gates and merge.
- Client input/presentation never becomes authoritative gameplay state.
- All Stage 05 casts must terminate in the canonical Stage 02 ingress/channel pipeline.
- World-mutating content remains subject to frozen Stage 04 policy and budgets.
