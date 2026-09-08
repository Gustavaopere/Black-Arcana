# The Amethyst Golem / Knockback Resistance

- Registry ID: `ars_nouveau:thread_amethyst_golem`
- Source class: `KnockbackResistPerk`
- Minimum slot: Tier 1 (inherited default).
- Attribute path: adds `0.15 * slotValue` to vanilla `Attributes.KNOCKBACK_RESISTANCE` with `ADD_VALUE`, i.e. 15% per slot level before vanilla attribute clamping/combination.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 3 items from tag `c:obsidians`; `sourceCost: 0`.

## Authority / integration

Knockback resistance is applied through the vanilla attribute system by Ars. Black Arcana must not duplicate this same modifier when calculating its own displacement/hazard responses; it should observe the resulting entity attributes and preserve provider causality.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.