# Soul Burst

- **ID:** `iss_magicfromtheeast:soul_burst`
- **School:** Spirit
- **Levels:** 1–10
- **Min rarity:** Common
- **Cast:** Long, 20 ticks
- **Mana neutral:** 40–130
- **Spell power / direct damage neutral:** 2–11
- **Cooldown:** 30 s
- **Radius:** 8 blocks
- **Soulburn duration:** `40 + 20×level` ticks = 3–12 s

## Contract

Creates an immediate radial blast around the caster. Eligible targets must not be friendly-fire filtered, must have line of sight, must be living, and must be inside the true 8-block radius. Each eligible target receives direct Spirit damage equal to final spell power plus provider-native `Soulburn` amplifier 0 for the level-scaled duration.

At default config Soulburn pulses once per second at amplifier 0, using 5% of max HP, clamped to 1–10 damage per pulse; immunity is controlled by the provider tag.

## Dedup / authority

Identity = close radial Spirit burst plus max-HP-scaled Soulburn. It is not a generic fire nova and should not be mirrored through a second DoT listener.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`SoulBurstSpell.java` + `SoulburnEffect.java`, source 1.1.5.
