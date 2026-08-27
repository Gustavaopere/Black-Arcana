# 07.06 — Forbidden Domains

## Objective
Reimagine reality/domain-style endgame magic as bounded, configurable temporary battle spaces or localized fields.

## Candidate variants
Arsenal, soul and blood-oriented domains only after Stage 01 approves them.

## Architecture decision required
Evaluate localized in-world field versus isolated temporary dimension/instance. Multiplayer, persistence, teleport recovery, death, logout, server restart and chunk cleanup take priority over spectacle.

## Safety
Hard radius/duration/entity budgets; no arbitrary terrain destruction by default; robust emergency return path.

## Acceptance
No stranded players, orphan dimensions/chunks/entities or duplicated inventory/state across all lifecycle tests.
