# Phase 2O — Somake Spells checkpoint

## Base

Work began from `main@9876a3e44c103209386c38c1bed916b852fb3a8c` after confirming the Phase 2N merge and post-merge CI success.

Concurrent work was checked before provider selection. Ars Nouveau remained owned by a separate active draft PR, so Phase 2O selected Somake rather than editing that area.

## Exact current provider

- `somakespells-1.0.8-1.21.1-fix.jar`;
- mod id `somakespells`;
- runtime `1.0.8`;
- physical SHA-1 `b0ad94c1504709662bee2d08700375ccecbb5ec7`;
- CurseForge Project `1461634`;
- exact File `8417850`;
- ARR.

## Scope advanced

- reconciled the previously preparatory `providers/somake-spells/` tree rather than creating a second provider tree;
- pinned the exact installed fix and its Symmetry/Spirit Elemental Charge correction;
- normalized public 1.0.x changelog evidence with current-line vs historical distinctions;
- cataloged publisher-named spells without pretending they are the complete 50+ registry;
- recorded explicit Aqua removal/rename history (`Tsunami`, `Tidal*`→`Ceraunus*`);
- cataloged tier-book progression, Upgrade Forge, Grimoires, Profane/Sanctum paths and Soul Fire/Infernal Fire ritual progression;
- cataloged publisher-current equipment families and historical weapon surfaces with craftability caveats;
- reconciled exact current required/optional provider descriptions against the physical modlist;
- recorded the live Somake + deprecated T.O Magic 1.21.1 alpha coexistence as a runtime-QA blocker rather than assuming Aqua authority migrated;
- added Black Arcana authority/deduplication rules and capability-matrix delta.

## Important corrections / non-promotions

1. `over 50 spells` remains publisher scale, not a closed registry count.
2. Current page language such as `1 Blood / 1 Ender` is not used as exact school count because public changelogs name multiple Blood spells across the line.
3. Generic CurseForge relation metadata is not allowed to override the 1.0.8 changelog that explicitly removed mandatory Magic From the East / Born in Chaos dependencies.
4. Somake's statement that Aqua would migrate if T.O Magic updated does not prove migration to the currently installed **deprecated 1.21.1 alpha**.
5. Historical changelog entries are not automatically promoted to exact current registry membership.

## Clean-room

No matching publisher source repository was located. The project is All Rights Reserved. No source code/assets were copied or adapted and no bytecode implementation was decompiled for this catalog.

## Remaining gates

- exact current complete spell registry and IDs;
- quantitative spell values and acquisition;
- complete content registries/config defaults;
- stable API/hooks;
- optional-provider runtime activation;
- Somake↔T.O Aqua collision/identity QA;
- full-modpack runtime QA.

## Runtime status

This checkpoint is documentation/provenance/deduplication work only. It does not change Black Arcana Stage 07 runtime status and must not be used as evidence that a Somake adapter is implemented.