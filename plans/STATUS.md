# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. Branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline. All 53 observable reference rows and 32 candidate specifications are frozen inputs for later content stages.

Stage 02 Arcana Core is ✅ complete, verified and merged. Canonical branch run `33169091342` and post-merge run `33169344809` both passed the full pipeline. The five Stage 02 tasks are frozen contracts.

Stage 03 Integration Layer is ✅ complete, verified and merged at `359dff669bdb9fe45c4db326668057ff4e28f725`. Canonical branch run `33170777944` and post-merge run `33171003791` both passed the full pipeline. Its six task files are frozen.

Stage 04 World Safety is ✅ complete, verified and merged at `b5a515335544cee5273ff67d033c68bacf98b05a`. Canonical branch run `33171942536` and post-merge main run `33172216821` both passed the full pipeline.

Stage 05 Casting & UX implementation is merged on `main` at `630db8d57a0703a1231075d68353447b8ce37add`. Branch run `33182063857` and post-merge main run `33182458511` both passed unit tests, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke. The stage remains 🟨 active because its required client visual/input matrix has not yet been manually executed.

Stage 06 Rituals is **preparatory-complete and full-CI GREEN** on `prep/06-rituals`. Source checkpoint `78bab54207965d906c607322417f92b10f6c86a3` was verified by `feat/verify-rituals-v8`, workflow run `33189742674`; unit tests, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke all passed. The branch is stacked linearly on the current Stage 05 main baseline. It remains non-canonical solely because Stage 05 manual client QA is still open.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | branch + post-merge full CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; canonical full CI green |
| 02 Arcana Core | ✅ Complete | branch `33169091342` + post-merge `33169344809` green |
| 03 Integration Layer | ✅ Complete | merged at `359dff66...`; branch `33170777944` + post-merge `33171003791` green |
| 04 World Safety | ✅ Complete | merged at `b5a51533...`; branch `33171942536` + post-merge `33172216821` green |
| 05 Casting & UX | 🟨 Active / code merged | automated gates green; manual client QA remains in `docs/qa/casting-ux-manual-matrix.md` |
| 06 Rituals | 🟦 Preparatory complete / CI green | v8 run `33189742674` full green; canonical merge blocked only by Stage 05 ordering gate |
| 07 Spell Domains | ⬜ Not started | may proceed only as stacked preparatory work until Stages 05–06 are canonical |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`05-casting-ux`

## Frozen predecessors

Stages 00, 01, 02, 03 and 04 may only change through explicit follow-up decisions recorded in `DECISIONS.md`.

## Stage 05 merged implementation

- rebindable radial/cast/quick-slot key mappings, with quick slots unbound by default to reduce pack conflicts;
- server-validated persistent loadout editing over bounded C2S/S2C payloads;
- client-only radial selector whose selection is separate from cast execution;
- direct selected-slot and quick-slot casting that still terminates in the canonical server ingress pipeline;
- contextual HUD for selected spell and authoritative cast denial/success feedback, with no permanent resource bar;
- CLIENT-only NeoForge config for HUD visibility/scale/anchor, feedback density, radial hold/toggle behavior, particle-density preference and reduced-motion/flash preferences;
- explicit client cache clearing on disconnect to prevent stale same-UUID reconnect state;
- dedicated-server smoke remains green after all client-only code was packaged.

## Stage 05 remaining closure work

Execute the real-client visual/input matrix in `docs/qa/casting-ux-manual-matrix.md`. Do not rename Stage 05 task files to ✅ until applicable rows are actually exercised. Future-only presentation flags (particle density, reduced motion/flashes) may be carried explicitly to Stage 09 if no corresponding effect exists yet.

## Stage 06 preparatory checkpoint

Implemented and automatically verified on `prep/06-rituals`:
- bounded ritual identity, anchor, definition and activation contracts;
- exactly-once duplicate/concurrency guards and active-session indexing;
- transactional component reservation/commit/refund and composite providers;
- persistent active sessions and persistent completion/reward ledger;
- production Eidolon anchor-attunement ritual through the supported ritual host path;
- typed Malum spirit requirements and transactional ritual component consumption;
- representative Black Arcana grand ritual for mechanics that should remain in the Black Arcana engine;
- runtime bootstrap/persistence wiring without global tick scans or chunk-force-load requirements;
- automated tests for core lifecycle, registry/completion semantics, persistence, Malum integration and grand-ritual component binding.

Architecture/evidence checkpoint: `docs/architecture/rituals-preparatory.md`.

## Stage 06 promotion gate

Stage 06 task files remain unrenamed and the branch remains unmerged until Stage 05 manual client QA closes. Once Stage 05 is frozen, canonicalize Stage 06 from the latest accepted preparatory checkpoint, rerun the full pipeline and merge only after it is green again.

## Preparatory next work

Stage 07 may proceed as a stacked isolated preparatory branch from the verified Stage 06 checkpoint. It must not be declared canonical or merged ahead of Stages 05 and 06.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- Client input/presentation never becomes authoritative gameplay state.
- All Stage 05 casts terminate in the canonical Stage 02 ingress/channel pipeline.
- World-mutating content remains subject to frozen Stage 04 policy and budgets.
- Stage 06 preparatory work cannot be promoted ahead of unresolved Stage 05 closure.
- Stage 07 preparatory work cannot be promoted ahead of Stages 05 and 06.
