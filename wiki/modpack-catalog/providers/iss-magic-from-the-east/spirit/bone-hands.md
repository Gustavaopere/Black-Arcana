# Bone Hands

- **ID:** `iss_magicfromtheeast:bone_hands`
- **School:** Spirit
- **Levels:** 1–5
- **Min rarity:** Rare
- **Cast:** Long, 30 ticks
- **Mana neutral:** 80–220
- **Cooldown:** 240 s
- **Summon lifetime:** 10 min
- **Recast count:** 2
- **Summon HP:** `60 + 32×level` = 92–220
- **Attack damage neutral:** final Spirit spell power = 2–18 before external modifiers

## Contract

Summons one `BoneHandsEntity` near the targeted block (8-block targeting helper), posts Iron's `SpellSummonEvent`, and enrolls the resulting creature in `SummonManager` lifecycle/recast data.

The summon is a flying melee follower with owner-target goals. It cannot drown, is fire immune, takes no fall damage, is not pushable, uses the spell's damage source for melee attacks and self-heals **2% of max HP every 80 ticks / 4 s**. During its rise animation, non-bypass damage is rejected; provider/base summon friendly-fire rules also apply.

## Dedup / authority

Identity = durable, self-healing flying melee summon. Summon ownership, duration, death/removal and recast lifecycle belong to Iron's `SummonManager` + provider entity.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`BoneHandsSpell.java` + `BoneHandsEntity.java`, source 1.1.5.
