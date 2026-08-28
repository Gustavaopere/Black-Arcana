# 02 — Arcana Core

Build the server-authoritative execution kernel used by integrations, UI, rituals and spells.

## Status

✅ Complete, verified and merged into `main` on 2026-08-28.

Canonical verification:
- branch run `33169091342`: unit tests, diff sanity, NeoForge build, JAR inspection, GameTest server and dedicated-server smoke all green;
- post-merge `main` run `33169344809`: the same full pipeline green.

## Completed tasks
- ✅ Cast validation/execution pipeline.
- ✅ Pluggable resource/cost providers.
- ✅ Target/effect runtime.
- ✅ Cooldowns and persistence.
- ✅ Networking and data-driven registration.

## Delivered contracts
- unique cast IDs, canonical server-owned spell/loadout validation and bounded replay protection;
- immediate and channelled casts converge through one execution pipeline with server-owned channel duration;
- transactional `check -> reserve -> effect -> commit/refund` resource semantics, including atomic composite costs;
- bounded server-fact targeting for all planned target kinds plus bounded follow-up work scheduling;
- persistent/shared cooldowns, reusable charge pools, migration/pruning and Overworld `SavedData` state;
- versioned/bounded C2S/S2C protocol, negotiated payload-safe sync and rate-limited ingress;
- strict atomic datapack reload of presentation metadata without client-authored gameplay authority.

## Exit criteria

Satisfied. A synthetic spell casts on dedicated server through the full canonical pipeline with deterministic costs, cooldown, target validation, persistence and client-result contracts, with no optional magic mod required.

Stage 03 Integration Layer is the next canonical stage. Completed Stage 02 contracts are frozen unless an explicit follow-up decision is recorded in `plans/DECISIONS.md`.
