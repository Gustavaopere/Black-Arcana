# Ars Elemental 0.7.10.1 — familiars

Status: `3/3 HOLDERS SOURCE-PINNED / TWO DESCRIPTION-PATH DIVERGENCES / RUNTIME QA PENDING`

All three holders are registered through Ars `FamiliarRegistry`.

## Flarecannon

Registry id: `ars_elemental:firenando_familiar`

Binding predicate: provider `FirenandoEntity`.

Confirmed source behavior:

- while alive and owned by the caster, Fire-school spell parts add `+2.0` damage modifier through `SpellModifierEvent`;
- `projectileGlyphs` is populated in `postInit()` with Arc Projectile, Homing Projectile, core Projectile, Propagate Homing and Propagate Arc;
- when the first spell part is in that list, `SpellCostCalcEvent.currentCost` is reduced by `context.getSpell().getCost() * 0.5`;
- owner interaction with Magma Cream consumes one and grants Fire Resistance for 1200 ticks;
- Magma Block / Soul Sand can change the familiar visual variant.

Divergence: the holder book description says projectile-based spells cost 20% less, but executable source subtracts 50% of base spell cost from current cost. `RUNTIME QA REQUIRED`.

## Flashjack

Registry id: `ars_elemental:flashjack_familiar`

Binding predicate: provider `FlashjackEntity`.

Confirmed source behavior:

- Air-school spell parts add `+2.0` damage modifier for the owner;
- `movementGlyphs` is populated with core Leap, Launch, Pull, Knockback, Blink and Glide;
- if the first spell part is in that list, source subtracts `spell.getCost() * 0.5` from current cost;
- feeding a Flashing Pod grants owner Movement Speed I and Night Vision I for 6000 ticks and gives the familiar Movement Speed I for 6000 ticks;
- supported dyes change the visual variant.

Divergence: holder documentation says 20% movement-spell cost reduction, while executable source subtracts 50% of base spell cost. `RUNTIME QA REQUIRED`.

## Siren

Registry id: `ars_elemental:siren_familiar`

Binding predicate: provider `MermaidEntity`.

Confirmed source behavior:

- Water-school spell parts add `+2.0` damage modifier for the owner;
- the familiar cannot drown in fluid types;
- while the familiar is in water, every 60 ticks it refreshes Dolphin's Grace amplifier 1 for 600 ticks on both owner and familiar;
- provider-supported color items change the familiar variant.

This matches the holder description's Water damage and Dolphin's Grace II behavior at the source level.

## Authority boundary

Familiar modifiers are Ars-owned event modifications. Black Arcana must not add a second +2 school damage, duplicate cost discounts, or settle a new root cast when the same provider event is observed.