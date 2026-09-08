# Ars Polymorphia — crafting resolution

Status: `EXACT 1.0.3 SOURCE CATALOGED`

## Server-side matrix observation

`CraftingLecternTileMixin` injects at the head of Ars Nouveau `CraftingLecternTile.onCraftingMatrixChanged(UUID)`.

The exact flow is:

1. obtain the current Minecraft server;
2. resolve the player by the supplied UUID;
3. require a `ServerLevel`;
4. read that player's Polymorph recipe-selection data;
5. query the server RecipeManager for every matching `CraftingRecipe` using the player's lectern crafting inventory;
6. discard recipes whose result item is empty;
7. build Polymorph `RecipePair` entries from recipe id + result item;
8. if the player's previously selected recipe id still appears in the valid set, assign that Ars `currentRecipe`;
9. send the current conflict set and selected id to the player through Polymorph's own sync/list payloads.

The provider does not invent recipe outputs. Candidate recipes come from the server RecipeManager.

## Player-specific state

The crafting inventory is resolved with `getCraftingInv(UUID)`, and Polymorph selection state is read from the corresponding player. This makes the intended authority player-specific even when multiple users access Ars storage infrastructure.

Multiplayer QA still needs to verify two players selecting different conflicting outputs on the same lectern do not contaminate one another under the current Ars/Polymorph+ host versions.

## Client selection

`CraftingTerminalWidget` extends Polymorph's `PlayerRecipesWidget`. The client can choose a displayed recipe id and sends only `ars_polymorphia:reset_crafting_result` to the server; the selected id itself remains in Polymorph's player-selection state rather than becoming an arbitrary Ars output packet.

The client additionally checks that the selected recipe id exists in its local RecipeManager before sending the reset request. That is presentation-side hygiene, not the security boundary.

## Server settlement

`PacketResetCraftingResult.onServerReceived` requires:

- a real server player;
- the currently open menu to be Ars `CraftingTerminalMenu`;
- that menu's tile to be an Ars `CraftingLecternTile`.

It then asks Polymorph's recipe manager for the player's valid crafting recipe against the current matrix and level. If no valid recipe resolves, it returns without modifying Ars state.

On success it:

1. writes the resolved recipe into Ars `currentRecipe` through the accessor;
2. invokes Ars `onCraftingMatrixChanged(player UUID)` again;
3. records the selected recipe through Polymorph player recipe data.

Thus the authoritative result is server re-resolution, not a client-supplied output stack.

## Deduplication consequence

Black Arcana has no reason to intercept or settle this recipe choice. If BA ever consumes crafting completion as progression/event evidence, it must observe the final Ars craft result rather than run a second recipe resolver or mutate Polymorph selection state.
