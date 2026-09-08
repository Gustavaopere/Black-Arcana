# The Whirlisprig / Saturation

- Registry ID: `ars_nouveau:thread_whirlisprig`
- Source class: `SaturationPerk`
- Minimum slot: Tier 1 (inherited default).
- Attribute path: maps slot value to modifier 1 -> 0.3, 2 -> 0.6, 3+ -> 1.0 on `PerkAttributes.WHIRLIESPRIG` using `ADD_MULTIPLIED_TOTAL`; the attribute base value is 1.0.
- Runtime food path: after consuming food, Ars multiplies the player's current saturation level by the effective provider perk value.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 3 Whirlisprig Shards + 2 Earth Essence + 1 Golden Apple; `sourceCost: 0`.

## Authority / integration

This is Ars-owned food/saturation amplification. Black Arcana must not multiply saturation again for the same perk event. Any nutrition integration should observe the provider result rather than replay its formula.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.