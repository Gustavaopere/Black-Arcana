# Displacement Cage

- ID: `firesenderexpansion:displacement_cage`
- School: `irons_spellbooks:ender`
- Levels: 1–10
- Min rarity: Common
- Cast: Long, 20 ticks (1 s)
- Mana neutral: 40 / 50 / 60 / 70 / 80 / 90 / 100 / 110 / 120 / 130
- Spell power neutral: 10 / 13 / 16 / 19 / 22 / 25 / 28 / 31 / 34 / 37
- Radius: 6
- Duration neutral: 35 / 49 / 63 / 77 / 91 / 105 / 119 / 133 / 147 / 161 ticks = 1.75–8.05 s
- Target acquisition: target or raycast up to 32 blocks
- Cooldown: 40 s

## Contract

Creates `TeleportAoe` + visual target area. The AoE tracks eligible living entities that enter the radius, excluding owner, friendly-fire relations and creative/spectator players. When a tracked target crosses beyond radius 6, the provider computes an interior destination and calls Iron's canonical `Utils.handleSpellTeleport(DISPLACEMENT_CAGE, target, destination)`.

The provider also listens for external `EntityTeleportEvent` near cages and removes the teleported entity from cage tracking, so the cage itself is not implemented as a universal teleport cancel. `displacement_cage_immune` is part of the provider's eligibility path. Anti-magic clears the tracked ledger and discards the AoE.

## Dedup / authority

This is boundary enforcement through the Iron's teleport pipeline, not movement-root. Do not add velocity clamps or a second teleport-back handler.

## Acquisition

Default Iron's spell eligibility; exact loot/crafting distribution: **NÃO VERIFICADO**.

## Source

`DisplacementCageSpell.java`, `TeleportAoe.java` and provider tags @ pin `5e4067e...`.