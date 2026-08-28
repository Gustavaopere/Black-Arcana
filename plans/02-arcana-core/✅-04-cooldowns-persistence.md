# 02.04 — Cooldowns & Persistence

## Scope
Per-spell, shared-category and grand-ritual cooldowns; optional charge pools; server persistence across logout/restart where balance requires it.

## Rules
- Use monotonic/game-time-safe representation appropriate to persistence.
- No logout reset exploits.
- Config changes clamp/migrate safely.
- Cooldowns can be reduced only through bounded, explicit modifiers.

## Acceptance
Tests cover save/load, dimension change, death, logout, clock edge cases and shared cooldown groups.
