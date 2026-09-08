# Spellweave

Status: `SOURCE-PINNED 21.3.0 / ENCHANTMENT+PERK BRIDGE AUDITED / RUNTIME+PACK QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:spellweave`.

## Enchantment definition

Spellweave is a datapack enchantment targeting the vanilla `#minecraft:enchantable/armor` set.

Source definition:

- weight: 30;
- maximum level: 3;
- anvil cost: 2;
- equipment slot group: ARMOR.

The addon injects an `Enchantment.isSupportedItem` guard for Spellweave. It rejects armor that already carries Ars Nouveau `ARMOR_PERKS` data and items in the provider `spellweave_incompatible` tag.

## Provider behavior

The purpose of Spellweave is to add Ars Thread/perk slots to armor that does not already have native Ars perk data.

When an enchanted armor item is used with the Ars Alteration Table, the mixin:

1. verifies the item is armor;
2. refuses to overwrite existing native Ars perk data unless this addon already marked the stack as its override;
3. reads the Spellweave enchantment level and clamps it to the provider PerkSlot range;
4. sets `ars_additions:override_perks=true`;
5. installs/updates Ars `ARMOR_PERKS` with tier `enchantment level - 1`.

A PerkRegistry mixin then supplies the addon override layout from the registered Ars `PerkSlot` values rather than the item's normal provider list.

If the stack becomes incompatible in the Alteration Table path, the mixin removes Spellweave instead of leaving an invalid provider override.

## Enchanting Apparatus acquisition

Level I — **10,000 Source**:

- Blank Thread;
- Magebloom Fiber ×4;
- Source Gem Block;
- Diamond Block;
- Lapis Block ×2.

Level II — **20,000 Source**:

- Blaze Rod-tag item ×2;
- Diamond Block ×2;
- Lapis Block;
- Source Gem Block.

Level III — **30,000 Source**:

- Ender Pearl-tag item ×2;
- Chorus Fruit;
- Wilden Tribute;
- Diamond Block ×3;
- Lapis Block.

## Black Arcana / RPG boundary

Spellweave remains Ars Additions -> Ars Nouveau perk infrastructure. RPG Skill Tree must not reinterpret Spellweave levels as RPG perk points, and Black Arcana must not duplicate Thread slots or modifiers. If integration observes Ars Threads on Spellweave armor, it must preserve the provider's `ARMOR_PERKS` authority and avoid double-applying the same stat/effect.
