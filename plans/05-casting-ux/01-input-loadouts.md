# 05.01 — Input & Loadouts

## Design
Support a configurable radial key, quick slots and direct-cast bindings. Weapon/book/staff invocation can coexist where integrations expose it.

## Requirements
- Key conflicts discoverable/rebindable.
- Loadouts persist per player; server validates spell availability.
- Switching loadouts never bypasses cooldown/progression.
- No gameplay-critical dependence on mouse side buttons.

## Acceptance
Client tests/manual matrix covers keyboard variants, GUI focus, death/relog and server-denied stale loadouts.
