# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stages 00 Foundation and 01 Reference Catalog are ✅ complete and frozen in `main`. Stage 01 merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6` after full CI run `33167246384` passed.

Stage 02 Arcana Core is the canonical active stage on `feat/02-arcana-core`. The reviewed preparatory implementation has been reapplied onto latest `main` without importing stale branch history. It includes server-authoritative ingress/replay, transactional costs, channeling, bounded targeting/work, cooldowns/charges/SavedData, versioned networking and strict data-driven presentation metadata.

Stage 03 and Stage 04 remain preparatory. Stage 04's integrated implementation has already demonstrated a full-green preparatory run (`33166679049`), but causal order remains mandatory.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | frozen |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; full CI green |
| 02 Arcana Core | 🟨 Active | canonical implementation reapplied; CI/review pending |
| 03 Integration Layer | 🟦 Preparatory | waits for Stage 02 merge |
| 04 World Safety | 🟦 Preparatory verified | integrated run `33166679049` full green; waits for Stages 02–03 |
| 05 Casting & UX | ⬜ Not started canonically | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`02-arcana-core`

## Stage 02 canonical scope

- unique cast identity, loadout validation and bounded replay protection;
- one immediate/channel execution pipeline with server-owned channel duration;
- transactional/composite cost reservation and explicit payment policy;
- shared/persistent cooldowns and charge pools with migration/pruning;
- all target kinds resolved from server facts with bounded geometry/work;
- Overworld SavedData for global player runtime state;
- bounded/versioned C2S/S2C protocol and rate-limited ingress;
- strict atomically reloaded datapack presentation metadata;
- JUnit + GameTest coverage for core behavior and persistence.

## Immediate next actions

1. Run full CI on `feat/02-arcana-core` using the canonical Foundation build.
2. Correct any compile/runtime differences exposed by current NeoForge 1.21.1.
3. Reconcile any Stage 02 decision wording from `PREPARATORY` to canonical after verification.
4. If green, merge Stage 02 to `main`, mark five tasks ✅ and activate Stage 03.
5. Reapply Stage 03 adapters from its preparatory branch onto that new `main`.

## Freeze rules

- Completed stages change only through explicit follow-up decisions.
- No Stage 02 task receives ✅ until canonical implementation passes CI and is merged.
- Client input/presentation never becomes authoritative gameplay state.
