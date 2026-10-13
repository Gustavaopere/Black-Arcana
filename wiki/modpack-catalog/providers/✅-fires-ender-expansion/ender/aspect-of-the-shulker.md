# Aspect of the Shulker

**✅ Identidade física exata 2026-10-13:** `firesenderexpansion:aspect_of_the_shulker` → `AspectOfTheShulkerSpell`, inscrito sem branch no JAR 2.4.1 SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`; [Java 21 #38434192044](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38434192044) SUCCESS, [dossiê](../EXACT-BINARY-SPELLS-2.4.1.md). Estado de registry `COUNTED_EXACT` **somente estático**; já contabilizado, **+0**. Mana/config/runtime de Iron's, teleport, domain e Survival ⚠️. Evidência anterior derivada de fonte abaixo mantém seu caráter histórico.


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