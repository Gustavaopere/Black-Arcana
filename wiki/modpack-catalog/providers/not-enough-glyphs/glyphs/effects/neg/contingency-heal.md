# Contingency: Heal

- Registry: `not_enough_glyphs:contingency_heal`
- Class: `HealContingency`; Sauce-backed contingency
- Status: enabled
- Trigger evidence: NEG handles `LivingHealEvent` and calls the active Sauce contingency when its trigger is `ON_HEAL`.
- Acquisition: Abjuration Essence + Repeater + Honey Bottle.
- Tier/mana/lifecycle inherited from Sauce/Ars where not overridden by NEG.
- Boundary: no second BA heal-triggered stored-spell engine.