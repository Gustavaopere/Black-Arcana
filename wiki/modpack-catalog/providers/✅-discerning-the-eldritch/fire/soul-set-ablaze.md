# Soul Set Ablaze

- **ID:** `discerning_the_eldritch:soul_set_ablaze`
- **School:** Fire
- **Level:** 1
- **Rarity:** Legendary
- **Cast:** Long, 60 ticks / 3 s base
- **Mana:** 150
- **Spell power neutral:** 40
- **Cooldown:** 210 s
- **AoE radius:** 12
- **Base damage:** `1.3*spellPower + weaponDamage` = neutral `52 + weaponDamage`
- **SpellDamageSource lifesteal:** 25%

## Acquisition gates

`canBeCraftedBy=false`, `allowCrafting=false`, `allowLooting=false`.

## Contract

Creates provider `SoulEruptionAoe` at ground-resolved point in front of caster.

If main-hand `SOUL_FIRE_STACKS >= 50`:

- AoE damage becomes **2×** the computed damage;
- exactly 50 stacks are consumed.

Otherwise the normal computed damage is used. SoulEruptionAoe owns hit cadence/effect settlement; tooltip references a Scorched Soul effect, but the exact entity-side application remains authority of that AoE and is not duplicated in this sheet.

## Dedup

This already fills the high-cost Soul Fire spender / large 12-radius eruption / 25% lifesteal signature. Black Arcana Infernal/Soul Fire content must compare against this before adding another stack-consuming ground nova.

## Source

`SoulSetAblazeSpell.java`, DTE 1.4.4 branch.
