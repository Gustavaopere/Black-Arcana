# Black Arcana — Status

Last updated: 2026-09-18

## Authoritative execution rule

D035 supersedes D034 for the timing of manual/physical/real-client/real-modpack/provider-native observation. The mandatory implementation order remains:

`05 -> 05A -> 06 -> 07 -> 07A -> 08 -> 09`

For each implementation stage:

`AUDIT -> IDENTIFY GAPS -> IMPLEMENT -> DETERMINISTIC TEST/CI -> TRANSFER ANY REQUIRED PHYSICAL ROWS TO STAGE 09 -> MARK ✅ -> AUDIT AGAIN -> ONLY THEN ADVANCE`

Functional implementation, integration, persistence/lifecycle/world-safety contracts and deterministic acceptance may not be deferred. Manual/physical rows transferred under D035 remain `PENDING / DEFERRED TO STAGE 09`; they are never inferred as PASS from CI.

Stage 09 is the consolidated exact-release-candidate validation campaign and remains release-blocked until every applicable transferred row is directly evidenced.

## Current active stage

**Stage 05A — Arcane Danger is the current numbered audit target. 05A.01–05A.03 are ✅ complete; 05A.04 — Arcane Strain is the next required audit target.**

Stage 05 — Casting & UX is `COMPLETE / ENGINEERING CLOSED / REAL-CLIENT RELEASE VALIDATION CARRIED TO STAGE 09`.

The Stage 05 ledger is in `plans/05-casting-ux/00-execution-status.md`. Its 05.01–05.07 engineering plans are ✅ under D035 because their runtime/integration/deterministic gates are closed and every unresolved real-client/provider observation is explicitly retained in the Stage 09 matrix.

The manual rows themselves remain unresolved:

- `docs/qa/casting-ux-manual-matrix.md` remains PENDING;
- `docs/qa/casting-ux-real-client-runbook.md` remains the execution procedure;
- `docs/qa/casting-ux-real-client-evidence.md` remains the evidence ledger;
- no manual row has been converted to PASS by the Stage 05 closeout.

## Stage table

| Stage | State | Promotion meaning |
|---|---|---|
| 00 Foundation | ✅ COMPLETE | historical completed predecessor |
| 01 Reference Catalog | ✅ COMPLETE | historical completed predecessor |
| 02 Arcana Core | ✅ COMPLETE | historical completed predecessor |
| 03 Integration Layer | ✅ COMPLETE | historical completed predecessor |
| 04 World Safety | ✅ COMPLETE | historical completed predecessor |
| 05 Casting & UX | ✅ ENGINEERING COMPLETE | real-client/provider-real rows transferred to Stage 09 under D035 |
| 05A Arcane Danger | 🟡 ACTIVE AUDIT TARGET | 05A.01–05A.03 ✅ complete; audit 05A.04 next, then continue strictly in order |
| 06 Rituals | ⛔ BLOCKED BY 05A | historical implementation may be reused after 05A closes |
| 07 Spell Domains | ⛔ BLOCKED BY 05A -> 06 | historical domain work remains reusable but is not the active target |
| 07A Arcane Polarity, Fusion & Metamagic | ⛔ BLOCKED BY 07 | do not start until Stage 07 engineering closes |
| 08 Progression & Balance | ⛔ BLOCKED BY 07A | RPG Skill Tree remains progression/attributes/Mastery/perks/gates authority |
| 09 Hardening & Release | ⛔ IMPLEMENTATION-ORDER BLOCKED BY 08 / RELEASE OWNER OF DEFERRED PHYSICAL QA | execute accumulated real-client/real-modpack/provider-native campaign on the exact release candidate |

## Authority boundaries

Black Arcana owns the authoritative magic runtime: casting, rituals, magical domains, Arcane Danger, persistence, world safety and provider-native magic integration.

RPG Skill Tree owns progression, attributes, Mastery, perks and progression gates. Later work must not duplicate that authority inside Black Arcana.

Client UI remains presentational/predictive only. External providers remain behind verified adapters and optional integrations fail closed where compatibility or causal identity is not proven.

## D035 release-validation debt

Moving physical validation to Stage 09 does not waive it. The carried Stage 05 rows include input rebinding/restart, GUI-focus suppression, loadout apply/clear/reconnect, canonical 16-slot physical reachability, radial toggle/hold/cast separation, stale-state behavior, client-config authority isolation and current-modpack/provider coexistence.

Any Stage 09 FAIL reopens the originating plan/stage for an authority-preserving correction and deterministic regression coverage where possible.

## Historical downstream implementation

Code and evidence already merged for 05A, 06 and 07 are preserved. Status labels such as `IMPLEMENTED`, `FINAL VALIDATION DEFERRED`, `CANONICAL RUNTIME` or partial-domain checkpoints are not automatically engineering-complete claims.

When a stage becomes active, audit it against its current plans and latest `main`, reuse correct canonical implementation, implement only what is missing, and explicitly carry any remaining physical/manual observation into Stage 09 under D035.
