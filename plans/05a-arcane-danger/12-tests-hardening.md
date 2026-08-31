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

## Optional-provider snapshot checkpoint
Equipment snapshot reuse is already covered by the canonical equipment tests, including root-cast reuse across Arcane/Corruption channels and later equipment-state recapture. `ArcaneOptionalProviderSnapshotHardeningTest` extends that acceptance evidence through the generic optional-provider boundary used by Curios/RPG contributions: a root cast freezes CURIO + RPG Arcane Resistance at activation, removing the Curio/perk afterward cannot rewrite delayed Backlash for that root, and a later root cast observes the new provider state at its own preflight boundary.

This checkpoint closes the explicit equipment/Curios/RPG/provider snapshot and post-cast swap row at the Stage 05A Arcane Resistance/Backlash boundary. It does not claim a concrete third-party Curios or RPG Skill Tree adapter where one is not loaded, and it does not by itself complete the remaining 05A.12 acceptance matrix.

## Damage-instance dedupe and bounded root-ledger checkpoint
`ArcaneBacklashLedgerTest` and `ArcaneHazardHardeningTest` already prove that a repeated `damageInstanceId` cannot settle twice, including concurrent attempts against the same root cast. `ArcaneBacklashLedgerRegistryTest.boundedCapacityRejectsOverflowUntilExpiryReopensSlotAtLeaseBoundary` now closes the registry-level bound: a full registry rejects an additional root without growing, the last valid lease tick still settles, the expiry boundary fails closed, and opening a new root at that boundary prunes the expired ledger before applying the capacity check so the freed slot can be reused without exceeding the configured maximum.

This checkpoint closes the explicit damage-instance dedupe and root-cast ledger-limit row. It does not by itself close the separate full stress row for concurrent casts, delayed settlements and bounded ledgers, and it does not complete the remaining 05A.12 acceptance matrix.

## Damage-family attribution checkpoint
`ArcaneBacklashGameTests.confirmedMultiHitDamageProducesExactNonRecursiveBacklash` already exercises a multi-target root cast through the live NeoForge damage hook, proving direct multi-hit/AoE-style aggregation from confirmed health loss rather than nominal damage. `ArcaneBacklashGameTests.projectileDotChainAndOwnedSummonAttributionRespectFrozenPolicy` extends the real Minecraft boundary across `PROJECTILE`, `DAMAGE_OVER_TIME`, `CHAIN` and `OWNED_SUMMON`: projectile/DoT/chain damage settles against the same root ledger, canonical policy lets a non-opted owned summon damage its target without creating Backlash credit, and a separate root with frozen `allowOwnedSummon=true` admits owned-summon damage and settles exact zero-resistance 1:1 Backlash.

This checkpoint closes the explicit direct/AoE/multi-hit/projectile/DoT/explicitly-owned-summon attribution row at the Stage 05A NeoForge gateway. Delayed lease timing remains independently covered by the core hardening tests; this checkpoint does not by itself complete the remaining 05A.12 acceptance matrix.

## Resistance numeric-boundary checkpoint
`ArcaneResistanceCurveTest`, `CorruptionResistanceCurveTest`, `ArcaneResistanceProviderRegistryTest`, `CorruptionResistanceProviderRegistryTest` and `CorruptionStateServiceTest` already establish the canonical diminishing-return curves, zero-resistance baseline, configured caps, monotonic behavior, corruption acquisition floor and fail-closed provider isolation. `ArcaneResistanceNumericHardeningTest` closes the remaining explicit numeric-boundary evidence: both channels reject `NaN`, positive/negative infinity, negative and above-absolute-cap contribution values; `Double.MAX_VALUE` curve inputs saturate to the configured resistance cap without non-finite output; null provider lists and null entries fail closed without poisoning valid sibling contributions; and canonical registries clamp maximum finite contributions before curve evaluation.

The same hardening test feeds real canonical Arcane Resistance snapshots into `ArcaneBacklashLedger`: `R=0` settles exactly 1:1 (`100%`) Backlash, while canonical capped resistance resolves to the expected `1/7` residual and settles a finite exact reduced amount. This checkpoint therefore closes the explicit `R=0 -> 100%` invariant and the Resistance/Corruption Resistance curves, floors, caps, null/NaN/infinity/negative/overflow-boundary row. It does not by itself complete the remaining 05A.12 acceptance matrix.

## Integrated concurrent/delayed bounded-ledger stress checkpoint
`ArcaneHazardHardeningTest` already proves isolated high-contention root-session admission, exactly-once concurrent damage claims and 200 linear concurrent settlements, while `ArcaneBacklashLedgerRegistryTest` proves deterministic capacity rejection plus lease-boundary reclamation. `ArcaneBacklashLedgerStressTest.concurrentRootsDelayedSettlementsAndCapacityReclamationStayBounded` combines those concerns at the actual Backlash ledger registry boundary: 48 simultaneous root opens race against a capacity of 32, every admitted root receives four delayed DoT settlements concurrently on the last valid lease tick, every root rejects a further settlement exactly at expiry without changing its accumulated totals, and a second 48-root admission race at the expiry boundary reclaims the expired ledgers and admits exactly 32 replacements without registry overgrowth or cross-root damage contamination.

This checkpoint closes the explicit stress row for concurrent casts, delayed settlements and bounded ledgers. It does not close the separate Backlash crit/lifesteal/proc/mastery exclusion row and therefore does not by itself complete 05A.12.

## Terminal Backlash offensive-credit exclusion checkpoint
The exclusion is enforced by existing server-side boundaries rather than by four parallel bonus systems. `ArcanaDamageProvenance` rejects any `ARCANE_BACKLASH` provenance marked `hazardEligible=true`; `ArcaneBacklashLedger` rejects terminal Backlash before claiming a damage-instance id; and `MinecraftArcaneDamagePipeline` applies the dedicated `black_arcana:arcane_backlash` `DamageSource` directly instead of routing it through `hurtAttributed(...)`. `ArcaneBacklashOffensiveCreditExclusionTest` locks the provenance, pre-claim and no-inference invariants.

`ArcaneBacklashGameTests.dedicatedBacklashSourceIsAttackerlessAndUnattributed` exercises the live NeoForge/Minecraft boundary: the dedicated Backlash source has neither causing nor direct attacker entity, deals real health damage, and still creates no eligible damage, recursive Backlash settlement or claimed damage-instance state in an active root ledger. That attackerless/unattributed topology is the canonical Black Arcana exclusion for crit-triggered additions, lifesteal/sustain and BA-owned offensive proc chains; no separate BA damage-side credit observer exists to bypass it.

RPG mastery is a concrete integration and is checked separately. `RpgMasteryAwardObserver` is a `CastSuccessObserver`, not a damage observer. `RpgMasteryBacklashExclusionTest` proves a terminal Backlash settlement produces zero mastery awards while an explicit committed-cast success callback remains able to award exactly once. Together with the existing live non-recursion GameTest, these regressions close the explicit Backlash recursion/crit/lifesteal/proc/mastery exclusion row for Black Arcana-owned behavior.

With this checkpoint, every row listed under `Required automated coverage` has explicit automated evidence. 05A.12's automated hardening matrix is therefore closed once the full runtime gates below are green. This does not close 05A.11 presentation, does not satisfy the Stage 05 real-client matrix, does not mark Stage 05A complete, and does not authorize promotion of Stage 06/07.

## Runtime gates
Full CI must pass JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke. Optional-provider profiles are tested separately where practical.

## Exit rule
No Stage 05A task receives ✅ and Rituals/Spell Domains are not canonicalized against hazard-sensitive behavior until these gates are green.
