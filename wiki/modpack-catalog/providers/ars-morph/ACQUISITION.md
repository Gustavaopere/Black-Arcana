# Ars Morph 2.0.0 — Acquisition

Status: `1/1 COMMITTED GLYPH RECIPE CATALOGED / INSTALLED DATAPACK QA OPEN`

## Morph glyph learning recipe

Committed generated resource:

`data/ars_morph/recipe/glyph_morph.json`

Recipe type: `ars_nouveau:glyph`.

Inputs:

1. `ars_nouveau:conjuration_essence`;
2. `ars_nouveau:abjuration_essence`;
3. one item from tag `ars_nouveau:wilden_drop`;
4. a second item from tag `ars_nouveau:wilden_drop`.

Output:

- `ars_morph:glyph_morph` ×1.

XP field: `55`.

No condition block is present on this recipe because Ars Nouveau and Identity2 are mandatory provider dependencies in Ars Morph metadata.

## Scope

Phase 2X found one generated Ars Morph recipe in the exact source tree and no additional Ars Morph crafting/apparatus/ritual recipes. Identity2 form acquisition is outside this addon and remains Identity2 authority.

## Runtime QA

- confirm recipe exists in the physical 2.0.0 JAR/datapack;
- validate tag resolution under current Ars 5.13.1;
- validate learning grants only the Ars glyph and does not independently unlock Identity2 forms;
- validate recipe/datapack reload behavior.
