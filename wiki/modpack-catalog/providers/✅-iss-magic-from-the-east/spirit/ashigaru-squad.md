# Ashigaru Squad

- **ID:** `iss_magicfromtheeast:ashigaru_squad`
- **School:** Spirit
- **Levels:** 1–8
- **Min rarity:** Uncommon
- **Cast:** Long, 20 ticks
- **Mana neutral:** 60–200
- **Cooldown:** 180 s
- **Summon lifetime:** 10 min
- **Recast count:** 2
- **Summon count:** exactly `spellLevel` = 1–8
- **HP:** `20 + 3×level` = 23–44
- **Armor:** 6
- **Attack damage:** `2 + floor(level/2)` = 2–6

## Contract

Creates a formation of 1–8 `SpiritAshigaruEntity`. Every third summon is marked ranged; all others are melee. All creatures use `SpellSummonEvent` + `SummonManager` and persist their melee/ranged type in entity data/NBT.

Melee variants attack through the spell damage source and explicitly clear target iFrames at their hit frame. Ranged variants fire `SpiritBulletProjectile` at speed 3 with damage = **1.5 × Ashigaru Attack Damage**; the projectile attributes damage back to the original summoner when available and also clears target iFrames on hit.

The entities follow/copy owner targets and ignore fire/fall/drowning while respecting summon ownership rules.

## Dedup / authority

Identity = level-sized mixed formation where every third soldier is a ranged gunner, not N identical minions. Do not add a second projectile or iFrame reset pipeline outside provider code.

## QA

`SpiritBulletProjectile.onHitEntity` contains a local owner/alliance condition that is not sufficient by itself to prove allied-target filtering beyond base projectile behavior. Friendly-fire behavior against third-party allies remains runtime-QA territory.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`AshigaruSquadSpell.java` + `SpiritAshigaruEntity.java` + `SpiritAshigaruAttackGoal.java` + `SpiritBulletProjectile.java`, source 1.1.5.
