# 05A.11 — HUD, Tooltip & Preflight

## Objective
Expose danger clearly before casting without making client prediction authoritative or adding a permanent clutter bar.

## Presentation
- Spell tooltip/radial metadata shows danger tier and concise resistance recommendation.
- Contextual preflight may show current effective Arcane/Corruption Resistance, expected risk class and hard-gate reason.
- Corruption/strain feedback appears only when relevant and respects Stage 05 accessibility/reduced-effects settings.
- Exact server settlement remains authoritative; client values are advisory presentation derived from synchronized bounded data.

## Networking
No client packet may submit resistance, corruption, backlash damage, danger tier or bypass decisions. Synchronization is event-driven and bounded, not per-tick full-state spam.

## Implemented selected-spell resistance sublane
The contextual HUD now has a server-authored read-only Arcane Resistance forecast for the currently selected spell:

- the client submits only a bounded spell id and monotonic request id;
- the server resolves the canonical danger profile and computes effective Arcane Resistance through a runtime-scoped preview mirror of gameplay resistance providers;
- preview availability fails closed unless every gameplay Arcane Resistance provider has a side-effect-free mirror and the aggregate snapshot is diagnostic-free;
- standard equipment, RPG Skill Tree hazard attributes and optional Curios equipment currently install preview mirrors;
- preview queries do not open hazard sessions, reserve corruption/strain state, consume emergency protection or award progression/mastery;
- the server rate-limits forecast requests and the client refreshes only while contextual selection feedback can be displayed;
- stale responses are rejected by request id and danger-profile reload clears the cached forecast;
- for non-normal danger tiers the HUD can display current/minimum/recommended Arcane Resistance plus `Safe`, `Attention`, `Dangerous` or `Unavailable` presentation state;
- the original synchronized static danger metadata remains the fallback when a dynamic forecast is unavailable or has not arrived.

The detailed authority/anti-abuse contract is recorded in `docs/qa/stage05a11-resistance-forecast.md`.

## Still open
This sublane does **not** complete 05A.11. The following remain open:

- complete pre-cast presentation of non-resistance hard-gate reasons where a safe read-only projection is justified; canonical strain, cooldown/resource/progression and other denials remain authoritative through normal cast results unless separately projected;
- spell-tooltip coverage beyond the existing radial/static hazard presentation;
- any Corruption Resistance / strain feedback that is ultimately retained by the design;
- real-client validation across the Stage 05 manual matrix, including reconnect/stale state, GUI scales, disabled HUD and accessibility settings.

## Acceptance
Automated tests cover payload bounds/state clearing, authoritative denial text, forecast payload/codec invariants and fail-closed preview-provider completeness/diagnostics. Manual Stage 05/09 visual matrix covers common GUI scales, disabled HUD, reduced-motion/flash settings, stale reconnect state and the selected-spell hazard forecast presentation.
