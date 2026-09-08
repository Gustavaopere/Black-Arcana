# Phase 2X — Ars Morph 2.0.0 checkpoint

Status: `SOURCE CATALOG COMPLETE / PRE-CI MAIN SYNC COMPLETE / INSTALLED JAR+RUNTIME QA DEFERRED`

Execution branch: `docs/magic-catalog-phase2x-ars-morph`
Base main at phase start: `7c7a7de74cccdfb6e81820a9d7aecea18de7d55b`
Pre-CI main confirmed: `7c7a7de74cccdfb6e81820a9d7aecea18de7d55b`
Provider source checkpoint: `Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58` (`RELEASE-ALIGNED`, not claimed byte-identical)
Physical JAR: `ars_morph-1.21.1-2.0.0.jar`
Physical SHA-1: `68ff47cc58c0ffe9570bb907f65c2910311ed45f`

## Closed source catalog

- physical mod id/JAR/runtime version/hash;
- exact source version and release-aligned pin;
- required Identity2 and optional Ars Elemental boundaries;
- source build vs physical host drift;
- 1/1 production Ars glyph;
- exact Tier II / 200 mana / Conjuration / no-augment defaults;
- exact `max_hp_morph` default/range/strict boundary;
- server-only real-player resolution;
- Mob Jar → Spawn Egg → target type selection semantics;
- target-player recipient and clear-morph semantics;
- FamiliarEntity rejection;
- cosmetic-item/NBT/Identity2 transaction boundary;
- 1/1 committed glyph acquisition recipe;
- 7/7 Java ability adapters;
- 11/11 committed Identity2 ability assignment files and exact cadence;
- 8/8 variant adapters;
- 6/6 additive Identity2 entity-type capability tags;
- Wilden Stalker server morph-tick/sync seam;
- 0/0 declared mixins;
- 0 Ars Morph-owned custom payload registrations identified;
- empty/unregistered standalone COMMON spec separated from glyph config;
- dormant/unregistered `MorphEffect` excluded from active counts;
- Wixie crouching random-index source-risk;
- capability/deduplication matrix;
- clean-room provenance and LGPL-vs-GPL repository metadata discrepancy.

## High-value factual consequences

1. Identity2, not Ars Morph or Black Arcana, is authoritative for form state and morph acceptance.
2. Morph is not self-only: a struck ServerPlayer can become the recipient.
3. A valid Ars Mob Jar takes form-selection precedence over target type; Spawn Egg applies only after the initial selected type still equals the target type.
4. The health cap is strict `<`, not `<=`.
5. Identity abilities internally reuse Ars spell/effect pipelines; those descendants are not independent casts/procs for BA/RPG deduplication.
6. Variant adapters preserve host state such as color/tamed/variant rather than only EntityType identity.
7. Passive traits are delivered through Identity2 additive tags and must not be mirrored into a second BA/RPG state ledger.
8. The exact Wixie crouching branch has a plausible 10-entry-list/12-bound indexing defect; runtime reproduction is required before calling it an installed failure.
9. `MorphEffect` is source-present but not registered in the audited production path and is excluded from runtime content claims.

## Version-drift gate

Source build:

- NeoForge 21.1.219;
- Ars 5.11.1.1289;
- Ars Elemental 0.7.9.3.168;
- Identity2 2.1.1.1 development artifact;
- Gabou's Libs 1.4 development artifact.

Physical pack:

- NeoForge 21.1.248;
- Ars 5.13.1;
- Ars Elemental 0.7.10.1;
- Identity2 2.2.4;
- Gabou's Libs 1.8.7.

Current-host runtime behavior is not promoted to PASS from source compatibility ranges.

## Deferred installed validation

- physical JAR extraction/package equality audit;
- current-host client/dedicated boot;
- complete Morph glyph selection/recipient/HP/config matrix;
- provider permission/friendly-target multiplayer behavior;
- all ability/cadence/event-cancel paths;
- Wixie source-risk reproduction;
- variant/tag state round trips;
- Wilden Stalker flight sync lifecycle;
- Ars Elemental present/absent classloading/data;
- unregistered `MorphEffect` artifact confirmation;
- full-pack morph/scale/combat interoperability.

These are runtime/package gates, not missing source-catalog entries.

## Pre-CI / merge gate

Pre-CI sync result:

- current `main` re-fetched after the catalog commit: `7c7a7de74cccdfb6e81820a9d7aecea18de7d55b`;
- branch compare at that checkpoint: 0 behind, catalog-only delta under `wiki/modpack-catalog/**`.

Remaining merge gate:

1. open/refresh the Phase 2X PR on this checkpointed branch;
2. run fresh CI on the exact final HEAD;
3. keep review threads clear;
4. immediately before merge, fetch/reconcile `main` again and revalidate if needed;
5. merge only after those gates pass;
6. confirm final `main` SHA.

Phase 2X is documentation/catalog state only and does not promote any Black Arcana runtime Stage.
