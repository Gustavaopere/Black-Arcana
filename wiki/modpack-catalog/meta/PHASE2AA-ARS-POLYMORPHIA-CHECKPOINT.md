# Phase 2AA — Ars Polymorphia 1.0.3 checkpoint

Status: `SOURCE CATALOG COMPLETE / CURRENT-HOST RUNTIME QA DEFERRED / CI NOT YET STARTED`

Execution branch: `docs/magic-catalog-phase2aa-ars-polymorphia`
Base main at phase start: `ede7dc310499ec21941504e8e6754d4f7c7f512e`
Physical JAR: `ars_polymorphia-1.0.3.jar`
Physical mod id/version: `ars_polymorphia` / `1.0.3`
Physical SHA-1: `8cce819e83f6360ab9aa8b44ac841511172a6a79`
Physical CurseForge hash: `3576413974`
Exact source: `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f`

## Exact catalog closed

- exact physical identity and source pin;
- Minecraft/NeoForge/Ars/Polymorph build/runtime declarations;
- LGPL 3.0 provenance;
- exact provider role: Ars Storage/Crafting Lectern ↔ Polymorph recipe-conflict adapter;
- zero provider-owned spells/glyphs/rituals/resources;
- 5/5 mixins/accessors classified;
- 1/1 provider-owned payload classified;
- server-side recipe enumeration and prior-selection reuse;
- client recipe selector behavior;
- server-side menu/tile/current-matrix validation and recipe re-resolution;
- player-specific state intent;
- Black Arcana authority/deduplication consequences.

## Current-host incompatibility questions kept fail-closed

- exact source requires mod id `polymorph`; physical top-level modlist exposes `polymorph_plus` 1.3.1+1.21.1;
- exact source targeted Ars Nouveau 5.4.2.938; physical pack uses Ars Nouveau 5.13.1;
- no runtime claim is made until the installed Polymorph+ metadata/API compatibility and Ars mixin targets are validated.

## Deferred QA

- physical Polymorph+ binary metadata/dependency alias/API validation;
- client boot and dedicated-server startup;
- Storage/Crafting Lectern selector with real conflicting recipes;
- datapack reload and stale selection invalidation;
- two-player same-lectern isolation;
- close/reopen/reconnect/server restart;
- current Ars 5.13.1 mixin compatibility;
- full-pack interop.

Phase 2AA is catalog/documentation work only and does not transfer recipe or spell authority to Black Arcana.
