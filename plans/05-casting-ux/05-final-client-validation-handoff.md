# 05.05 — Final Real-Client Validation Handoff

> **For agentic workers:** execute this document as a closeout plan. Do not implement new Casting & UX features unless a recorded real-client `FAIL` demonstrates a regression. Preserve the server-authoritative contracts in `plans/DECISIONS.md`, especially D005, D006, D019, D020, D023, D024, D029 and D031.

## Goal

Close the remaining Stage 05 acceptance surface with reproducible real-client evidence, without converting automated evidence into manual PASS and without changing Black Arcana casting authority.

## Current canonical state

- Baseline used to prepare this handoff: `main@1efe0eb2d4e0b93f130d16c84ea5ccfc6cf244dd`.
- Minecraft: `1.21.1`.
- NeoForge in the current physical modlist: `21.1.248`.
- Java: `21`.
- Stage 05 state: `IMPLEMENTED / FINAL VALIDATION DEFERRED`.
- Runtime implementation is already canonical on `main`.
- The acceptance authority for manual rows is `docs/qa/casting-ux-manual-matrix.md`.
- The execution procedure is `docs/qa/casting-ux-real-client-runbook.md`.
- Deterministic controls live under `docs/qa/fixtures/stage05-real-client/` and are test fixtures only, never production gameplay data.

The old feature branch `feat/05-casting-ux` is historical and must not be reused as an implementation base. Any closeout or bug-fix branch starts from the latest `origin/main` and records the exact base SHA.

## Architecture and authority boundaries

This validation must preserve the current architecture rather than silently redesign it:

1. `ClientInputController` emits bounded player intent only. Cast legality, progression, costs, cooldowns, targeting and world effects remain server-owned.
2. `ClientLoadoutSelection` is presentation/input state only. The synchronized/persisted loadout remains server authority.
3. `BlackArcanaRadialScreen` selects a spell but does not cast it.
4. `BlackArcanaHudLayer` is contextual and displays synchronized/server-authored presentation. It does not synthesize authoritative gate results.
5. `BlackArcanaClientConfig` contains client presentation preferences only.
6. Real-client validation must not introduce a second casting path, second resource authority, client-side admission shortcut or per-tick state synchronization.

If a manual failure appears to require changing one of those boundaries, stop that fix and record an architectural blocker instead of weakening the contract.

## Files involved

### Read before execution

- `plans/05-casting-ux/README.md`
- `plans/05-casting-ux/01-input-loadouts.md`
- `plans/05-casting-ux/02-radial-wheel.md`
- `plans/05-casting-ux/03-contextual-hud.md`
- `plans/05-casting-ux/04-accessibility-client-config.md`
- `plans/DECISIONS.md`
- `plans/STATUS.md`
- `docs/qa/casting-ux-manual-matrix.md`
- `docs/qa/casting-ux-real-client-runbook.md`

### Runtime surfaces to inspect only when a FAIL points there

- `src/main/java/dev/gustavopere/blackarcana/client/ClientInputController.java`
- `src/main/java/dev/gustavopere/blackarcana/client/ClientLoadoutSelection.java`
- `src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaLoadoutScreen.java`
- `src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaRadialScreen.java`
- `src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaHudLayer.java`
- `src/main/java/dev/gustavopere/blackarcana/client/BlackArcanaClientConfig.java`
- `src/main/java/dev/gustavopere/blackarcana/client/HudLayout.java`
- `src/main/java/dev/gustavopere/blackarcana/client/RadialLayout.java`
- `src/main/java/dev/gustavopere/blackarcana/network/ClientArcanaSyncState.java`

### Existing focused automated coverage

- `src/test/java/dev/gustavopere/blackarcana/client/ClientLoadoutSelectionTest.java`
- `src/test/java/dev/gustavopere/blackarcana/client/LoadoutDraftTest.java`
- `src/test/java/dev/gustavopere/blackarcana/client/HudLayoutTest.java`
- `src/test/java/dev/gustavopere/blackarcana/client/RadialLayoutTest.java`
- `src/test/java/dev/gustavopere/blackarcana/client/RadialToggleInputTest.java`
- `src/test/java/dev/gustavopere/blackarcana/client/SmallViewportLayoutContractTest.java`
- `src/test/java/dev/gustavopere/blackarcana/client/HazardForecastPresentationTest.java`

Automated tests are regression gates. They never substitute for a row that explicitly requires direct client observation.

---

## Task 1 — Freeze the exact build under test

**Deliverable:** one exact-SHA client build and an evidence report header that can be audited later.

- [ ] Fetch the latest `origin/main` immediately before the campaign and record its full SHA.
- [ ] Confirm the closeout branch contains no unmerged runtime work that changes Stage 05 behavior.
- [ ] Use the successful `main` CI artifact whose name matches that exact SHA: `black-arcana-<full commit SHA>`.
- [ ] If the exact artifact is unavailable, build exactly that SHA locally; do not substitute another revision without changing the recorded tested SHA.
- [ ] Use a Minecraft `1.21.1` / NeoForge `21.1.248` / Java `21` test instance matching the current project environment.
- [ ] Install only the Stage 05 fixture required for the scenarios being exercised, and keep it out of production data.
- [ ] Create `docs/qa/casting-ux-real-client-evidence.md` on the closeout branch using the evidence fields from the canonical runbook.
- [ ] Record at the top of that report: tested SHA, Minecraft version, NeoForge version, Java version, modpack/modlist snapshot identification, test date, client display mode and GPU/OS only when relevant to a visual failure.

**Stop condition:** if the client cannot launch the exact build, mark the campaign `BLOCKED` with the launch failure and fix the launch/runtime regression before evaluating presentation rows.

---

## Task 2 — Validate 05.01 Input & Loadouts

**Deliverable:** direct evidence for every applicable input/loadout/session matrix row.

### Scenarios

- [ ] Rebind radial, selected-cast and available quick-slot mappings through the vanilla controls screen.
- [ ] Confirm key conflicts remain discoverable and that a usable non-conflicting binding can be selected.
- [ ] With inventory open, press selected-cast and quick-cast bindings; no cast intent may fire through the GUI.
- [ ] Repeat with chat and one additional normal Minecraft `Screen`.
- [ ] Edit the loadout, apply it, close the editor and reopen it; the synchronized server response must be the state shown after reopen.
- [ ] Clear/apply/reopen the loadout and verify that client draft state does not bypass server slot/availability validation.
- [ ] Disconnect/reconnect as the same player and verify that old result/loadout/HUD state does not flash before fresh synchronized snapshots arrive.
- [ ] Exercise one legitimate server denial and verify that the client shows the authoritative denial rather than a locally invented gate reason.

### PASS invariants

- selection/loadout editing never grants authority;
- GUI focus suppresses direct cast input;
- reconnect converges from server snapshots;
- no stale client state executes or visually masquerades as current authority.

### FAIL triage

If any input/loadout row fails:

1. write the exact input sequence and observed packet/UI behavior in the evidence report;
2. reproduce twice on the same exact SHA;
3. add a focused regression test where the behavior is deterministic outside the physical client;
4. run that test RED before the fix;
5. implement the smallest fix that preserves D006/D019/D020/D023/D024;
6. rerun the focused test GREEN and then repeat the failed manual row.

Do not mark sibling rows PASS merely because the regression is fixed.

---

## Task 3 — Validate 05.02 Radial Wheel

**Deliverable:** direct evidence that radial layout, selection/cast separation and hold/toggle behavior work in real client conditions.

### Resolution/layout set

Exercise the radial at:

- [ ] 854×480;
- [ ] 1920×1080;
- [ ] 3440×1440 ultrawide;
- [ ] GUI scale Auto where available;
- [ ] GUI scale 2;
- [ ] GUI scale 3;
- [ ] GUI scale 4.

Record only combinations the real client actually permits. Do not infer an untested combination.

### Interaction set

- [ ] `TOGGLE`: open the radial, change selection, close/reopen and confirm the same open key closes it predictably when applicable.
- [ ] Verify left-clicking a wedge changes the selected spell and closes the wheel without executing a cast.
- [ ] Execute a separate cast input afterward to prove selection and casting are distinct operations.
- [ ] `HOLD`: open while holding the key, release it and confirm the wheel closes without a stuck key/input state.
- [ ] Page through a loadout large enough to require multiple radial pages when the synchronized test loadout permits it.
- [ ] Confirm hit regions remain usable and no visible card is clipped outside the viewport.

### PASS invariants

- radial interaction is client presentation only;
- selection never executes gameplay;
- no stuck input after close;
- layout remains on-screen/readable at every tested viewport/GUI scale.

Any failure that suggests adding a client-side cast shortcut is an architectural rejection, not an acceptable fix.

---

## Task 4 — Validate 05.03 Contextual HUD & Feedback

**Deliverable:** direct evidence for HUD lifecycle, denial, hazard/gate presentation, anchor/scale containment and stale-state behavior.

### Contextual lifecycle

- [ ] Trigger recent selection and verify the contextual panel appears.
- [ ] Stop interacting and verify the panel disappears after the configured lifetime.
- [ ] Confirm there is no permanent Black Arcana mana/resource bar.
- [ ] Trigger a server-authoritative denial and verify the actual bounded denial detail appears briefly.
- [ ] Toggle vanilla F1/hidden GUI behavior and record the observed Black Arcana layer behavior.

### Anchor/scale containment

Exercise every `HudLayout.Anchor` exposed by the client config at:

- [ ] HUD scale 0.5×;
- [ ] HUD scale 1×;
- [ ] HUD scale 2×.

For each anchor/scale set, use a state with the additional hazard/gate line visible and confirm the panel remains in the viewport and readable.

### Hazard resistance forecast

Using the deterministic Stage 05 fixture, exercise a non-normal selected spell with effective Arcane Resistance:

- [ ] below minimum;
- [ ] between minimum and recommended;
- [ ] at or above recommended.

The displayed current/minimum/recommended values and threshold status must come from synchronized server-authored projection. Wording may report `blocked below minimum`, `below recommended` or `recommendation met`; it must not claim that recommendation eliminates all Backlash risk.

### Predictable gate projection

Exercise legitimate states that the current runtime/fixture can produce:

- [ ] `CLEAR`;
- [ ] `COOLDOWN`;
- [ ] `COST`.

For `CLEAR`, verify the wording says only that no predictable gate blocks. It must not guarantee cast success because replay admission, target resolution, world policy and hazard preparation remain cast-time authority.

For identity/loadout, progression or unavailable projection states, follow the canonical runbook. If the production runtime cannot produce the state without a debug bypass or semantic change, mark the corresponding row `BLOCKED`; do not fabricate a PASS fixture.

### Refresh/stale protection

- [ ] Change available equipment/Curios/RPG-derived resistance while the spell remains selected and verify the client converges to the current server-authored projection.
- [ ] Use the alternate fixture danger profile and `/reload` while a forecast is active.
- [ ] Verify stale tier/threshold data cannot override the refreshed static preflight/forecast presentation.
- [ ] Record the reconnect/reload transition continuously when possible.

### Provider unavailable/incompatible state

If a reproducible supported test configuration exists:

- [ ] make preview unavailable/incompatible;
- [ ] verify the HUD shows `Unavailable` or synchronized static fallback;
- [ ] verify no known-partial resistance value is presented as complete.

If that state cannot be produced without changing production semantics, mark the row `BLOCKED` with the concrete limitation.

---

## Task 5 — Validate 05.04 Accessibility & Client Configuration

**Deliverable:** direct evidence that client-only preferences persist and affect presentation only.

- [ ] Set feedback to `MINIMAL`; verify non-denial contextual density is suppressed as designed and no unused forecast/gate presentation remains visible.
- [ ] Set feedback to `STANDARD`; verify selected-spell presentation appears without verbose success spam.
- [ ] Set feedback to `VERBOSE`; verify success feedback is presented without changing gameplay results.
- [ ] Toggle radial behavior between `TOGGLE` and `HOLD` and repeat the radial interaction row rather than assuming config persistence from the file alone.
- [ ] Toggle reduced motion and reduced flashes, restart the client and verify the preferences persist locally.
- [ ] Set particle density to `0`, `0.5` and `1`, restart where needed and verify persistence only.
- [ ] Do not claim effect-level compliance for reduced motion/flashes/particles where the corresponding Black Arcana effect does not yet exist; use `NOT APPLICABLE / CARRIED TO STAGE 09` exactly as authorized by the matrix closure rule.
- [ ] Remove/reset relevant client-config entries through a normal supported config-reset path and verify NeoForge defaults recover safely.
- [ ] Verify none of these client preferences changes damage, power, cooldown, cost, progression, targeting, hazard admission or world mutation authority.

A configuration preference changing gameplay authority is a release-blocking regression.

---

## Task 6 — Evidence reconciliation and failure loop

**Deliverable:** an auditable matrix where every row is one of the permitted result states.

Use exactly:

- `PASS` — directly observed expected behavior;
- `FAIL` — directly observed contradiction;
- `BLOCKED` — scenario could not be legitimately exercised;
- `NOT APPLICABLE / CARRIED TO STAGE 09` — only for genuinely future-only presentation features allowed by the matrix.

For every matrix row, `docs/qa/casting-ux-real-client-evidence.md` must include:

- Matrix row / scenario;
- Tested commit SHA;
- Minecraft / NeoForge instance identification;
- Relevant client settings;
- Steps performed;
- Observed result;
- Evidence reference;
- Result.

For every `FAIL`, additionally record:

- exact reproduction sequence;
- expected result;
- screenshot or recording for visual/input failures;
- regression-test path when one can represent the deterministic cause;
- fix commit SHA;
- rerun evidence on the fixed exact SHA.

A fixed failure changes only the rows actually rerun. Never bulk-convert untouched rows to PASS.

---

## Task 7 — Closeout gate

**Deliverable:** Stage 05 status changes only when supported by real-client evidence and fresh CI.

### Preconditions before changing Stage state

- [ ] Every applicable row in `docs/qa/casting-ux-manual-matrix.md` has direct evidence.
- [ ] No applicable row remains `FAIL`.
- [ ] Every `BLOCKED` row is either explicitly accepted as an external/manual limitation for Stage 09 or resolved and rerun.
- [ ] Future-only presentation rows use `NOT APPLICABLE / CARRIED TO STAGE 09` only where the matrix already permits that classification.
- [ ] The evidence report references the exact tested commit(s).
- [ ] Any implementation fixes have focused RED→GREEN regression coverage where technically representable.

### Final synchronization

Immediately before the closeout PR is finalized:

1. fetch the latest `origin/main`;
2. reconcile `main` into the closeout branch without discarding concurrent work;
3. review `main..HEAD` semantically;
4. rerun affected manual rows if the reconciliation changed any Stage 05 runtime/client surface;
5. run the full canonical automated gate on the reconciled HEAD.

CI evidence from before the last relevant synchronization is not final evidence.

### Files to update only after the gate is satisfied

- `docs/qa/casting-ux-manual-matrix.md` — replace only exercised row states from evidence;
- `plans/05-casting-ux/01-input-loadouts.md` — promote state only if its applicable rows are satisfied;
- `plans/05-casting-ux/02-radial-wheel.md` — promote state only if its applicable rows are satisfied;
- `plans/05-casting-ux/03-contextual-hud.md` — promote state only if its applicable rows are satisfied;
- `plans/05-casting-ux/04-accessibility-client-config.md` — promote state only if its applicable rows are satisfied or correctly carried to Stage 09;
- `plans/05-casting-ux/README.md` — remove `FINAL VALIDATION DEFERRED` only when the Stage-level gate is satisfied;
- `plans/STATUS.md` — record the final validated state and exact evidence/CI SHAs.

Do not change those status declarations merely because this handoff document exists.

---

## Required final automated verification

After all fixes and the final `origin/main` reconciliation, execute the repository's canonical CI-equivalent gate. The final evidence must include, as applicable to the current workflow:

- JUnit;
- diff sanity;
- NeoForge build;
- built-JAR verification;
- Foundation GameTests;
- dedicated-server smoke;
- canonical main artifact publication after merge.

The exact workflow names/commands are taken from the current repository at execution time; do not reuse stale workflow numbers as if they proved the new HEAD.

## Merge rule

The closeout PR may merge only after:

1. direct-client evidence is recorded for applicable Stage 05 rows;
2. all implementation `FAIL`s are fixed and rerun;
3. the branch is reconciled with the latest relevant `main`;
4. the full automated gate is green on the reconciled HEAD;
5. review threads are resolved;
6. the final diff does not weaken casting/server authority.

After merge, confirm the final `main` SHA and the exact post-merge CI result before declaring Stage 05 validated.

## Non-goals

This handoff does **not** authorize:

- a second mana/resource pool;
- a second cast pipeline;
- client-side cast legality decisions;
- client-authored hazard/gate truth;
- provider-specific gameplay authority moved into UI code;
- new spell content;
- Stage 05 redesign for aesthetics unrelated to a recorded FAIL;
- fake PASS states from screenshots, code inspection, GameTests or CI alone;
- weakening or deleting validation gates to obtain green.

## Closure statement template

Use this only after every gate above is actually satisfied:

> Stage 05 Casting & UX was validated on exact client build `<tested-main-sha>` using Minecraft 1.21.1 / NeoForge 21.1.248 / Java 21. Direct evidence is recorded in `docs/qa/casting-ux-real-client-evidence.md`; applicable manual matrix rows are PASS or explicitly carried according to the canonical closure rule. The final reconciled closeout HEAD `<head-sha>` passed the complete automated gate, the PR merged as `<merge-sha>`, and post-merge `main` verification `<workflow/run>` is GREEN.

Until those values exist as real evidence, Stage 05 remains `IMPLEMENTED / FINAL VALIDATION DEFERRED`.
