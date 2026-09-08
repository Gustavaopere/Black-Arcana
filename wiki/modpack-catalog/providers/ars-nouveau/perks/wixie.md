# The Wixie / Potion Duration

- Registry ID: `ars_nouveau:thread_wixie`
- Source class: `PotionDurationPerk`
- Minimum slot: Tier 1 (inherited default).
- Attribute path: adds `0.15 * slotValue` to `PerkAttributes.WIXIE` with `ADD_MULTIPLIED_BASE`; the attribute itself has base value 1.0.
- Runtime effect path: on `MobEffectEvent.Added`, Ars uses the target's WIXIE value for beneficial effects and the living applier's WIXIE value for harmful effects, then multiplies the incoming effect duration by that value when it is > 0.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 3 Wixie Shards + 2 Abjuration Essence + 2 items from `c:crops/nether_wart` + 1 Blaze Rod; `sourceCost: 0`.

## Authority / integration

Potion-duration mutation is Ars-owned and applies during the provider's effect-added event path. Black Arcana must not extend the same effect a second time when Ars caused the modification.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.