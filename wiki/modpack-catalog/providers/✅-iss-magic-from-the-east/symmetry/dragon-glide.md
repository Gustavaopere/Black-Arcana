# Dragon Glide

- **ID:** `iss_magicfromtheeast:dragon_glide`
- **School:** Symmetry
- **Levels:** 1–10
- **Min rarity:** Common
- **Cast:** Long, 30 ticks
- **Mana neutral:** 34–70
- **Spell power/damage neutral:** 2–20
- **Cooldown:** 5 s
- **Projectile speed:** 0.6
- **Lifetime:** 80 ticks / 4 s

## Contract

Creates `JadeLoong`, a no-gravity magic projectile moving along the caster look vector. Custom hit detection permits it to damage multiple entities while travelling; entity hit does not discard it in the audited class. On each entity hit it applies provider spell damage and requests Iron's `ignoreNextKnockback` for LivingEntity targets.

## Public-vs-source boundary

Public description mentions a chance to break magic shields. That behavior was **not located** in `DragonGlideSpell` or `JadeLoong` during this pass. It remains `NÃO VERIFICADO` until a current event/entity handler proves it.

## Dedup

Identity = slow, persistent multi-hit jade dragon projectile, not a normal one-impact bolt. Do not duplicate path damage or force discard after first entity hit.

## Source

`DragonGlideSpell.java` + `JadeLoong.java`.
