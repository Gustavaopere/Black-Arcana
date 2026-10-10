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

The historical 2026-10-01 deterministic audit in `docs/qa/rituals-final-validation-evidence.md` found no external caller of `RitualEngine.start(...)` on `main@44dfac8683a013e147f678e1016e91ed0ac128d8`. That finding is preserved as a dated checkpoint, not the current runtime status. PR #733 subsequently installed a server-authoritative Survival altar ingress (`MinecraftVeilAnchorConsecrationRuntime` → `VeilAnchorActivationService` → the existing `RitualEngine.start`), with additional lifecycle, fairness, persistence and restore hardening through PR #739. Latest reconciled source baseline: `main@1a7078dfc52ff1bcb97584a0216c5e3ffd764192` after PR #740. Stage 06.05 remains 🟡, and physical Malum/Eidolon, client/pack and save/restart/crash checks remain PENDING / DEFERRED TO STAGE 09 under D035; automated ingress is not a real-player PASS.

## Exit criteria
At least one integrated ritual and one Black Arcana grand ritual execute transactionally, respect progression/world safety and recover safely from interruption/restart as designed.
