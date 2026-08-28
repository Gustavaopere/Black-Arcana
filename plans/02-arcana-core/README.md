# 02 — Arcana Core

Build the server-authoritative execution kernel used by integrations, UI, rituals and spells.

## Tasks
- Cast validation/execution pipeline.
- Pluggable resource/cost providers.
- Target/effect runtime.
- Cooldowns and persistence.
- Networking and data-driven registration.

## Exit criteria
A synthetic spell can be cast on dedicated server through the full pipeline with deterministic costs, cooldown, target validation, persistence and client result messaging—without any optional magic mod installed.

## Preparatory implementation state

Branch: `prep/02-arcana-core`, based on the latest preparatory Foundation rather than canonical `main`.

Implemented as pure Black Arcana infrastructure:
- unique cast ids, identity validation seam and bounded replay guard;
- transactional composite costs with rollback of partial reservations;
- shared/persistent cooldown ledger with snapshot/restore;
- bounded target specifications and deterministic server-candidate filtering;
- bounded follow-up work scheduler;
- canonical compiled spell registry and atomic metadata catalog;
- versioned/bounded network payload contracts;
- ingress cast-intent rate limiter.

Detailed checkpoint and remaining work: `docs/architecture/arcana-core-preparatory.md`.

## Not complete

None of the five tasks is marked ✅ yet. Remaining work includes actual loadout resolution, charge/channel lifecycle, percent-of-max/creative cost policy, Minecraft target adapters, SavedData persistence, charge pools, NeoForge payload registration/codecs, reload listener integration and dedicated-server/GameTest validation.

This branch is preparatory only and cannot bypass Stage 00/01 canonical promotion.