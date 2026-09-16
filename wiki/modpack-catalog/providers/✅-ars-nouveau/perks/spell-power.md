# Spell Power

- Registry ID: `ars_nouveau:thread_spellpower`
- Source class: `SpellDamagePerk`
- Minimum slot: Tier 1 (inherited default).
- Attribute path: adds `2 * slotValue` to `PerkAttributes.SPELL_DAMAGE_BONUS` using `ADD_VALUE`.
- Core spell-damage path: Ars' `IDamageEffect.attemptDamage()` calculates `baseDamage + SpellStats.damageModifier + caster SPELL_DAMAGE_BONUS` before Randomize and `SpellDamageEvent.Pre` processing.
- Additional provider-owned consumers may use the same attribute (for example Bubble and Enchanter's Sword in the provider source line); Black Arcana must not assume the attribute is exclusively armor-derived.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; Fire Essence + Magebloom + Manipulation Essence + Water Essence + Abjuration Essence + Air Essence + Earth Essence + Conjuration Essence; `sourceCost: 0`.

## Authority / integration

Spell damage is calculated inside Ars' canonical damage path. Black Arcana must not add this perk again to Ars-originated spell damage. Any cross-provider power bridge must distinguish provider-native spell power from Black Arcana's own bounded power scaling.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.