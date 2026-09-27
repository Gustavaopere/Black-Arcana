# Release-bounded ability inventory — Reliquified L_Ender's Cataclysm 0.1.1

Checkpoint: 2026-09-27

## Evidence class

`COUNTED_RELEASE_BOUNDED`

This is intentionally weaker than `COUNTED_EXACT` because byte equality between the user's physical 0.1.1 JAR and CurseForge File `6882649` has not been established, and the exact 0.1.1 source revision is not published as a matching tag/commit.

## Physical authority

- installed runtime: `0.1.1`;
- installed JAR: `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`;
- installed SHA-1: `be89d697455f04a1531ed81b45bcc038354430c8`;
- sibling physical checkpoint: `neoforge-rpg-skilltree@ac23fc1c67937deeffe982ae971c21d4f3561bc5`.

## Publisher release line

CurseForge project `1232116` contains exactly two public 1.21.1 release files:

| File | Version | Upload | Publisher change |
|---|---|---|---|
| `6415478` | `0.1` | 2025-04-12 | Initial release |
| `6882649` | `0.1.1` | 2025-08-13 | Fixed compatibility with OctoLib 0.6 |

The project page identifies the provider as a Relics × L_Ender's Cataclysm compatibility addon.

## Initial-release source checkpoint

Official repository:
`Octo-Studios/reliquified-lenders-cataclysm`

Checkpoint:
`291f066c0471e44f50fe78ea8e7d786f6775446e`

At this checkpoint `gradle.properties` declares `mod_version=0.1`, and `ItemRegistry` registers exactly:

1. `scouring_eye`;
2. `void_vortex_in_bottle`;
3. `void_cloak`;
4. `vacuum_glove`;
5. `void_bubble`.

The English localization at the same checkpoint exposes exactly seven owner-scoped ability roots for those five relics:

| Owner | Ability root | Display name |
|---|---|---|
| Scouring Eye | `glowing_scour` | Pursuit |
| Void Vortex in Bottle | `spawn_vortex` | Void Tornado |
| Void Cloak | `void_invulnerability` | Invulnerability |
| Void Cloak | `void_rune` | Call of the Void |
| Void Cloak | `seismic_zone` | Final Cry |
| Vacuum Glove | `vacuum_slowdown` | The Edge |
| Void Bubble | `protective_bubble` | Protective Bubble |

No relic item is counted separately from its ability roots.

## Later-development exclusion

The public branch continued development after the initial release and later introduced extra relics while the development property still temporarily read `0.1`, followed by commit `d7df82b857158a68d2c3430605d2a15137dc31ad` (`Version Bump [0.1 -> 0.2]`).

Those later WIP relics are **not** evidence that the published 0.1.1 artifact contains them. The published 0.1.1 changelog is compatibility-only, and the current compatibility fix enumerates the same five legacy relic owners as its adaptation scope.

Therefore only the seven initial-release ability roots are admitted into the current semantic ledger.

## Acquisition

At the initial-release checkpoint all five owners have Relics `LootData` routes.

Provider-defined Cataclysm-specific entries:

- `CURSED_PYRAMID` -> `cataclysm:archaeology/cursed_pyramid(_necklace)?`;
- `FROSTED_PRISON` -> `cataclysm:chests/frosted_prison_treasure`.

The relic classes combine those entries with the Relics `THE_END` route, closing source-level catalog reachability for all five owners.

## Clean-room boundary

The upstream license is All Rights Reserved.

This audit records only factual public registry names, localization identifiers, release metadata and ownership/reachability relationships required for interoperability/cataloging. It does not reuse implementation bodies, assets or provider text as Black Arcana implementation.

## Semantic result

- relic owners: **5**;
- provider-owned ability roots: **7**;
- strict semantic contribution: **+7**;
- evidence class: **`COUNTED_RELEASE_BOUNDED`**;
- runtime QA: separate / fail-closed.
