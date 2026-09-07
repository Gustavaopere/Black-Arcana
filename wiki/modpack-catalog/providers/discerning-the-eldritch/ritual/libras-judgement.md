# Libra's Judgement

- **ID:** `discerning_the_eldritch:libras_judgement`
- **School:** Ritual
- **Level:** 1
- **Rarity:** Legendary
- **Cast:** Long, 20 ticks
- **Mana:** 100
- **Spell power neutral:** 35
- **Cooldown:** 45 s
- **Target range:** 32 blocks
- **Complexity:** complex, not super-complex

## Deterministic HP judgement

The spell branches by current target health percentage.

### Target at >=50% max HP

Spawns a `MourningStarProjectile` 10 blocks above target center and shoots downward.

Damage = `1.1*spellPower + weaponDamage` → neutral **38.5 + weaponDamage**.

### Target below 50% max HP

Applies `ACCURSED_EFFECT` for 15 s and creates circular `RitualBurnAoE`:

- duration: 100 ticks / 5 s;
- damage field: 1.5;
- radius: 3.

`AccursedPotionEffect` modifies:

- Spell Resist: **-15% ADD_MULTIPLIED_BASE**;
- Armor: **-5 ADD_VALUE**;
- Attack Damage: **-25% ADD_MULTIPLIED_BASE**.

## Authority / dedup

This is not random judgement: the 50% threshold deterministically selects execution mode. Do not run both branches or evaluate HP after the provider has already settled selection.

Damage source override uses iFrames 0; projectile/AoE hit cadence remains provider-native.

## Source

`LibrasJudgementSpell.java`, `AccursedPotionEffect.java`, DTE 1.4.4 branch.
