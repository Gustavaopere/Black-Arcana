# Black Arcana — Status

Last updated: 2026-08-29

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. Branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline.

Stage 02 Arcana Core is ✅ complete, verified and merged. Canonical branch run `33169091342` and post-merge run `33169344809` both passed the full pipeline.

Stage 03 Integration Layer is ✅ complete, verified and merged at `359dff669bdb9fe45c4db326668057ff4e28f725`. Canonical branch run `33170777944` and post-merge run `33171003791` both passed the full pipeline.

Stage 04 World Safety is ✅ complete, verified and merged at `b5a515335544cee5273ff67d033c68bacf98b05a`. Canonical branch run `33171942536` and post-merge main run `33172216821` both passed the full pipeline.

Stage 05 Casting & UX implementation is merged on `main` at `630db8d57a0703a1231075d68353447b8ce37add`. Branch run `33182063857` and post-merge main run `33182458511` both passed the automated pipeline. The stage remains 🟨 active because its required real-client visual/input matrix in `docs/qa/casting-ux-manual-matrix.md` has not yet been manually executed. All current applicable rows remain explicitly `PENDING`.

Inserted Stage 05A Arcane Danger now has its server/gameplay implementation and contracts frozen on `main` through PR #20. The current Stage 05A main checkpoint is `07263ae9bad12eba6ed500992991faa36ad598b2`; post-merge workflow run `33277492248` (#512) passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTests and dedicated-server smoke. Stage 05A must not be reopened implicitly by downstream stages; changes require an explicit follow-up decision.

Stage 06 Rituals has now been re-synchronized from the historical preparatory branch onto the frozen Stage 05A contracts in PR #21 (`feat/stage-06-rituals-mainline`). Functional checkpoint `26c11072b041981e02265377382b5e568e54a79a` passed workflow run `33277837831` (#521) in full: JUnit, diff sanity, NeoForge build, JAR inspection, GameTests and dedicated-server smoke. The PR is mergeable, but Stage 06 remains 🟦 promotion-ready / blocked because project ordering explicitly forbids merging Stage 06 ahead of Stage 05 manual client QA.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | branch + post-merge full CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; canonical full CI green |
| 02 Arcana Core | ✅ Complete | branch `33169091342` + post-merge `33169344809` green |
| 03 Integration Layer | ✅ Complete | merged at `359dff66...`; branch + post-merge CI green |
| 04 World Safety | ✅ Complete | merged at `b5a51533...`; branch + post-merge CI green |
| 05 Casting & UX | 🟨 Active / code merged | automated gates green; real-client manual matrix remains open |
| 05A Arcane Danger | ✅ Server contracts frozen | implementation merged through #20; post-merge #512 full green |
| 06 Rituals | 🟦 Promotion-ready / blocked | re-synced in #21; functional #521 full green; merge waits for Stage 05 manual QA |
| 07 Spell Domains | 🟦 Preparatory | downstream non-canonical work must consume frozen 05A contracts |
| 08 Progression & Balance | 🟦 Preparatory | downstream non-canonical work must consume frozen 05A contracts |
| 09 Hardening & Release | ⬜ Not started | final closure after predecessor stages |

## Canonical active stage

`05-casting-ux` remains the formal active stage until its real-client visual/input matrix is closed. Stage 05A server contracts are frozen and may be consumed by downstream preparatory work, but their completion does not bypass the Stage 05 manual gate.

## Frozen predecessors

Stages 00, 01, 02, 03, 04 and the Stage 05A server/gameplay contracts may only change through explicit follow-up decisions recorded in `DECISIONS.md` or an equivalent reviewed correction.

## Stage 05 remaining closure work

Execute the real-client visual/input matrix in `docs/qa/casting-ux-manual-matrix.md`. Do not rename Stage 05 task files to ✅ until applicable rows are actually exercised. Future-only presentation flags may be carried explicitly to Stage 09 if no corresponding effect exists yet.

## Stage 05A frozen contract

The frozen Stage 05A contract now includes:
- authoritative danger profiles/schema and root-cast attribution;
- immutable Arcane Resistance and Corruption Resistance snapshots with bounded provider registries;
- standard equipment and optional Curios snapshot providers;
- explicit equipment-set identities and deterministic cumulative set thresholds;
- RPG Skill Tree resistance integration through the public provider model;
- corruption and strain acquisition/persistence/recovery services;
- confirmed post-mitigation damage settlement and dedicated non-recursive Arcane Backlash;
- delayed/offline backlash persistence with frozen causal and emergency-protection context;
- transactional emergency backlash protection with bounded persistent cooldown state;
- authoritative server preflight publication for HUD/radial presentation;
- hardening for duplicate settlement, late damage, restart/relog, optional-provider absence and bounded state.

Zero Arcane Resistance retains exact deterministic 1:1 settlement for eligible confirmed damage under the canonical dangerous/forbidden profile. `ARCANE_BACKLASH` remains a terminal dedicated damage family and never re-enters the eligible damage ledger.

## Stage 06 re-synchronization

The stale `prep/06-rituals` branch was not merged directly because it diverged substantially from current `main`. PR #21 instead promotes its Stage 06-specific contracts from a fresh branch based on `07263ae9bad12eba6ed500992991faa36ad598b2` and manually reconciles shared runtime/persistence files so Stage 05A hazard state is preserved.

The synchronized implementation includes:
- bounded ritual definitions, sessions, activation/replay guard and exactly-once completion ledger;
- validate-before-consume and transactional component reservation/commit/refund semantics;
- bounded ritual tick processing with no implicit chunk-force-load contract;
- active ritual-session persistence merged into the current hazard-aware `BlackArcanaSavedData`;
- production Eidolon anchor-attunement ritual registration through the supported host API;
- Malum typed spirit component requirements and transactional consumption;
- representative Black Arcana grand ritual with loaded-dimension/chunk checks and durable duplicate-reward prevention;
- restart coverage proving an already committed ritual does not consume components twice.

Functional checkpoint `26c11072b041981e02265377382b5e568e54a79a` is full-CI GREEN in run `33277837831` (#521).

## Stage 06 promotion gate

Do not rename Stage 06 task files to ✅ and do not merge PR #21 while Stage 05's required real-client QA remains unresolved. Once the applicable Stage 05 rows are actually exercised and recorded, re-run the final PR head if necessary and only then promote Stage 06 to `main`.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- Client input/presentation never becomes authoritative gameplay state.
- All casts terminate in the canonical Stage 02 ingress/channel pipeline.
- World-mutating content remains subject to frozen Stage 04 policy and budgets.
- Stage 05A owns forbidden-magic hazard computation; downstream stages consume it rather than implementing parallel backlash systems.
- Stage 06/07 content may be prepared against frozen predecessors, but Stage 06 is not canonicalized ahead of unresolved Stage 05 manual closure.
