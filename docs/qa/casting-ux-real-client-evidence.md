# Stage 05 / 05A — Real-client QA Evidence

## State

`PREPARED / MANUAL EXECUTION NOT STARTED`

This ledger is the evidence target required by `plans/05-casting-ux/05-final-client-validation-handoff.md` and `docs/qa/casting-ux-real-client-runbook.md`.

It currently records **campaign preparation only**. No Minecraft client observation has been performed through this ledger, no manual matrix row is PASS/FAIL/BLOCKED from this file, and `docs/qa/casting-ux-manual-matrix.md` remains unchanged.

Automated CI, artifact publication, repository inspection and fixture availability are supporting/preflight evidence only. They do not satisfy any row that requires direct real-client observation.

---

## 1. Candidate build freeze

This candidate was frozen before manual execution so the later evidence can identify one exact build rather than an approximate branch state.

- Repository: `Gustavaopere/Black-Arcana`
- Candidate `main` SHA: `d103b259eed27705b2d4e44cbec60d78d4228054`
- Candidate commit: merge of PR #133, `docs: catalog Ars Zero 2.0.2 provider`
- Automated workflow: `Black Arcana CI`
- Workflow run number: `#2123`
- Workflow run ID: `34293089532`
- Workflow conclusion: `SUCCESS`
- Canonical QA artifact: `black-arcana-d103b259eed27705b2d4e44cbec60d78d4228054`
- Artifact ID: `10082179121`
- Artifact digest: `sha256:4d20073e3691edd9c00815598c60853d196c6de1b62797dec74356d3acec3a16`
- Artifact created: `2026-09-09T00:03:46Z`
- Artifact expires: `2026-09-16T00:03:44Z`
- Artifact state at campaign preparation: `AVAILABLE / NOT EXPIRED`

The successful automated workflow proves only that the candidate passed the repository's applicable automated delivery gate. It is **not** evidence that any visual/input/manual acceptance row passes.

### Candidate invalidation rule

If `origin/main` advances **before the real-client campaign begins**, do not silently treat this candidate as the latest build. Re-read the current physical modlist, freeze the exact `main` SHA actually selected for testing, use/build the matching exact-SHA artifact and update this header before recording manual results.

If the campaign has already begun on this exact SHA, do not mix evidence from a later SHA into the same result set. A changed build requires an explicit new/revalidated campaign boundary for affected rows.

---

## 2. Physical modpack freeze at preparation

Physical modlist authority checked during campaign preparation:

- Snapshot filename: `modlist.txt`
- Snapshot date: `2026-09-08`
- Top-level mod count: `595`
- Minecraft: `1.21.1`
- NeoForge: `21.1.248`
- Java target: `21`

Relevant physically present coexistence surfaces confirmed for Stage 05 planning/QA include:

| Component | Physical version | QA relevance |
|---|---:|---|
| Iron's Spells 'n Spellbooks | `1.21.1-3.16.3` | provider/casting coexistence |
| Spell Actionbar | `1.1.4` | external spell actionbar/casting UI |
| Epic Fight | `21.17.3.1` | combat/input/animation environment |
| Epic Fight & Iron's Spellbook animation compat | `3.1.0` | Iron's↔Epic Fight presentation coexistence |
| Punchy | `2.7e` | first-person action presentation |
| Punchy Epic Fight Compat | `1.0.0` | Punchy↔Epic Fight coexistence |
| FirstPerson | `2.7.2` | first-person body/camera presentation |
| Better Lock On | `2.0.8-neoforge` | lock-on/target presentation coexistence |
| Lock-On Movement Fix | `1.0.2` | lock-on movement/camera coexistence |
| Controlling | `19.0.5` | keybinding discovery/conflict management |

Presence/version does not establish a Black Arcana integration API or transfer authority. Any observed provider conflict still requires exact-version API/source evidence before a direct integration is introduced.

---

## 3. Manual test environment — not recorded yet

The following fields must be filled from the actual Minecraft client used for evidence collection. They are intentionally not guessed from repository or modlist metadata.

- Manual campaign start date: `NOT RECORDED — MANUAL CAMPAIGN NOT STARTED`
- Tester: `NOT RECORDED`
- Client instance/profile identification: `NOT RECORDED`
- Operating system: `NOT RECORDED`
- GPU / driver: `NOT RECORDED`
- Display mode: `NOT RECORDED`
- Native display resolution: `NOT RECORDED`
- Java runtime actually used to launch the client: `NOT RECORDED`
- Black Arcana JAR actually installed: `NOT RECORDED`
- Artifact digest independently checked after extraction: `NOT RECORDED`
- Stage 05 deterministic fixture installed: `NOT RECORDED`

Do not copy these values from assumptions or from another machine. Record the actual client instance.

---

## 4. Fixture boundary

Where applicable, use the removable deterministic fixture under:

`docs/qa/fixtures/stage05-real-client/`

The fixture may provide deterministic hazard/resistance/gate/reload states described by the canonical runbook. It is test-only data and must not be treated as production gameplay content.

Fixture presence does not create PASS evidence. If a matrix state cannot be produced legitimately with the runtime/fixture, record the concrete limitation according to the runbook rather than adding a debug bypass merely to obtain a result.

---

## 5. Evidence rules

For each matrix row that is actually exercised, record exactly one canonical result:

- `PASS` — expected behavior directly observed in a real Minecraft client;
- `FAIL` — observed behavior contradicts the expected behavior, with reproduction/evidence;
- `BLOCKED` — the scenario was attempted but could not be exercised; record the concrete blocker;
- `NOT APPLICABLE / CARRIED TO STAGE 09` — only for a genuinely future-only feature allowed by the matrix closure rule.

Do not use `BLOCKED` merely because an automated agent or repository-only environment cannot launch a graphical client. Until a human/authorized real-client campaign attempts a row, its existing matrix state remains `PENDING`.

Do not infer one configuration from another. A pass at one resolution, GUI scale, HUD anchor, feedback level, provider state or client mode does not prove a sibling configuration.

### Minimum evidence

- Visual/layout row: full-viewport screenshot showing the relevant Black Arcana UI.
- Interaction/input row: short recording or concise timestamped observation log proving input sequence and result.
- Reconnect/reload/stale-state row: before/after evidence or one capture spanning the transition.
- Any `FAIL`: exact SHA, relevant client configuration, exact reproduction steps, observed result, expected result and visual/input evidence where applicable.

---

## 6. Manual execution blocks

These blocks mirror `docs/qa/casting-ux-real-client-runbook.md`. Their state here is campaign progress only; row-level results remain authoritative in the evidence entries and are copied to the manual matrix only after direct observation.

| Block | Scope | Execution state |
|---|---|---|
| A | Resolution, GUI scale and viewport containment | `NOT STARTED` |
| B | Radial, cast separation and key bindings | `NOT STARTED` |
| C | Loadout authority and tooltip | `NOT STARTED` |
| D | HUD lifecycle and authoritative denial | `NOT STARTED` |
| E | Arcane Resistance forecast | `NOT STARTED` |
| F | Predictable read-only cast gates | `NOT STARTED` |
| G | Reconnect, stale state and datapack reload | `NOT STARTED` |
| H | Accessibility and client configuration | `NOT STARTED` |

### Block A — Resolution, GUI scale and viewport containment

Execution state: `NOT STARTED`

Required coverage includes the real-client combinations allowed by the client for:

- `854×480`;
- `1920×1080`;
- `3440×1440`;
- GUI scale `Auto`, `2`, `3`, `4` where supported;
- radial;
- loadout editor;
- hazard tooltip;
- contextual HUD with additional hazard/gate lines.

### Block B — Radial, cast separation and key bindings

Execution state: `NOT STARTED`

Required coverage includes:

- radial `TOGGLE`;
- radial `HOLD`;
- selection never casting by itself;
- rebound radial/cast/quick-slot mappings;
- conflict discoverability;
- inventory/chat/other `Screen` suppressing direct cast input.

### Block C — Loadout authority and tooltip

Execution state: `NOT STARTED`

Required coverage includes:

- edit/apply/reopen;
- clear/apply/reopen;
- server response remaining canonical;
- normal and non-normal static hazard tooltip;
- hover causing no cast and no dynamic forecast request;
- tooltip edge/small-window/GUI-scale containment.

### Block D — HUD lifecycle and authoritative denial

Execution state: `NOT STARTED`

Required coverage includes:

- actual server-authored denial;
- transient HUD lifecycle;
- no permanent duplicate Black Arcana resource bar;
- all five HUD anchors at `0.5×`, `1×`, `2×`;
- F1/hidden-GUI behavior.

### Block E — Arcane Resistance forecast

Execution state: `NOT STARTED`

Required coverage includes:

- below minimum;
- between minimum and recommended;
- at/above recommended;
- unavailable/incompatible preview where reproducible;
- armor/Curios/RPG resistance change and refresh convergence.

### Block F — Predictable read-only cast gates

Execution state: `NOT STARTED`

Exercise only states the current production runtime/fixture can legitimately produce. The runbook explicitly requires unsupported identity/loadout, progression or unavailable states to remain non-PASS when they cannot be produced without changing production semantics.

Required categories include, where legitimate:

- identity/loadout denial;
- progression denial;
- cooldown denial;
- resource-cost denial;
- all predictable gates clear;
- projection/runtime unavailable.

### Block G — Reconnect, stale state and datapack reload

Execution state: `NOT STARTED`

Required coverage includes:

- visible selected-spell forecast state;
- disconnect/reconnect as the same player;
- no old result/loadout/HUD flash before fresh snapshots;
- alternate fixture danger profile;
- `/reload`;
- stale forecast not overriding refreshed static preflight.

### Block H — Accessibility and client configuration

Execution state: `NOT STARTED`

Required coverage includes:

- feedback `MINIMAL`, `STANDARD`, `VERBOSE`;
- reduced motion;
- reduced flashes;
- particle density `0`, `0.5`, `1`;
- NeoForge client-config default recovery.

Future-only effects must remain subject to the matrix Stage 09 carry rule; preference persistence alone is not proof that a not-yet-existing effect obeys the preference.

---

## 7. Per-row evidence entry template

Copy this section once for each matrix row actually exercised. Do not pre-fill an observed result.

### Matrix row / scenario: `<exact matrix scenario>`

- Tested commit SHA: `<exact SHA>`
- Minecraft / NeoForge instance identification: `<actual instance>`
- Relevant client settings: `<actual settings>`
- Steps performed: `<exact sequence>`
- Observed result: `<direct observation>`
- Evidence reference: `<screenshot / recording / timestamped log>`
- Result: `PASS | FAIL | BLOCKED | NOT APPLICABLE / CARRIED TO STAGE 09`

---

## 8. Matrix/status update rule

`docs/qa/casting-ux-manual-matrix.md` must be updated only from completed entries in this ledger.

Do not:

- batch-convert untouched rows to PASS;
- infer manual PASS from CI/GameTests/static inspection;
- infer one GUI scale/resolution/provider state from another;
- rename Stage 05/05A tasks to `✅` while applicable manual rows lack evidence;
- promote Stage 05/05A to `VALIDATED / COMPLETE` before the actual client gate is satisfied;
- change Black Arcana gameplay authority to make a visual test easier.

If a real-client `FAIL` is found, reproduce it on the exact tested SHA, add deterministic regression coverage where possible, apply the smallest authority-preserving fix, synchronize with the latest `main`, rerun applicable automated CI and then repeat the failed manual row.

---

## 9. Current evidence conclusion

At preparation time:

- exact candidate build: frozen;
- automated CI: green;
- canonical QA artifact: available;
- latest physical modlist: checked;
- manual client environment: not yet recorded;
- Blocks A–H: not started;
- manual matrix changes: none;
- Stage 05 state: `IMPLEMENTED / FINAL VALIDATION DEFERRED`;
- Stage 05A state: `IMPLEMENTED / FINAL VALIDATION DEFERRED`.

**This file currently contains zero manual PASS claims.**
