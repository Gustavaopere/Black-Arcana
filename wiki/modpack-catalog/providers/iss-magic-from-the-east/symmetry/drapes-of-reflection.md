# Drapes Of Reflection

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
