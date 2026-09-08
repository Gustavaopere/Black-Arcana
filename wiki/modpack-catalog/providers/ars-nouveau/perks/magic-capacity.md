# Magic Capacity

- Registry ID: `ars_nouveau:thread_magic_capacity`
- Source class: `MagicCapacityPerk`
- Minimum slot: Tier 1 (inherited default).
- Attribute path: adds `0.1 * slotValue` to `PerkAttributes.MAX_MANA` with `ADD_MULTIPLIED_TOTAL`, i.e. +10% max mana per slot level.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 3 Sourceberry Bush + 3 Magebloom; `sourceCost: 0`.

## Authority / integration

This modifies Ars Nouveau's max-mana attribute. It does **not** authorize Black Arcana to create a second mana pool or mirror the modifier into a Black Arcana resource. Any RPG Skill Tree bridge may expose progression/gating only through a real contract; Ars remains authority for this mana quantity.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.