# Phase 2BQ — Ars Nouveau: Two-Way Portals 2.0.0 exact checkpoint

## State

`EXACT PHYSICAL/PUBLISHER ARTIFACT HASH-MATCHED / ZERO_SEMANTIC_PORTAL_INFRA / COMPONENT #65 CANDIDATE / RUNTIME QA FAIL-CLOSED`

Base `main` at phase start: `1d61267a2fdeaa273df2415d37500eded32c93b3`.

Evidence source:

- NON-MERGE PR #222;
- exact audit HEAD `9a3620209e27bb74934c8a9740678b7e59df39c6`;
- exact audit workflow run `34735280002` — GREEN;
- text-only artifact `10311071402`;
- evidence digest `sha256:908bad67ee1d98aa0da19ec90750dfeb0636c8ff7c211367e30217b7e593a898`.

## Exact identity

- physical JAR `ars_two_way_portals-2.0.0.jar`;
- mod id/version `ars_two_way_portals / 2.0.0`;
- physical SHA-1 `233846fc30667893c5f36a719da576d5eed43f5c`;
- exact CurseForge project/file `1599062 / 8515817`;
- exact downloaded artifact SHA-1 equals the physical SHA-1;
- exact downloaded artifact SHA-256 `616a07c0510ca7222698d90e365ae0c70b7a7c3d1f296acada8f5354a7be4166`;
- exact publisher/license line: NeoForge 1.21.1 / LGPLv3.

## What Phase 2BQ closes

The exact 2.0.0 binary replaces the old Phase 2Z 1.3.4-source-only uncertainties for structural classification:

- exact NeoForge metadata/dependency ranges;
- exact optional Immersive dependency id and range;
- exact class inventory: 25 provider classes;
- exact provider item registry: 2 items;
- exact recipe inventory: 3 resources;
- exact required mixin inventory: 7 common mixins, Java 21, `defaultRequire=1`;
- exact absence of provider-owned spell/glyph/ritual/rite/ability registry indicators;
- exact absence of semantic spell/glyph/ritual/rite/ability resource paths.

Exact dependency metadata is compatible by declared range with the physical baselines already recorded by the catalog: NeoForge 21.1.248 satisfies `[21.1.243,)`, Ars Nouveau 5.13.1 satisfies `[5.12.1,6.0.0)`, and the current Immersive surface previously reconciled as `immersive_portals_core` 6.0.7 satisfies `[6.0.7,7.0.0)`.

This is metadata/range compatibility evidence, not runtime execution proof.

## Semantic accounting

Two-Way Portals contributes portal infrastructure, two provider items and their acquisition/reset recipes. Under the current semantic metric these are not independent spells, glyphs, rituals, rites or equivalent cast actions.

- Phase 2BQ semantic delta: **+0**;
- classification: `ZERO_SEMANTIC_PORTAL_INFRA`;
- strict reconstructible semantic minimum remains **1332**.

## Component accounting

`ars_two_way_portals` is present in the historical 103-provider candidate set and was never canonically closed: the only earlier provider PR (#125 / Phase 2Z) remains unmerged and explicitly left exact 2.0.0 binary inspection open.

Therefore Phase 2BQ is eligible to become technical provider component **#65** after:

1. this durable closure branch is synchronized to the latest `main`;
2. exact reconciled-HEAD Black Arcana CI is GREEN;
3. diff/review is clear;
4. the durable PR is merged;
5. exact merge-SHA post-merge CI is GREEN;
6. shared provider/semantic ledgers are reconciled separately.

Until those gates complete, `64/100` remains the canonical shared-ledger value.

## Runtime gates intentionally left open

- seven required mixins applying successfully under the physical host;
- effective deployed config values;
- live regular/Immersive pair creation;
- cross-dimension and persistence lifecycle;
- cooldown exactly-once behavior;
- nullification and ordinary pair teardown;
- frame mutation/Weave behavior;
- rotation/gravity interop;
- multiplayer, reconnect, duplicate-processing and protection/world-safety behavior.

No Black Arcana runtime integration is introduced.

## Authority

Ars Nouveau remains owner of base warp/portal primitives. Two-Way Portals owns its pair/item/cooldown/nullification/frame integration. Immersive Portals owns its portal-engine entities when active. Black Arcana does not duplicate provider settlement or persistence.
