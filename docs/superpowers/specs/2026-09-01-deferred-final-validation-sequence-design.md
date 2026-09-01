# Deferred Final Validation Stage Sequence

Date: 2026-09-01
Status: in-chat design approved; written-spec review pending before implementation planning
Scope: project governance and stage-promotion sequencing, plus the explicitly approved Stage 07.06 architecture default

## 1. Purpose

Black Arcana has a legitimate unresolved real-client acceptance gate in Stage 05 Casting & UX and Stage 05A presentation acceptance. The project owner cannot execute that real-client testing now and has explicitly chosen to finish the remaining implementation plans before running the accumulated final validation.

This design changes sequencing so unresolved manual/final validation does not stop downstream implementation work. It does **not** weaken acceptance criteria, convert PENDING rows to PASS, or permit release-readiness claims without evidence.

The causal implementation order remains:

`05/05A frozen runtime contracts -> 06 Rituals -> 07 Spell Domains -> 08 Progression & Balance -> 09 Hardening & Release infrastructure -> accumulated final validation`

Downstream implementation and stage-local automated verification may proceed while the deferred real-client/final-validation ledger remains open.

## 2. Scope and non-goals

This change governs promotion and truth states. It does not redesign Stage 06, 07.01-07.05, 07.07, Stage 08, or Stage 09 gameplay semantics. The one explicit gameplay-architecture decision included here is the already approved Stage 07.06 default: bounded localized in-world fields/arenas rather than dynamic dimensions.

This change does not:

- change server authority, transactions, hazards, world safety, or provider ownership;
- waive Stage 05/05A real-client requirements;
- treat CI, GameTests, screenshots, fixtures, or static inspection as substitutes for real-client evidence;
- permit a release while release-blocking rows remain unverified;
- invent optional-provider behavior when the actual provider API/runtime is unavailable;
- allow task files to be renamed to `✅-*` unless their own documented acceptance criteria are genuinely verified and the implementation is merged;
- permit Stage 09 release completion before the final validation phase.

## 3. Canonical state model

Implementation progress and final validation progress are separate facts.

### `IMPLEMENTATION ACTIVE`

Code/design work for the stage is incomplete.

### `IMPLEMENTED / AUTOMATED GATES GREEN`

The intended runtime/configuration/infrastructure is present and applicable deterministic automated checks pass. This does not imply real-client or real-modpack validation.

### `IMPLEMENTED / FINAL VALIDATION DEFERRED`

No known implementation work remains, but one or more acceptance items require later real-client, real-modpack, representative performance, upgrade-fixture, compatibility, or exact-release-head evidence.

### `VALIDATED / COMPLETE`

All stage-local acceptance criteria have direct evidence, applicable CI/tests are green, and the implementation is merged to `main`. Only then may the existing `✅-*` task-file convention be used.

### `RELEASE BLOCKED`

Stage 09 implementation/harness work may be ready while release-blocking validation remains open. A built JAR is never sufficient for release completion.

## 4. Promotion rule

The prior practical rule treated unresolved Stage 05 manual QA as a hard blocker for canonicalizing Stage 06 and later work. Replace it with:

> An unresolved manual/final-validation item blocks **validation and release claims**, but does not block downstream implementation or merge when all causal runtime contracts required by that downstream stage are frozen, the downstream diff is independently reviewable, and its applicable automated gates are green.

Consequences:

1. Stage 05 and Stage 05A remain open with their real-client rows unchanged.
2. Stage 06 may be resynchronized to the latest `main`, verified against frozen 05A contracts, and merged.
3. Stage 07 then moves onto the resulting latest `main` rather than remaining stacked on stale ancestry.
4. Stage 08 begins only after Stage 07 implementation contracts are canonical on `main`.
5. Stage 09 implementation/hardening infrastructure begins only after Stage 08 implementation is canonical.
6. Final integrated/manual/release validation runs after implementation work is exhausted.

This changes sequencing, not truth conditions.

## 5. Merge gate for every implementation stage

A downstream stage may merge only when all of the following are true:

- its diff is scoped to that stage plus necessary synchronization/documentation;
- current `main` authority is preserved when resolving stale-branch conflicts;
- deterministic tests required to build the feature safely have been written and run;
- repository CI is green for the final PR head;
- no unresolved issue requires redesign of an upstream frozen contract;
- documentation records any real-client/real-provider/performance acceptance that remains deferred;
- after merge, `main` is confirmed at the merge SHA and post-merge CI is green when the repository workflow applies.

Manual/final validation is not a promotion prerequisite unless the specific stage's own acceptance criterion genuinely cannot be separated from that evidence.

## 6. Branch and PR strategy

Use sequential, stage-scoped integration rather than one large stacked release branch.

### Stage 06

- Start synchronization from the latest `main`.
- Prefer preserving PR #21 / `feat/stage-06-rituals-mainline` if it can be resynchronized without unsafe history manipulation or accidental regression.
- If #21's divergence makes a clean resync unsafe or unreviewable, create a replacement Stage 06 branch from current `main`, transplant only the intended Stage 06 changes, open a replacement PR, and close #21 with a link/explanation.
- Preserve current Stage 05A hazard/presentation contracts and exact-SHA QA artifact infrastructure.
- Merge only after the Stage 06 merge gate is satisfied.

### Stage 07

- After Stage 06 merges, move Stage 07 onto the new `main`.
- Prefer reusing PR #22 only if its branch can be safely rebased/resynchronized without losing reviewability.
- Otherwise create a replacement Stage 07 branch from the new `main`, transplant verified 07.01-07.03 behavior and current 07.04 work deliberately, then continue 07.04-07.07 there. Close #22 with a link/explanation if replaced.
- Preserve behavior and evidence, not obsolete stacked ancestry.
- Finish 07.04-07.07 domain-by-domain with TDD and bounded server-authoritative contracts.

### Stage 08

- Create from the then-current `main` after Stage 07.
- Implement progression/unlock persistence, RPG gates/mastery, quantitative budget infrastructure, caps/diminishing returns, exploit controls, and server presets.
- Where acceptance depends on representative real-pack tuning, record `FINAL VALIDATION DEFERRED` instead of inventing benchmark evidence.

### Stage 09

- Create from the then-current `main` after Stage 08.
- Implement/complete the executable test matrix, performance instrumentation and regression thresholds, dedicated-server/multiplayer abuse harnesses, migration fixtures, release/provenance validators, packaging checks, and release-documentation infrastructure.
- Stage 09 remains `RELEASE BLOCKED` until accumulated final validation is executed on the exact release-candidate HEAD.

## 7. Stage-specific closure semantics

### Stage 05 / 05A

No manual matrix row changes state without direct observation. Existing deterministic fixtures and exact-SHA CI artifact delivery remain support infrastructure only.

Stage 05/05A may coexist with downstream merged implementation while remaining `IMPLEMENTED / FINAL VALIDATION DEFERRED`.

### Stage 06 Rituals

Stage-local acceptance covers transactional ritual behavior, provider bridges, world/progression safety, interruption/restart recovery, and applicable automated integration coverage.

If all Stage 06 criteria are genuinely verified, Stage 06 may reach `VALIDATED / COMPLETE` while Stage 05 manual UX remains deferred. If any Stage 06 criterion genuinely needs unavailable real-client/provider-host evidence, Stage 06 stops at `IMPLEMENTED / FINAL VALIDATION DEFERRED`.

### Stage 07 Spell Domains

Each domain keeps its documented acceptance. Deterministic server behavior must be tested during implementation. Optional-provider visual/in-game compatibility that cannot be proven in repository CI is deferred explicitly.

A synthetic adapter test does not prove a real host-runtime criterion.

### Stage 08 Progression & Balance

Implement and test core equations, caps, persistence, gates, anti-spam rules, presets, malformed-input behavior, and deterministic budget calculations now.

Representative modpack comparison and final numerical tuning that require real progression points/gameplay remain part of accumulated final validation. Every provisional production value still needs a documented budget rationale.

### Stage 09 Hardening & Release

Implement test/profiling/migration/provenance infrastructure now. Execution-dependent acceptance stays open.

The release checklist remains blocked until the exact release candidate has direct evidence for CI/build/tests, dedicated server, required real-client/real-pack rows, representative performance, upgrades/migrations, dependency/version review, provenance/license review, packaged notices, incompatibilities, and release notes.

## 8. Stage 07.06 Forbidden Domains default

Implement Forbidden Domains as bounded localized in-world fields/arenas by default, not dynamically-created dimensions/instances.

Rationale:

- avoids dynamic-dimension lifecycle and save-format complexity;
- reduces stranded-player recovery risk;
- avoids orphan dimensions/chunks;
- reuses existing world border, protection, loaded-chunk, teleport-recovery, and `WorldEffectPolicy` contracts;
- is easier to bound by radius, duration, entity count, and restoration budget.

A temporary isolated dimension requires a separate explicit architectural decision supported by a concrete requirement the in-world model cannot satisfy.

## 9. Error handling and fail-closed rules

The sequence change does not relax failure semantics.

- Optional integrations remain fail-closed/safe when absent or incompatible.
- No client-authored value becomes authoritative.
- Stale downstream branches are never merged wholesale merely to preserve history.
- Synchronization conflicts preserve current `main` authority first, then reapply downstream intent.
- Missing real-client evidence results in `FINAL VALIDATION DEFERRED`, never inferred PASS.
- Missing representative performance evidence leaves an open Stage 09 row, never an optimization claim.
- Unknown provenance/permission remains release-blocking.

## 10. Testing policy during implementation

"Test later" means deferring the final integrated/manual/release campaign. It does **not** mean deferring deterministic engineering tests required for safe implementation.

During Stages 06-09 continue to use, as applicable:

- TDD for deterministic behavior;
- unit/codec/config tests;
- GameTests for world/entity/lifecycle behavior;
- networking/authority tests;
- dedicated-server smoke;
- CI build/JAR verification;
- malformed-input, boundary, idempotency, replay, dedupe, and concurrency tests.

Deferred until the final campaign are checks that genuinely require a real client, actual modpack/provider hosts, representative gameplay/performance environment, prior-world fixtures not yet available, or exact release-candidate review.

## 11. Canonical documentation changes required before Stage 06 promotion

The first implementation subproject must update governance so later sessions cannot reintroduce the old gate interpretation:

- `plans/README.md` — promotion policy and completion-state distinction;
- `plans/DECISIONS.md` — durable architectural decision for deferred final validation and sequential downstream promotion, including the Stage 07.06 in-world-field default;
- `plans/STATUS.md` — Stage 05/05A remain final-validation-deferred while Stage 06 promotion becomes permitted;
- `plans/PENDING.md` — preserve genuine unknowns, remove/resolve the Forbidden Domains architecture decision because this design selects the in-world default, and remove any wording that treats Stage 05 manual acceptance as a universal downstream implementation blocker;
- PR #21/#22 descriptions, or replacement PR descriptions — reflect the new promotion rule and actual base/head state.

No Stage 05 manual evidence file is changed to manufacture completion.

## 12. Success criteria

The sequencing change is implemented correctly when:

1. Canonical governance distinguishes implementation completion from final validation.
2. Stage 05/05A manual rows remain truthful and open.
3. Stage 06 can integrate from latest `main` without weakening 05A contracts.
4. Stage 07 proceeds only after Stage 06 is canonical and is resynchronized to the resulting latest `main`.
5. Stage 08 proceeds only after Stage 07 implementation is canonical.
6. Stage 09 infrastructure proceeds only after Stage 08 implementation is canonical.
7. Every merge still requires applicable automated CI to be green and post-merge `main` confirmation.
8. No stage/release is called validated or complete while its own acceptance evidence is missing.
9. Final accumulated validation remains an explicit release-blocking phase after implementation work is exhausted.

## 13. Implementation decomposition

This is an umbrella governance design, not a replacement for the existing stage feature plans. Work remains decomposed into sequential subprojects:

1. Governance update + Stage 06 resynchronization/promotion.
2. Stage 07 resynchronization + completion of 07.04-07.07.
3. Stage 08 implementation.
4. Stage 09 hardening/release infrastructure implementation.
5. Final accumulated validation and release closeout.

Each subproject uses the existing stage plans as its feature specification and must not silently expand into the next stage before the current stage's implementation merge is complete.
