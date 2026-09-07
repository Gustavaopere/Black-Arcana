# 05.01 — Input & Loadouts

## State

`IMPLEMENTED / FINAL VALIDATION DEFERRED`

## Contract

Support a configurable radial key, quick slots and direct-cast bindings. Weapon/book/staff invocation may coexist where integrations expose it.

- Key conflicts remain discoverable/rebindable through Minecraft key mappings.
- Quick-slot defaults are unbound where collision risk is high; no gameplay-critical action requires mouse side buttons.
- Loadouts are server-owned persistent state. The client submits an edit; `ArcanaServerRuntimeManager.handleLoadoutUpdate` validates both registered spell identity and an installed server execution engine before accepting it, then persists accepted state through `BlackArcanaSavedData`.
- A spell may appear only once in a loadout. `LoadoutRegistry` preserves the same bounded/unique invariant for direct writes and snapshot restore, with invalid restore snapshots rejected atomically.
- Persisted loadout entries are parsed fail-closed per caster. An oversized, unparsable or duplicate persisted entry is discarded without invalidating valid neighboring caster entries or aborting server restore.
- `ClientInputController` sends cast intent only. Switching or selecting a loadout cannot bypass server progression, cooldown or resource gates.
- GUI focus suppresses direct cast input.

## Automated coverage

Focused coverage includes `ClientLoadoutSelectionTest`, `LoadoutDraftTest`, `LoadoutRegistryTest`, `ArcanaServerRuntimeManagerLoadoutWiringTest` and `BlackArcanaSavedDataLoadoutTest`; the full CI pipeline also exercises NeoForge build/JAR verification, Foundation GameTests and dedicated-server startup.

Follow-up hardening on 2026-09-07 was developed through isolated RED → GREEN cycles:

- workflow `34147636556` proved that loadout update wiring accepted registry presence without proving an installed execution engine;
- workflow `34148523955` proved that direct `LoadoutRegistry.setLoadout` accepted duplicate spells;
- workflow `34149143928` proved that `LoadoutRegistry.restoreSnapshot` accepted duplicate spells;
- workflow `34149596497` proved that a duplicate persisted loadout could propagate into strict restore and abort that restore path;
- final code checkpoint `30b111fc2a50f8fa3efb4bbf9b8cac1ad4c1f053` passed workflow `34150180682` (#1704): unit tests, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke all GREEN.

These are automated implementation/hardening gates only. They do not promote this task to `VALIDATED / COMPLETE`.

## Deferred acceptance

Keyboard variants, GUI focus in a real client, death/relog and stale server-denied loadouts remain in `docs/qa/casting-ux-manual-matrix.md`. Those rows remain PENDING until directly observed.
