# Phase 2AC Checkpoint — Ars Sophisticated Compatibility 0.3.0

## Scope

Catalog the installed Ars Nouveau ↔ Sophisticated Storage compatibility layer without promoting a distinct official 0.3.0 artifact into exact physical-binary authority.

## Baseline

- branch: `docs/magic-catalog-phase2ac-ars-sophisticated-compat`;
- phase base/main considered: `ede7dc310499ec21941504e8e6754d4f7c7f512e`;
- latest physical modlist supplied 2026-09-08: 595 top-level entries.

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

1. fetch latest `origin/main`;
2. reconcile if it advanced;
3. verify diff remains documentation-only under `wiki/modpack-catalog/**`;
4. run exact reconciled-head CI;
5. do not claim green if external CurseMaven 429 prevents the pipeline;
6. merge only after required CI evidence is actually green.