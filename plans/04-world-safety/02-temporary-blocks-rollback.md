# 04.02 — Temporary Blocks & Rollback

## Objective
Support impactful-looking magic without permanent grief.

## Work
- Track Black Arcana-owned temporary mutations with owner, original state, expiry and dimension/chunk identity.
- Restore safely only when the current state is still the Black Arcana replacement; never overwrite later player edits blindly.
- Persist pending restoration where necessary.
- Bound storage and clean stale entries.

## Acceptance
Tests cover restart, chunk unload, player modification after cast, overlapping temporary effects and expiry cleanup.
