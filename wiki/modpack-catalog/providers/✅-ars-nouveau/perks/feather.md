# Feather

- Registry ID: `ars_nouveau:thread_feather`
- Source class: `FeatherPerk`
- Minimum slot: Tier 1 (`PerkSlot.ONE`, inherited default)
- Attribute path: adds `0.2 * slotValue` to `PerkAttributes.FEATHER` with `ADD_VALUE`.
- Runtime damage path: Ars Nouveau's `LivingDamageEvent.Pre` handler reads the effective FEATHER attribute and, for fall damage, applies `amount -= amount * feather` before clamping the final damage to at least zero.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 4 items in tag `c:feathers` + 2 `ars_nouveau:abjuration_essence`; `sourceCost: 0`.

## Authority / integration

This is Ars-owned fall-damage mitigation carried by its perk attribute/event pipeline. Black Arcana must not independently reapply the same reduction when Ars already caused it. Any cross-provider mobility/fall logic must preserve single causality and avoid double mitigation.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.