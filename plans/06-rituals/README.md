# 06 — Rituals

Rituals are reserved for meaningful occult preparation rather than routine combat casting.

## Candidate purposes
Permanent knowledge unlocks, soul contracts, rare transformations, domain creation/upgrades, high-impact bargains and grand world effects.

## Implementation state

Stage 06 is canonical on `main` as `IMPLEMENTED / FINAL VALIDATION DEFERRED` via PR #43. Its bounded ritual core, session persistence, exactly-once completion ledger, lifecycle wiring, Eidolon bridge and Malum spirit-backed grand-ritual path have automated evidence. Real-modpack/manual provider acceptance remains deferred under D031 and must not be inferred as PASS from CI.

## Tasks
- [Ritual contracts/validation](✅-01-ritual-contracts.md).
- [Eidolon ritual bridge](✅-02-eidolon-ritual-bridge.md).
- [Malum spirit components](✅-03-malum-spirit-components.md).
- [Black Arcana grand rituals](✅-04-grand-rituals.md) for gaps not supported by external APIs.
- [Final Validation Handoff](05-final-validation-handoff.md).

## Final validation handoff

`plans/06-rituals/05-final-validation-handoff.md` is the executable closeout plan for the remaining real-provider/modpack evidence. It uses the current production representatives `black_arcana:eidolon_anchor_attunement` and `black_arcana:veil_anchor_consecration`, preserves the different anchor-scoped versus caster-scoped completion contracts, and requires a real production activation surface before the native grand ritual may receive manual PASS.

Creating or merging the handoff does **not** validate Stage 06, does not alter `plans/STATUS.md`, and does not convert automated provider tests into real-provider acceptance.

## Exit criteria
At least one integrated ritual and one Black Arcana grand ritual execute transactionally, respect progression/world safety and recover safely from interruption/restart as designed.
