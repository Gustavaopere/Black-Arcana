# The Drygmy / Looting

- Registry ID: `ars_nouveau:thread_drygmy`
- Source class: `LootingPerk`
- Minimum slot: Tier 1 (inherited default).
- Attribute path: adds `slotValue` to `PerkAttributes.DRYGMY` using `ADD_VALUE`.
- The same Ars attribute is also used by the active Drygmy familiar's `LOOTING_EFFECT` (+1), while the older direct `LootingLevelEvent` familiar handler is commented out in 5.13.1.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 3 Drygmy Shard + 2 Earth Essence + 1 Rabbit's Foot; `sourceCost: 0`.

## Authority / integration

Loot attribution and extra-drop semantics are Ars-owned. Black Arcana must not independently add a second looting reward to an Ars-caused kill. Cross-provider kill rewards require a single canonical causal event and explicit deduplication.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`. Exact downstream loot-table/mixin consumption of `PerkAttributes.DRYGMY` belongs to the provider and must not be reimplemented by Black Arcana.