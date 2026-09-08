# 06.05 — Rituals Final Validation Handoff

> **For agentic workers:** execute this document as a validation/closeout plan. Do not redesign the Stage 06 ritual runtime or invent provider hooks to make a manual row pass. Preserve `plans/DECISIONS.md`, especially D006–D009, D011, D028–D031, and preserve the canonical Stage 06 implementation merged by PR #43.

## Goal

Close the remaining Stage 06 real-modpack/provider acceptance surface with reproducible exact-SHA evidence while keeping Black Arcana authoritative for ritual identity, lifecycle, persistence, completion accounting, progression-facing outcomes and world safety.

## Current canonical state

- Baseline used to prepare this handoff: `main@0138e994bf2390d4903277a8d945baabf9b8c733`.
- Stage 06 implementation is canonical via PR #43, merge `4a79d440a4bba3920002eb8fc49a520e15744c48`.
- Stage 06 state remains `IMPLEMENTED / FINAL VALIDATION DEFERRED` under D031.
- Minecraft: `1.21.1`.
- NeoForge in the current physical modlist: `21.1.248`.
- Java: `21`.
- Current physical Eidolon artifact: `eidolon_repraised-1.21.1-0.5.0.2.jar`, mod id `eidolon_repraised`, version `0.5.0.2`.
- Current physical Malum artifact: `malum-1.21.1-1.8.2.jar`, mod id `malum`, version `1.8.2`.
- PR #43's post-merge workflow `33561613644` already passed the complete automated gate and published the canonical Stage 06 artifact for that historical merge SHA. That evidence proves the implemented contracts; it is not real-modpack/manual provider acceptance.
- The current `main` contains later Stages and documentation. Final Stage 06 acceptance must therefore test a fresh exact candidate from the latest reconciled `main`, not reuse the historical PR #43 artifact as if it represented the current release candidate.

## Frozen runtime facts

The closeout campaign must preserve the implementation that actually exists:

1. `RitualEngine` is the single Black Arcana activation/interruption/completion pipeline.
2. Ritual definitions, bindings, active sessions, replay claims and completion accounting are bounded server-owned state.
3. Requirements are checked before component reservation where possible.
4. Components are reserved/committed at the ritual commit phase. A pre-commit interruption consumes nothing; a post-commit interruption does not retroactively refund committed components.
5. Provider/runtime failures fail closed before outcome execution.
6. Active ritual sessions are persisted/restored with bounded parsing; completion uses a separate exactly-once completion ledger.
7. Ritual anchors do not create implicit chunk tickets. The runtime processes bounded active sessions rather than globally scanning structures every tick.
8. World mutation remains subject to Stage 04 policy. Stage 06 does not own a bypass around `WorldEffectPolicy`/protection admission.
9. Stage 05A remains the authority for Arcane Danger, Backlash, Corruption and Arcane Strain. Rituals may consume those contracts when a production ritual explicitly does so; Stage 06 must not invent parallel hazard semantics.
10. Optional Eidolon/Malum integration remains behind Black Arcana-owned boundaries. Provider presence never transfers Black Arcana progression, completion or world-safety authority.

If a real-modpack finding appears to require changing ritual identity, transaction phase, persistence ownership, provider authority or Stage 04/05A boundaries, stop and register an architectural blocker before implementing the change.

## Canonical production representatives

### Eidolon — `black_arcana:eidolon_anchor_attunement`

The current production bridge uses Eidolon Repraised's public ritual API and recipe host.

Current recipe contract:

- type: `eidolon_repraised:ritual_brazier`;
- core: `minecraft:echo_shard`;
- sacrifices: `minecraft:soul_sand`, `minecraft:amethyst_shard`, `minecraft:ender_pearl`, `minecraft:crying_obsidian`;
- health cost: `6.0`;
- ritual id: `black_arcana:eidolon_anchor_attunement`;
- loaded only when `eidolon_repraised` is present.

The public Eidolon start hook used by the current version does not provide caster identity. The Black Arcana durable result is therefore intentionally **anchor-scoped**, using the dimension + ritual position in `RitualCompletionSavedData`. Do not rewrite this acceptance criterion as a player-scoped unlock and do not guess a nearby caster.

Registration is ownership-safe: an existing third-party ritual under a Black Arcana-owned id must fail instead of being silently replaced.

### Black Arcana/Malum — `black_arcana:veil_anchor_consecration`

The representative native grand ritual is defined with:

- commit delay: `100` ticks;
- completion delay: `400` ticks;
- Malum component requirements: `4 arcane` spirits + `2 wicked` spirits;
- caster must remain online;
- anchor dimension must exist on the server;
- anchor chunk must already be loaded;
- completion is caster-scoped and exactly-once through `RitualCompletionSavedData`.

The current code installs the definition/binding when the verified Malum integration is available. **Do not assume that a player-facing production activation ingress exists merely because the definition and binding exist.** Task 4 explicitly audits that surface first. If no legitimate in-world/player ingress exists in the exact candidate, real-player acceptance for this ritual is `BLOCKED — NO CANONICAL PLAYER ACTIVATION SURFACE`; do not add a debug command/item solely to manufacture PASS evidence.

## Canonical source set for execution

Read before beginning the campaign:

- `plans/06-rituals/README.md`
- `plans/06-rituals/✅-01-ritual-contracts.md`
- `plans/06-rituals/✅-02-eidolon-ritual-bridge.md`
- `plans/06-rituals/✅-03-malum-spirit-components.md`
- `plans/06-rituals/✅-04-grand-rituals.md`
- `plans/DECISIONS.md`
- `plans/STATUS.md`
- `src/main/java/dev/gustavopere/blackarcana/core/ritual/`
- `src/main/java/dev/gustavopere/blackarcana/integration/eidolon/`
- `src/main/java/dev/gustavopere/blackarcana/integration/malum/`
- `src/main/resources/data/black_arcana/recipe/rituals/eidolon_anchor_attunement.json`
- Stage 06 unit/integration/persistence tests under `src/test/java/dev/gustavopere/blackarcana/`

The latest physical modlist is authority for provider presence/version. Notion and project guides are design/editorial context and do not override the current implementation, `plans/STATUS.md`, `plans/DECISIONS.md` or exact provider code/API evidence.

---

## Task 1 — Freeze the exact validation candidate

**Deliverable:** one exact-SHA candidate and a Stage 06 evidence ledger.

- [ ] Fetch latest `origin/main` immediately before the campaign and record the full SHA.
- [ ] Confirm no open Stage 06 validation branch/PR contains equivalent work that must be reconciled first.
- [ ] Record the exact physical modlist snapshot used by the test instance.
- [ ] Record Minecraft, NeoForge and Java versions from that physical instance.
- [ ] Record exact Eidolon and Malum JAR names, mod ids and versions from the same instance.
- [ ] Use the canonical successful CI artifact matching the exact candidate SHA. If unavailable, build exactly that SHA; never substitute a nearby commit.
- [ ] Create `docs/qa/rituals-final-validation-evidence.md` on the actual closeout branch.
- [ ] Record topology: integrated client/server or dedicated server, world/save identity, player identities used for multiplayer/restart rows, relevant provider/config variants, and exact candidate SHA.

**Stop condition:** if the exact candidate cannot start with the intended physical provider topology, classify the launch scenario `FAIL` or `BLOCKED` from direct evidence before attempting downstream ritual acceptance.

---

## Task 2 — Validate Eidolon host registration and recipe gating

**Deliverable:** real-provider evidence that `eidolon_anchor_attunement` is hosted by Eidolon Repraised without transferring Black Arcana authority.

- [ ] Start the exact modpack candidate with Eidolon Repraised present.
- [ ] Confirm the Black Arcana ritual recipe is available through the legitimate Eidolon ritual-brazier path.
- [ ] Confirm the recipe uses the production component set and `6.0` health cost rather than a QA-only substitute.
- [ ] Execute the recipe through the real Eidolon host.
- [ ] Record observed consumption/health-cost behavior from the host.
- [ ] Record server evidence that the Black Arcana anchor completion was `RECORDED` for the ritual anchor.
- [ ] Confirm the result is anchor-scoped. Do not claim a player-specific unlock from this ritual.
- [ ] Attempt the same completed anchor again when the host permits a legitimate repeat and record that durable completion remains exactly-once (`ALREADY_COMPLETED` rather than a second durable reward).
- [ ] Restart the same server/world and verify the anchor-scoped completion record remains present.

### Registration ownership

- [ ] Verify normal startup does not silently replace a foreign ritual registration.
- [ ] Do not inject an id collision into a production pack merely for manual testing; the deterministic ownership-collision invariant remains automated evidence unless a safe isolated QA variant is deliberately prepared.

### Provider-absence variant

- [ ] If a legitimate Eidolon-absent QA profile exists, boot the same Black Arcana candidate without Eidolon Repraised and confirm the conditional recipe/host content is absent without making the server fail to start.
- [ ] If no legitimate provider-absence profile exists, record this row `BLOCKED — NO CONTROLLED EIDOLON-ABSENT QA PROFILE`; do not mutate the user's production instance ad hoc.

### PASS invariants

- Eidolon provides host/presentation only;
- the Black Arcana ritual id is ownership-safe;
- the durable BA result is server-owned and anchor-scoped;
- missing Eidolon never turns the ritual into a free fallback;
- no internal Eidolon patching is introduced to make validation pass.

---

## Task 3 — Audit the real Malum provider boundary before ritual execution

**Deliverable:** proof that the current physical Malum artifact activates the verified integration path used by Stage 06.

- [ ] Confirm current physical Malum is the exact artifact recorded in Task 1.
- [ ] Confirm server startup reports the Black Arcana Malum integration as available before treating any spirit-backed ritual as applicable.
- [ ] Confirm `veil_anchor_consecration` is installed only when that integration path is available.
- [ ] Confirm the production requirements remain exactly `4 arcane` + `2 wicked` spirits.
- [ ] Do not substitute synthetic/test spirit access for real-provider evidence.
- [ ] If the current Malum artifact is present but the Black Arcana bridge reports unavailable/incompatible, mark the provider row `FAIL` or `BLOCKED` according to the observed diagnostic and do not fall through to a free ritual.

The Stage 06 automated tests remain the authority for synthetic provider failure injection. This manual task is about the physically loaded provider.

---

## Task 4 — Audit the production activation surface for `veil_anchor_consecration`

**Deliverable:** a definitive answer on whether the native grand ritual is reachable through a legitimate production player/server flow in the exact candidate.

- [ ] Inspect the current production UI/block/item/event/network/server entrypoints that can reach `RitualEngine.start(...)` for this ritual.
- [ ] Identify the exact player-facing/server-owned activation mechanism if one exists.
- [ ] Confirm that mechanism creates a server-owned `RitualActivationId`, `RitualContext` and `RitualAnchor` without accepting client authority over ritual result/cost/state.
- [ ] Record the concrete entrypoint in the evidence ledger before executing Task 5.

If no canonical production activation surface exists:

- mark Tasks 5–8 rows requiring real grand-ritual activation as `BLOCKED — NO CANONICAL PLAYER ACTIVATION SURFACE`;
- do not create a temporary production command, debug item, client packet or second ritual pipeline solely to obtain a PASS;
- record this as a Stage 06 validation blocker requiring a separately reviewed product/architecture decision if real-player grand-ritual usability is required for `VALIDATED / COMPLETE`.

A unit test or direct Java call to `runtime.rituals().start(...)` is automated/runtime evidence, not proof of a production player ingress.

---

## Task 5 — Validate native grand-ritual transaction phases

**Applicability:** execute only after Task 4 identifies a legitimate production activation surface.

**Deliverable:** real-runtime evidence for precommit, commit, interruption and completion semantics.

Use a fresh caster without an existing completion record.

### Requirement failures before consumption

- [ ] Attempt with fewer than `4 arcane` spirits and confirm denial/no consumption.
- [ ] Attempt with enough arcane but fewer than `2 wicked` spirits and confirm denial/no consumption.
- [ ] Attempt with correct total count but wrong spirit affinity where a legitimate inventory setup permits it; confirm typed requirements do not collapse to generic quantity.
- [ ] Attempt while caster requirement, dimension or loaded-chunk condition is legitimately false when the production activation surface allows the scenario; confirm fail-closed/no outcome.

### Precommit interruption

- [ ] Start with all requirements satisfied.
- [ ] Interrupt before the 100-tick commit boundary through a legitimate gameplay/lifecycle interruption supported by the production surface.
- [ ] Confirm the session ends and no Malum spirits were committed.
- [ ] Confirm no completion record was created.

### Commit and post-commit interruption

- [ ] Start another valid activation.
- [ ] Allow it to cross the 100-tick commit boundary.
- [ ] Confirm exactly `4 arcane` and `2 wicked` spirits were committed once.
- [ ] Interrupt after commit but before the 400-tick completion boundary through a legitimate supported path.
- [ ] Confirm the committed components are not retroactively refunded.
- [ ] Confirm no completion reward/record is invented by the interrupted session.

### Successful completion

- [ ] Start a fresh valid activation.
- [ ] Keep caster online, dimension available and anchor chunk loaded through completion.
- [ ] Confirm components commit exactly once.
- [ ] Confirm completion is recorded exactly once for the caster.
- [ ] Confirm a later activation for the same completed caster is denied by the completion gate rather than producing a second reward.

Do not infer exact component or completion behavior from visual effects alone; record server-owned evidence plus before/after provider state.

---

## Task 6 — Validate duplicate activation and multiplayer ownership

**Applicability:** real grand-ritual rows require Task 4 to have found a production activation surface.

**Deliverable:** direct evidence that one anchor/session cannot be raced into double consumption or double completion.

- [ ] Have two legitimate activation attempts target the same ritual anchor as close together as the production interface permits.
- [ ] Confirm only one active session owns the anchor.
- [ ] Confirm the losing attempt does not consume ritual components.
- [ ] Re-submit/replay the same activation identity only if the production protocol legitimately allows observing that identity; otherwise keep replay-id injection as automated evidence.
- [ ] Confirm a second player can complete their own caster-scoped `veil_anchor_consecration` when all requirements are independently satisfied and the completion ledger has capacity.
- [ ] Confirm one player's completion record does not satisfy or block another player's caster-scoped completion key except through shared anchor/session exclusion while an activation is active.

Do not weaken synchronization or invent client-supplied activation ids to force a race scenario.

---

## Task 7 — Validate chunk lifecycle, disconnect and restart persistence

**Applicability:** exercise only through production-supported activation/lifecycle paths.

**Deliverable:** real save/restart evidence for active ritual sessions and exactly-once completion.

### Active session lifecycle

- [ ] Start a valid ritual and record whether it is PRECOMMIT or COMMITTED before stopping/restarting the server.
- [ ] Restart using the same save and exact candidate.
- [ ] Confirm the bounded session restore either restores the valid session or rejects it according to the canonical restore contract; record the observed state rather than assuming continuation.
- [ ] Confirm restore does not duplicate activation ownership or create a second session on the same anchor.
- [ ] Confirm malformed-state sanitation remains automated evidence unless a safe isolated save-copy migration test is deliberately prepared.

### Chunk lifecycle

- [ ] Verify the ritual does not force-load its anchor chunk merely because a session exists.
- [ ] If the chunk unloads through normal gameplay before the grand ritual completes, record the canonical observed behavior and ensure no global scanning/implicit chunk ticket appears.
- [ ] Because `veil_anchor_consecration` requirements demand an already-loaded chunk at admission, do not reinterpret that check as permission to force-load it.

### Completion persistence

- [ ] Complete the ritual once.
- [ ] Restart the same world.
- [ ] Confirm the completion record still prevents duplicate reward for the same completion key.
- [ ] Repeat the same persistence check for Eidolon's anchor-scoped completion record from Task 2.

A restart result that duplicates cost or reward is release-blocking for Stage 06.

---

## Task 8 — Validate optional-provider isolation

**Deliverable:** an acceptance ledger that distinguishes real provider evidence from automated test doubles.

For each Stage 06 provider, record:

- JAR name;
- mod id;
- version;
- Black Arcana bridge availability/diagnostic;
- ritual/content affected;
- scenario exercised;
- `PASS`, `FAIL` or `BLOCKED`;
- evidence type: `REAL PROVIDER` or `AUTOMATED CONTRACT`.

### Eidolon

- [ ] Presence: verify `eidolon_anchor_attunement` recipe/registration with the real provider.
- [ ] Absence/incompatibility: verify only in a controlled provider-variant profile; otherwise classify `BLOCKED`.

### Malum

- [ ] Presence: verify real typed-spirit access before grand-ritual acceptance.
- [ ] Absence/incompatibility: dependent Malum ritual components/content must disable/fail closed, never become free.
- [ ] Confirm Black Arcana core ritual classes and unrelated content do not require Malum classes to load on a provider-absent dedicated server profile when that profile is legitimately available.

### RPG Skill Tree

RPG Skill Tree is not a required owner of Stage 06 ritual runtime. The current Malum bootstrap may optionally pass an RPG bridge to separate synthetic content, but the canonical `veil_anchor_consecration` spirit requirement/completion path does not transfer ritual authority to RPG.

- [ ] Do not make Stage 06 closure depend on a sibling RPG artifact unless a specific production ritual requirement is shown by current code/data.
- [ ] Do not implement a second progression/resource system inside Black Arcana to compensate for an unavailable sibling provider.

---

## Task 9 — Validate Stage 04 and Stage 05A boundaries where applicable

**Deliverable:** proof that ritual validation does not create an authority bypass.

- [ ] For any Stage 06 outcome that mutates the world in the exact production candidate, verify the mutation reaches the existing Stage 04 world-safety admission path.
- [ ] If the two current representative rituals only record durable completion and do not perform a world mutation, record `NOT APPLICABLE` rather than inventing a mutation to test the policy.
- [ ] For any production ritual explicitly configured to incur Arcane Danger, verify it consumes Stage 05A hazard contracts without creating ritual-local Backlash/Corruption/Strain calculations.
- [ ] If no current production Stage 06 ritual is hazard-bearing, record `NOT APPLICABLE`; do not add danger semantics solely for QA.
- [ ] Provider-hosted effects may not bypass Black Arcana progression/world-safety requirements for Black Arcana-owned outcomes.

---

## Task 10 — Dedicated-server and bounded-work acceptance

**Deliverable:** real runtime evidence that Stage 06 stays server-safe and bounded in the target topology.

- [ ] Start the exact release candidate in the canonical dedicated-server topology.
- [ ] Confirm Stage 06 does not require client-only Eidolon/Malum classes on the server path.
- [ ] Confirm normal idle operation does not scan the whole world for ritual structures.
- [ ] With one or more active rituals, confirm processing remains tied to the active-session registry rather than world/chunk-wide scans.
- [ ] Confirm no ritual creates an implicit chunk ticket/force-load requirement.
- [ ] Treat deterministic registry/session bounds, replay retention and per-tick session limits as automated evidence unless the real server exposes a legitimate way to observe them without artificial overload.

Do not stress a production save with thousands of synthetic activations merely to duplicate unit-test capacity coverage.

---

## Task 11 — Evidence reconciliation and regression loop

**Deliverable:** one auditable `docs/qa/rituals-final-validation-evidence.md` with no unsupported promotion.

Use these result states:

- `PASS` — the applicable expected behavior was directly observed with the stated exact candidate/provider topology;
- `FAIL` — observed behavior contradicts the frozen Stage 06 contract;
- `BLOCKED` — the scenario cannot be legitimately exercised in the current physical/provider/product topology;
- `NOT APPLICABLE` — the exact production ritual does not exercise that boundary;
- `CARRIED TO STAGE 09` — only for a release-level performance/modpack-combination row that D031 legitimately permits to remain in the accumulated final campaign.

For every scenario record:

- Stage task / scenario;
- exact tested commit SHA;
- physical provider JAR/version/mod id;
- client/server topology;
- activation surface used;
- relevant world/save/player identity;
- preconditions/components;
- steps;
- expected contract;
- observed result;
- evidence reference;
- classification.

For every `FAIL`:

1. reproduce on the same exact SHA;
2. locate the violated existing contract;
3. add a focused automated regression where the deterministic cause is representable;
4. prove RED before the fix;
5. implement the smallest correction without changing authority/identity/transaction semantics;
6. prove the focused regression GREEN;
7. run the relevant broader automated gates;
8. rerun the failed real-modpack scenario on the corrected exact SHA;
9. update only evidence rows actually rerun.

If the required correction changes ritual identity, commit/refund semantics, completion-key scope, persistence schema ownership, provider authority, world-safety admission or hazard ownership, stop and require an explicit architectural decision/review before implementation.

---

## Task 12 — Stage 06 closeout gate

**Deliverable:** promote Stage 06 only when direct evidence justifies it.

### Preconditions

- [ ] All four existing Stage 06 implementation tasks remain canonical and automated-green on the final reconciled code.
- [ ] Real Eidolon `eidolon_anchor_attunement` host/recipe execution has direct evidence with the exact physical provider.
- [ ] Eidolon anchor-scoped completion persistence/exactly-once behavior has no unresolved `FAIL`.
- [ ] Real Malum bridge availability/typed-spirit access is directly evidenced when Malum is present.
- [ ] A legitimate production activation surface for `veil_anchor_consecration` is identified and exercised, **or** the absence is explicitly recorded as a Stage 06 validation blocker rather than silently waived.
- [ ] Applicable grand-ritual transaction/interruption/completion rows have no unresolved `FAIL`.
- [ ] Applicable session/restart/completion-ledger rows have no unresolved `FAIL`.
- [ ] Optional-provider absence/incompatibility rows are either directly evidenced in controlled profiles or honestly `BLOCKED`; no test double is promoted to real-provider proof.
- [ ] Stage 04/05A boundaries remain intact.
- [ ] No unresolved finding requires a new duplicate ritual, casting, resource, progression or hazard pipeline.

### Promotion rule

A `BLOCKED — NO CANONICAL PLAYER ACTIVATION SURFACE` result for the representative Black Arcana grand ritual prevents Stage 06 from becoming `VALIDATED / COMPLETE`, because the existing Stage 06 exit criterion requires at least one Black Arcana grand ritual to execute transactionally. It does **not** erase the already-canonical implementation or automated evidence; the state remains `IMPLEMENTED / FINAL VALIDATION DEFERRED` until a separately approved production ingress exists and is validated.

Provider-absence variants that cannot be safely reproduced may remain explicit `BLOCKED` under D031 when the presence-path is directly validated and automated fail-closed coverage remains green. Do not reinterpret `BLOCKED` as `PASS`.

### Final synchronization

Immediately before finalizing a future Stage 06 closeout PR:

1. fetch latest `origin/main` and record the SHA;
2. reconcile `origin/main` into the closeout branch without discarding concurrent work;
3. review `main..HEAD` semantically;
4. rerun every real scenario affected by reconciliation on the new exact SHA;
5. rerun the complete canonical CI on that reconciled HEAD;
6. resolve all review threads;
7. repeat synchronization if `main` advances again in a relevant area before merge.

CI/manual evidence from before the last relevant synchronization is not final evidence.

### Status files eligible for promotion only after the gate

- `plans/06-rituals/README.md`;
- applicable Stage 06 task files only if their wording truly requires an evidence-state adjustment;
- `plans/STATUS.md`;
- `docs/qa/rituals-final-validation-evidence.md`.

Do not alter those validation states merely because this handoff exists.

### Merge and post-merge proof

A future closeout PR may merge only after:

- applicable real-provider/manual evidence is reconciled to the reviewed HEAD;
- full CI is GREEN on that reconciled HEAD;
- all review threads are resolved;
- the final diff preserves ritual/server/provider/world-safety/hazard boundaries.

After merge:

- fetch `main` and record the actual merge SHA;
- confirm the post-merge workflow runs on that exact SHA;
- require the canonical post-merge gate, including dedicated-server smoke and main-only QA artifact publication, to finish successfully before claiming Stage 06 `VALIDATED / COMPLETE`.

---

## Non-goals

This handoff does **not** authorize:

- a second ritual engine or alternate completion ledger;
- client-authoritative ritual activation/result/cost state;
- arbitrary global/per-tick ritual structure scans;
- implicit ritual chunk force-loading;
- genericizing typed Malum spirits into an interchangeable resource;
- making a missing optional provider produce free components/results;
- guessing an Eidolon caster identity not supplied by the verified public hook;
- changing anchor-scoped Eidolon completion into player-scoped completion without a new verified provider contract;
- a production debug command/item/packet solely to obtain manual PASS;
- direct patching of Eidolon/Malum internals when the supported boundary is insufficient;
- moving Black Arcana ritual/progression/world-safety authority into Eidolon, Malum or RPG Skill Tree;
- adding ritual-local Backlash/Corruption/Strain implementations;
- bypassing Stage 04 `WorldEffectPolicy` for grand outcomes;
- weakening, deleting or relabeling automated/manual gates to obtain green;
- adding new ritual content as part of this validation handoff.

## Closure statement template

Use only after the closeout gate is actually satisfied:

> Stage 06 Rituals was validated on exact candidate `<tested-main-sha>` with the physical provider topology recorded in `docs/qa/rituals-final-validation-evidence.md`. The Eidolon-hosted anchor ritual and Black Arcana grand ritual were exercised through their canonical production surfaces; applicable transaction, provider, persistence, duplicate-completion, lifecycle and world-safety rows are PASS or explicitly classified under the approved D031 rules. Final reconciled HEAD `<head-sha>` passed the complete automated gate, the closeout PR merged as `<merge-sha>`, and exact-SHA post-merge workflow `<workflow-run>` completed GREEN with canonical QA artifact publication.

Until those values exist as direct evidence, Stage 06 remains `IMPLEMENTED / FINAL VALIDATION DEFERRED`.
