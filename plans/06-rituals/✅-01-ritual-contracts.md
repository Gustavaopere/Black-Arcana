# 06.01 — Ritual Contracts

## Model
Ritual definition includes anchor, participant/caster, components, spatial conditions, time/environment predicates, progression gates, cost transaction and result.

## Requirements
- Validate before consumption where possible.
- Commit components atomically at the defined ritual phase.
- Define interruption/refund semantics.
- No chunk-force-load requirement by default.
- Observable state uses bounded persistence.

## Acceptance
Tests cover invalid layouts, missing components, interruption, duplicate activation and multiplayer race conditions.
