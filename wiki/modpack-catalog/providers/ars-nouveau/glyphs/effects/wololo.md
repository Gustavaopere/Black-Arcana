# Wololo

Status: `SOURCE-PINNED 5.13.1 / MANIPULATION EFFECT`

- Registry id: `ars_nouveau:wololo`
- Display name: `Wololo`
- Default mana cost: `30`
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Wololo` recolors compatible entities, equipment and blocks using dye/color data selected from the caster, spell color or Randomize.

The pinned source can:

- recolor sheep and compatible mobs;
- recolor dyeable armor when Sensitive or when targeting an armor stand;
- recolor item entities with compatible color components;
- recolor signs;
- recolor blocks through matching crafting recipes while preserving compatible block-entity data;
- call `IWololoable` on provider-compatible block entities;
- use a bounded crafting-recipe cache (`MAX_RECIPE_CACHE = 16`).

Compatible augments are `Randomize` and `Sensitive`.

## Black Arcana boundary

Wololo owns its recoloring/transformation settlement. Black Arcana must not replay the same block/item/entity transformation and must not infer generic transformation authority from a cosmetic result.

If future Black Arcana transmutation overlaps, uniqueness must be mechanical rather than presentation-only.

## QA / runtime

Source is pinned to 5.13.1. Full-pack recipe/mod-interaction QA remains pending.