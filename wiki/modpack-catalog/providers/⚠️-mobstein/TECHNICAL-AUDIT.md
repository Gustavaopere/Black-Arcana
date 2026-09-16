# Mobstein 5.4.4 — technical and provenance audit

## Audit class

`EXACT ARTIFACT + EXACT PUBLIC RELEASE + PUBLISHER DOCUMENTATION / ALL RIGHTS RESERVED / NO SOURCE-DERIVED INTERNAL CONTRACT / NO DECOMPILATION`

## Exact installed artifact

Physical modlist:

- `mobstein-5.4.4-neoforge-1.21.1.jar`;
- mod id `mobstein`;
- runtime `5.4.4`;
- SHA-1 `3672d88f940ddd474a5429d7066b099cd0ce0c29`;
- package fingerprint `3386302902`.

## Exact publisher release

CurseForge File ID: `8040734`.

Public release metadata confirms:

- same exact filename as the installed artifact;
- NeoForge;
- Minecraft 1.21.1;
- release channel stable/release;
- upload date 2026-05-04;
- client/server environment;
- project license All Rights Reserved.

The exact public changelog has a single compatibility statement: Mobstein is compatible with **Sable Mod**.

## Clean-room boundary

Because the project is All Rights Reserved, this audit does not:

- decompile the installed JAR;
- reconstruct bytecode;
- copy source code;
- copy textures/models/sounds/translations;
- infer class names, registries, events or signatures;
- infer an addon API from package naming;
- treat MCreator provenance as permission to inspect/copy generated implementation.

The catalog uses only:

- exact installed metadata supplied by the modlist;
- publisher-authored CurseForge release metadata;
- publisher-authored current gameplay guide;
- publisher-authored historical changelogs needed to understand the current 5.4.x line.

## Dependency evidence

### GeckoLib

The official CurseForge dependency relation marks GeckoLib as required for the supported project line. That establishes runtime/library dependency only.

It does not establish:

- animation event hooks for Black Arcana;
- entity ownership API;
- resurrection API;
- stable entity registry identifiers.

### JEI / recipe visibility

The public guide repeatedly directs users to JEI for recipes. That is player-facing guidance. Unless an exact dependency relation marks JEI as required, Black Arcana must not reinterpret guide wording as a mandatory hard runtime dependency.

### Sable 2.0.5

Current pack identity:

- `sable-neoforge-1.21.1-2.0.5.jar`;
- mod id `sable`;
- runtime `2.0.5`;
- SHA-1 `05f666e973d32baaaf405acb9bbed6615b909971`;
- package fingerprint `2399697702`.

Public Sable documentation describes the core project as infrastructure for interactive moving block structures/sub-level-like spaces. Mobstein 5.4.4 merely declares compatibility in its changelog.

No public exact-version evidence located in this checkpoint proves:

- which Mobstein blocks/entities participate in Sable movement;
- whether resurrection machines can operate while moving;
- persistence/ownership behavior across Sable spaces;
- cross-level entity transport semantics;
- chunk/loading/world-safety behavior;
- any API method or event Mobstein uses.

Therefore the safe status is:

`TARGET MOD PRESENT / COMPATIBILITY DECLARED / BOUNDARY SEMANTICS UNVERIFIED`

## Public behavior confidence tiers

### High confidence — exact/current publisher evidence

- installed/release version 5.4.4;
- public 5.4.4 Sable compatibility declaration;
- core resurrection machines and guidebook-based loop;
- resurrected creature roster described by the current official guide;
- Surgery Stretch and internal Attack/Health/Speed/Template modifiers;
- Subject Assembly Machine / head creation workflow;
- Igor, failed experiments and Suspicious Syringe;
- syringe family roles;
- Frankenstein Castle, Witherstein Ruins and Old Ruins;
- Dr. Mobstenio and Witherstein progression.

### Medium confidence — current guide qualitative details

- tame items;
- nearby aura/effect descriptions;
- approximately 15-second resurrection wording;
- qualitative speed/jump/defense descriptions;
- experiment behavior descriptions.

These are valid catalog facts but still need runtime QA before numerical or hook-sensitive Black Arcana integration.

### Historical-release evidence only

Older official changelogs establish when systems changed, but do not automatically prove every older behavior survived unchanged in 5.4.4.

One explicit documentation drift is preserved:

- older 5.2.0 changelog: Experiment 091 tame item = Sweet Berries;
- current official guide: Experiment 091 tame item = Strawberries.

No silent reconciliation is made.

## No supported external API proven

This checkpoint did not establish a supported Mobstein addon API for:

- corpse/body acquisition;
- resurrection request/commit;
- tame ownership;
- organ drops;
- surgery construction;
- experiment generation;
- boss awakening;
- companion damage attribution;
- lifecycle cleanup.

Consequently all Mobstein-specific Black Arcana runtime integration remains fail-closed.

## Runtime QA backlog

Before any integration depending on exact behavior, validate in the real 1.21.1 pack:

1. Mobstein 5.4.4 loads with installed GeckoLib and Sable 2.0.5;
2. Clinical Stretch night resurrection timing and loaded-chunk behavior;
3. Lightningbolt Syringe daytime path;
4. Reviver exceptions for Warden/Frankenstein;
5. tame/ownership persistence of resurrected creatures;
6. aura/effect semantics and whether they are server-owned;
7. Surgery Stretch perk ranges/effective stats;
8. Subject Assembly constraints;
9. Igor attempt cap/random pool, including 062/097 exclusion;
10. Experiment 091 current tame item;
11. structures and Witherstein activation/lifecycle;
12. Sable 2.0.5 compatibility behavior;
13. dedicated-server behavior;
14. any safe, stable observable boundary for mastery credit or Black Arcana reactions.

## Implementation gate

Until a legitimate supported boundary is found:

- no direct Mobstein class references;
- no reflective probing of private internals;
- no bytecode-derived event contracts;
- no copied generated MCreator implementation;
- no registry IDs guessed from display names;
- no Black Arcana code that assumes Sable compatibility semantics.

Provider-specific runtime integration remains `BLOCKED / FAIL-CLOSED`.