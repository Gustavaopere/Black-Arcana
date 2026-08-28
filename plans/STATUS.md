# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. Branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline.

Stage 02 Arcana Core is ✅ complete, verified and merged. Canonical branch run `33169091342` and post-merge run `33169344809` both passed the full pipeline.

Stage 03 Integration Layer is ✅ complete, verified and merged at `359dff669bdb9fe45c4db326668057ff4e28f725`. Canonical branch run `33170777944` and post-merge run `33171003791` both passed the full pipeline.

Stage 04 World Safety is ✅ complete, verified and merged at `b5a515335544cee5273ff67d033c68bacf98b05a`. Canonical branch run `33171942536` and post-merge main run `33172216821` both passed the full pipeline.

Stage 05 Casting & UX implementation is merged on `main` at `630db8d57a0703a1231075d68353447b8ce37add`. Branch run `33182063857` and post-merge main run `33182458511` both passed the automated pipeline. The stage remains 🟨 active because its required client visual/input matrix has not yet been manually executed.

Inserted Stage 05A Arcane Danger is the next server/gameplay contract stage. It must freeze backlash, resistance, corruption, strain, hazard snapshots and public provider APIs before Rituals or Spell Domains are canonicalized against dangerous/forbidden content.

Stage 06 Rituals already has substantial preparatory work. `feat/verify-rituals-v8` at `78bab54207965d906c607322417f92b10f6c86a3` passed CI run `33189742674`; `prep/06-rituals` only added architecture/status documentation after that verified functional checkpoint. This work is preserved but is downstream of Stage 05A and must be synchronized/retested after Stage 05A contracts freeze.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | branch + post-merge full CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; canonical full CI green |
| 02 Arcana Core | ✅ Complete | branch `33169091342` + post-merge `33169344809` green |
| 03 Integration Layer | ✅ Complete | merged at `359dff66...`; branch + post-merge CI green |
| 04 World Safety | ✅ Complete | merged at `b5a51533...`; branch + post-merge CI green |
| 05 Casting & UX | 🟨 Active / code merged | automated gates green; manual client QA remains in `docs/qa/casting-ux-manual-matrix.md` |
| 05A Arcane Danger | ⬜ Planned / next contract stage | must precede canonical Rituals/Spell Domains |
| 06 Rituals | 🟦 Preparatory advanced | v8 functional checkpoint CI green; re-sync after 05A freeze required |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`05-casting-ux` remains the formal active stage until its manual client matrix is closed. `05a-arcane-danger` is authorized for isolated preparatory implementation because its server-side contracts do not depend on unresolved visual QA.

## Frozen predecessors

Stages 00, 01, 02, 03 and 04 may only change through explicit follow-up decisions recorded in `DECISIONS.md`.

## Stage 05 remaining closure work

Execute the real-client visual/input matrix in `docs/qa/casting-ux-manual-matrix.md`. Do not rename Stage 05 task files to ✅ until applicable rows are actually exercised. Future-only presentation flags may be carried explicitly to Stage 09 if no corresponding effect exists yet.

## Stage 05A preparatory authorization

Stage 05A may proceed in `prep/05a-arcane-danger` or equivalent isolated implementation branches from the latest green `main`. It may not be declared complete ahead of Stage 05's manual closure, but its deterministic server contracts may be implemented and fully CI-verified now.

Required freeze before downstream canonicalization:
- danger profile/schema and root-cast attribution;
- Arcane/Corruption Resistance provider API and snapshot semantics;
- strain/corruption persistence and recovery rules;
- confirmed-damage/backlash settlement with recursion exclusions;
- Curios/RPG optional-provider contracts;
- client preflight remains presentational only.

## Stage 06 preservation rule

The existing ritual preparatory branch remains valuable and must not be discarded. Because it predates Stage 05A, it is treated as a downstream prototype. After Stage 05A freezes, rebase/merge-sync Rituals onto the new canonical contracts, update hazard-sensitive ritual semantics, rerun the full pipeline, then consider promotion.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- Client input/presentation never becomes authoritative gameplay state.
- All casts terminate in the canonical Stage 02 ingress/channel pipeline.
- World-mutating content remains subject to frozen Stage 04 policy and budgets.
- Stage 05A owns forbidden-magic hazard computation; downstream stages consume it rather than implementing parallel backlash systems.
- Stage 06/07 content is not canonicalized ahead of unresolved Stage 05 closure and Stage 05A contract freeze.
