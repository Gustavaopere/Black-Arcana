# Stage 05 / 05A — Real-client QA Evidence

## State

`PREPARED / MANUAL EXECUTION NOT STARTED / STAGE 05 ACTIVE`

This ledger is the evidence target required by `plans/05-casting-ux/🟡-PENDENTE-05-final-client-validation-handoff.md` and `docs/qa/casting-ux-real-client-runbook.md`.

It currently records **campaign preparation only**. No Minecraft client observation has been performed through this ledger and no manual matrix row is PASS/FAIL/BLOCKED from this file. Preparation/reconciliation may add or refine `PENDING` coverage rows when canonical numbered-plan requirements were not yet represented; observed row results/statuses remain unchanged until direct evidence is recorded.

Automated CI, artifact publication, repository inspection and fixture availability are supporting/preflight evidence only. They do not satisfy any row that requires direct real-client observation.

Under D034, Stage 05 is the active blocking numbered stage. Stage 05A remains blocked from promotion/audit progression until Stage 05 is fully complete. Historical 05A implementation/evidence remains reusable later but does not authorize skipping the Stage 05 client gate.

---

## 1. Preparation reference build

This build was recorded while the manual campaign infrastructure was being prepared. It is a historical, exact-SHA **preparation reference**, not an automatically selected manual campaign candidate.

- Repository: `Gustavaopere/Black-Arcana`
- Preparation-reference `main` SHA: `d103b259eed27705b2d4e44cbec60d78d4228054`
- Preparation-reference commit: merge of PR #133, `docs: catalog Ars Zero 2.0.2 provider`
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

The successful automated workflow proves only that this reference build passed the repository's applicable automated delivery gate. It is **not** evidence that any visual/input/manual acceptance row passes, and it does not require the later manual campaign to use this SHA.

### Latest validated `main` candidate available for a future campaign

The latest runtime-affecting exact-SHA `main` build validated during the current Stage 05 reconciliation is:

- `main` SHA: `1944e45c122a24c36101e97efe2195730b5019f0`;
- merge: PR #317, `fix(stage05): make Iron's hosted probe loadout-reachable`;
- post-merge workflow: `35292207167` (#3212) — GREEN for unit tests, diff sanity, NeoForge build, built-JAR verification, Stage 05 QA companion JAR isolation, Foundation GameTests, production dedicated-server smoke, publication of both exact-SHA artifacts, and the separate `stage05_qa_companion_smoke` job including the companion dedicated-server smoke;
- canonical artifact: `black-arcana-1944e45c122a24c36101e97efe2195730b5019f0`;
- canonical artifact ID: `10527221605`;
- canonical artifact digest reported by GitHub Actions: `sha256:45b754d81597c9f75e00b203347f93c99be94883fe5b2874abfce33ea72a0e43`;
- Block I companion artifact: `black-arcana-stage05-qa-1944e45c122a24c36101e97efe2195730b5019f0`;
- Block I companion artifact ID: `10526747373`;
- Block I companion artifact digest reported by GitHub Actions: `sha256:278741a5742f1e7090242dc739329eb362fa33bc8c62689279b49cf04119a5b6`;
- Block J provider-real preparation profile: `docs/qa/stage05-block-j-provider-real-profile.md`, merged with the same runtime checkpoint;
- automated Block J presentation/loadout preflight: GREEN after two explicit RED cycles covering missing provider-conditional presentation metadata and partial hosted runtime installation on presentation-ID collision.

The two exact-SHA artifacts were independently downloaded from GitHub Actions in a repository-only verification session. Their ZIP SHA-256 values matched the GitHub-reported digests exactly. Extraction produced only the expected JAR in each archive: production `black_arcana-0.1.0-dev.jar` (`1,650,141` bytes, SHA-256 `27fcf7b61aed0ddb53a1c9718ea52fb0292805ed367a89265e1020d2b039eade`) and companion `black_arcana_stage05_qa-0.1.0-dev.jar` (`21,354` bytes, SHA-256 `611850b68f83feb5bfd87093545ec9a1e80c6555c74d635a8d0f00065112e398`). Descriptor inspection confirmed production `modId="black_arcana"` with Iron's declared optional and companion `modId="black_arcana_stage05_qa"`; the production JAR contains `SpellDataCatalog`, `IronsSyntheticContent` and `NeoForgeIronsManaAccess`, while the companion contains the Stage 05 fixture content and all sixteen slot JSON definitions. No physical client installed these JARs, so this closes artifact identity/extraction preflight only and does not satisfy any manual row.

This build is **available as the current runtime candidate**, but the manual campaign candidate remains unselected until actual real-client execution starts, as required below. No manual row becomes PASS, FAIL or BLOCKED from this automated evidence.

### Manual campaign candidate freeze rule

The manual campaign candidate is selected **at the start of actual real-client execution**, before the first manual observation is recorded. Record the exact tested SHA, successful exact-SHA CI run, artifact/JAR identity and digest in section 3.

The Git commit containing this evidence document does **not** have to equal the tested candidate SHA. Documentation-only commits made to prepare or record the campaign therefore do not recursively invalidate the candidate. The authority is the exact Black Arcana JAR actually installed in the client and the exact SHA/artifact recorded for that campaign.

If `origin/main` advances before the first real-client observation, re-read the current physical modlist and deliberately choose which exact `main` SHA will be tested. Prefer the latest compatible successful `main` build unless a specific earlier exact-SHA build is intentionally being reproduced. Never silently describe this preparation reference as the latest build.

Once the first real-client observation is recorded, the campaign candidate is locked. Do not mix evidence from a later Black Arcana JAR/SHA into that result set. Changing the tested build requires an explicit new/revalidated campaign boundary and repetition of every affected row.

For Block I, the removable `black_arcana_stage05_qa` companion must match that same exact campaign SHA. The companion artifact/JAR is a second identity that must be recorded separately; it does not change the campaign candidate or authorize mixing SHAs.

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
- Manual campaign candidate SHA: `NOT SELECTED`
- Candidate exact-SHA CI run number / ID: `NOT SELECTED`
- Candidate canonical artifact name / ID: `NOT SELECTED`
- Candidate artifact digest: `NOT SELECTED`
- Client instance/profile identification: `NOT RECORDED`
- Operating system: `NOT RECORDED`
- GPU / driver: `NOT RECORDED`
- Display mode: `NOT RECORDED`
- Native display resolution: `NOT RECORDED`
- Java runtime actually used to launch the client: `NOT RECORDED`
- Black Arcana JAR actually installed: `NOT RECORDED`
- Artifact/JAR digest independently checked after extraction: `NOT RECORDED`
- Stage 05 deterministic datapack fixture installed: `NOT RECORDED`
- Block I Stage 05 QA companion artifact name / ID: `NOT SELECTED`
- Block I Stage 05 QA companion artifact digest: `NOT SELECTED`
- Block I Stage 05 QA companion JAR actually installed: `NOT RECORDED`
- Block I companion JAR digest independently checked after extraction: `NOT RECORDED`

Current execution-environment note: the most recent authorized desktop discovery returned **no connected device**, so no real Minecraft client campaign was started from this session. Per the evidence rules below, this does **not** convert untouched matrix rows from `PENDING` to `BLOCKED`.

Do not copy these values from assumptions or from another machine. Record the actual client instance and the actual Black Arcana JAR used for the first observation before assigning any manual result. For Block I, also record the matching exact-SHA companion artifact and extracted JAR before exercising the row.

---

## 4. Fixture boundary

The Stage 05 campaign has two different removable fixture surfaces and they must not be conflated.

### Deterministic datapack fixture

Where applicable, use the removable deterministic fixture under:

`docs/qa/fixtures/stage05-real-client/`

The datapack fixture may provide deterministic hazard/resistance/gate/reload states described by the canonical runbook. It is test-only data and must not be treated as production gameplay content.

### Block I 16-slot companion mod

Block I may use the removable NeoForge companion mod documented in:

`docs/qa/stage05-16slot-qa-companion.md`

The companion mod ID is `black_arcana_stage05_qa`. It exists only to register sixteen legitimate selection-only Black Arcana spell identities through the existing server-runtime initializer boundary, so a server-owned 16-entry loadout can be exercised physically. It must be built/published separately from the production Black Arcana JAR and use the same exact campaign SHA.

The companion changes the available spell registry. Evidence collected while it is installed must therefore declare that profile explicitly. Do not silently reuse companion-enabled observations to satisfy unrelated production-only rows. Remove it before returning to Blocks A–H or J unless a specific row explicitly declares the companion as part of its test profile.

Fixture or companion presence does not create PASS evidence. If a matrix state cannot be produced legitimately with the approved test profile, record the concrete limitation according to the runbook rather than adding a production debug bypass merely to obtain a result.

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
- Input-persistence row: one before/restart/after capture or timestamped log showing the rebind, full client restart and successful reuse of the rebound mapping.
- Reconnect/reload/stale-state row: before/after evidence or one capture spanning the transition.
- Cast-result correlation row: positive evidence linking a known emitted cast to its authoritative result through matching observable `castId` values where available, or another unambiguous existing spell-specific correlation surface; generic-only presentation is insufficient for PASS.
- Client-authority-isolation row: one before/after evidence entry for every gameplay-authority dimension applicable to the exact candidate/test content, plus evidence that passive presentation interaction does not mutate synchronized hazard/gate/resource state.
- Provider coexistence row: recording or timestamped observation log that proves the provider action/state transition plus the resulting Black Arcana authority outcome; record relevant resource/cooldown state where settlement is under test.
- Provider-free core-input row: evidence for every required core keyboard/mouse path under the provider-absent/incompatible profile, not one representative action.
- Block I companion row: exact-SHA production and companion artifact/JAR identities and digests plus a recording or timestamped log proving the sixteen server-owned identities are accepted and every canonical slot `0..15` is reached through the supported client path.
- Any `FAIL`: exact SHA, relevant client configuration, exact reproduction steps, observed result, expected result and visual/input evidence where applicable.

---

## 6. Manual execution blocks

These blocks mirror `docs/qa/casting-ux-real-client-runbook.md`. Their state here is campaign progress only; row-level results remain authoritative in the evidence entries and are copied to the manual matrix only after direct observation.

| Block | Scope | Execution state |
|---|---|---|
| A | Resolution, GUI scale and viewport containment | `NOT STARTED` |
| B | Radial, cast separation, key bindings and restart persistence | `NOT STARTED` |
| C | Loadout authority and tooltip | `NOT STARTED` |
| D | HUD lifecycle, authoritative denial and cast-result correlation | `NOT STARTED` |
| E | Arcane Resistance forecast | `NOT STARTED` |
| F | Predictable read-only cast gates | `NOT STARTED` |
| G | Reconnect, stale state and datapack reload | `NOT STARTED` |
| H | Accessibility, client configuration and authority isolation | `NOT STARTED` |
| I | Canonical 16-slot loadout reachability | `NOT STARTED` |
| J | Current-modpack provider coexistence and provider-free core input | `NOT STARTED` |

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

### Block B — Radial, cast separation, key bindings and restart persistence

Execution state: `NOT STARTED`

Required coverage includes:

- radial `TOGGLE`;
- radial `HOLD`;
- selection never casting by itself;
- rebound radial/cast/quick-slot mappings;
- conflict discoverability;
- full client restart after rebind, followed by successful reuse of the rebound mappings;
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

### Block D — HUD lifecycle, authoritative denial and cast-result correlation

Execution state: `NOT STARTED`

Required coverage includes:

- actual server-authored denial;
- positive attribution of a matched result to its known emitted cast context, using matching observable `castId` values where available or another unambiguous existing spell-specific correlation surface;
- selection changed to a distinguishable spell before the known result, without relabeling that result as the new selection;
- unmatched/generic result remaining generic when a safe production path exists;
- if no positive correlation surface is observable, the correlation row remains `BLOCKED` rather than being passed from generic-only behavior;
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

### Block H — Accessibility, client configuration and authority isolation

Execution state: `NOT STARTED`

Required coverage includes:

- feedback `MINIMAL`, `STANDARD`, `VERBOSE`;
- reduced motion;
- reduced flashes;
- particle density `0`, `0.5`, `1`;
- NeoForge client-config default recovery;
- explicit applicability inventory for resource cost, cooldown, progression gate, target admission, Arcane Danger settlement and world settlement;
- equivalent before/after server-owned evidence for every authority dimension applicable to the exact campaign;
- applicable-but-unexercisable dimensions keeping the row `BLOCKED` rather than being inferred from another dimension;
- radial/HUD/forecast/gate interaction not mutating synchronized hazard/gate/resource state without a new authoritative gameplay action.

Future-only effects must remain subject to the matrix Stage 09 carry rule; preference persistence alone is not proof that a not-yet-existing effect obeys the preference.

### Block I — Canonical 16-slot loadout reachability

Execution state: `NOT STARTED`

Use the matching exact-SHA `black_arcana_stage05_qa` companion profile defined in `docs/qa/stage05-16slot-qa-companion.md`. Record both production and companion artifacts/JARs and independently checked digests before exercising this block.

Required coverage includes:

- physical instance loads the exact-SHA production Black Arcana JAR and matching companion without duplicate-mod/dependency error;
- sixteen companion identities form a legitimate server-accepted 16-slot loadout;
- synchronized state still reflects that loadout after reopen/reconnect as applicable;
- direct physical reachability of every canonical slot `0..15` through supported selection/radial paging;
- paging/selection staying within the synchronized loadout bound;
- no forged seventeenth slot or substituted spell identity;
- selection remaining non-casting.

If the matching companion cannot load or cannot legitimately supply the sixteen server-owned identities, the row must be attempted and recorded `FAIL` or `BLOCKED` according to the concrete observed condition. Do not add a production bypass to manufacture PASS evidence. Remove the companion before returning to production-only rows unless another row explicitly declares it as part of its profile.

### Block J — Current-modpack provider coexistence authority and provider-free core input

Execution state: `NOT STARTED`

Before execution, record the actual physical modlist versions used by the campaign rather than assuming the preparation snapshot is unchanged.

Required coverage includes, where the assembled runtime legitimately exposes the path:

- one Iron's-hosted `black_arcana:irons_integration_probe` invocation producing at most one Black Arcana root cast/result;
- the one Black Arcana transactional probe cost settling exactly once, without an additional provider-native Iron's mana deduction;
- the Black Arcana cooldown settling exactly once, without a second provider-native cooldown;
- Epic Fight/EFIS client combat or animation state not becoming Black Arcana cast-legality authority;
- optional-provider absence/incompatibility failing only the dependent feature, with no crash, duplicate/free fallback or unrelated Black Arcana authority change;
- in the provider-absent/incompatible profile, ordinary keyboard/mouse coverage for open radial, radial selection/close, cast selected and open/edit loadout, plus each quick-cast mapping intentionally bound for the campaign;
- no core input path silently acquiring a provider/controller dependency for an operation that itself does not require that provider.

A physical provider row is not proven by static source inspection, deterministic authority tests or dedicated-server CI. If the path cannot be reproduced safely on the campaign instance, record `BLOCKED` with the concrete reason rather than inferring PASS.

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

For Block I also include:

- Companion artifact name / ID: `<exact artifact>`
- Companion artifact digest: `<sha256>`
- Companion JAR filename: `<exact filename>`
- Companion JAR digest: `<sha256 independently checked>`

---

## 8. Matrix/status update rule

Observed row results/statuses in `docs/qa/casting-ux-manual-matrix.md` must be updated only from completed entries in this ledger. Preparation/reconciliation may add or refine `PENDING` coverage rows needed to represent canonical numbered-plan requirements, but it must not assign `PASS`, `FAIL` or `BLOCKED` without direct evidence.

Do not:

- batch-convert untouched rows to PASS;
- infer manual PASS from CI/GameTests/static inspection;
- infer one GUI scale/resolution/provider state from another;
- rename Stage 05 tasks to `✅` while applicable manual rows lack evidence;
- promote Stage 05 to `VALIDATED / COMPLETE` before the actual client gate is satisfied;
- audit/promote Stage 05A while Stage 05 remains incomplete under D034;
- change Black Arcana gameplay authority to make a visual test easier.

If a real-client `FAIL` is found, reproduce it on the exact tested SHA, add deterministic regression coverage where possible, apply the smallest authority-preserving fix, synchronize with the latest `main`, rerun applicable automated CI and then repeat the failed manual row.

---

## 9. Current evidence conclusion

At the latest preparation/reconciliation checkpoint:

- historical preparation-reference build: recorded;
- latest runtime-affecting validated `main` build available for a future campaign: `1944e45c122a24c36101e97efe2195730b5019f0`;
- exact-SHA automated CI for that build: GREEN (`35292207167`, #3212), including both `verify` and the separate `stage05_qa_companion_smoke` job;
- exact-SHA canonical QA artifact: recorded (`black-arcana-1944e45c122a24c36101e97efe2195730b5019f0`, ID `10527221605`, GitHub Actions SHA-256 `45b754d81597c9f75e00b203347f93c99be94883fe5b2874abfce33ea72a0e43`);
- exact-SHA Block I companion artifact: recorded (`black-arcana-stage05-qa-1944e45c122a24c36101e97efe2195730b5019f0`, ID `10526747373`, GitHub Actions SHA-256 `278741a5742f1e7090242dc739329eb362fa33bc8c62689279b49cf04119a5b6`);
- independent extraction/JAR digest verification: `PASS AS REPOSITORY-ONLY PREFLIGHT` — ZIP digests matched GitHub; production JAR `black_arcana-0.1.0-dev.jar` is `1,650,141` bytes / SHA-256 `27fcf7b61aed0ddb53a1c9718ea52fb0292805ed367a89265e1020d2b039eade`; companion JAR `black_arcana_stage05_qa-0.1.0-dev.jar` is `21,354` bytes / SHA-256 `611850b68f83feb5bfd87093545ec9a1e80c6555c74d635a8d0f00065112e398`;
- Block J provider presentation/loadout preflight blocker: corrected and canonical via PR #317; provider-real execution remains `NOT STARTED`;
- manual campaign candidate: `NOT SELECTED`;
- latest physical modlist preparation snapshot: recorded;
- authorized real-client device in the current execution session: none connected;
- manual client environment: not yet recorded;
- Block I companion artifact/JAR: available as exact-SHA preflight evidence but not selected or installed because the manual campaign has not started;
- Blocks A–J: not started;
- manual matrix rows: remain `PENDING` until direct observation;
- Stage 05 state: `ACTIVE / IMPLEMENTATION PRESENT / REQUIRED PHYSICAL VALIDATION PENDING`;
- Stage 05A state: `BLOCKED BY STAGE 05` under D034.

**This file currently contains zero manual PASS claims.**
