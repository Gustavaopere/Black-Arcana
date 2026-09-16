# Dragon's Fury

- ID: `firesenderexpansion:dragons_fury`
- School: `irons_spellbooks:ender`
- Levels: 1–7
- Min rarity: Uncommon
- Cast: Long, fixed effective 16 ticks (0.8 s)
- Mana neutral: 75 / 90 / 105 / 120 / 135 / 150 / 165
- Spell power neutral: 10 / 15 / 20 / 25 / 30 / 35 / 40
- Damage: `spellPower/4 + current weapon damage`
- Knockback force: `1 + spellPower×0.01`
- Cooldown: 15 s

## Contract

Short-range Ender melee blast centered near the caster's forward ray. Successful eligible hits receive provider spell damage, knockback, Iron's `AIRBORNE` for 60 ticks at amplifier 1, and Minecraft enchantment post-attack effects. A zero-damage `EarthquakeAoe` is also created for the impact presentation/area behavior.

The class overrides effective cast time so cast-time attributes do not change the intended melee-animation timing.

## Dedup / authority

Weapon damage contribution, post-attack enchantment hooks, Airborne and knockback are one canonical hit pipeline. Do not separately reapply enchantments or Airborne.

## Acquisition

Default Iron's spell eligibility; exact loot/crafting distribution: **NÃO VERIFICADO**.

## Source

`DragonsFurySpell.java` @ pin `5e4067e...`.