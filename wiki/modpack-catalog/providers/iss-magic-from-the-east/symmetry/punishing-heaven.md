# Punishing Heaven

- **ID:** `iss_magicfromtheeast:punishing_heaven`
- **School:** Symmetry
- **Levels:** 1–4
- **Min rarity:** Epic
- **Cast:** Long, 30 ticks
- **Mana neutral:** 250–550
- **Cooldown:** 320 s
- **Summon duration:** 3 minutes
- **Recast count:** 2
- **Jade Executioner damage:** 12 / 16 / 20 / 24
- **HP:** 300 / 350 / 400 / 450
- **Armor:** 12

## Contract

Spawns one `JadeExecutionerEntity` at target block within 8, posts `SpellSummonEvent`, then initializes it with `SummonManager` for 3 minutes.

The displayed summon stats are explicit level formulas and do not depend on the caster's Symmetry power in the audited methods, despite the spell also declaring its own spell-power fields.

## Dedup

This is a long-duration elite Symmetry summon, distinct from Jiangshi's three-unit squad. Black Arcana must preserve SpellSummonEvent replacement and SummonManager ownership.

## Source

`PunishingHeavenSpell.java`.
