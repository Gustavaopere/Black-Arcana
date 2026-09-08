# Heights

- Registry ID: `ars_nouveau:thread_heights`
- Source class: `JumpHeightPerk`
- Minimum slot: Tier 1 (inherited default).
- Jump path: Ars' `PerkLivingEntity` mixin adds `0.1f * countForPerk(thread_heights)` to `LivingEntity#getJumpBoostPower()`.
- Fall path: `LivingFallEvent` reduces the event distance by `count / 0.1`, i.e. 10 blocks of recorded fall distance per counted perk instance before downstream fall handling.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 1 Spider Eye + 3 Rabbit Hide + 2 Air Essence; `sourceCost: 0`.

## Authority / integration

This perk owns both its jump-power modifier and its fall-distance adjustment inside Ars. Black Arcana must not add the same mobility benefit again when Ars is causal.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.