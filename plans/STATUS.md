# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation is ✅ complete, verified and merged. The validated Foundation history is included in `main`; branch run `33166799319` and post-merge run `33167079272` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is ✅ complete, verified and merged at `88059dc73d8abae12fe5dd4d8e99e08f8e0a8ed6`. Canonical CI run `33167246384` passed the full pipeline. All 53 observable reference rows and 32 candidate specifications are frozen inputs for later content stages.

Stage 02 Arcana Core is ✅ complete, verified and merged. Canonical branch run `33169091342` passed the full pipeline, followed by post-merge `main` run `33169344809`, also fully green. The five Stage 02 tasks are now frozen contracts.

Stage 03 Integration Layer is the canonical active stage. Its preparatory implementation must be reapplied onto the latest `main` without importing stale Stage 02/04 history.

Stage 04 World Safety remains preparatory verified. Its stacked implementation has full-green evidence, but it must wait for Stage 03 canonical merge before being reapplied and merged causally.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | branch + post-merge full CI green |
| 01 Reference Catalog | ✅ Complete | merged at `88059dc...`; canonical full CI green |
| 02 Arcana Core | ✅ Complete | branch run `33169091342` + post-merge run `33169344809` full green |
| 03 Integration Layer | 🟨 Active | canonicalization from preparatory adapters starts now |
| 04 World Safety | 🟦 Preparatory verified | stacked implementation full-green; waits for Stage 03 |
| 05 Casting & UX | ⬜ Not started canonically | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`03-integration-layer`

## Frozen predecessors

Stages 00, 01 and 02 may only change through explicit follow-up decisions recorded in `DECISIONS.md`.

Stage 02 frozen outputs include:
- server-authoritative cast identity, ingress, loadout and replay contracts;
- one immediate/channel execution pipeline;
- transactional/composite resource reservations;
- bounded server-fact targeting and follow-up scheduler;
- persistent cooldown/charge/loadout state with migrations and pruning;
- versioned bounded networking with negotiated payload-safe sync;
- strict atomic presentation-metadata reload contracts.

## Immediate next actions

1. Create/rebase `feat/03-integration-layer` from latest `main`.
2. Reapply only Stage 03 integration code, metadata, tests and architecture artifacts from `prep/03-integration-layer`.
3. Keep Iron's, Ars, Eidolon, Malum and RPG dependencies optional and fail-closed.
4. Run full canonical CI, including representative provider profiles where the harness supports them.
5. If green, merge Stage 03, mark its six tasks ✅ and activate Stage 04.

## Freeze rules

- Completed stages change only through an explicit follow-up decision.
- No Stage 03 task receives ✅ until canonical implementation passes its acceptance gates and merge.
- Optional-provider absence or API mismatch must never silently weaken cost/progression requirements.
- Client input/presentation never becomes authoritative gameplay state.
