# Create: Enchantment Industry 2.5.3b — evidence and provenance

## Physical authority

Current sibling physical authority at `neoforge-rpg-skilltree@b9edb403c06567423d6c101d136b73a1065f2ad4`:

- JAR `create-enchantment-industry-2.5.3b.jar`;
- mod id `create_enchantment_industry`;
- runtime `2.5.3b`;
- SHA-1 `f39af237b8bff853a89e8784518bdc36ba54a32e`.

The sibling dossier remains the current pack authority for installed identity.

## Publisher release

CurseForge project/file:

- project `688768`;
- file `8762719`;
- filename `create-enchantment-industry-2.5.3b.jar`;
- NeoForge / Minecraft 1.21.1;
- Beta release uploaded 2026-08-29;
- publisher note: Apothic Enchanting integration requires 1.6.1+;
- 2.5.3b fix: Infuser crash with Apothic Enchanting 1.6.1+.

A later 1.21.1 NeoForge 2.5.4 exists, but it does not replace the physical 2.5.3b pack authority.

## Exact source-version evidence

Official repository: `DragonsPlusMinecraft/CreateEnchantmentIndustry`.

Exact source checkpoint:

`9a523a3a0fb967f28658eb289534e692f6c03a9b`

The commit is titled `fix: support Apothic Enchanting 1.6.1`, dated 2026-08-29. Its `gradle.properties` changes the project version to `2.5.3b` and pins the development baseline described in the provider README.

The source files carry SPDX `LGPL-3.0-or-later`. Black Arcana retains only factual registry/API/data-shape facts for cataloging and interoperability; no provider code or assets are copied into Black Arcana.

## Exact semantic checks

### No provider enchantment definitions

At the exact source pin:

- `CEIEnchantments` creates tag keys against `Registries.ENCHANTMENT`; it does not register enchantment objects;
- recursive source-tree inspection finds no packaged `data/create_enchantment_industry/enchantment/**` definitions;
- packaged enchantment data are under `tags/enchantment/**` and `data_maps/enchantment/**`;
- `CEIDataMaps` operates on existing `Registries.ENCHANTMENT` entries.

Result: **0 CEI-owned enchantment identities established**.

### No spell/glyph construction surface

The exact source audit found no provider spell/glyph registry surface. No CEI path or inspected registration class establishes an Ars `AbstractSpellPart`, Iron's `AbstractSpell`, spell registry, glyph registry or ritual registry.

Result:

- standalone spells: **0**;
- glyphs: **0**;
- rituals: **0**.

### Enchantment system surfaces

Exact source establishes seven CEI enchantment tags and five enchantment-keyed data maps. These govern eligibility/cost/level-extension/processing behavior of existing enchantments.

The exact generated super-enchanting custom-level-extension map contains an empty `values` object. This is not evidence of provider enchantment creation.

### Custom registry and content support

`CEIRegistries` adds a CEI registry key for `printing_behaviour`. `CEIDamageTypes` defines `create_enchantment_industry:grind`; CEI also registers Liquid Experience plus processing blocks/items.

These are provider infrastructure/content facts and are not promoted into spell/glyph/ritual identities.

## Clean-room conclusion

Catalog decision:

`✅ CATALOGED / +0 STRICT MAGIC IDENTITIES`

Reason: exact physical identity and exact source version are known; the provider's magic relevance is enchantment/XP processing rather than ownership of new spell, glyph, ritual or enchantment identities.

Runtime balance, transaction conservation and integration behavior remain a separate validation layer.
