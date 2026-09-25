# Provider Audit Queue — Ars Controle 1.6.16 delta

Date: `2026-09-23`

This is a narrow freshness overlay over the historical `PROVIDER-AUDIT-QUEUE.md`. It prevails for `ars_controle` until the current physical magic-provider queue is regenerated from the sibling's latest physical modlist.

## Current row

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `ars_controle` | `ars_controle-1.21.1-1.6.16.jar` / runtime `1.21.1-1.6.16` / physical SHA-1 `795567371450debec83fe634fd0114c295f7da5a` | `✅ SOURCE-PINNED 1.6.16 REVALIDATED / 9 REGISTERED ARS SPELL PARTS / REGISTRY BLOB IDENTICAL TO 1.6.15 / SEMANTIC +0 / RUNTIME QA FAIL-CLOSED` |

## Evidence

Physical authority:

- sibling `neoforge-rpg-skilltree@ee08513c9e8992418c508bae485f3a181deb7f9c`;
- certified physical row **#41**;
- JAR `ars_controle-1.21.1-1.6.16.jar`;
- mod id `ars_controle`;
- runtime `1.21.1-1.6.16`;
- physical SHA-1 `795567371450debec83fe634fd0114c295f7da5a`.

Publisher release:

- CurseForge project/file `1061812 / 8847869`;
- release date 2026-09-10;
- release changelog is limited to Warping Spell Prism fixes, Ars dependency bump, localization and asset optimization.

Exact source release:

`Vonr/Ars-Controle@14c5f4770a9ec265491fb9a7ae1a60a2123dfbc0`

Previous source checkpoint:

`Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`

Registry continuity:

`ACRegistry.java` is Git blob `b38959053740605768a8945ed40c012c6bef5953` at both 1.6.15 and 1.6.16.

## Semantic closure

The exact registered semantic surface remains **9 Ars spell parts**:

- 1 effect;
- 8 filters.

No new provider-owned spell/glyph/ritual identity is introduced by the 1.6.16 delta.

Semantic disposition: **9 `COUNTED_SOURCE_PINNED`, delta +0**.

## Runtime QA still open

The catalog does not claim:

- full assembled-pack runtime compatibility;
- Warping Spell Prism exactly-once Source settlement;
- cross-dimension causal correctness;
- provider mixin compatibility;
- persistence/reload correctness;
- multiplayer behavior;
- Black Arcana adapter safety.

These remain fail-closed.

## Global accounting consequence

The strict reconstructible semantic minimum remains **1382**. No technical percentage is changed because the global provider denominator remains under physical rebase.
