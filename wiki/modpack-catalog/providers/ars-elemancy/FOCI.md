# Ars Elemancy 1.18.3 — foci

Status: `7/7 SOURCE-PINNED / EFFECTIVE CONFIG+RUNTIME QA PENDING`

All seven foci extend Ars Elemental `GreaterElementalFocus` and are Curios-compatible through the generated `curios:an_focus` item tag.

## Shared mechanics

- source config discount return: `elemental_maj_focus_discount`, default `0.25`;
- matching spell parts receive `addAmplification(getBoostMultiplier() * 2)`;
- each mastery/buff config defaults to `1.0`, so the default builder addition is `2.0` amplification units;
- no percentage/final-damage interpretation is inferred from that builder value without the exact host spell-stat contract;
- every 20 server ticks, if `regen_bonus=true`, environmental effects are checked recursively for the focus school/subschools;
- foci containing Earth add `+0.2` Knockback Resistance through Curios attributes.

## Environmental effects

- Fire: while on fire or in lava -> Ars `SPELL_DAMAGE_EFFECT`, 200 ticks, amplifier 1.
- Water: in water/rain/bubble -> Mana Regen 120 ticks; amplifier 1 while swimming plus Dolphin's Grace 200 ticks amplifier 1, otherwise Mana Regen amplifier 0.
- Air: while Shocked -> Mana Regen + Spell Damage, 60 ticks amplifier 1; otherwise above Y=200 -> Mana Regen 120 ticks amplifier 0.
- Earth: below Y=0 -> Mana Regen 120 ticks amplifier 0.

A composite focus recursively receives checks for both of its subschools. Exact interaction when multiple environmental conditions are simultaneously true is provider-owned.

## Ars Elemental compatibility mixin

`SchoolFocusMixin` extends Ars Elemental `CompatUtils` checks:

- Fire accepts Cinder, Vapor, Lava, Elemancer;
- Water accepts Tempest, Mire, Vapor, Elemancer;
- Earth accepts Silt, Mire, Lava, Elemancer;
- Air accepts Tempest, Cinder, Silt, Elemancer.

This modifies host recognition of the same Ars spell action. Black Arcana must not turn that recognition into a second cast, second mana discount or second Mastery settlement.