# 05.03 — Contextual HUD & Feedback

## Philosophy
Show information when it matters; do not add a permanent Black Arcana resource bar by default.

## Display candidates
Selected spell, short cooldown, provider-specific cost, charge/channel state, denial reason and temporary grand-ritual/domain timer.

## Requirements
Provider adapters expose presentation data without client-side authority. HUD can be disabled/positioned/scaled.

## Acceptance
No persistent resource HUD when idle; failure messages identify the actual authoritative denial reason; dedicated server has zero client classloading.
