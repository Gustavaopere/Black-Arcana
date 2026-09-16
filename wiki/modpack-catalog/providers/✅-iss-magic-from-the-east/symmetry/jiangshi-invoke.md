# Jiangshi Invoke

- **ID:** `iss_magicfromtheeast:jiangshi_invoke`
- **School:** Symmetry
- **Levels:** 1–7
- **Min rarity:** Common
- **Cast:** Long, 30 ticks
- **Mana neutral:** 30–90
- **Cooldown:** 150 s
- **Summon count:** exactly 3
- **Summon duration:** 10 minutes
- **Recast count:** 2
- **Jiangshi attack:** `2+level` = 3–9
- **Jiangshi HP:** `10+5*level` = 15–45

## Contract

Spawns three `SummonedJiangshiEntity` around the caster. Each is posted through `SpellSummonEvent`, added to world and initialized through Iron's `SummonManager`; head drop chance is zero and XP drop is skipped.

The common Jiangshi melee goal confirms life absorption after successful melee hits:

- summoned Jiangshi heals **15% of its Attack Damage** normally;
- if the summoner is a ServerPlayer with `RUSTED_COINS_SWORD` equipped, heal becomes **35% of Attack Damage**.

## Dedup / authority

The heal belongs to Jiangshi AI/entity logic, not the spell cast. Do not credit caster lifesteal or run a duplicate heal event. Summon lifecycle is Iron's `SummonManager` authority.

## Source

`JiangshiInvokeSpell.java`, `JiangshiEntity.java`, `SummonedJiangshiEntity` registration path.
