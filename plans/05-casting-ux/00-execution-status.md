# Stage 05 — Casting Runtime & Client Contracts — Execution Status

## Current state

`IMPLEMENTED / PHYSICAL RUNTIME-INPUT VALIDATION PENDING`

The deterministic runtime/client-contract implementation is present. Remaining presentation polish and perceptual QA are tracked in `plans/visual-production/05-casting-ux/` and do not by themselves block downstream runtime implementation.

## Engineering ledger

| Item | State | Runtime truth | Remaining engineering gate |
|---|---|---|---|
| 05.01 Input & Loadouts | 🟡 | bounded server-owned loadout, persistence, rebindable intent and canonical cast convergence implemented | physical input/loadout/session rows |
| 05.02 Radial Selection | 🟡 | bounded paging/selection semantics implemented; selection is not casting | physical toggle/hold/input-lock authority rows; geometry/readability is visual-production |
| 05.03 Contextual Feedback Data | 🟡 | server-authored result/hazard/gate data and stale-state rules implemented | physical stale/correlation/state-authority rows; layout/wording is visual-production |
| 05.04 Client Config Authority | 🟡 | client-only config/persistence/input semantics implemented | prove client settings cannot affect gameplay; perceptual effect acceptance is visual-production |
| 05.05 Physical Validation | 🟡 | runtime/input/provider client handoff retained | execute remaining authority/input/integration rows; presentation matrix split to visual-production |
| 05.06 Modpack Coexistence | 🟡 | Iron's-hosted BA path now hard-disables provider mana/cooldown settlement, retains one-root convergence and optional-provider isolation with regression coverage | observe required runtime/provider coexistence; overlap/animation/readability is visual-production |
| 05.07 Presentation Data Contracts | ✅ | data-authority audit/gates complete | none inside the audit; new fields remain evidence-gated |

## Extracted presentation work

05.01–05.06 presentation halves and the former 05.08–05.16 presentation plans are tracked under `plans/visual-production/05-casting-ux/`. Historical checkpoints/evidence retain their factual meaning.

See `plans/visual-production/MIGRATION-MAP.md` for the exact move/split ledger.

## Completion rule

Stage 05 engineering completion is judged on runtime/input/authority contracts and required physical authority checks. Visual-production completion is judged separately on UI/HUD/art/audio/animation/accessibility/perceptual acceptance. Neither lane may fabricate PASS evidence for the other.
