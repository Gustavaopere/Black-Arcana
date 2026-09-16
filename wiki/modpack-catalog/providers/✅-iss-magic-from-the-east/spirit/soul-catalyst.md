# Soul Catalyst

- **ID:** `iss_magicfromtheeast:soul_catalyst`
- **School:** Spirit
- **Levels:** 1–8
- **Min rarity:** Common
- **Cast:** Long, 20 ticks
- **Mana neutral:** 35–70
- **Spell power neutral:** 2–9
- **Cooldown:** 60 s
- **Projectile count:** `2 + floor(level/2)` = 2–6
- **Damage per skull:** `0.5 × final Spirit spell power`

## Contract

Spawns 2–6 `SoulSkullProjectile` instances with slight inaccuracy. Each skull travels without gravity at speed 1.75, deals its stored Spirit damage on entity hit, applies `Soulburn` for 80 ticks (4 s), clears the target's current `invulnerableTime`, then discards. Block impact discards without an AoE.

`Soulburn` is provider-native health-scaling `SOUL_DAMAGE`, not vanilla fire damage. At default server config it attempts 5% of target max HP per amplifier-0 pulse, clamped to minimum 1 and maximum 10 damage, with an immunity tag.

## Dedup / authority

Identity = multi-skull volley whose per-projectile direct hit seeds provider-native Soulburn and explicitly manipulates iFrames. Projectile collision and Soulburn cadence belong to provider entities/effects; do not duplicate either in a bridge.

## QA

`SoulCatalystSpell.onCast` calls `super.onCast(...)` inside the projectile loop, therefore 2–6 times per cast. Whether the Iron's base implementation gives that repeated call any observable side effect requires runtime QA.

## Acquisition

`NÃO VERIFICADO` in this source pass.

## Source

`SoulCatalystSpell.java` + `SoulSkullProjectile.java` + `SoulburnEffect.java`, source 1.1.5 pin `13208302...`.
