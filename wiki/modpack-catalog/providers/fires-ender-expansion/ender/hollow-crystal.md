# Hollow Crystal

- ID: `firesenderexpansion:hollow_crystal`
- School: `irons_spellbooks:ender`
- Levels: 1–5
- Min rarity: Legendary
- Cast: Long; effective cast time 30 ticks (1.5 s)
- Mana neutral: 55 / 80 / 105 / 130 / 155
- Spell power neutral: 20 / 25 / 30 / 35 / 40
- Recast/charge count: spell level (1–5)
- Charge window: 400 ticks (20 s)
- Full-charge tooltip damage neutral: 6 / 15 / 27 / 42 / 60
- Cooldown: 30 s

## Contract

The first cast opens an Iron's `RecastInstance` and builds `hollow_crystal_effect` charges. Final firing creates a `HollowCrystal` entity after camera-lock/animation handling. The crystal launches after a 20-tick delay, can interact with projectiles and eventually resolves a 15-block living-entity damage sweep. Victims are tracked to avoid repeated full damage; the owner has a distinct half-damage path.

Crouching with the `Crystal Heart` Curio can force `handleFiring` before the normal recast lifecycle finishes. The entity is `AntiMagicSusceptible`; break/anti-magic paths move it into a 60-tick terminal countdown.

With defaults, Hollow Crystal may destroy nearby projectiles that are not in Iron's `CANT_PARRY` tag. If a Stabilized Core of Ender and End Stone are together near the active crystal and `crystal_heart_obtainable=true`, the provider can create a Crystal Heart in-world.

## Dedup / authority

Recast count, charge amplifier, projectile destruction, victim ledger, terminal AoE and Crystal Heart conversion are provider-owned. No parallel charge ledger or extra detonation damage.

## Acquisition

Spell class uses normal Iron's eligibility; exact scroll source: **NÃO VERIFICADO**. Crystal Heart is an interaction item, not the spell's primary acquisition route.

## Source

`HollowCrystalSpell.java`, `HollowCrystal.java`, `HollowCrystalEffect.java`, `Config.java` @ pin `5e4067e...`.