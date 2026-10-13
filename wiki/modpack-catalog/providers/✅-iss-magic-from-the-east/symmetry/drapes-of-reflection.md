# Drapes Of Reflection

**Registro físico confirmado (2026-10-13):** ✅ `COUNTED_EXACT` — `iss_magicfromtheeast:drapes_of_reflection` / `net.warphan.iss_magicfromtheeast.spells.symmetry.DrapesOfReflectionSpell`, school default `MFTESchoolRegistries.SYMMETRY_RESOURCE` ([prova Java 21 #38449995162](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449995162); [dossiê](../EXACT-BINARY-SPELLS-1.1.5.md)). Os números e comportamentos descritos abaixo continuam derivados da fonte pinada, não aprovados em runtime físico/Survival. **+0 identidade adicional**.

- **ID:** `iss_magicfromtheeast:drapes_of_reflection`
- **School:** Symmetry
- **Levels:** 1–6
- **Min rarity:** Rare
- **Cast:** Instant
- **Mana neutral:** 35–65
- **Spell power neutral:** 2–7
- **Cooldown:** 30 s
- **Barrier HP neutral:** `1+power` = 3–8
- **Reflection multiplier:** 20%–70%
- **Barrier lifetime:** 20 s
- **Placement range:** 3

## Contract

Creates `JadeDrapesEntity`, an `AbstractShieldEntity` composed of 77 shield parts (11×7) with summoner ownership.

`ProjectileImpactEvent` is the reflection authority. When a projectile hits a drape ShieldPart:

- event is canceled;
- projectile velocity is reversed;
- if it is `AbstractMagicProjectile`, owner is reassigned to the drape summoner and projectile damage becomes `oldDamage * reflectionPercent`;
- null-owner projectiles are assigned to the summoner before reverse;
- counterspell explicitly starts Jade Drapes unsummon/close behavior.

The shield itself takes damage and closes when HP/lifetime ends.

## Dedup / safety

Do not create a second projectile-reflection listener. Owner rewrite matters for kill/damage provenance; integrations must observe the reflected projectile state after provider handling.

## QA

`JadeDrapesEntity.idlePredicate` redundantly checks `isAnimatingClose()` twice. This is a presentation-only static quirk unless runtime demonstrates more impact.

## Source

`DrapesOfReflectionSpell.java`, `JadeDrapesEntity.java`, `MFTEServerEvent.drapeReflectionEvent`.
