# 05A.09 — Public Hazard API

## Objective
Expose stable, server-side Black Arcana contracts so RPG Skill Tree and future mods can contribute hazard mitigation without owning the calculation.

## Contracts
- `ArcaneResistanceProvider` and `CorruptionResistanceProvider` return bounded, read-only contributions plus provenance.
- Provider registration is explicit, duplicate-safe and bounded.
- Immutable snapshots expose total + source breakdown without leaking mutable provider state.
- Danger-profile/preflight queries are read-only and side-effect free.
- Hazard observers receive settled immutable events and cannot mutate the original cast transaction.
- Missing/incompatible optional providers fail safely and contribute zero; they never grant bypasses.

## Safety
Provider exceptions/linkage failures are isolated and diagnosed. No provider may trigger inventory mutation, resource spending, chunk loads or network traffic from a query callback.

## Acceptance
Unit tests cover ordering, duplicate ids, invalid/NaN/negative contributions, provider exceptions, caps and deterministic snapshot totals. Dedicated-server smoke proves the API loads without optional consumers.
