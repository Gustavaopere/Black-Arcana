# Splitting Shuriken

**Registro físico confirmado:** ✅ `COUNTED_EXACT` — `iss_magicfromtheeast:splitting_shuriken`, classe `net.warphan.iss_magicfromtheeast.spells.spirit.SplittingShurikenSpell`, escola `MFTESchoolRegistries.SPIRIT_RESOURCE`, por [Java 21 #38449995162](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449995162). Dados numéricos source-pinned; runtime/Survival ⚠️; +0. [Dossiê](../EXACT-BINARY-SPELLS-1.1.5.md).

- **ID:** `iss_magicfromtheeast:splitting_shuriken`
- **School:** Spirit
- **Levels:** 1–10
- **Min rarity:** Common
- **Cast:** Instant
- **Mana neutral:** 15–42
- **Primary damage neutral:** 4–13
- **Cooldown:** 3 s
- **Secondary count after entity hit:** `level+2` = 3–12
- **Secondary damage:** 50% of primary stored damage

## Contract

Casts one primary `SplittingShurikenProjectile`. The projectile has no gravity and speed 1.5. If the primary hits a block, it simply discards. If it hits an entity, it first applies full stored Spirit damage, then spawns 3–12 secondary shuriken in a 360° radial pattern at the impact point. Secondaries carry half the primary damage and are not marked primary, preventing recursive splitting.

## Dedup / authority

Identity = **entity-hit-triggered** radial split. It is not a shotgun on cast and does not split on block impact. The projectile entity is the authority for when/where splitting occurs.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`SplittingShurikenSpell.java` + `SplittingShurikenProjectile.java`, source 1.1.5.
