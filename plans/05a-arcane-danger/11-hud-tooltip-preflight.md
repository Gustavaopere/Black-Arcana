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

## Acceptance
Tests cover payload bounds/state clearing and authoritative denial text. Manual Stage 05/09 visual matrix covers common GUI scales, disabled HUD, reduced-motion/flash settings and stale reconnect state.
