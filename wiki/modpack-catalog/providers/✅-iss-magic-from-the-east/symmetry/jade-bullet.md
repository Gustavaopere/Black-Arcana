# Jade Bullet

- **ID:** `iss_magicfromtheeast:jade_bullet`
- **School:** Symmetry
- **Levels:** 1–10
- **Min rarity:** Common
- **Cast:** Instant
- **Mana neutral:** 10–55
- **Spell power/direct damage neutral:** 2–11
- **Cooldown:** 5 s
- **Projectile speed:** 1.6
- **Shockwave radius:** 2.5
- **Shockwave damage:** 50% of projectile damage

## Contract

Creates no-gravity `JadeBulletProjectile`.

- Entity impact: applies full projectile damage, then radial shockwave, then discards.
- Block impact: radial shockwave, then discards.
- Shockwave checks entities within true 2.5-block radius and applies 50% of projectile damage through the same spell damage source.

## Dedup

One cast already contains direct projectile hit + impact AoE. Do not treat these as two independent casts or add another shockwave in an integration.

## Source

`JadeBulletSpell.java` + `JadeBulletProjectile.java`.
