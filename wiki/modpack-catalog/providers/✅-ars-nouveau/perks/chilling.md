# Chilling

- Registry ID: `ars_nouveau:thread_chilling`
- Source class: `ChillingPerk`
- Minimum slot: Tier 1 (inherited default).
- Trigger: `EffectResolveEvent.Pre` for an `IDamageEffect` resolving against another living entity that `canDamage(...)` permits.
- Before damage resolves, the target gains 1 frozen tick and Ars' `FREEZING_EFFECT` for `slotValue * 10 * 20` ticks.
- Source amplifier expression: slot value 1/2 -> amplifier `1`; slot value 3+ -> amplifier `2`.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; Blue Ice + 2 Water Essence + Powder Snow Bucket; `sourceCost: 0`.

## Source/description mismatch

The English description says the effect "becomes Freezing 2 at a level 3 slot". Minecraft effect amplifiers are zero-based, while the 5.13.1 code passes amplifier 1 for slots 1/2 and amplifier 2 for slot 3. Therefore the displayed/effective level implied by the executable path may not match that sentence. Catalog status: `QA_REQUIRED`; do not normalize the amplifier by assumption.

## Authority / integration

This pre-damage status application is Ars-owned. Black Arcana must not add a second freeze proc to the same Ars damage resolution.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.