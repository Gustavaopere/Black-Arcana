# Zealous Harbinger

- **ID:** `discerning_the_eldritch:zealous_harbinger`
- **School:** Ritual
- **Level:** 1
- **Rarity:** Legendary
- **Cast:** Long, 20 ticks
- **Mana:** 100
- **Spell power neutral:** 25
- **Cooldown:** 35 s
- **Target range:** 16 blocks
- **Damage each projectile:** `0.45*power + weaponDamage` = neutral `11.25 + weaponDamage`
- **Complexity:** complex, not super-complex

## Cast-source gate

No crafting/normal loot. `AbstractRitualSpell` rejects SPELLBOOK for complex non-super rituals; its super-complex SPELLBOOK/SWORD gate does not apply, so SWORD is not rejected by that base condition.

## Contract

With valid target data, loops 6 times creating `CataclysmBladeBigProjectile`, assigns damage, target homing and zero-iFrame spell damage behavior.

## Static source quirk

Inside each loop the projectile position is first assigned `z + i` and immediately overwritten by `z - i`. The apparent symmetric pair is not produced by these two calls. Runtime visuals should be tested before documentation claims bilateral spawning.

The projectile is still provider authority for homing/path/hit behavior.

## Source

`ZealousHarbingerSpell.java`, DTE 1.4.4 branch.
