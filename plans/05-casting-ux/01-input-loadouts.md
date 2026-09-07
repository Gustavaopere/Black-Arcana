# 05.01 — Input & Loadouts

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

## Contract

Support a configurable radial key, quick slots and direct-cast bindings. Weapon/book/staff invocation may coexist where integrations expose it.

- Key conflicts remain discoverable/rebindable through Minecraft key mappings.
- Quick-slot defaults are unbound where collision risk is high; no gameplay-critical action requires mouse side buttons.
- Loadouts are server-owned persistent state. The client submits an edit; `ArcanaServerRuntimeManager.handleLoadoutUpdate` validates resolved spell availability before accepting it and persists accepted state through `BlackArcanaSavedData`.
- `ClientInputController` sends cast intent only. Switching or selecting a loadout cannot bypass server progression, cooldown or resource gates.
- GUI focus suppresses direct cast input.

## Automated coverage

Focused tests include `ClientLoadoutSelectionTest` and `LoadoutDraftTest`; the full CI pipeline also exercises server runtime/persistence and dedicated-server startup.

## Deferred acceptance

Keyboard variants, GUI focus in a real client, death/relog and stale server-denied loadouts remain in `docs/qa/casting-ux-manual-matrix.md`. Those rows remain PENDING until directly observed.
