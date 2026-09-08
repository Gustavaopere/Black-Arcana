# Warding

- Registry ID: `ars_nouveau:thread_warding`
- Source class: `MagicResistPerk`
- Minimum slot: Tier 1 (inherited default).
- Attribute path: adds `2 * slotValue` to `PerkAttributes.WARDING` with `ADD_VALUE`.
- Runtime damage path: Ars' `LivingDamageEvent.Pre` reads WARDING and subtracts that flat value when the source matches the provider's magic-damage tag, then clamps final damage to >= 0.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 8 Magebloom Fiber; `sourceCost: 0`.

## Authority / integration

Warding is Ars-owned magic-damage mitigation. Black Arcana must not independently subtract a second copy for the same incoming event. Any generic Arcane Danger/defence bridge must preserve the provider's already-applied mitigation and avoid double-processing.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.