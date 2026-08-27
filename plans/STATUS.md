# Black Arcana — Status

Last updated: 2026-08-27

## Current state

Repository initialized. Canonical planning structure created. No gameplay stage is complete and no implementation should be treated as frozen yet.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ⬜ Not started | Scaffold, CI, provenance, contracts |
| 01 Reference Catalog | ⬜ Not started | Clean-room mechanic inventory/classification |
| 02 Arcana Core | ⬜ Not started | Server-authoritative execution kernel |
| 03 Integration Layer | ⬜ Not started | Iron's, Ars, Eidolon, Malum, RPG adapters |
| 04 World Safety | ⬜ Not started | Destruction policy, rollback, budgets |
| 05 Casting & UX | ⬜ Not started | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Active stage

`00-foundation`

## Immediate next actions

1. Scaffold the NeoForge 1.21.1 / Java 21 project and CI.
2. Establish clean-room provenance rules and upstream/reference inventory format.
3. Freeze core public contracts before any content implementation.
4. Do not start spell ports/reimplementations until Stage 01 classification is reviewed.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation, tests, CI and merge are complete.
- Later stages may inspect or prototype against frozen contracts but may not silently redefine them.
