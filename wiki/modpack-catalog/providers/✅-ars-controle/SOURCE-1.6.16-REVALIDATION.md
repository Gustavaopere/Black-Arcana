# Ars Controle 1.6.16 — source revalidation

Date: `2026-09-23`

Status: `COUNTED_SOURCE_PINNED / REGISTRY CONTINUITY PROVEN / 9 SEMANTIC SPELL PARTS / RUNTIME QA FAIL-CLOSED`

## Physical authority

Current sibling authority used for this revalidation:

- repository: `Gustavaopere/neoforge-rpg-skilltree`;
- sibling HEAD consulted: `ee08513c9e8992418c508bae485f3a181deb7f9c`;
- certified physical position: **#41**;
- JAR: `ars_controle-1.21.1-1.6.16.jar`;
- mod id: `ars_controle`;
- runtime: `1.21.1-1.6.16`;
- physical SHA-1: `795567371450debec83fe634fd0114c295f7da5a`.

The sibling dossier explicitly identifies `modlist(1).txt` from 22/09/2026 as the current physical authority for this row.

## Publisher release

CurseForge project/file:

- project: `1061812`;
- file: `8847869`;
- release: **Ars Controle 1.6.16 for 1.21.1**;
- filename: `ars_controle-1.21.1-1.6.16.jar`;
- loader: NeoForge;
- release date: 2026-09-10.

Publisher changelog:

- fix Warping Spell Prism direct-block-hit direction;
- fix Warping Spell Prism compatibility with Ars Nouveau 5.13.1;
- bump Ars dependency version;
- localization updates;
- asset optimization.

Publisher identity is corroborative. Physical byte equality is not inferred from the CurseForge page alone; the current installed SHA-1 is the sibling's physical evidence above.

## Exact source checkpoint

Official source repository:

`Vonr/Ars-Controle`

Exact release commit:

`14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`

Commit message:

`ver: 1.6.16`

At this commit, `gradle.properties` declares:

- `mc_version=1.21.1`;
- `neo_version=21.1.217`;
- `mod_id=ars_controle`;
- `mod_version=1.6.16`;
- `ars_version=5.13.1.1403`;
- `curios_version=9.0.12`;
- `cc_tweaked_version=1.112.0`;
- `mod_license=LGPLv3`.

## Exact 1.6.15 -> 1.6.16 delta

Previous catalog source checkpoint:

`ecbb83ba512bc9ca7a025556fb9c62dbd32b6430` — `ver: 1.6.15`

GitHub compare to the 1.6.16 release commit contains exactly six commits:

1. `8cd13c923ce52f3cd7852f3575aa3264b7809871` — asset optimization;
2. `08f2c3079daebe4646359277ba0099e23061eeb8` — localization updates;
3. `6e49854c5676b8a781b51ebb07e02d0b413bb6cc` — Ars dependency bump;
4. `ba7ed377003626b3263bafc9510c4ebbc9116f2f` — Ars 5.13.1 Warping Spell Prism compatibility;
5. `a4a91a3c0adc67b36ff514a1e4fdcd877bde4770` — direct-hit spell-direction fix;
6. `14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0` — version bump to 1.6.16.

The only gameplay Java file changed in this release delta is:

`src/main/java/dev/qther/ars_controle/block/WarpingSpellPrismBlock.java`

No registry source file changed.

## Registry continuity proof

The authoritative registry source file:

`src/main/java/dev/qther/ars_controle/registry/ACRegistry.java`

has the same Git blob at both release checkpoints:

`b38959053740605768a8945ed40c012c6bef5953`

Therefore 1.6.16 preserves the exact 1.6.15 registration surface:

- 4 blocks;
- 6 items;
- 3 BlockEntityTypes;
- 2 persistent/network-synchronized data components;
- 4 attachment types;
- 1 creative tab;
- **9 Ars spell parts**.

The nine semantic spell parts remain:

- `ars_controle:glyph_precise_delay`;
- `ars_controle:glyph_filter_above`;
- `ars_controle:glyph_filter_below`;
- `ars_controle:glyph_filter_level`;
- `ars_controle:glyph_filter_or`;
- `ars_controle:glyph_filter_xor`;
- `ars_controle:glyph_filter_xnor`;
- `ars_controle:glyph_filter_not`;
- `ars_controle:glyph_filter_random`.

No spell/glyph identity is added or removed by 1.6.16.

## Semantic consequence

Ars Controle remains:

- ✅ cataloged;
- `COUNTED_SOURCE_PINNED`;
- **9 semantic magic objects**;
- semantic delta relative to the previous catalog: **+0**;
- global strict minimum remains **1382**.

This is a version-freshness correction, not a new semantic-count tranche.

## Runtime boundary

The release modifies Warping Spell Prism runtime behavior, so assembled-pack runtime validation remains fail-closed for:

- direct-hit redirection;
- cross-dimension projectile recreation;
- Source settlement;
- causal ownership;
- region-ticket behavior;
- mixin application against the exact installed stack;
- persistence/reload;
- multiplayer deduplication;
- Black Arcana integration.

Catalog closure does not imply runtime compatibility.

## Clean-room

The upstream source is LGPLv3. This revalidation records factual identity, source metadata, registry continuity and API-facing behavior only. No upstream code, assets or localization text are copied into Black Arcana.
