# Dimensional Adaptation

**✅ Identidade física exata 2026-10-13:** `firesenderexpansion:dimensional_adaptation` → `DimensionalAdaptationSpell`, inscrito sem branch no JAR 2.4.1 SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`; [Java 21 #38434192044](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38434192044) SUCCESS, [dossiê](../EXACT-BINARY-SPELLS-2.4.1.md). Estado de registry `COUNTED_EXACT` **somente estático**; já contabilizado, **+0**. Mana/config/runtime de Iron's, teleport, domain e Survival ⚠️. Evidência anterior derivada de fonte abaixo mantém seu caráter histórico.


- ID: `firesenderexpansion:dimensional_adaptation`
- School: `irons_spellbooks:ender`
- Levels: 1–6
- Min rarity: Rare
- Cast: Instant, self buff
- Mana neutral: 55 / 80 / 105 / 130 / 155 / 180
- Spell power neutral: 10 / 12 / 14 / 16 / 18 / 20
- Duration multiplier neutral: 1.0× / 1.2× / 1.4× / 1.6× / 1.8× / 2.0×
- Cooldown: 60 s

## Contract

Data-driven dimension adaptation. The provider looks up the caster's dimension in `adaptable_dimensions.json`; if no entry exists, the cast completes without a buff and emits a cannot-adapt message/sound.

Built-in 2.4.1 mappings:

- Overworld → Night Vision, 400 ticks base;
- Nether → Fire Resistance, 400 ticks base;
- The End → Slow Falling, 200 ticks base;
- Iron's pocket dimension → Saturation, 2 ticks base.

All use amplifier 0. Final duration is `baseDuration × spellPower/10`.

## Acquisition

`canBeCraftedBy` requires the player to possess the provider's `Endchiridion` either in inventory or as a Curio. Other acquisition channels/loot: **NÃO VERIFICADO**.

## Dedup / authority

Do not recreate dimension detection or apply a second adaptation buff. The JSON mapping and provider class are authoritative.

## Source

`DimensionalAdaptationSpell.java`, `EffectDimensionMatcher.java`, `data/firesenderexpansion/adaptable_dimensions.json` @ pin `5e4067e...`.