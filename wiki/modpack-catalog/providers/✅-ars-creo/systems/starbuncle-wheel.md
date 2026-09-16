# Starbuncle Wheel

State: `SOURCE-PINNED 5.4.0 / RUNTIME QA PENDING`

Registry id: `ars_creo:starbuncle_wheel`

## Exact behavior

`StarbuncleWheelTile` is a Create `GeneratingKineticBlockEntity`.

Default source config:

- base generated speed: `16`;
- bonus generated speed: `24`;
- stress capacity registered through Create: `16`.

On load and relevant neighbor-shape updates, the tile recalculates speed. For horizontal facings, if the block on the clockwise side relative to the wheel's facing is in NeoForge tag `storage_blocks/gold`, the wheel uses the bonus speed; otherwise it uses base speed. Vertical facing does not take the gold-block bonus path.

The exact runtime path does **not** search for, bind, feed or tick a living Starbuncle entity. The Starbuncle connection in the exact provider-owned acquisition path is the `ars_nouveau:starbuncle_charm` ingredient used with a Create Water Wheel.

## Authority

- Create owns kinetic network, stress and rotation propagation.
- Ars Creo owns the wheel bridge/block and its configured generator values.
- Ars Nouveau owns the Starbuncle Charm item used by the recipe.
- Black Arcana does not reinterpret kinetic production as mana/Source/Arcane Danger generation.

## QA pending

Validate effective server config, Create stress behavior, update timing and compatibility with moving/sublevel contexts in the installed full pack.
