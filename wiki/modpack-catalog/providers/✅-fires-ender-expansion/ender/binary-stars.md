# Binary Stars

- ID: `firesenderexpansion:binary_stars`
- School: `irons_spellbooks:ender`
- Levels: 1–5
- Min rarity: Rare
- Cast: Instant
- Mana neutral: 55 / 80 / 105 / 130 / 155
- Spell power neutral: 30 / 40 / 50 / 60 / 70
- Star direct damage neutral: 4.5 / 6.0 / 7.5 / 9.0 / 10.5
- Debuff duration neutral: 60 / 80 / 100 / 120 / 140 ticks = 3–7 s
- Target range: 64
- Recast window: 80 ticks
- Target set: 1–2 living targets
- Cooldown: 60 s

## Contract

The first/second target selections are stored in Iron's `MultiTargetEntityCastData`. When the recast finishes, one Nova Star and one Obsidian Star are fired as homing projectiles. With one stored target, both stars use the same target; with two, Nova uses the first and Obsidian the second.

Nova Star applies `Nova Burn`; Obsidian Star applies `Eclipsed`. Eclipsed dynamically tracks beneficial effects and reduces Attack Damage and Attack Speed by 5% per beneficial effect, capped at 10 buffs / −50%.

## QA finding — Nova Burn

`NovaBurnEffect` computes spell-cast self-damage as `5 × beneficial buffs × effect amplifier`. Nova Star applies the effect without an amplifier argument, i.e. amplifier 0. The source-pinned provider path therefore computes 0 damage unless another runtime path changes the amplifier. **Runtime QA required; do not silently rewrite this as functional damage.**

## QA finding — commented slam

`BinaryStarEntity` contains code for teleporting above the target and a later slam/AoE, but the entire phase is commented out at the 2.4.1 pin. It is not part of the active contract documented here.

## Dedup / authority

Target storage, homing, star assignment and debuffs are provider-owned. Do not add a second post-hit AoE or compensate Nova Burn in a bridge.

## Acquisition

Default Iron's spell eligibility; exact loot/crafting distribution: **NÃO VERIFICADO**.

## Source

`BinaryStarsSpell.java`, `BinaryStarEntity.java`, `NovaStarEntity.java`, `ObsidianStarEntity.java`, `NovaBurnEffect.java`, `EclipsedEffect.java` @ pin `5e4067e...`.