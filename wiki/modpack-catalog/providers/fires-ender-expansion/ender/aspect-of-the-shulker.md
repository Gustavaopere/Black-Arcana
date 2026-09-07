# Aspect of the Shulker

- ID: `firesenderexpansion:aspect_of_the_shulker`
- School: `irons_spellbooks:ender`
- Levels: 1–5
- Min rarity: Uncommon
- Cast: Instant, self buff
- Mana neutral: 55 / 80 / 105 / 130 / 155
- Spell power neutral: 10 / 14 / 18 / 22 / 26
- Duration neutral: 150 / 210 / 270 / 330 / 390 ticks = 7.5 / 10.5 / 13.5 / 16.5 / 19.5 s
- Cooldown: 80 s
- Proc ICD default: 20 ticks

## Contract

Applies `aspect_of_the_shulker_effect`. While active, when the buffed living entity is the source of incoming `SpellDamageSource` damage against a victim, the provider spawns a `MagicShulkerBullet` homing on that victim if the per-caster internal cooldown is zero. The projectile subclasses vanilla `ShulkerBullet`; the audited 2.4.1 class does not add custom speed logic.

## Dedup / authority

This is a provider-native spell-hit proc. Do not separately spawn bullets from Black Arcana on the same damage event.

## Acquisition

Default Iron's spell eligibility; exact loot/crafting distribution: **NÃO VERIFICADO**.

## Source

`AspectOfTheShulkerSpell.java`, `AspectOfTheShulkerEffect.java`, `MagicShulkerBullet.java`, `Config.java` @ pin `5e4067e...`.