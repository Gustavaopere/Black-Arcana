# Obsidian Rod

- ID: `firesenderexpansion:obsidian_rod`
- School: `irons_spellbooks:ender`
- Levels: 1–5
- Min rarity: Uncommon
- Cast: Continuous
- Mana neutral: 5 / 6 / 7 / 8 / 9
- Spell power neutral: 30 / 38 / 46 / 54 / 62
- Channel time neutral: 65 / 70 / 75 / 80 / 85 ticks
- Rod cadence: every 5 server cast ticks
- Direct damage per rod neutral: 0.30 / 0.38 / 0.46 / 0.54 / 0.62
- Anchored duration neutral: 60 / 76 / 92 / 108 / 124 ticks = 3.0–6.2 s
- Cooldown: 60 s

## Contract

Channels repeated `ObsidianRod` projectiles. A successful living-entity hit applies provider spell damage and `anchored_effect`. Anchored is enforced outside the empty MobEffect class through provider events/mixins: ordinary entity teleports are canceled (TeleportCommand excluded), with additional portal/evasion interception present in the 2.4.1 source tree.

On Ancient Debris impact, with default `fragments_obtainable=true`, the provider destroys the block and spawns one Infused Obsidian Fragment.

## Dedup / authority

The anti-teleport state and Ancient Debris conversion are provider-owned. Do not add a second teleport cancellation listener or duplicate fragment drop.

## Acquisition

Default Iron's spell eligibility; exact scroll/crafting weights: **NÃO VERIFICADO**.

## Source

`ObsidianRodSpell.java`, `ObsidianRod.java`, `AnchoredEffect.java`, `ServerEvents.java`, Anchored mixins and `Config.java` @ pin `5e4067e...`.