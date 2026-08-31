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

## Runtime gates
Full CI must pass JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke. Optional-provider profiles are tested separately where practical.

## Exit rule
No Stage 05A task receives ✅ and Rituals/Spell Domains are not canonicalized against hazard-sensitive behavior until these gates are green.
