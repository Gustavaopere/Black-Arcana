# Calamity Cut

- **ID:** `iss_magicfromtheeast:calamity_cut`
- **School:** Spirit
- **Levels:** 1–5
- **Min rarity:** Common
- **Cast:** Long, fixed 24 ticks; `canBeInterrupted=false`
- **Mana neutral:** 30–102
- **Spirit spell power neutral:** 4–20
- **Cooldown:** 25 s
- **Range:** `9 + 2×level` = 11–19 blocks
- **Damage:** `final Spirit spell power + Utils.getWeaponDamage(caster)`

## Contract

Executes a forward horizontal line cut sampled along the 11–19 block range. Each sampled segment queries a narrow vertical AABB and requires line of sight. Valid hits receive the combined Spirit-power + weapon-damage value through the provider spell damage source. Successful hits also invoke vanilla/NeoForge enchantment post-attack effects.

The spell explicitly cannot be interrupted and returns its unshortened configured cast time, with an upstream comment indicating this prevents spam/animation breaks.

## Dedup / authority

Identity = non-interruptible weapon-scaled Spirit line slash with enchantment post-hit integration. It is not equivalent to a generic spell-power projectile or ordinary melee hit.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`CalamityCutSpell.java`, source 1.1.5.
