# Phase 2AY checkpoint — GTBC's SpellLib 2.2.0

## Base

- base `main`: `ff5b99106c91723cce2a13f363f7af1336c5d5c1`
- branch: `docs/phase2ay-gtbcs-spelllib`
- Minecraft: `1.21.1`
- NeoForge: `21.1.248`
- physical modlist: `595` top-level entries

## Physical provider

- JAR: `gtbcs_spell_lib-2.2.0-1.21.1.jar`
- mod id: `gtbcs_spell_lib`
- runtime version: `2.2.0-1.21.1`
- SHA-1: `36cce8ab3117e89ae992a84a566d596709db2ffe`
- CurseForge Project/File: `1194714 / 8824651`
- exact public release date: `2026-09-06`
- license: `All Rights Reserved`

## Audit result

The exact current publisher surface closes GTBC's SpellLib as shared library/API infrastructure for Iron's Spellbooks add-ons. Publisher documentation explicitly states that the library provides no standalone gameplay on its own and describes reusable attributes/helper abstractions rather than an independent spell registry.

Phase 2AY semantic disposition:

- standalone spells: `0`;
- rituals/rites: `0`;
- glyph/spell-part primitives: `0`;
- equivalent discrete supernatural player actions: `0`;
- semantic delta: `+0`;
- strict reconstructible semantic minimum remains `796`.

## Component metric

- canonical base: `52/100`;
- Phase 2AY candidate: `53/100`;
- denominator unchanged at `100`.

The candidate component point must not be promoted to canonical until exact-HEAD validation, latest-main reconciliation, merge and post-merge main confirmation.

## Clean-room / provider boundary

No JAR is decompiled. No private source is requested or used. Public publisher documentation is used only for factual classification. Internal signatures/registries remain fail-closed.

Iron's owns its casting/spell identities; consumer add-ons own their concrete spells; GTBC's SpellLib owns only its support/API layer. Black Arcana does not mirror those external authorities.

## Validation still required before merge

1. fetch latest `origin/main` and reconcile if it advanced;
2. review branch diff;
3. run repository CI/workflow on the exact reconciled branch HEAD;
4. require GREEN before merge;
5. after merge, confirm final `main` SHA and post-merge status;
6. only then promote component coverage to canonical `53/100` in the current coverage ledger.