# More Relics 1.7.7 / Relics 0.12.8 compatibility build — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER ARTIFACT / CLEAN-ROOM TEXT EVIDENCE / 29 OWNERS / 61 OWNER-SCOPED ABILITY ROOTS`

## Audit provenance

- NON-MERGE PR: **#409**;
- audit branch HEAD: `71df915ab0129ab820b4a220835d27099eedc7f8`;
- workflow run: `36283756384` — GREEN;
- text-only evidence artifact: `10920290413`;
- artifact digest: `sha256:6debd2b6caabe7622dd571724e1ad10ea8754cd0f0bc712f3e6b59c73a7d7463`.

## Exact identity

- CurseForge project/file: `1269280 / 8859015`;
- filename: `morerelics-1.7.7-forRelics-0.12.8-1.0-1.21.1.jar`;
- physical SHA-1: `bc220ed291187c97bd1896f1fdd29b2377879ae1`;
- audit SHA-1: `bc220ed291187c97bd1896f1fdd29b2377879ae1`;
- audit SHA-256: `c3d71a841ef483d36e062fed5b17c4724260ce4e78ffe7ab9368264ab64d42d2`;
- size: `830791` bytes;
- metadata version: `1.7.7-forRelics-0.12.8-1.0`;
- license metadata: All Rights Reserved.

Hash equality closes physical↔publisher artifact identity.

## Clean-room extraction

The isolated workflow retained only factual text evidence. It did not publish the JAR, implementation bodies, decompiled source, assets, models or sounds.

Extracted facts:

- 29 localized provider relic item IDs;
- 61 `AbilityTemplate.builder(...)` calls;
- 61 resolved root arguments, 0 unresolved;
- 61 owner→ability localization pairs;
- 56 unique root strings;
- exact equality between builder-root and localization-root sets;
- narrow `LootTemplate` category observations.

See [`ABILITY-INVENTORY-EXACT.md`](ABILITY-INVENTORY-EXACT.md) for the durable owner-scoped inventory.

## Runtime boundary

`COUNTED_EXACT` closes semantic inventory, not assembled runtime behavior. Config, equip/progression, evolution persistence, loot injection, networking and combat regressions remain fail-closed QA.