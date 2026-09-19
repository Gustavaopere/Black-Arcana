# 05A.01 — Arcane Danger Model

## Objective
Freeze the domain language and server-owned lifecycle for dangerous/forbidden magic before any spell is retrofitted.

## Contracts
Introduce Black Arcana-owned immutable contracts under `dev.gustavopere.blackarcana.api.hazard` and implementation under `core/hazard`:
- `ArcaneDangerTier`;
- `ArcaneDangerProfile`;
- `ArcaneHazardSnapshot`;
- `ArcaneHazardSession` / bounded session registry;
- `ArcanaDamageInstanceId`;
- `ArcanaDamageProvenance`;
- `ArcaneDamageFamily`/ownership enum;
- preflight decision codes and insufficient-resistance policy.

`ArcanaCastId` remains the root cast identity. Do not create another root cast identifier.

## Danger semantics
Profiles distinguish at least:
- `NORMAL` — no severe hazard system by default;
- `UNSTABLE` — limited strain/backlash risk;
- `DANGEROUS` — canonical serious backlash;
- `FORBIDDEN` — serious backlash plus corruption by default;
- `CATASTROPHIC` — explicitly capable of killing an unprepared caster and may preserve full multi-target aggregation.

Tier is descriptive; exact behavior remains explicit in the profile. A tier must never silently inject unbounded numbers.

## Cast lifecycle
Read-only preflight happens before resource reservation. Hazard session activation happens only after all ordinary prechecks and cost reservation succeed, immediately before effects can cause damage. Activation snapshots all hazard-relevant state. If the effect transaction fails before successful commitment, the session is cancelled/closed according to whether any confirmed damage was already produced.

This task must document the interaction with the frozen Stage 02 engine rather than adding a parallel execution path.

## RED
Add tests proving:
- root cast identity is preserved;
- duplicate damage-instance IDs cannot be recorded twice;
- session registry has hard capacity and TTL/lease semantics;
- invalid/non-finite profile numbers are rejected;
- `NORMAL` can bypass severe hazard processing while dangerous tiers cannot silently become safe;
- session snapshot is immutable after activation.

## GREEN
Implement only the domain model, bounded registries and lifecycle state needed for those tests. No Minecraft damage event integration yet.

## REFACTOR
Keep all pure math/domain types independent from NeoForge event classes. Minecraft adapters belong in later tasks.

## Acceptance
A synthetic dangerous cast can create one bounded immutable hazard session keyed by `ArcanaCastId`, accept deterministic subordinate damage-instance provenance and close without leaking state.

## Engineering closure evidence — 2026-09-19

05A.01 was re-audited against `main@688ff33b583ac9c9938ad2938e376c1f6ed08f61` after the insufficient-resistance policy gap was corrected by PR #345.

Deterministic closure evidence:
- `ArcanaCastId` remains the single root cast identity; damage identities are subordinate only.
- `ArcaneDangerProfile`, `ArcaneHazardSnapshot`, damage provenance/family and bounded session registry are Black Arcana-owned domain contracts.
- insufficient resistance is explicit and server-owned through `ArcaneInsufficientResistancePolicy`; legacy/schema-v1 omission remains fail-closed as `DENY_CAST`, while `ALLOW_WITH_RISK` must be declared explicitly.
- stable hazard preflight decision codes are centralized in `ArcaneHazardPreflightCode`.
- policy-aware server metadata/forecast transport is protocol-versioned and bounded; the client presents the policy but does not decide cast legality.
- canonical Stage 02 ordering is covered by `ArcanaCastHazardHookTest`: hazard preflight precedes reservation, activation follows successful reservation and precedes effects, and failed activation/effect cancels/refunds through the existing cast transaction.
- `ArcaneDangerProfileTest` covers bounded/non-finite rejection, NORMAL bypass and explicit policy semantics.
- `ArcaneHazardSessionRegistryTest` covers root preservation, duplicate damage-instance rejection, capacity, TTL/lease expiry, immutable activated snapshot and closeout without registry leakage.
- the reconciled PR head `c8a8a9ce3560ee15a77a8cae00db4d347cebcb67` passed full CI run `35466146982`, including unit tests, NeoForge build, Foundation GameTest, dedicated-server smoke and Stage 05 QA companion smoke.
- merged `main@688ff33b583ac9c9938ad2938e376c1f6ed08f61` passed canonical post-merge run `35466427939`, including both dedicated-server smoke paths.

No real-client/provider-native observation is required by 05A.01 itself. Later 05A plans retain their own D035/Stage 09 physical-validation obligations.

