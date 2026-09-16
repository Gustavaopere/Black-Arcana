# Ars Nouveau — Player Mana

State: `SOURCE-PINNED 5.13.1 / PROVIDER AUTHORITY VERIFIED`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`.

## Capability

Ars exposes `IManaCap` with provider-native operations for current mana, max mana, add/remove/set mana, glyph bonus and book tier. `ManaCap` persists that data through Ars' mana attachment and clamps current mana to `[0, maxMana]`.

## Max mana

`ManaUtil.calcMaxMana(Player)` derives raw max mana from:

`INIT_MAX_MANA + knownGlyphCount * GLYPH_MAX_BONUS + bookTier * TIER_MAX_BONUS`

The value is then represented through Ars' `PerkAttributes.MAX_MANA`, so armor/perk modifiers participate in the final attribute value. Ars posts `MaxManaCalcEvent`, allowing provider/addon modification, and reads an event-supplied reserve fraction.

Usable max mana is `Max * (1 - Reserve)`.

Familiars participate in this reserve path through `MaxManaCalcEvent`; the common familiar runtime contributes a 0.15 reserve modifier per active familiar entity path unless overridden.

## Mana regeneration

`ManaUtil.getManaRegen(Player)` starts from:

`knownGlyphCount * GLYPH_REGEN_BONUS + bookTier * TIER_REGEN_BONUS + INIT_MANA_REGEN`

It then resolves through `PerkAttributes.MANA_REGEN_BONUS` and `ManaRegenCalcEvent`.

Config-backed terms are intentionally left symbolic here. The physical modpack/runtime config is the authority for their actual values.

## Spell settlement

`SpellResolver` validates the spell, computes resolve cost, checks caster mana and only calls `expendMana()` when the cast method returns `CastResolveType.SUCCESS`. Resolve cost and expended cost each pass through Ars' spell-cost events and provider-native discount calculation. Turret tile casters are explicitly exempted from `expendMana()` in this path.

## Authority / Black Arcana boundary

Ars player mana is the authoritative resource for Ars casts. Black Arcana must not create a shadow copy of Ars mana, mirror Thread modifiers into a second resource, or charge an additional Black Arcana mana cost for the same Ars-owned cast. If Black Arcana ever consumes Ars mana through an integration, that must use a verified adapter/transaction contract; otherwise fail closed.
