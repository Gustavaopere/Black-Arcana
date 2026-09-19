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
