# Phase 2AI checkpoint — Somake Spells 1.0.8-fix

## State

`AUDITED / CLOSURE BLOCKED / ZERO COVERAGE DELTA / FAIL-CLOSED`

## Base

- canonical `main` at Phase 2AI start: `e8b7c4a0b77c2f803423047f5d1442f870d02fc8`
- branch: `docs/magic-catalog-phase2ai-somake-1.0.8-fix`
- canonical coverage at Phase 2AI start: **37/100 = 37%**
- historical Somake audit: Phase 2O / PR #86, already merged; this phase re-audits that material against the stricter current closure rule rather than creating a second provider tree.

## Exact physical identity

- artifact: `somakespells-1.0.8-1.21.1-fix.jar`
- mod id: `somakespells`
- runtime version: `1.0.8`
- physical SHA-1: `b0ad94c1504709662bee2d08700375ccecbb5ec7`
- CurseForge project/file: `1461634 / 8417850`
- exact file line: NeoForge / Minecraft 1.21.1 / Release / 2026-07-12
- license: All Rights Reserved
- host casting substrate: Iron's Spells 'n Spellbooks

The physical modlist remains authority for installed presence/version/hash. Publisher release metadata is used for the exact public 1.0.8-fix delta.

## Phase 2AI evidence audit

The official 1.0.x release surface was re-reviewed through the currently published 1.0.8-fix line.

Strong evidence available:

- publisher-current project description states **over 50 spells**, Aqua/Symmetry/elemental-charge surfaces and progression/equipment features;
- exact 1.0.8-fix states that Symmetry and Spirit Elemental Charges were not applying their buffs and were fixed;
- exact 1.0.8 publicly names Ritual Flame, Custodia Caeli, Bloody Legacy, Fragmented Requiem, The Rose's Secret and Jingle Bell, moves Chain Connection to Aqua, and reworks Fire Orbs / Ignis Shield;
- 1.0.7 publicly names Guardian Connetion, Blessed Connetion, Cursed Connection, Chain Connection, Bloodmark, Water Control and Firestorm Vortex;
- 1.0.6 explicitly removes Tsunami and renames Tidal Grasp/Dash to Ceraunus Grasp/Dash;
- the release line documents tier-book progression, Upgrade Forge, Grimoires, Profane/Sanctum branching, Soul Fire/Infernal Fire ritual progression and Elemental Charges.

## Evidence ceiling reached

Phase 2AI did **not** locate any of the following exact-current evidence sources:

1. a publisher-controlled source revision that can be pinned to `1.0.8-fix`;
2. a publisher-native complete spell/registry table for `1.0.8-fix`;
3. an exact-current public registry/resource dump with all spell IDs and membership;
4. a directly inspectable copy of the exact installed JAR through the available repository/web tooling.

The current publisher statement `over 50 spells` is a scale statement, not a registry count. Official changelogs name only a subset of that surface and are not cumulative registry manifests.

Therefore Phase 2AI must not manufacture missing spell identities, school totals, registry IDs, class names, values, configs, hooks, networking or persistence contracts.

## Coverage verdict

**No numerator increment.**

`somakespells` remains a partial component under the current global metric because its current granular inventory is not closed. Canonical coverage remains **37/100 = 37%** after this audit.

This is deliberate: Phase 2AI closes the question of what can be proven from currently accessible public evidence; it does not close the provider's exact current inventory.

## Closure conditions for a future Somake point

A future Somake closure may be reconsidered when at least one trusted exact-current path becomes available, for example:

- clean-room inspection of the exact `1.0.8-fix` artifact sufficient to enumerate registry/resource identity without copying implementation;
- publisher-controlled exact source / registry / API evidence for the installed line;
- equivalent trusted exact inventory evidence that closes current spell membership.

Even after static inventory closure, runtime QA remains separately required for:

- Somake Aqua versus physically present `traveloptics` 1.21.1 alpha/deprecated coexistence;
- optional-provider activation;
- stable adapter/API boundaries;
- server authority, event ordering and deduplication for link/retaliation/charge mechanics.

## Authority / safety consequences

- Iron's remains host cast/resource/cooldown authority.
- Somake owns its registered spell semantics, Elemental Charges and provider-specific progression/equipment state.
- Black Arcana must not create a second Somake charge ledger, duplicate provider ritual completion, mirror provider casts, or guess school/spell IDs.
- RPG Skill Tree may gate or modify only through a real contract; it does not own Somake runtime state.
- unresolved APIs or runtime identities fail closed.
- unknown Somake content remains occupied provider space for deduplication; absence from the public changelog is not evidence of a Black Arcana gap.

## Stage consequence

This phase is catalog/provenance/deduplication work only. It does not promote Stage 07 runtime and does not unblock Phase 3.