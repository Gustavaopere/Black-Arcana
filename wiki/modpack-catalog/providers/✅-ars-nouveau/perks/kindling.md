# Kindling

- Registry ID: `ars_nouveau:thread_kindling`
- Source class: `IgnitePerk`
- Minimum slot: Tier 1 (inherited default).
- Trigger: `EffectResolveEvent.Pre` for an `IDamageEffect` that may damage a non-self entity target.
- Runtime: sets target remaining fire ticks to `20 * 5 * slotValue`, i.e. 5 seconds per slot level, before the damage effect resolves.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; Magma Cream + Fire Essence + Fire Charge; `sourceCost: 0`.

## Authority / integration

Kindling is an Ars-owned pre-damage fire proc. Black Arcana must not independently add an equivalent ignite proc to the same Ars effect resolution, and Black Flame must remain a separate Black Arcana domain rather than being conflated with vanilla/Ars fire.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.