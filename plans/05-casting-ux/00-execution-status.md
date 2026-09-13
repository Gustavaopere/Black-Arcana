# Stage 05 — Casting Runtime & Client Contracts — Execution Status

## Current state

`IMPLEMENTED / PHYSICAL RUNTIME-INPUT VALIDATION PENDING`

The deterministic runtime/client-contract implementation is present. Remaining presentation polish and visual QA are tracked outside the numbered stage in `plans/visual-production/05-casting-ux/` and do not by themselves block downstream runtime implementation.

## Engineering ledger

| Item | State | Runtime truth | Remaining engineering gate |
|---|---|---|---|
| 05.01 Input & Loadouts | 🟡 | bounded server-owned loadout, persistence, rebindable intent and canonical cast convergence implemented | physical input/loadout/session rows |
| 05.02 Radial Selection | 🟡 | bounded paging/selection semantics implemented; selection is not casting | physical toggle/hold/page/input-lock rows |
| 05.03 Contextual Feedback Data | 🟡 | server-authored result/hazard/gate presentation data and stale-state rules implemented | physical stale/correlation/state rows where required |
| 05.04 Client Config Authority | 🟡 | client-only config/persistence/input semantics implemented | physical config/input lifecycle rows |
| 05.05 Validation Handoff | 🟡 | closeout procedure exists | execute remaining runtime/input/full-pack rows; visual-only rows are delegated |
| 05.06 Modpack Coexistence | 🟡 | authority/coexistence policy exists | observe required input/provider coexistence scenarios |
| 05.07 Presentation Data Contracts | ✅ | data-authority audit/gates complete | none inside the audit; new fields remain evidence-gated |

## Extracted presentation work

Former 05.08–05.16 planning remains historically implemented/evidenced where stated, but future planning and perceptual QA ownership moved to `plans/visual-production/05-casting-ux/`.

The moved files are not deleted work and are not renumbered runtime stages. See `plans/visual-production/MIGRATION-MAP.md`.

## Completion rule

Stage 05 engineering completion is judged on its runtime/input/authority contracts and required physical checks. Visual-production completion is judged separately on UI/HUD/art/audio/animation/accessibility presentation acceptance.

Neither lane may fabricate PASS evidence for the other.
