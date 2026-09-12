# Phase 2BM — Ars Polymorphia 1.0.3 checkpoint

Status: `EXACT SOURCE CATALOG COMPLETE / ZERO SEMANTIC MAGIC / COMPONENT PROMOTION PENDING SHARED-QUEUE RECONCILIATION`

Execution branch: `docs/magic-catalog-phase2bm-ars-polymorphia`
Base main at phase start: `6b574368d6af80b31fa4a0c636c9d4742fbf6b16`
Physical JAR: `ars_polymorphia-1.0.3.jar`
Physical mod id/version: `ars_polymorphia` / `1.0.3`
Physical SHA-1: `8cce819e83f6360ab9aa8b44ac841511172a6a79`
Physical CurseForge hash: `3576413974`
Exact official source: `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f`

## Evidence closed in this tranche

- physical identity/version/hash from the current 595-entry modlist;
- exact signed source commit matching version 1.0.3;
- source license declaration GNU LGPL 3.0;
- exact provider role: Ars Storage/Crafting Lectern ↔ Polymorph recipe-conflict adapter;
- no provider-owned spell/glyph/ritual/school/resource/action registry surfaced by the exact source tree;
- five direct mixins/accessors: four common + one client;
- protocol registrar version `1`;
- one provider-owned play-to-server unit payload, `ars_polymorphia:reset_crafting_result`;
- server-side recipe re-resolution before Ars current-recipe settlement;
- player-scoped lectern/Polymorph selection intent;
- Black Arcana authority/deduplication boundary;
- source metadata drift/inconsistency recorded without inference.

## Semantic disposition

Ars Polymorphia contributes **0 independent semantic magic objects** under `SEMANTIC-MAGIC-COVERAGE.md`. The current strict semantic minimum therefore remains **1316**.

The component is technically auditable as a zero-semantic bridge. Promotion to component **#61 / 61 of 100** is deliberately left for the shared `PROVIDER-AUDIT-QUEUE.md` reconciliation after this branch has current CI evidence, mirroring the gate discipline used after prior audit tranches.

## Current-host QA kept open

1. The exact source metadata requires dependency mod id `polymorph`, while the physical modlist exposes `polymorph_plus` `1.3.1+1.21.1`.
2. The exact source built against Ars Nouveau `5.4.2.938`; the physical pack uses `5.13.1`, while the provider has five required direct mixin targets.
3. Exact source declares `minecraft_version=1.21.1` but `minecraft_version_range=[1.21,1.21.1)`; no corrected binary metadata is inferred from source intent.
4. Client boot and dedicated-server startup with the installed host set are not established by this source audit.
5. Real conflicting-recipe behavior, datapack reload invalidation, two-player same-lectern isolation, close/reopen/reconnect/restart behavior and full-pack interop remain untested here.

## Clean-room boundary

The exact source was read only to establish factual provider behavior, dependency declarations, mixin/network footprint, authority boundaries and compatibility risks. No upstream implementation body, assets, GUI sprites, localization prose or other creative content is copied/adapted into Black Arcana.
