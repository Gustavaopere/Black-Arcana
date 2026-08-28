# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. The validated Foundation history is included in `main`; branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline. All 53 observable reference rows and 32 candidate specifications are now frozen inputs for later content stages.

Stage 02 Arcana Core is now the canonical active stage. Its existing preparatory implementation must be reapplied onto this latest `main` without importing stale Foundation/Stage 01 history.

Stage 03 and Stage 04 remain preparatory. Stage 04 has already demonstrated a full-green integrated preparatory run (`33166679049`), but causal merge order remains mandatory.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | full branch and post-merge CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; run `33167246384` full green |
| 02 Arcana Core | 🟨 Active | canonicalization from preparatory implementation starts now |
| 03 Integration Layer | 🟦 Preparatory | waits for Stage 02 canonical merge |
| 04 World Safety | 🟦 Preparatory verified | integrated run `33166679049` full green; waits for Stages 02–03 |
| 05 Casting & UX | ⬜ Not started canonically | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`02-arcana-core`

## Frozen predecessors

Stage 00 and Stage 01 may only change through explicit follow-up decisions recorded in `DECISIONS.md`.

Stage 01 frozen outputs include:
- 53/53 observable reference mechanics reconciled exactly once;
- `KEEP / REIMAGINE / MERGE / DROP / DEFER` classification;
- 32 original Black Arcana implementation contracts;
- `CORE / PUBLIC_API / PROBE` host viability model;
- hard safety ceilings and balance/runtime risk register;
- clean-room provenance ledger.

## Immediate next actions

1. Create/rebase `feat/02-arcana-core` from latest `main`.
2. Reapply only Stage 02 implementation and architecture artifacts from `prep/02-arcana-core`.
3. Reconcile Stage 02 decisions against frozen Stage 00/01 contracts.
4. Run full canonical CI.
5. If green, merge Stage 02, mark its five tasks ✅ and activate Stage 03.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation/specification acceptance, tests/CI and merge are complete.
- Later stages may inspect or prototype against frozen contracts but may not silently redefine them.
