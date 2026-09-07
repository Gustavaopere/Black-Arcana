# Kitsune Pack

- **ID:** `iss_magicfromtheeast:kitsune_pack`
- **School:** Spirit
- **Levels:** 1–10
- **Min rarity:** Common
- **Cast:** Long, 20 ticks
- **Mana neutral:** 30–165
- **Cooldown:** 180 s
- **Summon lifetime:** 10 min
- **Recast count:** 2
- **Small kitsunes:** `1 + floor(level/2)` = 1–6
- **Total summons:** one alpha + 1–6 small = 2–7
- **Small HP:** `8 + 2×level` = 10–28
- **Small attack:** `0.5 + level/2.0` = 1.0–5.5
- **Alpha HP:** `2.4 × small HP`
- **Alpha attack:** `1.2 × small attack`

## Contract

Always summons one `SummonedKitsuneAlpha` plus the level-scaled pack of small `SummonedKitsune`, posts `SpellSummonEvent` for every creature and enrolls all of them in the same `SummonManager` cast data.

Small kitsunes follow/protect the owner, apply Soulburn for 60 ticks (3 s) on melee engagement, clear the target's current iFrames, ignore fall damage/provider-friendly damage and self-heal 1 HP every 4 s. The alpha extends the same combat entity and additionally can be mounted/controlled by its summoner as a ground ride.

## Dedup / authority

Identity = mixed pack summon with a stronger mountable alpha and Soulburn melee pressure. Do not split alpha and pack into parallel Black Arcana summons or replicate their Soulburn/iFrame logic externally.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`KitsunePackSpell.java` + `SummonedKitsune.java` + `SummonedKitsuneAlpha.java`, source 1.1.5.
