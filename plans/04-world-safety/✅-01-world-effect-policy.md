# 04.01 — World Effect Policy

## Modes
At minimum: `OFF`, `COSMETIC`, `TEMPORARY`, `LIMITED`, `FULL`.

## Scope
Explosion block damage, fire/spread, block replacement, terrain carving, fluid mutation, persistent summoned structures and other grief-capable effects.

## Requirements
- Server default favors `TEMPORARY`/`LIMITED` for destructive magic.
- Global cap plus per-spell override.
- Entity damage can be configured independently from terrain damage where mechanically sensible.
- Policy check is centralized; content code cannot directly mutate world when the mutation is policy-governed.

## Acceptance
Unit/GameTests prove each mode's semantics and deny direct bypass paths in Black Arcana code review/tests.
