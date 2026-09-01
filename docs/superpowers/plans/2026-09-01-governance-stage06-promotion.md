# Governance + Stage 06 Promotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Canonicalize the deferred-final-validation governance and promote the prepared Stage 06 Rituals implementation onto the current `main` without weakening Stage 05/05A truth conditions or regressing the current CI/QA artifact path.

**Architecture:** Treat governance and Stage 06 runtime as one causally ordered subproject but keep the runtime transplant stage-scoped. First make the new promotion rule durable in canonical project memory; then recreate the Stage 06 change from the latest `main`, preserving current Stage 05A runtime/persistence/CI authority and reapplying only the ritual contracts already reviewed in PR #21. Stage 06 may merge with `IMPLEMENTED / FINAL VALIDATION DEFERRED` when host/client-only evidence is still unavailable; no Stage 05 manual row becomes PASS.

**Tech Stack:** Minecraft 1.21.1, NeoForge 21.1.248+, Java 21, Gradle 9.2.1 bootstrap, JUnit, NeoForge GameTests, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-01-deferred-final-validation-sequence-design.md`

## Global Constraints

- Preserve server authority for casting, hazards, rituals, costs, progression and world effects.
- Preserve the frozen Stage 05A contracts already canonical on current `main`.
- Preserve `.github/workflows/build.yml` exact-SHA main-only QA artifact publication after the full runtime gate.
- Stage 05/05A real-client rows remain unchanged unless direct real-client evidence exists.
- Downstream implementation may merge before deferred final validation, but missing evidence must remain explicit.
- Do not merge stale PR #21 wholesale over current `main`; transplant Stage 06 intent onto the latest canonical base.
- Optional integrations fail closed/safely when absent or incompatible.
- TDD remains mandatory for deterministic implementation changes; final manual/integrated validation alone is deferred.
- Do not rename Stage 06 task files to `✅-*` unless their own acceptance criteria are actually evidenced.

---

## File map

### Governance
- Modify `plans/README.md` — completion states and sequential promotion policy.
- Modify `plans/DECISIONS.md` — durable deferred-final-validation decision.
- Modify `plans/STATUS.md` — truthful current Stage 05/05A state and Stage 06 authorization.
- Modify `plans/PENDING.md` — retain real unknowns; remove obsolete universal Stage 05 promotion blocker if present.
- Keep `docs/qa/casting-ux-manual-matrix.md` unchanged.
- Keep `docs/qa/casting-ux-real-client-runbook.md` unchanged unless factual SHA/build delivery text becomes stale.

### Stage 06 ritual core to transplant from PR #21
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/ArcanaRitualId.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/BlackArcanaGrandRituals.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/CompositeRitualComponentProvider.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualActivationGuard.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualActivationId.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualAnchor.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualBindingRegistry.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualCompletionKey.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualCompletionLedger.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualComponentProvider.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualComponentReservation.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualContext.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualDefinition.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualDefinitionRegistry.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualEngine.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualOutcomeExecutor.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualRequirementEvaluator.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualRestoreResult.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualResult.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualSessionRegistry.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualSessionSnapshot.java`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/RitualSessionState.java`

### Shared runtime/persistence to reconcile manually, not overwrite wholesale
- Modify `src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntime.java` — add bounded ritual registries/engine/tick access while preserving current 05A services.
- Modify `src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeManager.java` — restore/persist ritual sessions while preserving current startup order, hazards and current packet/config behavior.
- Modify `src/main/java/dev/gustavopere/blackarcana/persistence/BlackArcanaSavedData.java` — add bounded ritual session serialization alongside current hazard/emergency state; never replace current file with stale PR content.
- Create/transplant `src/main/java/dev/gustavopere/blackarcana/persistence/RitualCompletionSavedData.java` — durable exactly-once ritual completion ledger.

### Provider bridges/content
- Create/transplant `src/main/java/dev/gustavopere/blackarcana/integration/eidolon/EidolonAnchorAttunementRitual.java`
- Create/transplant `src/main/java/dev/gustavopere/blackarcana/integration/eidolon/EidolonIntegrationIds.java`
- Create/transplant `src/main/java/dev/gustavopere/blackarcana/integration/eidolon/EidolonRitualRegistration.java`
- Create/transplant `src/main/java/dev/gustavopere/blackarcana/integration/malum/MalumRitualSpiritComponentProvider.java`
- Create/transplant `src/main/java/dev/gustavopere/blackarcana/integration/malum/MalumRitualSpiritRequirement.java`
- Modify/reconcile `src/main/java/dev/gustavopere/blackarcana/integration/malum/MalumServerIntegrationBootstrap.java`
- Create/transplant `src/main/resources/data/black_arcana/recipe/rituals/eidolon_anchor_attunement.json`
- Create/transplant `docs/architecture/rituals-preparatory.md`, rewriting status terminology so it no longer calls the implementation blocked by Stage 05 manual QA.

### Tests to transplant/reconcile
- `src/test/java/dev/gustavopere/blackarcana/core/ritual/BlackArcanaGrandRitualsTest.java`
- `src/test/java/dev/gustavopere/blackarcana/core/ritual/CompositeRitualComponentProviderTest.java`
- `src/test/java/dev/gustavopere/blackarcana/core/ritual/RitualCompletionLedgerTest.java`
- `src/test/java/dev/gustavopere/blackarcana/core/ritual/RitualEngineTest.java`
- `src/test/java/dev/gustavopere/blackarcana/core/ritual/RitualRegistryTest.java`
- `src/test/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeRitualTest.java`
- `src/test/java/dev/gustavopere/blackarcana/integration/malum/MalumGrandRitualIntegrationTest.java`
- `src/test/java/dev/gustavopere/blackarcana/integration/malum/MalumRitualSpiritComponentProviderTest.java`
- `src/test/java/dev/gustavopere/blackarcana/persistence/BlackArcanaSavedDataRitualSessionTest.java`
- `src/test/java/dev/gustavopere/blackarcana/persistence/RitualCompletionSavedDataTest.java`

---

### Task 1: Canonicalize the new governance

**Files:**
- Modify: `plans/README.md`
- Modify: `plans/DECISIONS.md`
- Modify: `plans/STATUS.md`
- Modify: `plans/PENDING.md`

**Interfaces:**
- Consumes: approved deferred-final-validation spec.
- Produces: canonical states `IMPLEMENTATION ACTIVE`, `IMPLEMENTED / AUTOMATED GATES GREEN`, `IMPLEMENTED / FINAL VALIDATION DEFERRED`, `VALIDATED / COMPLETE`, and Stage 09 `RELEASE BLOCKED`.

- [ ] **Step 1: Add the state model and promotion rule to `plans/README.md`**

Replace the single completion convention with text that preserves `✅-*` for genuinely complete tasks while explicitly allowing merged implementation to remain non-✅ when final evidence is deferred. State that branches for 06→07→08→09 are still created sequentially from the latest `main`, but missing manual/final evidence blocks completion/release claims rather than downstream implementation.

- [ ] **Step 2: Add one durable decision to `plans/DECISIONS.md`**

Append the next unused decision ID with this semantic contract:

```markdown
## Deferred final validation does not block downstream implementation
Missing manual, real-modpack, representative-performance, migration-fixture or exact-release-head evidence blocks validation/release claims, not downstream implementation, when predecessor runtime contracts are frozen and applicable automated gates are green. Stages 06→09 integrate sequentially through latest `main`. Deferred rows remain explicit and cannot be inferred as PASS. Stage 09 remains release-blocked until the accumulated final validation campaign is executed.
```

If the current file contains IDs beyond D030, use the numerically next free ID; do not renumber existing decisions.

- [ ] **Step 3: Rewrite `plans/STATUS.md` to match facts**

Record:

```text
05 Casting & UX: IMPLEMENTED / FINAL VALIDATION DEFERRED
05A Arcane Danger: IMPLEMENTED / FINAL VALIDATION DEFERRED for remaining presentation/manual acceptance; frozen server contracts remain canonical
06 Rituals: authorized for latest-main resynchronization/promotion
07 Spell Domains: downstream implementation continues only after 06 is canonical
08 Progression & Balance: waits for 07 implementation merge
09 Hardening & Release: waits for 08 implementation merge; final validation remains release-blocking
```

Do not remove or rewrite the pending Stage 05 manual matrix evidence.

- [ ] **Step 4: Reconcile `plans/PENDING.md`**

Keep genuine unresolved provider/version/license/domain questions. Remove only wording whose sole purpose is to treat Stage 05 manual QA as a universal implementation blocker. Do not resolve unrelated unknowns by assumption.

- [ ] **Step 5: Review governance diff**

Run:

```bash
git diff -- plans/README.md plans/DECISIONS.md plans/STATUS.md plans/PENDING.md docs/qa/casting-ux-manual-matrix.md
```

Expected: governance files changed; `docs/qa/casting-ux-manual-matrix.md` has no diff.

- [ ] **Step 6: Commit**

```bash
git add plans/README.md plans/DECISIONS.md plans/STATUS.md plans/PENDING.md
git commit -m "docs: defer final validation until implementation closure"
```

---

### Task 2: Establish a clean Stage 06 transplant branch from latest `main`

**Files:** no runtime edits yet; branch/history operation only.

**Interfaces:**
- Consumes: latest green `main`, PR #21 head `9b2fd70a60a487ffe17eb90cbc870e24af7e2a80` as historical Stage 06 source.
- Produces: fresh branch `feat/stage-06-rituals-current-main` whose first parent is the current canonical `main` after governance is merged.

- [ ] **Step 1: Verify latest `main` before branch creation**

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git rev-parse HEAD
```

Expected: HEAD equals the repository's current canonical main SHA at execution time.

- [ ] **Step 2: Create isolated execution branch/worktree**

Use `superpowers:using-git-worktrees` before editing. Create:

```bash
git switch -c feat/stage-06-rituals-current-main
```

or the equivalent worktree branch from the exact verified main SHA.

- [ ] **Step 3: Materialize a reference diff without merging stale ancestry**

```bash
git diff --binary main...9b2fd70a60a487ffe17eb90cbc870e24af7e2a80 -- \
  docs/architecture/rituals-preparatory.md \
  src/main/java/dev/gustavopere/blackarcana/core/ritual \
  src/main/java/dev/gustavopere/blackarcana/integration/eidolon \
  src/main/java/dev/gustavopere/blackarcana/integration/malum \
  src/main/java/dev/gustavopere/blackarcana/persistence/RitualCompletionSavedData.java \
  src/main/resources/data/black_arcana/recipe/rituals/eidolon_anchor_attunement.json \
  src/test/java/dev/gustavopere/blackarcana/core/ritual \
  src/test/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeRitualTest.java \
  src/test/java/dev/gustavopere/blackarcana/integration/malum \
  src/test/java/dev/gustavopere/blackarcana/persistence > /tmp/stage06-reference.patch
```

This patch is reference material only. Shared runtime/persistence files are reconciled manually in later tasks.

- [ ] **Step 4: Commit no code in this task**

This task ends when branch ancestry is correct and the historical Stage 06 source is available for comparison.

---

### Task 3: Restore the bounded ritual domain with its deterministic tests

**Files:**
- Create/transplant all `core/ritual/*` files listed in the File map.
- Create/transplant the five `core/ritual/*Test.java` files listed above.

**Interfaces:**
- Consumes: existing server-owned tick semantics and Java value types only.
- Produces: `RitualEngine`, `RitualDefinitionRegistry`, `RitualBindingRegistry`, `RitualSessionSnapshot`, `RitualRestoreResult`, `RitualCompletionLedger` and related bounded value objects.

- [ ] **Step 1: Restore the tests first**

Copy/reconstruct the Stage 06 ritual tests from PR #21 exactly enough to preserve tested semantics: bounded registry capacity, duplicate activation denial, reserve/commit/refund ordering, exactly-once completion, bounded tick advancement, malformed/invalid restore rejection.

- [ ] **Step 2: Run only the ritual unit tests and verify RED**

```bash
./gradlew test --tests 'dev.gustavopere.blackarcana.core.ritual.*'
```

Expected: FAIL because ritual production classes are absent on current `main`.

- [ ] **Step 3: Restore minimal ritual core implementation**

Transplant the reviewed PR #21 ritual-domain files. Preserve absolute capacity/retention limits and immutable snapshots; do not add new gameplay semantics.

- [ ] **Step 4: Run ritual unit tests**

```bash
./gradlew test --tests 'dev.gustavopere.blackarcana.core.ritual.*'
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/main/java/dev/gustavopere/blackarcana/core/ritual src/test/java/dev/gustavopere/blackarcana/core/ritual
git commit -m "feat(rituals): restore bounded ritual core"
```

---

### Task 4: Integrate ritual state into the current runtime and persistence model

**Files:**
- Modify: `src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntime.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeManager.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/persistence/BlackArcanaSavedData.java`
- Create/transplant: `src/main/java/dev/gustavopere/blackarcana/persistence/RitualCompletionSavedData.java`
- Test: `src/test/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeRitualTest.java`
- Test: `src/test/java/dev/gustavopere/blackarcana/persistence/BlackArcanaSavedDataRitualSessionTest.java`
- Test: `src/test/java/dev/gustavopere/blackarcana/persistence/RitualCompletionSavedDataTest.java`

**Interfaces:**
- Consumes: Task 3 ritual types; current Stage 05A `BlackArcanaSavedData` hazard/emergency persistence.
- Produces: ritual sessions restored/persisted alongside, not instead of, current hazard state; `ArcanaServerRuntime.rituals()` and bounded ritual tick summary.

- [ ] **Step 1: Restore runtime/persistence tests before implementation**

Ensure tests assert at minimum:

```java
// conceptual assertions the transplanted tests must preserve
assertEquals(originalRitualSession, restoredRitualSession);
assertEquals(originalCorruptionState, restoredCorruptionState);
assertEquals(originalStrainState, restoredStrainState);
assertEquals(originalEmergencyProtectionState, restoredEmergencyProtectionState);
assertEquals(1, exactlyOnceCompletionCount);
```

- [ ] **Step 2: Run targeted tests and verify RED**

```bash
./gradlew test \
  --tests 'dev.gustavopere.blackarcana.core.runtime.ArcanaServerRuntimeRitualTest' \
  --tests 'dev.gustavopere.blackarcana.persistence.BlackArcanaSavedDataRitualSessionTest' \
  --tests 'dev.gustavopere.blackarcana.persistence.RitualCompletionSavedDataTest'
```

Expected: FAIL because current runtime/persistence lacks Stage 06 state.

- [ ] **Step 3: Reconcile `ArcanaServerRuntime.java` manually**

Add ritual registries/engine/cap constants and bounded `rituals.tick(serverTick, DEFAULT_RITUAL_SESSIONS_PER_TICK)` to the current file. Do not replace any current hazard, emergency-protection, preview, networking or world-policy fields/methods.

- [ ] **Step 4: Reconcile `BlackArcanaSavedData.java` manually**

Add `MAX_PERSISTED_RITUAL_SESSIONS = 4_096`, bounded ritual session capture/read/write/restore, and overloads or current-signature integration that preserve every existing 05A persistence field. Malformed individual ritual entries are skipped/rejected without failing the whole world load.

- [ ] **Step 5: Reconcile `ArcanaServerRuntimeManager.java` manually**

Startup order must remain:

```text
install current initializers/contracts
load current SavedData
restore ordinary runtime + ritual sessions
restore Stage 05A hazard/emergency state
run runtime migrations
prune orphaned state
publish runtime
```

Log rejected ritual sessions but do not crash startup.

- [ ] **Step 6: Run targeted tests**

Use the command from Step 2. Expected: PASS.

- [ ] **Step 7: Run all unit tests**

```bash
./gradlew test
```

Expected: PASS with no regression in Stage 05/05A tests.

- [ ] **Step 8: Commit**

```bash
git add src/main/java/dev/gustavopere/blackarcana/core/runtime \
  src/main/java/dev/gustavopere/blackarcana/persistence \
  src/test/java/dev/gustavopere/blackarcana/core/runtime/ArcanaServerRuntimeRitualTest.java \
  src/test/java/dev/gustavopere/blackarcana/persistence
git commit -m "feat(rituals): integrate ritual lifecycle persistence"
```

---

### Task 5: Restore Eidolon and Malum ritual bridges without hard-dependency regressions

**Files:** provider bridge/content files listed in the File map.

**Interfaces:**
- Consumes: Task 3 ritual registries/components/outcomes; existing Stage 03 integration bootstrap boundaries.
- Produces: Eidolon anchor-attunement registration and Malum typed spirit component requirements/consumption without scattering optional-mod authority into core.

- [ ] **Step 1: Restore provider integration tests first**

Transplant `MalumGrandRitualIntegrationTest` and `MalumRitualSpiritComponentProviderTest`; preserve absence/fail-closed cases in addition to successful typed component behavior.

- [ ] **Step 2: Run provider tests and verify RED**

```bash
./gradlew test --tests 'dev.gustavopere.blackarcana.integration.malum.*Ritual*'
```

Expected: FAIL until Stage 06 bridge classes are restored.

- [ ] **Step 3: Restore Eidolon bridge and recipe**

Transplant only the reviewed Stage 06 anchor-attunement registration and recipe. Keep NeoForge `mod_loaded` conditioning and supported host-owned ritual API authority.

- [ ] **Step 4: Restore Malum typed component bridge**

Transplant the Stage 06 spirit requirement/provider and reconcile `MalumServerIntegrationBootstrap` against current main. Core must continue to compile/start without Malum classes present.

- [ ] **Step 5: Run provider tests**

Expected: PASS.

- [ ] **Step 6: Run all unit tests**

```bash
./gradlew test
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/main/java/dev/gustavopere/blackarcana/integration/eidolon \
  src/main/java/dev/gustavopere/blackarcana/integration/malum \
  src/main/resources/data/black_arcana/recipe/rituals/eidolon_anchor_attunement.json \
  src/test/java/dev/gustavopere/blackarcana/integration/malum
git commit -m "feat(rituals): restore optional ritual bridges"
```

---

### Task 6: Restore grand ritual behavior and restart/exactly-once coverage

**Files:**
- Modify/transplant: `BlackArcanaGrandRituals.java`
- Test: `BlackArcanaGrandRitualsTest.java`
- Test: `MalumGrandRitualIntegrationTest.java`
- Test: persistence/runtime ritual tests already present.

**Interfaces:**
- Consumes: ritual engine, completion ledger, provider component reservations, existing loaded-dimension/chunk/world-safety policy.
- Produces: at least one Black Arcana grand ritual satisfying Stage 06's transactional, interruption/restart and duplicate-reward semantics.

- [ ] **Step 1: Verify tests explicitly cover the Stage 06 exit criteria**

Required assertions:

```text
integrated ritual validates before consumption
failed activation refunds reservations
committed activation is not consumed/rewarded twice after restart
unloaded/invalid anchor fails closed
completion ledger prevents duplicate durable reward
bounded tick loop does not process more than configured sessions per tick
```

- [ ] **Step 2: Run focused tests**

```bash
./gradlew test \
  --tests 'dev.gustavopere.blackarcana.core.ritual.BlackArcanaGrandRitualsTest' \
  --tests 'dev.gustavopere.blackarcana.integration.malum.MalumGrandRitualIntegrationTest' \
  --tests 'dev.gustavopere.blackarcana.persistence.*Ritual*'
```

Expected: PASS after Tasks 3-5.

- [ ] **Step 3: Make only minimal fixes required by current-main API drift**

Do not add Stage 07 spell content, Stage 08 balance systems or new provider semantics.

- [ ] **Step 4: Commit any necessary fixes**

```bash
git add src/main/java/dev/gustavopere/blackarcana/core/ritual \
  src/test/java/dev/gustavopere/blackarcana/core/ritual \
  src/test/java/dev/gustavopere/blackarcana/integration/malum \
  src/test/java/dev/gustavopere/blackarcana/persistence
git commit -m "fix(rituals): reconcile Stage 06 with current contracts"
```

Skip this commit if no code changed.

---

### Task 7: Reconcile Stage 06 documentation and deferred-validation truth state

**Files:**
- Modify/create: `docs/architecture/rituals-preparatory.md`
- Modify: `plans/STATUS.md`
- Do not rename: `plans/06-rituals/01-ritual-contracts.md` through `04-grand-rituals.md` unless direct acceptance evidence supports completion.

**Interfaces:**
- Consumes: actual implementation/test evidence from Tasks 3-6.
- Produces: truthful `IMPLEMENTED / AUTOMATED GATES GREEN` or `IMPLEMENTED / FINAL VALIDATION DEFERRED` status.

- [ ] **Step 1: Update architecture document**

Record exact current behavior, capacity bounds, persistence semantics, Eidolon/Malum bridge status and which provider-host/client checks remain deferred.

- [ ] **Step 2: Update `plans/STATUS.md` from evidence only**

If repository CI lacks real optional host mods, use:

```text
Stage 06 Rituals — IMPLEMENTED / FINAL VALIDATION DEFERRED
```

and identify the exact deferred host/runtime checks. Do not use `VALIDATED / COMPLETE` merely because synthetic/no-host CI is green.

- [ ] **Step 3: Commit**

```bash
git add docs/architecture/rituals-preparatory.md plans/STATUS.md
git commit -m "docs(rituals): record Stage 06 implementation state"
```

---

### Task 8: Run the full automated gate and inspect the built JAR

**Files:** no intended source changes.

**Interfaces:**
- Consumes: complete Stage 06 branch.
- Produces: fresh automated evidence suitable for PR review; not manual-client evidence.

- [ ] **Step 1: Run unit tests**

```bash
./gradlew test
```

Expected: PASS.

- [ ] **Step 2: Run NeoForge build**

```bash
./gradlew build
```

Expected: BUILD SUCCESSFUL.

- [ ] **Step 3: Verify JAR contents**

```bash
jar tf build/libs/black_arcana-*.jar | grep -E 'META-INF/neoforge.mods.toml|dev/gustavopere/blackarcana/.+Ritual|data/black_arcana/recipe/rituals/eidolon_anchor_attunement.json'
```

Expected: mod metadata and intended Stage 06 runtime/data present; no `docs/qa/fixtures/stage05-real-client` content packaged.

- [ ] **Step 4: Run repository GameTest/dedicated-server tasks exactly as encoded by `.github/workflows/build.yml`**

Do not invent local task names; read the workflow at execution time and execute the same Gradle/launch commands where locally available.

- [ ] **Step 5: Push branch and require GitHub Actions GREEN**

All repository-required steps must pass: JUnit, diff sanity, NeoForge build, JAR verification, Foundation GameTests and dedicated-server smoke. The canonical QA artifact upload is expected to skip on PR refs and run only after main merge.

---

### Task 9: PR replacement/closure strategy for stale #21

**Files:** PR metadata only.

**Interfaces:**
- Consumes: fresh Stage 06 branch with green CI.
- Produces: one unambiguous Stage 06 PR targeting current `main`.

- [ ] **Step 1: Open a new Stage 06 PR**

Use title:

```text
Stage 06: promote Rituals under deferred final-validation policy
```

The body must state:

```text
- fresh base: latest main
- source lineage: reviewed Stage 06 behavior from historical PR #21
- shared runtime/persistence reconciled manually against current Stage 05A contracts
- Stage 05/05A manual evidence remains pending and unchanged
- Stage 06 host/client-only validation remains deferred where CI cannot exercise real providers
- full automated gate status and exact head SHA
```

- [ ] **Step 2: Close stale PR #21 without merging it**

Comment with the replacement PR number and explain that #21 is superseded because its base predates current main and the new sequencing policy. Then close #21.

- [ ] **Step 3: Re-check replacement PR diff**

Ensure no Stage 07 files, no fixture leakage and no rollback of current `.github/workflows/build.yml`.

---

### Task 10: Merge Stage 06 and verify post-merge `main`

**Files:** repository state only.

**Interfaces:**
- Consumes: replacement Stage 06 PR at exact green head SHA.
- Produces: Stage 06 implementation canonical on `main`, with deferred validation ledger still open.

- [ ] **Step 1: Apply verification-before-completion**

Re-fetch exact PR head, mergeability and latest CI immediately before merge. Do not rely on an older green run if head moved.

- [ ] **Step 2: Merge with expected head SHA**

Use normal repository merge method and supply the exact verified head SHA.

- [ ] **Step 3: Verify `main` points at the merge result**

Fetch branch `main` and confirm its SHA equals the merge SHA.

- [ ] **Step 4: Verify post-merge main CI**

Require the full workflow to complete GREEN on the merge SHA. Confirm the main-only canonical QA JAR upload succeeds and artifact name contains that exact merge SHA.

- [ ] **Step 5: Confirm truth state**

Final subproject state must be one of:

```text
Stage 06 IMPLEMENTED / FINAL VALIDATION DEFERRED
```

or, only if every Stage 06 acceptance criterion has direct evidence independent of the deferred Stage 05 manual UX gate:

```text
Stage 06 VALIDATED / COMPLETE
```

Stage 05/05A manual matrix remains unchanged. Stop after confirming main; Stage 07 is the next subproject and does not begin in the same execution checkpoint unless explicitly requested.
