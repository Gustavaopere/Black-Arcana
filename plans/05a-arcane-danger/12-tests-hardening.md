# 05A.12 — Tests & Hardening

## Required automated coverage
- Exact `R=0 -> 100%` linear backlash invariant.
- Resistance/corruption curves, floors, caps, NaN/infinity/negative inputs and overflow boundaries.
- Direct, AoE, multi-hit, projectile, DoT and explicitly-owned summon attribution.
- Damage-instance dedupe and root-cast ledger limits.
- Backlash recursion, crit, lifesteal, proc and mastery exclusions.
- Equipment/Curios/RPG/provider snapshots and post-cast gear/perk swaps.
- Corruption/strain persistence across relog/restart/death under the defined contracts.
- PvP/team/boss/protection semantics where hazard consequences interact with Stage 04 policies.
- Malformed datapack/profile rejection and migration of persisted hazard state.
- Stress tests for concurrent casts, delayed settlements and bounded ledgers.

## Persistence/death contract checkpoint
Corruption and Arcane Strain are server-owned states keyed by player UUID. Relog, restart and death/respawn are not cleanse paths; Strain may only decrease through its normal lazy recovery rules. `BlackArcanaSavedDataHazardStateTest` covers save/load/restart reconstruction and malformed-state sanitation. `BlackArcanaLifecycleGameTests.playerDeathDoesNotResetPersistentHazardState` exercises the real `ServerPlayer.die(...)` route and proves death does not clear either channel.

This checkpoint closes the explicit death-cleanse gap only. It does not by itself complete 05A.12; the remaining required rows still need their own verified coverage before the task receives ✅.

## Stage 04 entity-protection boundary checkpoint
Attributed hostile spell damage now has a canonical NeoForge gateway that resolves authoritative server facts and delegates PvP, allied-target, boss and optional protection-adapter decisions to the frozen Stage 04 `EntityInteractionAdmissionService` before invoking the lower-level hazard damage pipeline. Denied interactions never call `target.hurt`, never become confirmed eligible damage and therefore cannot create Arcane Backlash settlement. `ArcaneHazardProtectionGameTests` exercises PvP-disabled, allied, protected and boss targets against the live Minecraft/NeoForge path.

This checkpoint closes the explicit PvP/team/boss/protection interaction row at the Stage 05A damage boundary. It does not relax Stage 04 caps or create parallel protection heuristics, and it does not by itself complete the remaining 05A.12 acceptance matrix.

## Malformed profile and persisted-state migration checkpoint
The Stage 05A danger-profile datapack boundary is strict and non-executable. `ArcaneDangerDataReloadListenerTest` proves rejection of unknown executable-like fields, resource-id mismatch, unsupported `schemaVersion`, out-of-bounds `profileVersion`, impossible resistance hints and dangerous profiles that configure away mandatory Backlash.

Persisted pending Backlash has a real schema-1 migration path: legacy aggregate `pending_backlash` entries restore as explicit unprotected `PendingBacklashDebt.legacy(...)`, while contextual `pending_backlash_debts` preserves causal identity and frozen protection state when valid. `BlackArcanaSavedDataPendingBacklashContextTest` proves both the legacy migration and the fail-closed corruption rule: malformed contextual state retains only the bounded amount as an unprotected legacy debt and never invents root-cast, damage-instance or emergency-protection context.

This checkpoint closes the explicit malformed danger-profile / real persisted-hazard migration evidence row. No synthetic pre-schema format is introduced; unsupported top-level persistence schemas continue to fail closed. It does not by itself complete the remaining 05A.12 acceptance matrix.

## Runtime gates
Full CI must pass JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke. Optional-provider profiles are tested separately where practical.

## Exit rule
No Stage 05A task receives ✅ and Rituals/Spell Domains are not canonicalized against hazard-sensitive behavior until these gates are green.
