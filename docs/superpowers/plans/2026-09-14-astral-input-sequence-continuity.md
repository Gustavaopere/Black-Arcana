# Astral Input Sequence Continuity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve monotonic Astral Severance MOVE sequence state across temporary `MOVE_END` disarming while resetting the sequence domain only when the exact projection presentation ends, is replaced, or client state is cleared.

**Architecture:** Keep the existing server-owned `AstralSeveranceRuntime.lastProcessedControlSequence` contract unchanged. Add a client-only `disarm(UUID)` operation that preserves the current projection identity and sequence while discarding transient pending look input, then make `AstralSeveranceInputController` distinguish “movement temporarily unavailable for an otherwise desired projection” from “no Astral projection presentation exists”. No server reset, protocol field, production MOVE enablement, or cast/channel change is introduced.

**Tech Stack:** Java 21, Minecraft 1.21.1, NeoForge 21.1.x from the physical project baseline, JUnit 5, Gradle, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-14-astral-input-sequence-continuity-design.md`

## Global Constraints

- Black Arcana remains authoritative for the magical runtime; client code sends bounded intent only.
- D024 remains intact: channeling converges on the canonical `ArcanaCastEngine`; this plan must not introduce or modify a parallel cast path.
- D025 remains intact: typed canonical target references and server-owned target resolution are untouched.
- Caster identity is never client-authored; existing authenticated network-context ownership remains unchanged.
- `MOVE_END` is a temporary control revocation, not an Astral projection/session end.
- `END`, client state clear, or replacement with another `projectionId` ends the old client sequence domain.
- Production `ControlLimits` values remain absent and production MOVE remains fail-closed.
- No new payload fields, server sequence reset command, Mixin, resource/cooldown/progression values, remote interaction, combat, or world mutation are allowed in this tranche.
- TDD is mandatory: execute and record RED before production changes for each behavior-changing task.
- Branch work remains on `feat/stage07-astral-input-redirect`, reconciled with latest `main` by merge, never routine rebase/force-push.

---

## File Structure

- `src/main/java/dev/gustavopere/blackarcana/client/AstralControlIntentSequencer.java`
  - Owns client-local exact-projection sequence number and pending look accumulation.
  - Gains `disarm(UUID)` for temporary control revocation without resetting the sequence domain.
- `src/main/java/dev/gustavopere/blackarcana/client/AstralSeveranceClientController.java`
  - Continues to own camera/presentation state.
  - Exposes package-private read-only `desiredProjection()` so the input controller can distinguish temporary disarm from presentation end without inventing another authority source.
- `src/main/java/dev/gustavopere/blackarcana/client/AstralSeveranceInputController.java`
  - Continues to capture/suppress movement and look only while exact control is armed.
  - Uses desired presentation identity to preserve or reset sequencer lifetime correctly when `movementControl()` is absent.
- `src/test/java/dev/gustavopere/blackarcana/client/AstralControlIntentSequencerTest.java`
  - Behavioral regression for sequence continuity and pending-look disposal.
- `src/test/java/dev/gustavopere/blackarcana/client/AstralSeveranceClientWiringTest.java`
  - Existing repository-style source wiring regression ensuring the input controller distinguishes desired presentation from armed movement control.
- No server runtime, payload schema, cast binding, resource authority, cooldown, or world-effect file should change.

---

### Task 1: Preserve one exact projection's sequence across temporary disarm

**Files:**
- Modify: `src/test/java/dev/gustavopere/blackarcana/client/AstralControlIntentSequencerTest.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/client/AstralControlIntentSequencer.java`

**Interfaces:**
- Consumes: existing `captureLook(UUID,double,double,double,boolean)`, `capture(UUID,double,double,double)`, and `clear()`.
- Produces: package-private `void disarm(UUID projectionId)` with these exact semantics: retain sequence when `projectionId` is unchanged, reset sequence if the exact projection changes, and always discard pending look input.

- [ ] **Step 1: Add the failing continuity regression**

Add this test to `AstralControlIntentSequencerTest`:

```java
@Test
void disarmPreservesSameProjectionSequenceAndDropsPendingLook() {
    AstralControlIntentSequencer sequencer = new AstralControlIntentSequencer();
    UUID projection = UUID.randomUUID();

    AstralMoveIntentPayload first = sequencer
            .capture(projection, 1.0D, 0.0D, 0.0D)
            .orElseThrow();
    sequencer.captureLook(projection, 12.0D, -7.0D, 0.5D, false);

    sequencer.disarm(projection);

    AstralMoveIntentPayload second = sequencer
            .capture(projection, 0.0D, 0.0D, 1.0D)
            .orElseThrow();

    assertEquals(1L, first.sequence());
    assertEquals(2L, second.sequence(),
            "temporary disarm must preserve the exact projection sequence domain");
    assertEquals(0.0F, second.yawDeltaDegrees(),
            "pending look captured before disarm must not replay after re-arm");
    assertEquals(0.0F, second.pitchDeltaDegrees(),
            "pending look captured before disarm must not replay after re-arm");
}
```

- [ ] **Step 2: Run the targeted test and verify RED**

Run:

```bash
./gradlew --no-daemon test --tests dev.gustavopere.blackarcana.client.AstralControlIntentSequencerTest
```

Expected: test compilation fails because `AstralControlIntentSequencer.disarm(UUID)` does not exist. The failure must be the missing production method, not an unrelated compile/test error.

- [ ] **Step 3: Commit and push the test-only RED state**

```bash
git add src/test/java/dev/gustavopere/blackarcana/client/AstralControlIntentSequencerTest.java
git commit -m "test(stage07): preserve Astral sequence across disarm"
git push origin feat/stage07-astral-input-redirect
```

Record the exact commit SHA and the resulting `Black Arcana CI` run. The run is expected to fail at Unit tests/compile on the missing `disarm(UUID)` production method; do not claim later skipped jobs as executed.

- [ ] **Step 4: Implement the minimal sequencer operation**

Add this method to `AstralControlIntentSequencer` immediately before `clear()`:

```java
void disarm(UUID projectionId) {
    Objects.requireNonNull(projectionId, "projectionId");
    switchProjection(projectionId);
    clearPendingLook();
}
```

Do not change `clear()`:

```java
void clear() {
    projectionId = null;
    sequence = 0L;
    clearPendingLook();
}
```

This is intentional: `disarm()` preserves the sequence domain for the same exact projection; `clear()` remains the full end/reset operation.

- [ ] **Step 5: Verify the targeted test is GREEN**

Run:

```bash
./gradlew --no-daemon test --tests dev.gustavopere.blackarcana.client.AstralControlIntentSequencerTest
```

Expected: all `AstralControlIntentSequencerTest` methods PASS.

- [ ] **Step 6: Run the complete unit suite before committing production GREEN**

Run:

```bash
./gradlew --no-daemon test
```

Expected: full JUnit suite PASS with no new warnings/errors attributable to this change.

- [ ] **Step 7: Commit the minimal GREEN implementation**

```bash
git add src/main/java/dev/gustavopere/blackarcana/client/AstralControlIntentSequencer.java
git commit -m "fix(stage07): preserve Astral sequence while disarmed"
```

---

### Task 2: Bind sequencer reset lifetime to desired projection presentation, not MOVE arm state

**Files:**
- Modify: `src/test/java/dev/gustavopere/blackarcana/client/AstralSeveranceClientWiringTest.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/client/AstralSeveranceClientController.java`
- Modify: `src/main/java/dev/gustavopere/blackarcana/client/AstralSeveranceInputController.java`

**Interfaces:**
- Consumes: `AstralViewClientState.desired()`, existing `AstralSeveranceClientController.movementControl()`, and Task 1 `AstralControlIntentSequencer.disarm(UUID)`.
- Produces: package-private `static Optional<AstralViewClientState.Desired> desiredProjection()` in `AstralSeveranceClientController`; private `suspendOrResetSequencer()` in `AstralSeveranceInputController`.

- [ ] **Step 1: Add the failing wiring regression**

Add this test to `AstralSeveranceClientWiringTest`:

```java
@Test
void temporaryMoveDisarmPreservesSequenceUntilProjectionPresentationEnds() throws IOException {
    String cameraSource = Files.readString(CAMERA_CONTROLLER);
    String inputSource = Files.readString(INPUT_CONTROLLER);

    assertTrue(cameraSource.contains(
                    "static Optional<AstralViewClientState.Desired> desiredProjection()"),
            "input sequencing must be able to distinguish desired presentation from MOVE arm state");
    assertTrue(cameraSource.contains("return STATE.desired();"),
            "desired projection identity must come from the existing server-authored presentation state");
    assertTrue(inputSource.contains("AstralSeveranceClientController.desiredProjection()"),
            "temporary MOVE disarm must inspect whether the exact projection presentation still exists");
    assertTrue(inputSource.contains("SEQUENCER.disarm(desired.projectionId())"),
            "temporary MOVE disarm must preserve the exact projection sequence domain");
}
```

- [ ] **Step 2: Run the wiring test and verify RED**

Run:

```bash
./gradlew --no-daemon test --tests dev.gustavopere.blackarcana.client.AstralSeveranceClientWiringTest
```

Expected: the new test fails because `desiredProjection()` and `SEQUENCER.disarm(desired.projectionId())` are not yet present in production wiring.

- [ ] **Step 3: Commit and push the wiring RED state**

```bash
git add src/test/java/dev/gustavopere/blackarcana/client/AstralSeveranceClientWiringTest.java
git commit -m "test(stage07): bind Astral sequence lifetime to projection"
git push origin feat/stage07-astral-input-redirect
```

Record the exact commit SHA and its failing `Black Arcana CI` run. Confirm the failure is the intended new wiring assertion, not a regression from Task 1.

- [ ] **Step 4: Expose the existing desired projection identity read-only**

Add this package-private method to `AstralSeveranceClientController` immediately before `movementControl()`:

```java
static Optional<AstralViewClientState.Desired> desiredProjection() {
    return STATE.desired();
}
```

Do not expose mutable `AstralViewClientState`, do not add a second state store, and do not weaken the camera-ownership checks inside `movementControl()`.

- [ ] **Step 5: Add one helper that preserves on temporary disarm and fully resets on END/clear**

Add this private helper to `AstralSeveranceInputController`:

```java
private static void suspendOrResetSequencer() {
    AstralViewClientState.Desired desired =
            AstralSeveranceClientController.desiredProjection().orElse(null);
    if (desired == null) {
        SEQUENCER.clear();
        return;
    }
    SEQUENCER.disarm(desired.projectionId());
}
```

Then change only the two `control == null` branches in `onCalculatePlayerTurn(...)` and `onMovementInput(...)` from:

```java
SEQUENCER.clear();
return;
```

to:

```java
suspendOrResetSequencer();
return;
```

Keep the `minecraft.player == null` branch as a full reset:

```java
if (minecraft.player == null) {
    SEQUENCER.clear();
    return;
}
```

Do not change input suppression, event priorities, camera ownership checks, MOVE payload contents, or network send behavior.

- [ ] **Step 6: Verify the two focused client test classes are GREEN**

Run:

```bash
./gradlew --no-daemon test \
  --tests dev.gustavopere.blackarcana.client.AstralControlIntentSequencerTest \
  --tests dev.gustavopere.blackarcana.client.AstralSeveranceClientWiringTest
```

Expected: both test classes PASS.

- [ ] **Step 7: Verify the complete unit suite**

Run:

```bash
./gradlew --no-daemon test
```

Expected: full JUnit suite PASS.

- [ ] **Step 8: Commit the controller GREEN implementation**

```bash
git add \
  src/main/java/dev/gustavopere/blackarcana/client/AstralSeveranceClientController.java \
  src/main/java/dev/gustavopere/blackarcana/client/AstralSeveranceInputController.java
git commit -m "fix(stage07): retain Astral sequence across control disarm"
```

---

### Task 3: Reconcile, review, and obtain exact-head CI evidence

**Files:**
- Review only: all PR #248 changed files plus the design/plan documents.
- Update PR metadata/body only; no additional gameplay code unless review/CI identifies a concrete defect.

**Interfaces:**
- Consumes: completed Tasks 1–2, PR #248, review thread `PRRT_kwDOUGeLhc6iGQly`, latest `main`.
- Produces: reconciled exact PR head with all required CI gates green and review thread resolved.

- [ ] **Step 1: Re-fetch and reconcile latest main before final validation**

Run:

```bash
git fetch origin main
git rev-parse origin/main
git merge-base origin/main HEAD
git rev-list --left-right --count origin/main...HEAD
```

Expected before CI: branch is `behind 0`. If `main` advanced, merge `origin/main` into `feat/stage07-astral-input-redirect` with a normal merge commit, resolve conflicts semantically, and re-run Tasks 1–2 focused tests before continuing. Do not rebase or force-push.

- [ ] **Step 2: Run local deterministic verification on the reconciled head**

Run the same commands used by repository CI where practical:

```bash
./gradlew --no-daemon test
./gradlew --no-daemon build
mkdir -p runs/gameTestServer
printf 'eula=true\n' > runs/gameTestServer/eula.txt
./gradlew --no-daemon runGameTestServer
```

Expected: all commands complete successfully. Dedicated-server smoke remains covered by the repository workflow using `.github/workflows/build.yml` and must not be inferred from `runGameTestServer`.

- [ ] **Step 3: Push the final reconciled code head**

```bash
git push origin feat/stage07-astral-input-redirect
```

Wait for both relevant `Black Arcana CI` executions on the exact final head (`push` and `pull_request` when both are emitted). Required successful steps are exactly:

- Unit tests — `./gradlew --no-daemon test`
- Diff sanity — `git diff --check` against merge-base
- NeoForge build — `./gradlew --no-daemon build`
- Verify built JAR
- Foundation GameTest server — `./gradlew --no-daemon runGameTestServer`
- Dedicated-server smoke test — repository `runServer` smoke loop

`Publish canonical QA JAR` is expected to be skipped off `main`.

- [ ] **Step 4: Review the final diff for scope**

Expected gameplay/code changes relative to `main` are limited to the existing PR #248 client-input/presentation files plus the sequence-continuity edits from Tasks 1–2. The following server/cast files must remain unchanged by the fix:

```text
src/main/java/dev/gustavopere/blackarcana/api/ArcanaCastEngine.java
src/main/java/dev/gustavopere/blackarcana/api/ArcanaServices.java
src/main/java/dev/gustavopere/blackarcana/integration/neoforge/AstralSeveranceCastBinding.java
src/main/java/dev/gustavopere/blackarcana/content/noetic/AstralSeveranceRuntime.java
```

The branch may additionally contain only these planning artifacts from the approved design process:

```text
docs/superpowers/specs/2026-09-14-astral-input-sequence-continuity-design.md
docs/superpowers/plans/2026-09-14-astral-input-sequence-continuity.md
```

- [ ] **Step 5: Resolve the existing P2 only after code and CI prove the fix**

Reply in review thread `PRRT_kwDOUGeLhc6iGQly` with the concrete behavior and evidence: temporary disarm now preserves the same projection's sequence and clears only pending look; full `END`/desired-state absence still calls `clear()`; cite the RED and GREEN commit/workflow identifiers from Tasks 1–3.

Then resolve the thread. Do not resolve it before exact-head tests prove the correction.

- [ ] **Step 6: Update PR #248 body with current ancestry and TDD evidence**

Keep the existing summary/scope, and add:

```text
Sequence-continuity hardening:
- branch reconciled with canonical main containing PR #247 cast/channel binding
- RED: <exact test-only commit/run from Task 1>
- GREEN: <exact sequencer implementation commit/run>
- wiring RED: <exact test-only commit/run from Task 2>
- final GREEN: <exact reconciled head and push/PR workflow runs>
- P2 sequence-reset review thread resolved after exact-head validation
```

Replace the angle-bracket evidence with the actual identifiers produced during execution; do not guess them.

---

### Task 4: Merge safely and verify canonical main

**Files:**
- No new code files expected.
- GitHub PR/main state and Actions evidence only.

**Interfaces:**
- Consumes: exact final PR head, latest `main`, green exact-head CI, resolved P2.
- Produces: merged PR #248, verified post-merge main SHA and canonical QA artifact.

- [ ] **Step 1: Repeat all pre-merge invariants immediately before merge**

Confirm from GitHub, not cached local assumptions:

```text
PR #248 state = open
PR #248 mergeable = true
PR head SHA = exact CI-tested final head
base branch = main
branch behind latest main = 0
all review threads resolved
required push/PR CI on exact head = success
```

If `main` advanced, stop the merge, merge latest `main` into the branch, and rerun the exact-head validation. Old CI no longer counts.

- [ ] **Step 2: Merge PR #248 with head protection**

Use normal merge semantics with `expected_head_sha` equal to the exact validated PR head. Do not use rebase. Preserve TDD history rather than force-moving the branch.

Expected: GitHub reports `merged=true` and returns a merge commit SHA.

- [ ] **Step 3: Confirm canonical main immediately after merge**

Fetch the `main` branch and confirm its SHA is the PR merge commit (unless a concurrent merge advanced `main`, in which case confirm the PR merge commit is an ancestor and record the newer canonical SHA separately).

- [ ] **Step 4: Require post-merge CI on the exact PR merge SHA**

The `main` workflow must pass:

- Unit tests
- Diff sanity
- NeoForge build
- Verify built JAR
- Foundation GameTest server
- Dedicated-server smoke test
- Publish canonical QA JAR

Record the workflow run ID, artifact name/id, and SHA-256 if GitHub exposes it. Do not claim canonical delivery before this exact-SHA run succeeds.

- [ ] **Step 5: Final status boundary**

Report PR #248 as merged/canonical only after Step 4. Keep Stage 07.07 at **partial / in progress** because this tranche still does not:

- enable production MOVE execution;
- select/bundle `ControlLimits` values;
- select final resource/cooldown/scaling/progression values;
- add projection interaction or remote casting;
- execute required D031 real-client/modpack acceptance.

Stage 08 must still not consume 07.07 as final canonical balance input.
