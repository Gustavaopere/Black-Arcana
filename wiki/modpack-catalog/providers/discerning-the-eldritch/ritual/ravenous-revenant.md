# Ravenous Revenant

- **ID:** `discerning_the_eldritch:ravenous_revenant`
- **School:** Ritual
- **Level:** 1
- **Rarity:** Legendary
- **Cast:** Long, 20 ticks
- **Mana:** 100
- **Spell power neutral:** 35
- **Cooldown:** 35 s
- **Radius:** 15 blocks
- **Duration neutral:** 35 s
- **Complexity:** complex, not super-complex

## Contract

Applies `PREY_POTION_EFFECT` to every nearby LivingEntity except caster in a 15-block inflated box and applies `PREDATOR_POTION_EFFECT` to the caster for `20*spellPower` ticks.

`PredatorPotionEffect` listens to `LivingDamageEvent.Pre`. When the **direct source entity is a LivingEntity with Predator**, it spawns `RavenousJawEntity` at the victim with damage **20**.

## Upstream static bug / intended Prey bonus

The next branch is:

`else if (attacker has Predator && victim has Prey)`

but it follows an `if (attacker has Predator)`. Therefore it is logically unreachable whenever Predator is true. It also creates the 25-damage jaw without `addFreshEntity`.

Consequently the source-confirmed effective first branch is Predator → jaw 20, while the intended Predator+Prey bonus of 25 is a **QA/fix blocker**, not a mechanic Black Arcana should assume works.

## Dedup

Do not implement a second jaw proc merely to compensate in this documentation branch. Any compat fix must be explicit, tested and coordinated with runtime work.

## Source

`RavenousRevenantSpell.java`, `PredatorPotionEffect.java`, `PreyPotionEffect.java`.
