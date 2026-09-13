# Stage 05 — Casting & UX — Execution Status

This file is the quick execution ledger for `plans/05-casting-ux/`.

It answers two questions without requiring readers to reconstruct history from implementation checkpoints:

1. what has actually been implemented or completed;
2. what Black Arcana is working on **right now**.

The detailed subplans remain authoritative for scope and architecture. Production code/tests remain authoritative for runtime behavior. This ledger must be updated whenever a numbered Stage 05 item changes state.

## Legend

- ✅ **COMPLETE FOR DECLARED SCOPE** — the plan/audit deliverable is complete and no additional runtime work is implied by that item itself.
- 🟡 **IMPLEMENTED / VALIDATION PENDING** — bounded implementation is canonical or automated gates are green, but required direct real-client/full-pack validation remains pending, or the plan intentionally retains deferred evidence-gated work.
- 🔵 **IN PROGRESS** — this is the item currently being implemented.
- ⛔ **BLOCKED / DEFERRED BY EVIDENCE** — implementation is not authorized until the stated API/evidence/provider/runtime gate exists.

A green check does **not** mean that the entire Stage 05 physical-client campaign has passed. Overall Stage 05 remains `IMPLEMENTED / FINAL VALIDATION DEFERRED` until the manual matrix is directly executed.

## Current position

> 🔵 **NOW: 05.16 — Onboarding / Discoverability / Contextual Help**
>
> Branch: `feat/stage05-discoverability`
>
> Completed inside 05.16 so far:
>
> - first RED: `36c709bb93e620e98017c9651aaa370de85bfc21` — missing pure discoverability model/layout as expected;
> - first GREEN: `5dd76aff257cb8d51b64057fbb48e55c42730753` — pure `DiscoverabilityModel` + bounded hint layout; workflow `34758843055` GREEN through unit, diff sanity, NeoForge build, JAR verification, Foundation GameTests and dedicated-server smoke;
> - second RED: `9db31ea88d06097b03ec035d6c2b1ad864d700d4` — client discoverability wiring contract; workflow `34759052907` failed as the TDD RED for the not-yet-wired runtime/UI.
>
> **Next implementation step:** close the second RED with the physical-client wiring for current `KeyMapping` bindings, session-local first-use cue, bounded hint presentation and deterministic Help re-entry from the loadout editor. Then run the full GREEN pipeline before moving further.

## Numbered plan ledger

| Item | Status | What is actually true now | Remaining gate / next action |
|---|---|---|---|
| **05.01 — Input & Loadouts** | 🟡 | Runtime is implemented: bounded server-owned loadout, rebindable client intent, quick-cast/selected-cast workflow and persistence/synchronization. | Direct rows in the Stage 05 physical-client matrix remain pending. |
| **05.02 — Radial Wheel** | 🟡 | Runtime is implemented: client-only selection, 8 slots/page, paging, compact geometry and selection/cast separation. | Direct radial/input/readability validation remains pending. |
| **05.03 — Contextual HUD & Feedback** | 🟡 | Contextual/event-driven HUD runtime exists with server-authored result/hazard/gate presentation. | Direct HUD/readability/full-pack overlap validation remains pending. |
| **05.04 — Accessibility & Client Config** | 🟡 | Client-only presentation preferences, rebindability and bounded accessibility controls are implemented. | Direct reduced-motion/flash/scale/input validation remains pending. |
| **05.05 — Final Real-Client Validation Handoff** | 🟡 | Closeout/runbook exists and is the mandatory acceptance procedure. | **Physical assembled-pack campaign has not been executed to completion.** This is the principal reason Stage 05 is not `VALIDATED / COMPLETE`. |
| **05.06 — Modpack Coexistence** | ✅ | Coexistence planning/authority contract is complete. It intentionally adds no runtime bridge without exact API evidence. | Real-pack coexistence scenarios are exercised by 05.05; only observed failures may promote new compatibility work. |
| **05.07 — Presentation Data Contracts** | ✅ | Server/client presentation-authority audit and evidence gates are complete. It intentionally adds no runtime. | New cooldown/cost/channel/etc. presentation remains blocked unless a bounded server-authored contract is approved. |
| **05.08 — Visual Language & State Semantics** | 🟡 | Bounded semantic core is implemented and automated gates are GREEN. | Final direct client visual/accessibility validation remains deferred. |
| **05.09 — Keyboard Focus & Navigation** | 🟡 | Implementation is merged; post-merge automated gates and QA artifact publication are GREEN. | Real-client keyboard/accessibility/coexistence validation remains deferred. |
| **05.10 — Loadout Editor Information Architecture** | 🟡 | Phase A.1–A.6 implementation is present with automated gates GREEN: dense reorder/search/draft/editor hardening within existing authority. | A.7 real-client validation is pending; richer rejection/provider metadata remains evidence-gated. |
| **05.11 — Contextual Feedback Orchestration** | 🟡 | No-protocol Phase A bounded arbitration is implemented. | Real-client validation is deferred; later phases are not promoted unless their gates are satisfied. |
| **05.12 — Iconography & Resource Resolution** | 🟡 | Bounded Phase A–C resource/icon resolution tranche is implemented with automated gates GREEN. | Final client/resource-pack validation remains pending; provider assets remain provider-owned. |
| **05.13 — Targeting & Aim Presentation** | 🟡 | Authority-safe bounded local-observation presentation tranche is implemented with automated gates GREEN. | Direct client validation remains pending; authoritative target/world geometry must not be inferred. |
| **05.14 — Spell Details & Inspection** | 🟡 | Bounded Phase B static inspection is merged and automated/review gates are GREEN. | Real-client tooltip/readability/accessibility validation remains pending; richer runtime/provider facts stay fail-closed. |
| **05.15 — Casting VFX / Audio / Animation Presentation** | 🟡 | Provider-free A–D + H tranche is merged: cast correlation, bounded audiovisual pulse, original project audio, resource fallback and teardown. Canonical merge `6daec47b915e2caa54b7c5d64582cd5171108bcb`; post-merge workflow `34758313103` GREEN. | Phase G physical/full-pack audiovisual QA is pending. Provider animation/camera and gameplay geometry remain deferred by exact evidence/authority gates. |
| **05.16 — Onboarding / Discoverability / Contextual Help** | 🔵 | **CURRENT WORK.** Pure model/layout first RED→GREEN is complete. Second client-wiring RED is confirmed. | Implement current-binding/unbound presentation, bounded first-use cue, dismissal/re-entry and editor Help wiring; then full GREEN CI, checkpoint, reconciliation, PR, merge and post-merge CI. |

## Overall Stage 05 status

- [x] Deterministic server-authoritative casting workflow implemented.
- [x] Loadout/radial/HUD/client-config foundations implemented.
- [x] Presentation-data authority audit complete.
- [x] Visual semantics implemented.
- [x] Keyboard focus/navigation implemented.
- [x] Loadout-editor hardening tranche implemented.
- [x] Contextual-feedback bounded orchestration implemented.
- [x] Icon/resource-resolution bounded tranche implemented.
- [x] Target/aim bounded presentation tranche implemented.
- [x] Spell-inspection bounded presentation tranche implemented.
- [x] Casting audiovisual provider-free tranche implemented and merged.
- [ ] **05.16 onboarding/discoverability implementation complete.** ← **CURRENT**
- [ ] **Mandatory real-client/full-pack Stage 05 validation campaign complete.**

## Completion rule

Stage 05 may be labeled `VALIDATED / COMPLETE` only when:

1. the currently approved numbered implementation work is merged with exact-head and post-merge CI GREEN;
2. all applicable rows in `docs/qa/casting-ux-manual-matrix.md` are directly observed on the exact assembled build;
3. legitimate future-only/evidence-blocked rows are explicitly carried/deferred rather than falsely marked PASS;
4. this ledger and the Stage 05 README/master state are reconciled with the resulting canonical `main` state.

CI is evidence for deterministic implementation. It never fabricates a physical-client PASS.
