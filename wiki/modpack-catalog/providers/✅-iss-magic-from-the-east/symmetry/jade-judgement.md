# Jade Judgement

- **ID:** `iss_magicfromtheeast:jade_judgement`
- **School:** Symmetry
- **Levels:** 1–6
- **Min rarity:** Rare
- **Cast:** Long, 40 ticks
- **Mana neutral:** 65–140
- **Spell power/damage neutral:** 20–40
- **Cooldown:** 60 s
- **Pre-target helper:** 48 blocks
- **Fallback raycast:** 32 blocks
- **Impact radius:** 5

## Contract

Resolves target/location, raises the `JadeDao` spawn upward through free space by up to 16 blocks, and assigns airtime 35 ticks with target or 25 without target.

During the falling phase, each valid entity can be hit once for **25%** of the Dao's damage and has invulnerability time reset to 0 after successful damage.

On ground impact it performs a radius-5 AoE with cubic distance falloff:

`damage = baseDamage * (1 - (distance/radius)^3)`.

Then it plays impact feedback and discards.

## Dedup / authority

The Dao entity owns its tracking, descent, falling-contact hits and final AoE. Do not add a second impact explosion or separate falling hit listener.

## Source

`JadeJudgementSpell.java` + `JadeDao.java`.
