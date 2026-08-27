# 00.03 — Domain Contracts

## Objective
Freeze minimal Black Arcana-owned interfaces before external integrations or content.

## Candidate contracts
- `ArcanaSpellId` / `ArcanaSpellDefinition`
- `ArcanaCastContext` and immutable cast request/result
- `ArcanaCost` + `CostProvider`
- `CooldownService`
- `ProgressionGate`
- `TargetSelector`
- `ArcanaEffect` / effect result
- `WorldEffectPolicy` gateway
- `ArcanaIntegration` capability/availability descriptor
- presentation metadata separated from server execution

## Principles
No Minecraft client classes in domain contracts. External mod types stay in adapters. Failure results are structured, not exception-driven for expected denial.

## Acceptance
Unit tests prove deterministic validation ordering and contract invariants. A fake spell can execute against fake cost/target/world-policy providers with no external magic mod present.
