# Stage 05 — Casting & UX — Execution Status

This is the canonical quick-status ledger for `plans/05-casting-ux/`.

## Status convention

- ✅ **COMPLETE** — the declared plan/audit scope is closed and has no mandatory unresolved acceptance gate of its own.
- 🟡 **PENDENTE** — implementation/planning work is present, but a mandatory direct real-client/full-pack validation gate is still open.
- 🔵 **IN PROGRESS** — implementation is currently being changed and has not reached the merge/post-merge gate.
- ⛔ **BLOCKED / EVIDENCE-GATED** — a proposed optional extension is not authorized until exact API/runtime/provider evidence exists.

A plan is never marked ✅ merely because CI is green. Automated CI cannot fabricate a real-client PASS.

## Current position

All approved deterministic Stage 05.01–05.16 implementation/planning tranches are now either merged or complete for their declared evidence-gated scope.

The remaining blocking closeout is the assembled real-client/full-pack campaign defined by `🟡-PENDENTE-05-final-client-validation-handoff.md` and `docs/qa/casting-ux-manual-matrix.md`.

Stage 05 therefore remains:

`IMPLEMENTED / PHYSICAL VALIDATION PENDING`

## Numbered plan ledger

| Item | Status | Canonical state | Remaining mandatory gate |
|---|---|---|---|
| **05.01 — Input & Loadouts** | 🟡 PENDENTE | Runtime implemented: bounded server-owned loadout, rebindable intent, quick/selected cast, persistence and synchronization. | Direct physical-client input/loadout rows. |
| **05.02 — Radial Wheel** | 🟡 PENDENTE | Runtime implemented: 8 slots/page, paging, bounded geometry, selection/cast separation. | Direct radial/input/readability rows. |
| **05.03 — Contextual HUD & Feedback** | 🟡 PENDENTE | Contextual server-authored feedback runtime implemented. | Direct HUD/readability/full-pack overlap rows. |
| **05.04 — Accessibility & Client Config** | 🟡 PENDENTE | Client-only presentation/accessibility preferences implemented. | Direct scale/input/reduced-motion/reduced-flash rows. |
| **05.05 — Final Real-Client Validation Handoff** | 🟡 PENDENTE | Runbook and evidence procedure are complete. | **Execute the physical assembled-pack campaign.** |
| **05.06 — Modpack Coexistence** | ✅ COMPLETE | Coexistence/authority contract is complete. Unsupported integrations remain intentionally absent. | None inside this plan; observed real-pack failures are handled through 05.05. |
| **05.07 — Presentation Data Contracts** | ✅ COMPLETE | Presentation-authority audit/evidence gates are complete. | None inside this audit; future fields remain evidence-gated rather than unfinished. |
| **05.08 — Visual Language & State Semantics** | 🟡 PENDENTE | Bounded semantic core implemented; automated gates green. | Direct visual/accessibility validation. |
| **05.09 — Keyboard Focus & Navigation** | 🟡 PENDENTE | Merged keyboard navigation with post-merge automation green. | Direct keyboard/accessibility/coexistence validation. |
| **05.10 — Loadout Editor Information Architecture** | 🟡 PENDENTE | Approved Phase A.1–A.6 implementation present and green. | A.7 real-client validation. Evidence-gated richer metadata is not inferred. |
| **05.11 — Contextual Feedback Orchestration** | 🟡 PENDENTE | Approved no-protocol Phase A arbitration implemented. | Direct client validation. Later optional phases require their own evidence gate. |
| **05.12 — Iconography & Resource Resolution** | 🟡 PENDENTE | Approved bounded resource/icon tranche implemented. | Direct client/resource-pack validation. |
| **05.13 — Targeting & Aim Presentation** | 🟡 PENDENTE | Authority-safe local-observation tranche implemented. | Direct client validation; no client inference of authoritative geometry. |
| **05.14 — Spell Details & Inspection** | 🟡 PENDENTE | Bounded static inspection tranche merged and green. | Direct tooltip/readability/accessibility validation. |
| **05.15 — Casting VFX / Audio / Animation Presentation** | 🟡 PENDENTE | Provider-free A–D + H tranche merged; post-merge CI green; original project audio and teardown implemented. | Phase G physical/full-pack audiovisual QA. Provider animation/camera/geometry remain evidence-gated, not silently unfinished. |
| **05.16 — Onboarding / Discoverability / Contextual Help** | 🟡 PENDENTE | Phases A–C plus authorized current-binding/unbound subset of D implemented and merged. First-use cue, live bindings, editor Help, localization/config and teardown are present. | Physical/full-pack onboarding/help matrix. Optional provider-aware help/conflict integrations remain evidence-gated. |

## Deterministic implementation checklist

- [x] 05.01 deterministic runtime implemented.
- [x] 05.02 deterministic runtime implemented.
- [x] 05.03 deterministic runtime implemented.
- [x] 05.04 deterministic runtime implemented.
- [x] 05.05 physical closeout procedure defined.
- [x] 05.06 coexistence contract complete.
- [x] 05.07 presentation authority audit complete.
- [x] 05.08 semantic core implemented.
- [x] 05.09 keyboard navigation implemented.
- [x] 05.10 approved editor-hardening tranche implemented.
- [x] 05.11 approved feedback-orchestration tranche implemented.
- [x] 05.12 approved icon/resource tranche implemented.
- [x] 05.13 approved targeting-presentation tranche implemented.
- [x] 05.14 approved inspection tranche implemented.
- [x] 05.15 approved audiovisual tranche implemented.
- [x] 05.16 approved discoverability/help tranche implemented.
- [ ] **Mandatory real-client/full-pack Stage 05 validation campaign complete.**

## 05.16 merge evidence

- model/layout GREEN: workflow `34758843055`;
- wiring RED: workflow `34759052907`, failed for the expected missing-production contract;
- implementation GREEN: workflow `34760715703`;
- reconciled exact-head GREEN: workflow `34760965231` on `1b71443d2d3a8e7d6b48ab2b606da1218ceaab81`;
- PR #232 squash merge: `12ed7dab61cb32f7ac254ddc4f4f7e77c08a2f4a`;
- post-merge main workflow must remain GREEN before this checkpoint is considered technically closed.

## Completion rule

Stage 05 becomes `VALIDATED / COMPLETE` only when all applicable rows in `docs/qa/casting-ux-manual-matrix.md` are directly observed on the exact assembled build, any legitimate future/evidence-gated rows are explicitly carried forward, and no blocking physical validation failure remains.
