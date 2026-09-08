# Phase 2AC Checkpoint — Ars Sophisticated Compatibility 0.3.0

## Scope

Catalog the installed Ars Nouveau ↔ Sophisticated Storage compatibility layer without promoting a distinct official 0.3.0 artifact into exact physical-binary authority.

## Git synchronization

- branch: `docs/magic-catalog-phase2ac-ars-sophisticated-compat`;
- initial phase base: `ede7dc310499ec21941504e8e6754d4f7c7f512e`;
- first reconciliation: `main@38d1ba6554314099420482f04b9fda03cbd2189d` (compile-only provider resolution hardening);
- final pre-merge reconciliation recorded by this checkpoint: `main@c5c1fe1346f0e7e9e991018f62c2f2399b41075b` (Stage 05.14 documentation merge);
- latest physical modlist supplied 2026-09-08: 595 top-level entries.

The branch uses merge commits from current main rather than rebasing or discarding concurrent history. The resulting commit containing this checkpoint must receive a fresh exact-head CI before merge.

## Physical identity

Installed:

- `arssophisticatedcompat-0.3.0.jar`;
- mod id `arssophisticatedcompat`;
- version `0.3.0`;
- SHA-1 `7cc6c1e1d92d109230f68b6a63dc4bfb13c245a6`.

Current host stack:

- Ars Nouveau 5.13.1;
- Sophisticated Core 1.5.1;
- Sophisticated Storage 1.5.91.

## Provenance split

Secondary current modpack indexes associate the installed filename/SHA-1 with CurseForge file `8653384`.

The directly accessible official CurseForge 1.21.1 release is instead file `8655579`, filename `arssophisticatedstoragecompat-0.3.0.jar`, same nominal version 0.3.0, project license All Rights Reserved. Independent indexing reports a different SHA-1 (`1a5b5e...`).

Therefore official functional documentation is used as family-level evidence only.

## Cataloged capabilities

Official 0.3.0 family documents:

1. Source Storage Upgrade;
2. Storage Source Link Upgrade;
3. Potion Jar Upgrade;
4. Enchanter's Upgrade;
5. Stack Upgrade scaling for Source capacity and potion duration;
6. Ars-themed template/textures.

No spells, glyphs, rituals or independent mana/casting system are attributed to this compatibility layer from the available evidence.

## Authority result

- Ars Nouveau: Source/magic semantics.
- Sophisticated Storage/Core: storage/upgrades/inventory lifecycle.
- compat addon: bridge only.
- Black Arcana: must not duplicate Source, conversion, potion refresh or repair transactions.

## Open gates

Exact installed-binary source/API, registries, recipes, configs, formulas, networking/mixins, physical license and current-host runtime behavior remain unobserved and fail-closed.

Notion currently contains a stale Sophisticated Core 1.5.0 dependency value; this checkpoint uses physical 1.5.1 authority and records the drift instead of propagating it.

## Merge gate

Before merge:

1. fetch latest `origin/main` again;
2. reconcile again if it advanced;
3. verify diff remains documentation-only under `wiki/modpack-catalog/**`;
4. run exact reconciled-head CI;
5. require JUnit, diff sanity, NeoForge build, built-JAR verification, Foundation GameTests and dedicated-server smoke to pass;
6. review PR discussions/threads;
7. merge only after required evidence is actually green;
8. confirm final `main` SHA after merge.