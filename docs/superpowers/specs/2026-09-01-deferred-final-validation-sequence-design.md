# Deferred Final Validation Stage Sequence

Date: 2026-09-01
Status: approved design, pending implementation plan
Scope: project governance and stage-promotion sequencing only

## 1. Purpose

Black Arcana currently has an unresolved real-client acceptance gate in Stage 05 Casting & UX and Stage 05A presentation acceptance. That gate is legitimate, but the project owner cannot execute real-client testing now and has explicitly chosen to finish all remaining implementation plans before running the accumulated final validation.

This design changes the sequencing rule so unresolved manual/final validation does not stop downstream implementation work. It does **not** weaken any acceptance criterion, convert any PENDING row to PASS, or allow the project to claim release readiness without evidence.

The implementation order remains causal:

`05/05A contracts -> 06 Rituals -> 07 Spell Domains -> 08 Progression & Balance -> 09 Hardening & Release infrastructure -> accumulated final validation`

The difference is that downstream implementation and stage-local automated verification may proceed while the deferred real-client/final validation ledger remains open.

## 2. Non-goals

This change does not:

- redesign any Stage 06-09 gameplay mechanic;
- change server authority, transaction, hazard, world-safety, or provider contracts;
- waive Stage 05/05A real-client requirements;
- treat CI, GameTests, screenshots, fixture availability, or static inspection as substitutes for real-client evidence;
- permit a release while release-blocking rows remain unverified;
- invent optional-provider behavior when the actual provider API/runtime is unavailable;
- allow task files to be renamed to `✅-*` unless their own documented acceptance criteria are genuinely verified and the implementation is merged;
- permit Stage 09 release completion before the final validation phase.

## 3. Canonical state model

The project needs to distinguish implementation progress from final validation progress. The following states are canonical for Stages 05-09:

### 3.1 `IMPLEMENTATION ACTIVE`

Code/design work for the stage is still incomplete.

### 3.2 `IMPLEMENTED / AUTOMATED GATES GREEN`

The intended runtime/configuration/infrastructure is present and the applicable deterministic automated checks pass. This state does not imply real-client or real-modpack validation.

### 3.3 `IMPLEMENTED / FINAL VALIDATION DEFERRED`

The stage has no known implementation work remaining, but one or more acceptance items explicitly require later real-client, real-modpack, representative performance, upgrade-fixture, compatibility, or release-head validation.

This is the normal terminal state for work that cannot be honestly closed before the final validation phase.

### 3.4 `VALIDATED / COMPLETE`

All stage-local acceptance criteria are supported by direct evidence, applicable CI/tests are green, and the stage implementation is merged to `main`. Only then may its task files use the existing `✅-*` completion convention.

### 3.5 `RELEASE BLOCKED`

Used for Stage 09 while implementation/harness work is ready but release-blocking validation remains open. A built JAR is not release completion.

## 4. Promotion rule

The previous practical rule treated unresolved Stage 05 manual QA as a hard blocker for canonicalizing Stage 06 and later work. The new rule is:

> An unresolved manual/final-validation item blocks **validation/release claims**, but does not block downstream implementation or merge when all causal runtime contracts required by that downstream stage are frozen, the downstream change is independently reviewable, and its applicable automated gates are green.

Consequences:

1. Stage 05 and Stage 05A remain open with their real-client rows unchanged.
2. Stage 06 may be resynchronized to the latest `main`, verified against the frozen 05A contracts, and merged.
3. Stage 07 then moves onto the resulting latest `main`, not onto a stale preparatory branch.
4. Stage 08 begins only after Stage 07's implementation contracts are canonical on `main`.
5. Stage 09 implementation/hardening infrastructure begins only after Stage 08 implementation is canonical.
6. Final integrated/manual/release validation runs after implementation work is exhausted.

This policy changes sequencing, not truth conditions.

## 5. Branch and PR strategy

Use sequential, stage-scoped integration rather than one large stacked release branch.

### Stage 06

- Start from the latest `main`.
- Reuse/transplant only the intended Stage 06 work from PR #21 / `feat/stage-06-rituals-mainline`.
- Resolve divergence against current Stage 05A/CI infrastructure explicitly.
- Do not regress the exact-SHA QA artifact path or any current hazard/presentation contract.
- Run the full automated pipeline required by the repository.
- Merge only after branch/PR CI is green and the diff is Stage 06-scoped plus necessary synchronization/documentation.

### Stage 07

- After Stage 06 merges, resynchronize the Stage 07 work onto the new `main`.
- Preserve completed 07.01-07.03 behavior only after verifying it against the new base.
- Finish 07.04-07.07 domain-by-domain with TDD and bounded server-authoritative contracts.
- Avoid carrying stale branch ancestry merely to preserve history; preserve behavior/evidence, not obsolete merge topology.
- Merge Stage 07 only after its applicable automated gates are green.

### Stage 08

- Create from the then-current `main` after Stage 07.
- Implement progression/unlock persistence, RPG gates/mastery, quantitative budget infrastructure, caps/diminishing returns, exploit controls, and server presets.
- Where acceptance depends on representative real-pack tuning, record `FINAL VALIDATION DEFERRED` rather than inventing benchmark evidence.

### Stage 09

- Create from the then-current `main` after Stage 08.
- Implement/complete the executable test matrix, performance instrumentation and thresholds, dedicated-server/multiplayer abuse harnesses, migration fixtures, release/provenance validators, packaging checks, and release documentation infrastructure.
- Stage 09 remains `RELEASE BLOCKED` until the accumulated final validation is actually executed on the exact release candidate HEAD.

## 6. Stage-specific closure semantics

### 6.1 Stage 05 / 05A

No manual matrix row changes state without direct observation. Existing deterministic fixtures and exact-SHA CI artifact delivery remain support infrastructure only.

Stage 05/05A may coexist with downstream merged implementation while remaining `IMPLEMENTED / FINAL VALIDATION DEFERRED`.

### 6.2 Stage 06 Rituals

Stage-local acceptance is based on its documented transactional ritual behavior, provider bridges, world/progression safety, interruption/restart recovery, and applicable automated integration coverage.

If all Stage 06 criteria are genuinely automated and verified, Stage 06 may reach `VALIDATED / COMPLETE` even while Stage 05 manual UX remains deferred, because the upstream manual presentation gate is not evidence about ritual runtime correctness.

If any Stage 06 criterion actually requires real-client/provider-host evidence not available in CI, Stage 06 instead stops at `IMPLEMENTED / FINAL VALIDATION DEFERRED`.

### 6.3 Stage 07 Spell Domains

Each domain keeps its own documented acceptance. Deterministic server behavior must be tested during implementation; optional-provider visual/in-game compatibility that cannot be proven in the repository's CI is deferred explicitly.

No spell/domain is declared fully validated merely because a synthetic adapter test passes when its acceptance requires a real host runtime.

### 6.4 Stage 08 Progression & Balance

Core equations, caps, persistence, gates, anti-spam rules, presets, malformed-input behavior, and deterministic budget calculations are implemented/tested now.

Representative modpack comparison and final numerical tuning that require real progression points or real gameplay remain part of accumulated final validation. Quantitative values must be traceable to a budget rationale even before final tuning.

### 6.5 Stage 09 Hardening & Release

Implementation of test/profiling/migration/provenance infrastructure proceeds now. Execution-dependent acceptance stays open.

The release checklist cannot be completed until the exact release candidate has:

- clean CI/build/test evidence;
- dedicated-server evidence;
- required real-client/real-pack rows;
- representative performance evidence;
- upgrade/migration evidence;
- exact dependency/version review;
- final provenance/license review;
- packaged notice verification;
- documented incompatibilities and release notes.

## 7. Forbidden Domains architecture default

For Stage 07.06, the implementation default is a bounded localized in-world field/arena, not a dynamically-created dimension/instance.

Rationale:

- avoids dynamic-dimension lifecycle and save-format complexity;
- reduces stranded-player recovery risk;
- avoids orphan dimension/chunk state;
- reuses existing world border, protection, loaded-chunk, teleport recovery, and `WorldEffectPolicy` contracts;
- is easier to bound by radius, duration, entity count, and restoration budget.

A temporary isolated dimension may be reconsidered only through a separate explicit architectural decision supported by a concrete requirement that the in-world model cannot satisfy. It is not part of the default Stage 07 implementation.

## 8. Error handling and fail-closed rules

The sequence change must not relax existing failure semantics.

- Optional integrations remain fail-closed/safe when absent or incompatible.
- No client-authored value becomes authoritative.
- Stale downstream branches are not merged wholesale when their base no longer matches canonical contracts.
- Synchronization conflicts are resolved by preserving current `main` authority first, then reapplying downstream intent.
- Missing real-client evidence results in `FINAL VALIDATION DEFERRED`, never inferred PASS.
- Missing representative performance evidence results in an open Stage 09 row, never an optimization claim.
- Unknown provenance/permission remains release-blocking.

## 9. Testing policy during implementation

"Test later" means deferring the final integrated/manual/release campaign. It does **not** mean deferring deterministic engineering tests required to build safely.

During Stages 06-09 implementation, continue to use:

- TDD for deterministic behavior;
- unit/codec/config tests;
- GameTests for world/entity/lifecycle behavior;
- networking/authority tests;
- dedicated-server smoke;
- CI build/JAR verification;
- malformed input, boundary, idempotency, replay, dedupe, and concurrency tests where applicable.

Deferred until the final campaign are only checks that genuinely need the real client, actual modpack/provider hosts, representative gameplay/performance environment, prior-world fixtures not yet available, or exact release-candidate review.

## 10. Documentation updates required by implementation

The first implementation step after this design is approved must update canonical governance files so later sessions cannot accidentally reintroduce the old gate interpretation:

- `plans/README.md` — branch/promotion policy and completion semantics;
- `plans/DECISIONS.md` — add a durable architectural decision recording deferred final validation and sequential downstream promotion;
- `plans/STATUS.md` — record Stage 05/05A as final-validation-deferred while allowing Stage 06 implementation promotion;
- `plans/PENDING.md` — keep unresolved architectural/external unknowns, but remove wording that incorrectly treats manual Stage 05 acceptance as a universal implementation blocker if present;
- affected PR descriptions (#21/#22 or their replacement PRs) — reflect the new promotion rule and actual base/head state.

No Stage 05 manual evidence file is rewritten to manufacture completion.

## 11. Success criteria for this sequencing change

The sequencing change is correctly implemented when:

1. Canonical governance explicitly distinguishes implementation completion from final validation.
2. Stage 05/05A manual rows remain truthful and open.
3. Stage 06 can be integrated from latest `main` without weakening 05A contracts.
4. Stage 07 proceeds only after Stage 06 is canonical and is resynchronized to the resulting latest `main`.
5. Stage 08 proceeds only after Stage 07 implementation is canonical.
6. Stage 09 infrastructure proceeds only after Stage 08 implementation is canonical.
7. Every merge still requires the repository's applicable automated CI to be green.
8. No stage or release is called validated/complete when its own acceptance evidence is still missing.
9. The final validation campaign remains a single explicit release-blocking phase after implementation work is exhausted.

## 12. Implementation decomposition

This design is intentionally an umbrella governance design. Implementation is decomposed into sequential subprojects:

1. Governance update + Stage 06 resynchronization/promotion.
2. Stage 07 resynchronization + completion of 07.04-07.07.
3. Stage 08 implementation.
4. Stage 09 hardening/release infrastructure implementation.
5. Final accumulated validation and release closeout.

Each subproject must use the existing stage plans as its feature specification and must not silently expand scope into the next stage before the current stage's implementation merge is complete.
