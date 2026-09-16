# Ars Elemancy 1.18.3 — armor

Status: `84/84 REGISTRY IDS SOURCE-PINNED / HOST FORMULAS+RUNTIME QA PENDING`

Every armor item extends Ars animated magic armor through `ElemancyArmor`, implements Sauce/Ars Elemental elemental-armor contracts and Ars `IManaDiscountEquipment`.

## Common per-piece Ars mana attributes

Source defaults from `ConfigHandler`:

- `PerkAttributes.MAX_MANA`: +100 per piece;
- `PerkAttributes.MANA_REGEN_BONUS`: +4 per piece.

These are Ars attributes. They do not create a Black Arcana mana resource.

`getManaDiscount` delegates to an inherited `getDiscount(spell.unsafeList())` formula and rounds upward. The exact inherited Sauce/Ars Elemental formula is outside the local source class and remains host-contract QA; no local formula is invented.

## Light armor

Per piece:

- base protection: boots 2, leggings 5, chest 6, helmet 2;
- enchantment value 50;
- toughness 1;
- dual-school item: for each subschool, +12.5 own-school defense, +2 own-school power and -25 defense to the mapped weakness school;
- Elemancer item: +12.5 elemental defense, +2 elemental power.

## Medium armor

Per piece:

- base protection: boots 3, leggings 6, chest 8, helmet 3;
- enchantment value 40;
- toughness 2;
- dual-school item: +25 own-school defense, +1 own-school power and -12.5 defense to mapped weakness school for each subschool;
- Elemancer item: +25 elemental defense, +1 elemental power.

## Heavy armor

Per piece:

- base protection: boots 4, leggings 7, chest 10, helmet 4;
- enchantment value 30;
- toughness 4;
- dual-school item: +50 own-school defense, +0.5 own-school power and **+25** defense to the mapped `weaknessMap` school for each subschool;
- Elemancer item: +75 elemental defense, +0.5 elemental power.

The positive `+25` in HeavyArmorE is preserved exactly as source behavior; it is not silently changed to a negative value because the variable/path name suggests weakness.

## Weakness map used by item attributes

- Fire -> Water;
- Water -> Air;
- Earth -> Fire;
- Air -> Earth.

## Ars perk-slot providers

No local perks are registered. Armor pieces are instead registered as Ars perk providers.

Physical pack expectation, because `allthearcanistgear` is absent:

- medium: all pieces `[1,2,3]`;
- light: head/boots `[1,2,3]`, chest/legs `[2,2,3]`;
- heavy: head/boots `[1,2,2]`, chest/legs `[1,2,3]`;
- Elemancer medium: `[1,2,3]` all pieces;
- Elemancer light: head/boots `[1,2,3]`, chest/legs `[2,2,3]`;
- Elemancer heavy: head/boots `[1,2,2]`, chest/legs `[1,2,3]`.

If All the Arcanist Gear is present, source switches to higher values involving local slots 4 and 5. That compat branch is not considered active for the current physical modlist.

The armor tooltip displays an Ars tier value of 5 while `getMinTier()` returns 2. This source/UI discrepancy is left for runtime/progression QA rather than normalized.