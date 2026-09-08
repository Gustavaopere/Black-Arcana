# Enchanting Wixie automation

Status: `SOURCE-PINNED 21.3.0 / MIXIN+BLOCK SEMANTICS AUDITED / RUNTIME+PACK QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry block: `ars_additions:enchanting_wixie_cauldron`.

## Creation

Ars Additions injects into Ars Nouveau `WixieCharm.useOnBlock`. When a server player uses a Wixie Charm on an Ars `EnchantingApparatusBlock`, the provider replaces that block with the Enchanting Wixie Cauldron and triggers the addon advancement.

This is a provider block transformation, not a standalone crafting recipe.

## Recipe automation

`EnchantingWixieCauldronTile` extends Ars `WixieCauldronTile` and replaces its recipe lookup with `EnchantingApparatusRecipeWrapper`.

The wrapper scans the server recipe manager for Ars `EnchantingApparatusRecipe` entries matching the requested output item. For `EnchantmentRecipe` it validates the current enchantment level on the input; for ordinary apparatus recipes it also adds the apparatus reagent to the Wixie ingredient list.

The resulting craft continues through Ars Wixie/CraftingManager infrastructure; Ars remains authority for the base automation lifecycle and inventory/source behavior not overridden by this addon.

## Explicit output storage

Ars Additions injects `IWandable` + `IWixieOutputStorage` behavior into the base Wixie Cauldron tile.

A connected block position with an item-handler capability may be persisted as `FinishedStorage` in block-entity NBT. On craft completion:

- the addon attempts insertion into that target using an Ars `FilterableItemHandler` and the Wixie's current filters;
- if the handler disappears, the stored output target is cleared and normal item-output behavior resumes;
- if insertion is partial, the remainder follows normal dropped-item output;
- if insertion succeeds completely, a flying-item visual is spawned only when a player is within 64 blocks of the destination.

The flying item is presentation; inventory insertion is the gameplay settlement.

## Advanced Dominion interaction

Because the mixin exposes `IWandable`, the normal/Advanced Dominion Wand can configure the output target through provider connection callbacks. The target must expose an item-handler capability before it is stored.

## Black Arcana boundary

Do not treat Wixie recipe completion, flying-item visuals or output insertion as Black Arcana spell execution. Black Arcana must not duplicate item insertion, consume ingredients/source a second time, or infer magical production credit from the visual entity.
