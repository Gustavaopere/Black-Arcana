# 05 — Casting & UX

## State

`IMPLEMENTED / PHYSICAL VALIDATION PENDING`

The approved deterministic Stage 05.01–05.16 implementation/planning tranches are complete or merged. Stage 05 is **not** yet `VALIDATED / COMPLETE` because the mandatory assembled real-client/full-pack campaign has not been directly executed to completion.

Automated CI is implementation evidence. It never converts a manual row to PASS.

For the fastest current view, open [`00-execution-status.md`](00-execution-status.md).

## Filename convention

This directory uses the same visual completion convention as completed earlier stages:

- `✅-...` — declared plan/audit scope is fully closed;
- `🟡-PENDENTE-...` — implementation/planning is present, but a mandatory direct validation gate remains open;
- unprefixed implementation checkpoints record evidence and are not separate numbered plans.

Evidence-gated optional integrations are not treated as unfinished work when the plan explicitly requires exact API/provider/runtime evidence before implementation.

Historical planning prose and implementation checkpoints may retain a pre-normalization basename in backticks when referring to the artifact name that existed at the time of that evidence. Those occurrences are historical identifiers, not the current canonical path. The links in this README are the authoritative current filenames.

## Canonical planning map

- [`00-master-plan.md`](00-master-plan.md) — Stage 05 architecture and planning map.
- [`00-execution-status.md`](00-execution-status.md) — current completion/pending ledger.

### Numbered plans

1. [`🟡-PENDENTE-01-input-loadouts.md`](🟡-PENDENTE-01-input-loadouts.md) — input lifecycle, loadouts, quick/selected casting, persistence and synchronization. Runtime implemented; physical validation pending.
2. [`🟡-PENDENTE-02-radial-wheel.md`](🟡-PENDENTE-02-radial-wheel.md) — radial selection/paging/geometry. Runtime implemented; physical validation pending.
3. [`🟡-PENDENTE-03-contextual-hud.md`](🟡-PENDENTE-03-contextual-hud.md) — contextual HUD/result/hazard/gate presentation. Runtime implemented; physical validation pending.
4. [`🟡-PENDENTE-04-accessibility-client-config.md`](🟡-PENDENTE-04-accessibility-client-config.md) — client presentation/accessibility preferences. Runtime implemented; physical validation pending.
5. [`🟡-PENDENTE-05-final-client-validation-handoff.md`](🟡-PENDENTE-05-final-client-validation-handoff.md) — mandatory assembled-client closeout campaign. **This is the principal remaining Stage 05 blocker.**
6. [`✅-06-modpack-coexistence.md`](✅-06-modpack-coexistence.md) — coexistence/authority contract complete; unsupported integrations remain evidence-gated.
7. [`✅-07-presentation-data-contracts.md`](✅-07-presentation-data-contracts.md) — presentation-authority/data-contract audit complete.
8. [`🟡-PENDENTE-08-visual-language-state-semantics.md`](🟡-PENDENTE-08-visual-language-state-semantics.md) — semantic core implemented; direct client validation pending.
9. [`🟡-PENDENTE-09-keyboard-focus-navigation.md`](🟡-PENDENTE-09-keyboard-focus-navigation.md) — keyboard navigation implemented; direct client validation pending.
10. [`🟡-PENDENTE-10-loadout-editor-information-architecture.md`](🟡-PENDENTE-10-loadout-editor-information-architecture.md) — approved editor-hardening tranche implemented; A.7 physical validation pending.
11. [`🟡-PENDENTE-11-contextual-feedback-orchestration.md`](🟡-PENDENTE-11-contextual-feedback-orchestration.md) — approved bounded arbitration implemented; direct client validation pending.
12. [`🟡-PENDENTE-12-iconography-resource-resolution.md`](🟡-PENDENTE-12-iconography-resource-resolution.md) — approved icon/resource tranche implemented; direct resource/client validation pending.
13. [`🟡-PENDENTE-13-targeting-aim-presentation.md`](🟡-PENDENTE-13-targeting-aim-presentation.md) — authority-safe local-observation tranche implemented; direct client validation pending.
14. [`🟡-PENDENTE-14-spell-details-inspection-presentation.md`](🟡-PENDENTE-14-spell-details-inspection-presentation.md) — bounded static inspection implemented; direct client validation pending.
15. [`🟡-PENDENTE-15-casting-vfx-audio-animation-presentation.md`](🟡-PENDENTE-15-casting-vfx-audio-animation-presentation.md) — provider-free audiovisual tranche implemented; physical/full-pack audiovisual QA pending.
16. [`🟡-PENDENTE-16-onboarding-discoverability-contextual-help.md`](🟡-PENDENTE-16-onboarding-discoverability-contextual-help.md) — bounded first-use/help/live-binding tranche implemented; physical/full-pack help validation pending.

## Implementation checkpoints

The following files record exact implementation evidence and do not represent extra numbered plans:

- `10-loadout-editor-implementation-checkpoint.md`;
- `11-contextual-feedback-implementation-checkpoint.md`;
- `12-iconography-resource-implementation-checkpoint.md`;
- `13-targeting-aim-implementation-checkpoint.md`;
- `14-spell-details-inspection-implementation-checkpoint.md`;
- `15-casting-vfx-audio-animation-implementation-checkpoint.md`;
- `16-onboarding-discoverability-implementation-checkpoint.md`.

## Authority boundary

Stage 05 remains presentation/input infrastructure. The client expresses intent and renders legitimately available state; the server remains authoritative for spell identity/admission, progression, cost, cooldown, target resolution, Arcane Danger and world-effect admission. Provider-specific resources and presentation remain provider-owned unless an exact supported integration contract is proven.

RPG Skill Tree remains responsible only for progression/Mastery/perks/gates; Black Arcana remains authoritative for the magic runtime.

## Remaining closeout

The mandatory remaining work is the direct real-client/full-pack campaign in `docs/qa/casting-ux-manual-matrix.md`, using the exact assembled build and recording PASS/FAIL/BLOCKED evidence. Any actual FAIL discovered there is fixed, retested and reflected in the affected `🟡-PENDENTE-...` plan before that file can become `✅-...`.
