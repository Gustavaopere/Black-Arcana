# Black Arcana — Status

Last updated: 2026-08-28

## Current state

Stage 00 Foundation is **complete, verified and merged into `main`**. The validated Foundation fix was incorporated through merge commit `b78993ac7e5866e81a206b0b6c7f3d96b5481bd8`; its source branch run `33166799319` passed JUnit, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke.

Stage 01 Reference Catalog is the canonical active stage on `feat/01-reference-catalog`. The clean-room catalog was reapplied onto latest `main` without importing stale Foundation history. It reconciles all 53 observable reference rows, 32 implementation candidates, original identity, host viability, risk register, safety ceilings and provenance ledger.

Later stages remain preparatory until their causal predecessors merge. Stage 04 has already demonstrated an integrated full-green preparatory run (`33166679049`), but that evidence does not bypass Stages 01–03.

| Stage | State | Notes |
|---|---|---|
| 00 Foundation | ✅ Complete | merged; source branch full CI green |
| 01 Reference Catalog | 🟨 Active | canonical branch assembled; full CI/merge pending |
| 02 Arcana Core | 🟦 Preparatory | implementation exists downstream; canonicalization waits for Stage 01 |
| 03 Integration Layer | 🟦 Preparatory | Iron's, Ars, Eidolon, Malum and RPG adapters exist downstream |
| 04 World Safety | 🟦 Preparatory verified | integrated run `33166679049` fully green; canonicalization still waits for Stages 01–03 |
| 05 Casting & UX | ⬜ Not started canonically | Direct cast, loadouts, radial HUD |
| 06 Rituals | ⬜ Not started | Ritual contracts and occult/grand rituals |
| 07 Spell Domains | ⬜ Not started | Blood, souls, projection, displacement, forbidden |
| 08 Progression & Balance | ⬜ Not started | Knowledge, mastery, caps, presets |
| 09 Hardening & Release | ⬜ Not started | Tests, performance, upgrade, release |

## Canonical active stage

`01-reference-catalog`

## Stage 00 freeze

Foundation contracts are frozen unless an explicit follow-up decision is recorded in `DECISIONS.md`.

## Stage 01 acceptance state

Canonical catalog contents:
- 53/53 observable reference mechanics reconciled exactly once;
- every row classified `KEEP / REIMAGINE / MERGE / DROP / DEFER`;
- 32 candidate implementation contracts with original Black Arcana identity;
- host decisions separated into `CORE / PUBLIC_API / PROBE` rather than thematic assumptions;
- hard safety ceilings and balance/runtime risk register;
- clean-room provenance ledger with no copied/decompiled Mahou source/assets.

No Stage 01 task receives ✅ until this canonical branch passes the full CI and is merged.

## Immediate next actions

1. Run full CI on `feat/01-reference-catalog`.
2. If green, merge Stage 01 to `main`.
3. After merge, mark the four Stage 01 task files ✅ and activate Stage 02.
4. Recut/reapply Stage 02 from the new `main`; do not merge preparatory downstream branches out of order.

## Freeze rules

- A completed stage can only be changed by an explicit follow-up decision recorded in `DECISIONS.md`.
- No task receives ✅ until implementation/specification acceptance, tests/CI and merge are complete.
- Later stages may inspect or prototype against frozen contracts but may not silently redefine them.
