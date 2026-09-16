# Bagua Array Circle

- **ID:** `iss_magicfromtheeast:bagua_array_circle`
- **School:** Symmetry
- **Levels:** 1–8
- **Min rarity:** Uncommon
- **Cast:** Long, 20 ticks
- **Mana neutral:** 70–140
- **Spell power neutral:** 1–8
- **Cooldown:** 60 s
- **Targeting:** helper/raycast up to 32
- **Radius:** 5
- **Duration:** 200 ticks / 10 s
- **Undead damage per provider application:** `0.5*spellPower`
- **Reversal Healing amplifier:** level−1 = 10%–80%

## Actual entity contract

`BaguaCircle` damages only LivingEntities that:

- are not the owner; and
- have an entity type in vanilla `UNDEAD`.

The owner is not damaged. Instead, while inside the circle it receives `REVERSAL_HEALING` for 40 ticks at the spell amplifier.

`ReversalHealingEffect` hooks `LivingDamageEvent.Pre` server-side. For eligible damage it:

1. sets incoming damage to **0**;
2. heals the entity by `originalDamage * (amplifier+1)*0.1`.

Thus level 1–8 converts an eligible hit into healing equal to 10%–80% of the original damage while negating that hit. It does not trigger for damage tagged provider `BYPASS_REVERSAL_HEALING`, fall damage or bypass-invulnerability damage.

The circle is `AntiMagicSusceptible` and discards on anti-magic.

## Dedup

This is much stronger/specific than a simple “healing circle”: undead-only offense + owner-only damage inversion. Never implement Reversal Healing again from health-delta observation.

## Source

`BaguaArrayCircleSpell.java`, `BaguaCircle.java`, `ReversalHealingEffect.java`.
