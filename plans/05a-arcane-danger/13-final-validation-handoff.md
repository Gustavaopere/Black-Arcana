# 05A.13 — Arcane Danger Final Validation Handoff

> **For agentic workers:** execute this document as a validation/closeout plan. Do not redesign Arcane Danger or add new hazard semantics unless direct evidence exposes a regression that cannot be fixed inside the frozen contracts. Preserve `plans/DECISIONS.md`, especially D006, D007, D008, D009, D028, D029, D030 and D031.

## Goal

Close the remaining Stage 05A acceptance surface with reproducible real-client, real-modpack and provider evidence while preserving Black Arcana as the sole authority for Arcane Danger, Backlash, Corruption and Arcane Strain.

## Current canonical state

- Baseline used to prepare this handoff: `main@71c9b6bd6ba11b52f24be2d14c03c45207ee6b1c`.
- Minecraft: `1.21.1`.
- NeoForge in the current physical modlist: `21.1.248`.
- Java: `21`.
- Curios in the current physical modlist: `curios-neoforge-9.5.1+1.21.1.jar`, mod id `curios`, version `9.5.1+1.21.1`.
- The current physical modlist does not expose an identifiable top-level RPG Skill Tree JAR. This blocks real loaded-provider acceptance for the RPG integration; it does **not** mean the Black Arcana integration code or automated contract tests are absent.
- Stage 05A state remains `IMPLEMENTED / FINAL VALIDATION DEFERRED`.
- `05A.12` automated hardening is already closed by explicit tests and full runtime gates. This handoff must not repeat those tests merely to manufacture activity.
- `05A.11` real-client presentation acceptance shares the Stage 05 manual campaign in `docs/qa/casting-ux-manual-matrix.md` and `docs/qa/casting-ux-real-client-runbook.md`.
- Deterministic forecast/preflight automated evidence is recorded in `docs/qa/stage05a11-resistance-forecast.md`.
- The removable Stage 05/05A fixture under `docs/qa/fixtures/stage05-real-client/` is QA data only and must not ship as production gameplay content.

## Frozen authority and causal invariants

The validation campaign is required to preserve these contracts:

1. Black Arcana owns danger-profile resolution, hazard preflight, hazard preparation/commit, Backlash, Corruption and Arcane Strain.
2. Stage 05A extends the canonical `ArcanaCastEngine`; it never creates a second cast pipeline.
3. The client may present synchronized forecasts and bounded gate categories but never decides cast legality, resistance truth, cost, cooldown, target admission or world policy.
4. Arcane Resistance and Corruption Resistance remain separate channels. They may not be collapsed into a generic magic-resistance value.
5. Arcane Strain is persistent bounded hazard state, not a second mana pool.
6. D030 remains authoritative: schema-v1 corruption/strain coefficients do not imply per-damage acquisition, unavoidable floors, strain bonus multipliers or a strain hard gate unless a later explicit schema adds those fields.
7. Delayed eligible damage uses the root-cast hazard snapshot. Gear/provider swaps after activation cannot retroactively rewrite that root cast.
8. `ARCANE_BACKLASH` is terminal hazard damage. It may not recurse, crit, lifesteal, trigger ordinary offensive proc chains, award ordinary offensive mastery or create a new root cast.
9. External providers contribute through Black Arcana-owned boundaries. Provider presence never transfers hazard or casting authority.
10. Optional provider failure is fail-closed and isolated; it must not poison valid sibling contributions or make the dedicated server require optional/client-only classes.

If a manual/provider failure appears to require weakening one of these contracts, record an architectural blocker instead of applying the weakening as a bug fix.

## Canonical source set for execution

Read before beginning the campaign:

- `plans/05a-arcane-danger/README.md`
- `plans/05a-arcane-danger/01-arcane-danger-model.md`
- `plans/05a-arcane-danger/02-arcane-resistance.md`
- `plans/05a-arcane-danger/03-corruption-resistance.md`
- `plans/05a-arcane-danger/04-arcane-strain.md`
- `plans/05a-arcane-danger/05-backlash-pipeline.md`
- `plans/05a-arcane-danger/06-equipment.md`
- `plans/05a-arcane-danger/07-curios.md`
- `plans/05a-arcane-danger/08-spell-profiles.md`
- `plans/05a-arcane-danger/09-public-api.md`
- `plans/05a-arcane-danger/10-rpg-skilltree-integration.md`
- `plans/05a-arcane-danger/11-hud-tooltip-preflight.md`
- `plans/05a-arcane-danger/12-tests-hardening.md`
- `plans/DECISIONS.md`
- `plans/STATUS.md`
- `docs/qa/casting-ux-manual-matrix.md`
- `docs/qa/casting-ux-real-client-runbook.md`
- `docs/qa/stage05a11-resistance-forecast.md`

The latest physical modlist is authority for which optional providers are actually present in the QA instance. Notion and project guides are editorial/design sources and do not override current code/tests, `plans/DECISIONS.md` or the physical modlist.

---

## Task 1 — Freeze the exact validation candidate

**Deliverable:** one auditable exact-SHA test candidate and one evidence report header.

- [ ] Fetch the latest `origin/main` immediately before the campaign and record its full SHA.
- [ ] Confirm no open branch/PR contains equivalent 05A closeout work that must be reconciled first.
- [ ] Record the exact physical modlist snapshot used by the client/server test instance.
- [ ] Confirm Minecraft `1.21.1`, NeoForge `21.1.248` and Java `21` for the current target snapshot; if the physical modlist changes before execution, use the newer physical values and record the divergence instead of preserving stale numbers from this handoff.
- [ ] Use the canonical successful `main` CI artifact matching the exact tested SHA. If it is unavailable, build exactly that SHA locally; do not silently substitute a different revision.
- [ ] Create `docs/qa/arcane-danger-final-validation-evidence.md` on the actual closeout branch.
- [ ] Record tested SHA, modlist identification, provider-presence list, Minecraft/NeoForge/Java versions, date, client/server topology and fixture/config variants at the top of the evidence report.
- [ ] Keep the Stage 05/05A fixture out of production data and identify every scenario that depends on it.

**Stop condition:** if the exact candidate cannot start in the intended client/server topology, record `BLOCKED` and fix the launch/runtime regression before treating any downstream observation as validation evidence.

---

## Task 2 — Validate danger profiles and reload behavior in the real instance

**Deliverable:** real-instance evidence that data-driven danger metadata converges safely without changing authority.

- [ ] Exercise at least one canonical normal profile and one non-normal/dangerous profile available in the exact candidate.
- [ ] Confirm the dangerous profile exposes the synchronized tier/minimum/recommended metadata expected by 05A.11 without making the client authoritative.
- [ ] Use the deterministic alternate danger-profile fixture and run `/reload` while the dangerous spell is selected.
- [ ] Confirm the static preflight metadata converges to the reloaded profile.
- [ ] Confirm an in-flight forecast whose tier or thresholds belong to the old profile cannot overwrite the newly synchronized presentation.
- [ ] Confirm malformed or unsupported test data is not introduced as a production workaround; malformed-schema behavior remains covered by the canonical automated tests in 05A.12.
- [ ] Remove the QA fixture after the scenario and verify production data remains unchanged.

### PASS invariants

- reload is data-driven and bounded;
- stale presentation cannot regain authority after reload;
- datapacks remain declarative and non-executable;
- no Java class name, command or script is introduced to satisfy QA.

---

## Task 3 — Validate Arcane/Corruption Resistance providers and snapshot behavior

**Deliverable:** representative real-modpack evidence that available resistance providers contribute through the frozen snapshot model.

### Baseline/equipment

- [ ] Establish a baseline state with no intentional Black Arcana resistance equipment contribution.
- [ ] Equip one canonical Black Arcana resistance source supported by the current production data and record the server-authored forecast change for a selected dangerous spell.
- [ ] Start/commit a root cast whose delayed eligible damage is observable, then change the equipment state after activation where the current spell/fixture permits it.
- [ ] Confirm presentation for a later root cast observes the new provider state while the already-activated root remains governed by its frozen snapshot.

### Curios

The current physical modlist contains Curios `9.5.1+1.21.1`, so Curios acceptance is applicable when a legitimate registered contribution can be equipped in the QA instance.

- [ ] Confirm the Curios integration activates only when its compatible provider boundary is available.
- [ ] Exercise a legitimate Curios resistance contribution without adding a per-tick/global inventory scan.
- [ ] Change/remove the contribution after root-cast activation and verify the next root observes the new state while the prior root remains snapshot-safe.
- [ ] Repeat client forecast refresh after the Curio change and verify convergence without visible stale rollback or per-tick request spam symptoms.

If the exact pack contains Curios but no legitimate registered resistance-contributing Curio, mark the concrete scenario `BLOCKED`; do not add a production debug item solely to obtain a PASS.

### RPG Skill Tree

The current physical modlist does not expose an identifiable sibling RPG Skill Tree JAR.

- [ ] Recheck the latest physical modlist immediately before execution.
- [ ] If a compatible RPG Skill Tree artifact is present, identify its exact file/version/mod id and exercise the real provider contribution through the Black Arcana boundary.
- [ ] If it is still absent, mark real loaded-provider acceptance `BLOCKED — PROVIDER ARTIFACT NOT PRESENT IN QA MODLIST`.
- [ ] Do not convert the existing automated provider/mastery tests into evidence that a real external artifact was loaded.
- [ ] Do not add a second attribute/mastery/resource implementation inside Black Arcana to remove this blocker.

### PASS invariants

- Arcane and Corruption Resistance remain distinct;
- provider values are server-owned snapshots;
- post-activation swaps cannot retroactively rewrite a root;
- optional provider absence/incompatibility fails safely;
- RPG remains a progression/resistance provider only and never owns hazard settlement.

---

## Task 4 — Validate Corruption and Arcane Strain persistence/recovery

**Deliverable:** real-runtime evidence that persistent hazard state follows the frozen lifecycle contract.

Use production-supported ways to acquire non-zero Corruption and Arcane Strain; do not write state directly with a production debug bypass.

- [ ] Record a known non-zero Corruption state after a committed dangerous cast.
- [ ] Record a known non-zero Arcane Strain state after a committed dangerous cast.
- [ ] Disconnect/reconnect the same player and confirm neither channel is silently cleansed.
- [ ] Exercise normal Strain lazy recovery over elapsed server gameplay time and confirm it decreases only through the defined recovery path.
- [ ] Die/respawn through the real player lifecycle and confirm death is not a cleanse path for either persistent channel.
- [ ] Restart the server/world using the same save and confirm persisted hazard state reconstructs correctly.
- [ ] Confirm a cancelled/failed cast that never reaches successful hazard commit does not invent persistent Corruption or Strain.

### Presentation boundary

- [ ] Do not add a client Corruption/Strain meter to make these checks easier.
- [ ] Use server-owned evidence/logical inspection supported by the existing runtime/QA facilities.
- [ ] Corruption/Strain client values remain intentionally absent until a separate bounded synchronization contract is explicitly approved.

A persistence failure is release-blocking for Stage 05A even if the corresponding unit/GameTest remains green.

---

## Task 5 — Validate Backlash causality in representative real-modpack interactions

**Deliverable:** representative runtime evidence that Backlash remains causal, terminal and non-offensive.

05A.12 already provides deterministic automated coverage for direct/AoE/multi-hit/projectile/DoT/chain/owned-summon attribution, dedupe, ledger bounds, concurrency, protection and offensive-credit exclusions. The real-modpack campaign therefore samples those contracts instead of reproducing the entire automated matrix manually.

- [ ] Exercise one canonical linear dangerous profile at zero effective Arcane Resistance and record that its eligible causal confirmed damage produces the expected 1:1 Backlash relationship defined by the profile/invariant.
- [ ] Repeat the same profile with a legitimate non-zero Arcane Resistance state and record a finite reduced Backlash result consistent with server-owned computation.
- [ ] Exercise one delayed or multi-hit hazard path available in the candidate and verify settlement remains associated with the original root cast.
- [ ] Confirm terminal Backlash damage does not visibly start another Black Arcana cast or recursive Backlash cycle.
- [ ] Where the loaded pack exposes normal offensive lifesteal/on-hit/mastery/proc surfaces, observe that Backlash does not receive ordinary offensive credit from Black Arcana-owned pathways.
- [ ] If a third-party mod reacts generically to all Minecraft damage despite Black Arcana provenance exclusions, record the exact provider/event as an integration finding; do not silently add provider-specific suppression without verifying a safe hook and authority boundary.

### Protection boundary

- [ ] In any PvP/team/protected-area scenario exercised, preserve Stage 04 `EntityInteractionAdmissionService` authority.
- [ ] A denied interaction must not be converted into eligible confirmed damage solely to test Backlash.
- [ ] Do not create parallel protection heuristics in 05A.

---

## Task 6 — Execute the shared 05A.11 real-client presentation campaign

**Deliverable:** direct client evidence for the 05A rows already represented in the canonical Stage 05 manual matrix.

Use `docs/qa/casting-ux-real-client-runbook.md` and record the results in the Stage 05 evidence report required by its handoff plus the 05A final evidence report when the row also proves a hazard contract.

### Hazard forecast thresholds

For one selected non-normal spell, exercise server-authored effective Arcane Resistance:

- [ ] below minimum;
- [ ] between minimum and recommended;
- [ ] at or above recommended.

Verify that current/minimum/recommended values and factual status remain synchronized server presentation. `recommendation met` may not imply that all Backlash risk is eliminated.

### Predictable gate categories

Exercise only legitimate production/fixture states:

- [ ] `CLEAR`;
- [ ] `COOLDOWN`;
- [ ] `COST`.

If identity/loadout, progression or unavailable projection cannot be created without changing production semantics, preserve the canonical runbook result as `BLOCKED` rather than inventing a debug bypass.

### Provider refresh and fail-closed presentation

- [ ] Change applicable equipment/Curios/RPG resistance sources while the spell remains selected and verify forecast refresh converges to the latest server result.
- [ ] Verify lower/older request ids cannot visibly overwrite a newer response.
- [ ] Exercise preview provider unavailable/incompatible behavior when a legitimate reproducible configuration exists.
- [ ] Confirm the client shows `Unavailable` or synchronized static fallback and never presents a known-partial value as complete.
- [ ] Disconnect/reconnect and confirm stale hazard/gate state does not flash as current authority before fresh snapshots arrive.

### Traffic boundary

- [ ] Confirm normal idle play does not cause visible symptoms of per-tick forecast traffic.
- [ ] Confirm `MINIMAL` feedback mode does not leave unnecessary forecast/gate presentation activity visible.
- [ ] Do not introduce a packet trace requirement if the current QA environment cannot observe it; deterministic rate/request-id bounds remain automated evidence from `docs/qa/stage05a11-resistance-forecast.md`.

---

## Task 7 — Validate optional-provider and dedicated-server isolation

**Deliverable:** an explicit provider acceptance ledger that distinguishes automated contracts from physically loaded providers.

For each relevant provider, record:

- exact mod/JAR identity from the physical modlist;
- version/mod id when present;
- whether a Black Arcana adapter/provider boundary is active;
- scenario exercised;
- result `PASS`, `FAIL` or `BLOCKED`;
- whether the evidence is real-provider or automated test-double/contract evidence.

### Required classifications for the current snapshot

- Curios: physically present (`9.5.1+1.21.1`); real-provider acceptance is applicable only if a legitimate registered contribution exists.
- RPG Skill Tree: no identifiable physical JAR in the current modlist; real-provider acceptance is currently `BLOCKED` pending an actual compatible artifact.
- Black Arcana baseline/equipment providers: core and applicable.

- [ ] Start or use the canonical dedicated-server smoke topology without requiring client-only classes.
- [ ] Confirm absence of an optional provider does not prevent server startup.
- [ ] Confirm an unavailable/incompatible optional provider fails closed without deleting valid baseline/equipment contributions.
- [ ] Do not declare third-party compatibility from thematic similarity or from a test double.

---

## Task 8 — Evidence reconciliation and regression loop

**Deliverable:** one auditable 05A evidence document and no unsupported status promotion.

Use these result states:

- `PASS` — the applicable expected behavior was directly observed with the stated exact candidate/provider topology;
- `FAIL` — the observed behavior contradicts the frozen contract;
- `BLOCKED` — the scenario cannot be legitimately exercised in the current physical/provider topology;
- `NOT APPLICABLE / CARRIED TO STAGE 09` — only for presentation/performance acceptance already permitted to move to the accumulated Stage 09 release campaign.

For each row/scenario record:

- Stage task / scenario;
- tested commit SHA;
- physical modlist/provider identity;
- client/server topology;
- relevant config/data fixture;
- steps performed;
- observed result;
- expected contract;
- evidence reference;
- result classification.

For every `FAIL`:

1. reproduce on the same exact SHA;
2. identify the smallest frozen contract violated;
3. add a focused regression test where the deterministic cause can be represented automatically;
4. run the regression RED before the fix;
5. implement the minimum correction without changing authority/identity semantics;
6. run the focused test GREEN;
7. run the relevant broader automated gate;
8. repeat the failed real scenario on the new exact SHA;
9. update only the evidence rows actually rerun.

If the fix would change hazard identity, resistance channels, D030 coefficient semantics, casting transaction order, provider authority or Backlash exclusions, stop and register an architectural decision/blocker before implementation.

---

## Task 9 — Stage 05A closeout gate

**Deliverable:** Stage 05A state changes only after direct evidence and fresh post-reconciliation CI justify it.

### Preconditions

- [ ] `05A.12` automated hardening remains green on the final reconciled runtime.
- [ ] Every applicable real-client 05A.11 row has direct evidence or an explicitly legitimate `BLOCKED`/Stage-09 carry classification.
- [ ] Core/equipment real-modpack hazard acceptance has no unresolved `FAIL`.
- [ ] Corruption/Strain persistence/recovery has no unresolved `FAIL`.
- [ ] Representative Backlash causality/non-recursion acceptance has no unresolved `FAIL`.
- [ ] Curios real-provider acceptance is recorded when a legitimate contributing Curio is available; otherwise the exact blocker is recorded.
- [ ] RPG Skill Tree loaded-provider acceptance is either performed against an exact compatible physical artifact or remains explicitly `BLOCKED`; no test double is promoted to real-provider evidence.
- [ ] No unresolved finding weakens D028–D031 or Stage 04 authority.

### Final synchronization

Immediately before finalizing the closeout PR:

1. fetch the latest `origin/main` and record its SHA;
2. reconcile `origin/main` into the closeout branch without discarding concurrent work;
3. review `main..HEAD` semantically;
4. if reconciliation changes any 05A runtime/client/provider surface used by the campaign, rerun the affected real scenarios on the reconciled exact SHA;
5. rerun the full canonical CI on the reconciled HEAD;
6. resolve every review thread;
7. repeat synchronization if `main` advances again in a relevant area before merge.

CI or manual evidence produced before the last relevant synchronization is not final evidence.

### Status files eligible for promotion only after the gate

- applicable task files under `plans/05a-arcane-danger/`;
- `plans/05a-arcane-danger/README.md`;
- `plans/STATUS.md`;
- `docs/qa/casting-ux-manual-matrix.md` only for rows directly exercised through the shared Stage 05/05A campaign;
- `docs/qa/arcane-danger-final-validation-evidence.md` as the evidence ledger.

Do not change those states merely because this handoff exists.

### Merge and post-merge proof

The closeout PR may merge only after:

- final relevant manual/provider evidence is reconciled to the HEAD under review;
- full CI is GREEN on that reconciled HEAD;
- the final diff preserves server authority, Backlash exclusions and provider boundaries;
- all review threads are resolved.

After merge:

- fetch `main` and record the actual merge SHA;
- confirm the post-merge workflow runs on that exact SHA;
- require the canonical post-merge gate, including dedicated-server smoke and main-only QA artifact publication, to finish successfully before claiming Stage 05A validated.

---

## Non-goals

This handoff does **not** authorize:

- a second mana/resource pool;
- a second cast or hazard pipeline;
- client-side resistance/hazard/gate authority;
- merging Arcane Resistance and Corruption Resistance;
- treating Arcane Strain as mana;
- inferring D030 semantics not present in the current profile schema;
- a new client Corruption/Strain meter without a separately approved bounded sync contract;
- production debug bypasses solely to obtain PASS evidence;
- per-tick global equipment/Curios/RPG scans;
- provider-specific hooks invented without exact API evidence;
- transferring hazard authority to RPG Skill Tree or another provider;
- classifying automated mocks/test doubles as real-provider QA;
- weakening/deleting automated or manual gates to obtain green;
- adding new dangerous spell content as part of validation.

## Closure statement template

Use only after the closeout gate is actually satisfied:

> Stage 05A Arcane Danger was validated on exact candidate `<tested-main-sha>` using the recorded Minecraft 1.21.1 / NeoForge / Java / provider topology in `docs/qa/arcane-danger-final-validation-evidence.md`. Applicable real-client and real-modpack rows are PASS or explicitly classified under the approved blocked/Stage-09 rules; all implementation failures were fixed and rerun. Final reconciled HEAD `<head-sha>` passed the complete automated gate, the closeout PR merged as `<merge-sha>`, and exact-SHA post-merge workflow `<workflow-run>` completed GREEN with canonical QA artifact publication.

Until those values exist as real evidence, Stage 05A remains `IMPLEMENTED / FINAL VALIDATION DEFERRED`.