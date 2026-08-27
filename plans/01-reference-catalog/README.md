# 01 — Reference Catalog

Convert inspiration into an original, implementable Black Arcana specification before coding spells.

## Tasks
1. Inventory public/observable Mahou-like mechanics relevant to the project.
2. Classify every mechanic: `KEEP`, `REIMAGINE`, `MERGE`, `DROP`, `DEFER`.
3. Assign original Black Arcana names/domains and intended host integration.
4. Audit balance/destruction/multiplayer risks.
5. Separate thematic host preference from proven extension capability.

## Preparatory artifacts

- `docs/reference/mahou-observable-catalog.md` — clean-room public behavior inventory.
- `docs/reference/classification-matrix.md` — 53/53 disposition matrix.
- `docs/design/identity-language.md` — original names/domains/visual vocabulary.
- `docs/design/candidate-specifications.md` — 32 implementation-facing contracts.
- `docs/design/balance-risk-register.md` — exploit, PvP, boss and runtime risks.
- `docs/design/server-safety-ceilings.md` — hard safety ceilings/default budgets.
- `docs/reference/host-capability-map.md` — responsibility split among Black Arcana and optional hosts.
- `docs/reference/runtime-host-baseline.md` — exact installed host versions versus upstream.
- `docs/reference/candidate-host-viability.md` — per-candidate `CORE / PUBLIC_API / PROBE` engineering matrix and Stage 03 probe queue.
- `docs/reference/stage-01-completeness-audit.md` — reconciliation and preparatory verdict.

## Exit criteria

No Stage 07 mechanic begins without an approved spec containing behavior, cost model, progression gate, safety policy, host integration and acceptance tests.

A thematic host name is never sufficient to authorize an integration. Any route marked `PROBE` must be proven against the exact installed NeoForge 1.21.1 host version during Stage 03. Black Arcana core remains authoritative for cross-cutting safety, persistent state, transactions, privacy and world mutation.

## Current preparatory verdict

The isolated Stage 01 work is specification-complete and ready for canonical rebase/review once Stage 00 lands on `main`. It is intentionally not marked ✅ and must not become a gameplay implementation base before that promotion.