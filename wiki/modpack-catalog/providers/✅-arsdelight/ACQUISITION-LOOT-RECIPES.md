# Ars Delight 2.2.2 — acquisition, loot and recipe/data boundaries

Status: `SOURCE ACQUISITION SURFACE CATALOGED / INSTALLED DATAPACK+LOOT QA OPEN`

## No provider-owned production glyph registry

The exact source content tree contains helper classes for resolving existing Ars effects on Farmer's Delight blocks, but Phase 2Y identified no Ars Delight-owned production `AbstractSpellPart`/glyph registration.

Ars Delight therefore contributes Ars-aware caster/content behavior without becoming a standalone spell-school/glyph provider.

## Enchanter's Knife acquisition

The Enchanting Apparatus recipe is exact and source-generated:

- Farmer's Delight Diamond Knife reagent;
- one diamond pedestal ingredient;
- one gold storage-block pedestal ingredient;
- one Ars Source Gem Block pedestal ingredient;
- output `arsdelight:enchanters_knife`;
- preserve reagent NBT.

Black Arcana must not create a second unlock/crafting ledger around this provider recipe.

## Global loot modifier intents — 3

`ADGLMProvider` generates three provider global-loot modifiers:

1. `scavenge_chimera_meat`
   - target: Ars Wilden Boss;
   - attacker main hand must match Farmer's Delight/common knife tag;
   - adds 4 Chimera Meat.

2. `scavenge_wilden_hunter_meat`
   - target: Ars Wilden Hunter;
   - attacker main hand must match knife tag;
   - adds 1 Wilden Meat.

3. `scavenge_chimera_horn`
   - target: Ars Wilden Boss;
   - attacker main hand must match axe tag;
   - adds 1 Chimera Horn.

These rewards are provider-owned descendants of the death/loot transaction. A BA death observer must not duplicate them.

## Recipe families

`RecipeGen` source generates multiple Ars Delight recipe families rather than a single custom machine pipeline:

- meat cooking and meat slicing;
- Archwood bark stripping;
- fruit-pod storage crates and unpacking;
- pies/slices;
- Farmer's Delight Cutting Board processing;
- source-berry food recipes;
- skewers;
- Cooking Pot sauces, soups, stews and feasts;
- jelly/tea/hornbeer/jam fruit processing;
- bark/paper/organic-compost utility recipes;
- conditional Ars Elemental and Archwood Good recipe generation.

Phase 2Y does not invent a total generated-recipe count from source snippets; exact installed datapack inventory remains a JAR extraction/data validation task.

## Cuisine Delight data

`ADConfigGen` emits Cuisine Delight ingredient/config transforms for provider meats, fruits, jams and sauces, including cooking-stage and fluid-color data. The source build referenced Cuisine Delight 1.2.1+1 while the current pack has 1.2.10, so current data compatibility remains unproven.

## Tags/data maps

Provider content also participates in Ars magic-food tags, Farmer's Delight/common food/tool/storage tags, Diet tags when applicable, furnace-fuel data and compostability data.

Tag membership is declarative provider data. BA may query standard/provider tags when a real design needs them, but must not copy provider recipe/tag tables into a second runtime authority.

## Runtime QA

Validate physical generated recipes/tags/loot modifiers, recipe reload, loot exactly-once behavior and compatibility with current recipe/loot/nutrition addons before reporting installed-runtime PASS.
