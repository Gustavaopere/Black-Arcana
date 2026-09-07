# Underworld Aid / Impermanence's Verdict

- **Registry ID:** `iss_magicfromtheeast:underworld_aid`
- **School:** Symmetry
- **Levels:** 1–4
- **Min rarity:** Rare
- **Cast:** Long, 40 ticks
- **Mana neutral:** 180–450
- **Spell power/base damage neutral:** 1–4
- **Cooldown:** 160 s
- **Target range:** 32
- **Radius:** 4
- **Duration:** 80 ticks / 4 s
- **Lost-health coefficient:** 10%–40%
- **Default absolute cap:** 20% of target max HP per provider damage application

## Contract

Creates `VerdictCircle`. For non-owner LivingEntities in the area, provider entity applies:

- Slowness amplifier 4 for 20 ticks;
- Blindness amplifier 1 for 20 ticks;
- Darkness amplifier 1 for 20 ticks;
- damage = `spellBaseDamage + missingHealth * (level/10)`;
- final damage is capped at `target.maxHealth * impermanencePercentLimit`.

Upstream config default for `impermanencePercentLimit` is **0.2**. Pack config may override it.

The circle is `AntiMagicSusceptible` and discards under anti-magic.

## Dedup

Identity = short control field whose damage grows with target missing HP but is max-HP capped. Do not separately calculate an execute bonus after provider damage settles.

## Source

`UnderworldAidSpell.java`, `VerdictCircle.java`, `MFTEServerConfigs`.
