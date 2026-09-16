# Soul Slice

- **ID:** `discerning_the_eldritch:soul_slice`
- **School:** Fire
- **Level:** 1
- **Rarity:** Legendary
- **Cast:** Long, 10 ticks base; effective cast time forced to base value
- **Interruptible:** no
- **Mana:** 75
- **Spell power neutral:** 35
- **Cooldown:** 25 s
- **Base damage:** `spellPower + weaponDamage`
- **SpellDamageSource lifesteal:** 10%

## Acquisition gates

`canBeCraftedBy=false`, `allowCrafting=false`, `allowLooting=false`. Concrete granting route remains `NÃO VERIFICADO`.

## Contract

Performs a forward melee-like scan centered ~1.9 blocks ahead with radius 3.25, requiring LivingEntity, forward-facing geometry and line of sight.

Normal hit:

`damage = getSpellPower + weaponDamage`.

If the main-hand item contains at least **2 `SOUL_FIRE_STACKS`**:

- damage receives `+2`;
- 2 stacks are consumed after successful damage.

Successful hits call Prometheus `FireManager.setOnFire(target, 10, SOUL_FIRE_TYPE)` and trigger post-attack enchantment effects. The spell's Iron's `SpellDamageSource` itself uses fireTicks 0 and lifesteal 10%, so Soul Fire application is a separate provider pipeline.

## Dedup / authority

Do not duplicate the forward scan, stack spend, Soul Fire application, lifesteal or post-attack enchant callbacks. The soul-stack item component is the authoritative resource, not a parallel Black Arcana counter.

## Source

`SoulSliceSpell.java`, DTE 1.4.4 branch.
