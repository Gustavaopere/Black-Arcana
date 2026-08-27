# 07.05 — Black Flame

## Fantasy
A soul-corrupting flame family with visually aggressive behavior but server-controlled terrain impact.

## Model
Separate entity burn/status, visual flame propagation and block mutation. Spread uses a bounded frontier scheduler.

## World modes
`COSMETIC`: visual only. `TEMPORARY`: reversible scorched/fire-like blocks. `LIMITED`: bounded permanent mutation. `FULL`: explicit server opt-in.

## Balance
Boss damage modifier/cap, spread radius/count, duration, concurrent frontier cap and friendly-fire policy.

## Acceptance
No vanilla-style uncontrolled fire cascade; restart/chunk tests clean temporary state; stress test proves bounded spread work.
