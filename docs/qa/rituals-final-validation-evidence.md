# Stage 06 — Rituals Final Validation Evidence

> **Status:** Stage 06 remains `IMPLEMENTED / FINAL VALIDATION DEFERRED`. This ledger records the 2026-10-01 deterministic audit checkpoint and unresolved physical/manual acceptance. No real-provider/manual row is promoted to PASS by automation or source inspection.

## Audit candidate

- Black Arcana candidate audited: `main@44dfac8683a013e147f678e1016e91ed0ac128d8`.
- Canonical post-merge CI: workflow **#4003** on the same SHA, GREEN across `verify` and `stage05_qa_companion_smoke`.
- Canonical build artifact inspected: `black_arcana-0.1.0-dev.jar` from workflow #4003.
- Physical-modlist authority: sibling `neoforge-rpg-skilltree@6830865ec4d3fc4a778aa99293a8e232d2097981`.
- Minecraft: `1.21.1`.
- NeoForge target: `21.1.248`.
- Java: `21`.
- Eidolon: Repraised physical authority: `eidolon_repraised-1.21.1-0.5.0.2.jar`, mod id `eidolon_repraised`, version `0.5.0.2`.
- Malum physical authority: `malum-1.21.1-1.8.2.jar`, mod id `malum`, version `1.8.2`.
- Real modpack/client device available in this audit session: **NO**. No authorized Desktop Commander device is connected.

The modlist proves provider presence/version in the intended pack. It does not prove those JARs were physically loaded and exercised in this audit session.

## Result vocabulary

- `PASS` — directly observed on the stated physical candidate/provider topology.
- `FAIL` — directly observed behavior contradicts the frozen Stage 06 contract.
- `BLOCKED` — the scenario cannot be legitimately exercised or a required production surface is absent.
- `PENDING` — physical/manual execution has not occurred.
- `NOT APPLICABLE` — the current production representative does not exercise the boundary.
- `AUTOMATED / STATIC EVIDENCE` — supporting evidence only; never a substitute for real-provider/manual PASS.

## Deterministic activation-surface audit

### Finding: native grand ritual has no canonical player activation surface

The current production code installs `black_arcana:veil_anchor_consecration` into the server-owned `RitualEngine`, but exposes no production entrypoint that starts it for a player.

Evidence on `main@44dfac8683a013e147f678e1016e91ed0ac128d8`:

1. `MalumServerIntegrationBootstrap.installGrandRitual(...)` only registers the grand-ritual definition, requirement evaluator, Malum component provider and completion outcome.
2. `ArcanaServerRuntimeManager` exposes casting/channel/loadout lifecycle handlers, ticks ritual sessions and persists/restores them, but exposes no ritual-start handler.
3. `BlackArcanaMod` registers casting, channel, hazard forecast, loadout, noetic and other runtime bridges; it registers no ritual activation packet/command/UI handler.
4. The production source tree has no ritual activation packet, ritual command, ritual block/item ingress or equivalent player-facing Stage 06 activation class.
5. Bytecode inspection of the canonical CI JAR found **no external method reference to `RitualEngine.start(...)`**. Outside `RitualEngine` itself, references are limited to constructor/tick/restore/snapshot lifecycle use.

Result: **BLOCKED — NO CANONICAL PLAYER ACTIVATION SURFACE**.

Per `plans/06-rituals/05-final-validation-handoff.md`, this blocks real-player execution of the representative Black Arcana grand ritual and prevents Stage 06 from becoming `VALIDATED / COMPLETE`. A production command/debug item/client packet must not be invented solely to manufacture validation evidence.

## Physical/manual acceptance ledger

| ID | Scenario | Current evidence | Result |
| --- | --- | --- | --- |
| 06-P01 | Exact candidate boots in intended assembled modpack topology with recorded Eidolon/Malum providers | No authorized real-modpack device in this session | PENDING |
| 06-P02 | Real Eidolon host exposes and executes `black_arcana:eidolon_anchor_attunement` with production inputs/6.0 health cost | Recipe/API contract exists; no real provider execution performed | PENDING |
| 06-P03 | Eidolon anchor-scoped completion remains exactly-once across repeat/restart | Deterministic completion-ledger tests exist; no real host/restart execution performed | PENDING |
| 06-P04 | Real Malum 1.8.2 bridge reports available and typed `4 arcane + 2 wicked` spirit access works | Exact physical JAR/version known; no real provider execution performed | PENDING |
| 06-P05 | Legitimate production activation surface for `veil_anchor_consecration` | Source + canonical JAR audit finds no caller of `RitualEngine.start(...)` | **BLOCKED — NO CANONICAL PLAYER ACTIVATION SURFACE** |
| 06-P06 | Grand ritual requirement failures before consumption | Requires 06-P05 | BLOCKED |
| 06-P07 | Grand ritual precommit interruption/refund behavior through production gameplay | Requires 06-P05 | BLOCKED |
| 06-P08 | Grand ritual post-commit interruption without retroactive refund | Requires 06-P05 | BLOCKED |
| 06-P09 | Grand ritual successful completion / duplicate-completion denial | Requires 06-P05 | BLOCKED |
| 06-P10 | Multiplayer same-anchor race through production activation | Requires 06-P05 | BLOCKED |
| 06-P11 | Grand ritual active-session restart/chunk lifecycle through production activation | Requires 06-P05 | BLOCKED |
| 06-P12 | Eidolon provider-absence controlled profile | No controlled provider-absence runtime executed in this session | PENDING |
| 06-P13 | Malum provider-absence/incompatibility controlled profile | No controlled provider-absence runtime executed in this session | PENDING |
| 06-P14 | Dedicated-server provider isolation in exact Eidolon/Malum topology | Generic canonical dedicated-server CI is GREEN; exact physical provider topology not exercised here | PENDING |
| 06-P15 | Stage 04 world-mutation admission for current representative ritual outcomes | Current representative Eidolon/Malum outcomes only record durable completion and do not perform BA world mutation | NOT APPLICABLE |
| 06-P16 | Stage 05A hazard ownership for current representative ritual outcomes | Current representative ritual definitions/outcomes do not invoke ritual-local Backlash/Corruption/Strain semantics | NOT APPLICABLE |

## Automated/static evidence retained

Existing Stage 06 automated coverage remains valid supporting evidence for:

- bounded ritual definitions, activation replay and session capacity;
- requirement-before-consumption ordering;
- transactional component reservation/commit/refund semantics;
- duplicate activation/anchor exclusion;
- session snapshot/restore and bounded persistence;
- exactly-once completion ledger behavior;
- Eidolon registration ownership safety and recipe contract;
- Malum typed-spirit requirement/consumption semantics;
- provider failure fail-closed behavior.

These rows do not convert `06-P02`–`06-P14` into physical PASS.

## Required next action

Stage 06 remains the active audit target. To close it legitimately:

1. provide/use an authorized real modpack client/server QA environment;
2. rerun the exact physical provider checks on a fresh reconciled `main`;
3. resolve the production activation-surface blocker through a separately reviewed product/architecture decision if player-facing `veil_anchor_consecration` execution is required;
4. only then execute the dependent grand-ritual transaction/lifecycle rows;
5. preserve all unresolved rows as PENDING/BLOCKED until directly observed.

No Stage 07 promotion is authorized by this checkpoint.
