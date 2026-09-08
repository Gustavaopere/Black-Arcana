# Ars Polymorphia 1.0.3

Status: `EXACT SOURCE-PINNED 1.0.3 / CRAFTING-RESOLUTION ADAPTER CATALOGED / CURRENT-HOST POLYMORPH+ QA OPEN`

## Installed identity

- mod id: `ars_polymorphia`;
- JAR: `ars_polymorphia-1.0.3.jar`;
- version: `1.0.3`;
- physical SHA-1: `8cce819e83f6360ab9aa8b44ac841511172a6a79`;
- physical CurseForge hash: `3576413974`.

Physical modlist also contains Ars Nouveau `5.13.1` and Polymorph+ `1.3.1+1.21.1`.

## Exact source checkpoint

Official source: `Vonr/Ars-Polymorphia@e09b6c9ab434ccbb3232ca47b37ca5666becfb6f` (`ver: 1.0.3`).

The source declares:

- Minecraft `1.21.1`;
- NeoForge `21.1.115+`;
- mod id `ars_polymorphia`;
- LGPL 3.0;
- Ars Nouveau build host `5.4.2.938`, runtime range `[5.4.2,)`;
- Polymorph build reference corresponding to 1.0.7-era line, runtime range `[1.0.7,)`;
- required dependency mod id `polymorph`.

## What the provider actually does

Ars Polymorphia is not a spell provider. It is a narrow compatibility adapter for Ars Nouveau's Storage/Crafting Lectern.

It:

1. observes Ars `CraftingLecternTile.onCraftingMatrixChanged(UUID)`;
2. queries the server RecipeManager for all matching `CraftingRecipe` results for that player's lectern matrix;
3. presents the conflict set through Polymorph's player recipe-selection API;
4. adds the Polymorph recipe selector to the Ars Crafting Terminal screen;
5. accepts a single serverbound reset/reselection request;
6. re-resolves the selected recipe server-side before updating Ars `currentRecipe` and Polymorph player recipe data.

No provider-owned glyph, spell, ritual, mana pool, Source pool, block, item or entity registration was found in the exact 1.0.3 source tree.

## Authority boundary

- Ars Nouveau owns the Storage/Crafting Lectern, its crafting inventory and actual craft execution.
- Polymorph-compatible recipe-selection state owns recipe conflict choice.
- Ars Polymorphia is only the adapter between those systems.
- Black Arcana must not add a second conflict resolver, recipe-selection persistence layer or craft execution path around the same terminal.
- Client UI never becomes recipe authority; selection is re-resolved on the server.

## Current-host caution

The exact 1.0.3 metadata requires dependency mod id `polymorph`, while the current physical top-level modlist exposes `polymorph_plus` 1.3.1+1.21.1. The Notion dossier classifies Polymorph+ as the replacement provider, but Phase 2AA does not treat that editorial statement as proof that the installed JAR satisfies the exact dependency-id/API contract.

Therefore current Ars Polymorphia ↔ Polymorph+ compatibility remains runtime/binary QA until the physical Polymorph+ metadata/API alias behavior is directly confirmed.

The source also targeted Ars Nouveau 5.4.2 while the pack uses 5.13.1; the mixin targets are therefore version-drift-sensitive and require current-host validation.
