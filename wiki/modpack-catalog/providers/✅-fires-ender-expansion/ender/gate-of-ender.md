# Gate of Ender

**✅ Identidade física exata 2026-10-13:** `firesenderexpansion:gate_of_ender` → `GateOfEnderSpell`, inscrito sem branch no JAR 2.4.1 SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`; [Java 21 #38434192044](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38434192044) SUCCESS, [dossiê](../EXACT-BINARY-SPELLS-2.4.1.md). Estado de registry `COUNTED_EXACT` **somente estático**; já contabilizado, **+0**. Mana/config/runtime de Iron's, teleport, domain e Survival ⚠️. Evidência anterior derivada de fonte abaixo mantém seu caráter histórico.


- ID: `firesenderexpansion:gate_of_ender`
- School: `irons_spellbooks:ender`
- Levels: 1
- Rarity: Legendary
- Cast: Continuous, 200 ticks (10 s)
- Mana: 15
- Neutral spell power: 15
- Neutral per-weapon damage: 7.5 normal/hail; targeted portal sets 3.75
- Neutral computed portal radius: ~3.78
- Neutral sword count per 5-tick emission: 2
- Cooldown: 60 s
- Normal crafting/looting: disabled
- `allow_sword_hail`: false by default

## Contract

Every 5 server cast ticks, the spell creates `GatePortal` entities. Each portal later chooses one unstable weapon type at random: Sword, Rapier or Claymore.

Modes:

- Targeted: when target cast data resolves, emits targeted portals; the audited neutral level creates one sword per emission at half normal damage.
- Normal: emits the computed sword count around the caster with full spell damage.
- Sword hail: when crouching and config-enabled, emits homing unstable weapons; disabled by default.

Unstable weapons are fire-immune projectiles. After their startup they move at speed 2, apply Gate of Ender spell damage to entities passing `canHitEntity`, and expire after 100 ticks. Homing mode uses an Iron's raycast predicate that rejects friendly-fire targets.

## Dedup / authority

Portal cadence, random weapon selection, homing/normal modes and projectile hit eligibility belong to the provider. Do not spawn a second sword wave.

## Acquisition

`allowCrafting=false` and `allowLooting=false`. Alternative progression source: **NÃO VERIFICADO**.

## Source

`GateOfEnderSpell.java`, `GatePortal.java`, `UnstableWeaponEntity.java`, concrete unstable weapon classes and `Config.java` @ pin `5e4067e...`.