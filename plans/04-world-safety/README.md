# 04 — World Safety

All dangerous Black Arcana content consumes these contracts before spells are implemented.

## Tasks
- Global/per-spell world-effect policy.
- Temporary block/effect lifecycle and rollback.
- Area budgets, chunk safety and scheduler.
- PvP, bosses, claims/protected-area adapters where appropriate.

## Exit criteria
Synthetic explosions/fire/block mutation cannot bypass policy, exceed configured budgets or leak temporary world state across restart/chunk unload.
