# Imbued Spell Parchment

Status: `SOURCE-PINNED 21.3.0 / CASTING+ACQUISITION AUDITED / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:imbued_spell_parchment`.

## Acquisition

The custom `imbue_scroll` Imbuement Chamber recipe accepts only:

- Ars Nouveau Spell Parchment as reagent;
- a valid spell already stored on that parchment;
- **no pedestal items**.

Source cost is `stored spell cost × 10` Source. If the reagent cannot be interpreted as the expected caster provider, the recipe method returns a 10,000 fallback cost, but normal recipe matching already rejects that case.

The result copies the Ars `SPELL_CASTER` component into the Imbued Spell Parchment.

The provider also injects Imbued Spell Parchments generated from Ars Caster Tome recipe data into Ars basic dungeon loot through its Caster Tome registry mixin.

## Cast behavior

Use starts a bow-style use action. Use duration is based on the stored spell's nominal cost:

`ceil(spell cost / 100) × 10 ticks`

At completion it calls the stored Ars caster's `castSpell`. If that action consumes successfully, the parchment consumes one item.

A provider `SpellCostCalcEvent` listener sets current spell cost to **0** when the caster tool is an Imbued Spell Parchment. The preparation Source cost therefore occurs at imbuement time; casting itself is provider-zero-cost under this event path.

## Black Arcana boundary

This remains an Ars spell cast. Black Arcana must not treat the zero mana cost as a free Black Arcana cast, settle a second mana/cooldown transaction, or count the imbuement Source payment as Black Arcana progression. Causal identity remains the single provider cast executed from the parchment.
