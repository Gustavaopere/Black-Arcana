# Thermal Process

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:thermal_process`
- **Iron's school:** Fire
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 150`
- `baseManaCost = 10`
- `manaCostPerLevel = 5`
- `castTime = 200 ticks`
- fixed range: **12 blocks**

Raw damage formula:

`0.5 + 1.5 * spellPower / 100`

then multiplied by `DamageMultiplierKey.THERMAL_PROCESS`.

Base item-processing speed:

`2 * spellPower / 100 items/second`

When the provider's Craftsman's Delight bonus is enabled/equipped, that provider item may further modify process speed and casting mobility. Black Arcana must not reapply those bonuses.

## What it does

The provider guide describes a summoned magical flamethrower that continuously sears targets along the caster's line of sight. Sustained heat applies an intense-heat behavior and can process smeltable items. The guide explicitly states that the spell does not ignite unrelated terrain/entities around the beam.

The summoned thrower entity owns the continuous execution. The spell seeds level, damage, range and processing speed into that entity, then releases it when casting completes/cancels.

## Compatibility surface

The spell is explicitly marked as affected by:

- Apprentice's Codex **Craftsman's Delight**;
- Apprentice's Codex **Magi Agent Suit** behavior.

Those are provider-internal modifiers. They are not RPG Skill Tree perks and must not be double-counted by Black Arcana mastery/attribute hooks without a real integration contract.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **continuous Fire damage + smelting/processing utility** niche. A Black Arcana spell that simply acts as a magical furnace/flamethrower would duplicate provider functionality unless its domain, resource, risk and world-effect contract are materially different.

## Confidence

`SOURCE-PINNED SPELL / SUMMONED THROWER + OPTIONAL ITEM MODIFIERS EXIST / PACK CONFIG MULTIPLIER + RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Código da implementação:** [`ThermalProcess.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/thermalprocess/ThermalProcess.java); classe `jp.aquafactory.apprenticecodex.spell.thermalprocess.ThermalProcess`.
- **Registro comprovado:** `SpellRegistry.reg("thermal_process", ThermalProcess::new)`; entrada distinta de escola, registry e documento.
- **Localização de parâmetros:** conservar as fórmulas, constantes, tempo, mana, configurações e advertências da seção `Exact source coefficients` desta própria ficha; conferir na classe qualquer setter de entidade/efeito, sem presumir que o campo possa ser alterado externamente.
- **Atributos/modificadores:** como addon do Iron's, `AbstractSpell` resolve spell power/custo e escola conforme seu contrato exato; parâmetros como raio, alvos e projéteis podem depender da classe acima ou de helpers/entidades *provider-owned*. Sua mutabilidade por perk está **CONDICIONADA** a evento/API/adapter validado na versão exata.
- **Causalidade e proteção:** associar progressão ao cast original; não premiar projétil, dano indireto, summon ou recast como outro cast automaticamente. Nenhum teste de alteração de runtime, Survival ou hook foi conduzido por esta ficha.
- **Proveniência:** fonte no commit 0.9.7.1 `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Metadados e localizadores factuais; nenhuma cópia de implementação ou asset upstream.
