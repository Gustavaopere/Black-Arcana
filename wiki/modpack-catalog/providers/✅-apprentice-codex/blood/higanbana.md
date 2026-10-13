# Higanbana

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:higanbana`
- **Iron's school:** Blood
- **Levels:** 1–5
- **Minimum rarity:** Common
- **Cast type:** Instant
- **Cooldown:** 4 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 40`
- `manaCostPerLevel = 20`
- `castTime = 0`
- fixed slash count: `4`
- first slash standby: `5 ticks`

The exact effective mana/power at a particular level is settled through Iron's `AbstractSpell` semantics. This page preserves the provider coefficients rather than independently reimplementing that formula.

## Damage

Exact Higanbana spell source computes per-slash raw damage as:

`1 + spellPower / 100`

then multiplies it by Apprentice's Codex server config `DamageMultiplierKey.HIGANBANA`.

The exact configured runtime multiplier in the user's pack remains runtime/config QA.

## What it does

The provider guide describes Higanbana as summoning a cursed magical blade in place and unleashing a flurry of strikes. The strikes cause no knockback and heal the caster for **50% of damage dealt**.

The exact spell source fixes the sequence at four slashes. The weapon entity owns the actual multi-hit execution after the spell seeds its damage/count state.

## Blood Brand interaction

The exact Blood Brand guide states that killing a branded target with Higanbana causes a **more powerful Blood Brand burst**. That proc belongs to Apprentice's Codex/Blood Brand causality; Black Arcana must not generate a second death burst from the same kill.

## Acquisition

This spell is registered as an Iron's spell and uses the normal Iron's spell/scroll ecosystem unless Apprentice's Codex data overrides acquisition. Exact 0.9.7.1 loot/recipe availability remains a separate acquisition audit item.

## Deduplication

Occupies a close-range Blood summoned-blade/multihit/lifesteal niche. Future Black Arcana Blood content must not reproduce the same four-hit stationary cursed-blade + lifesteal identity merely with different VFX.

## Confidence

`SOURCE-PINNED SPELL CONFIG + PROVIDER GUIDE / PACK CONFIG MULTIPLIER QA PENDING`

## Localizadores para Codex — source exato

- **Código da implementação:** [`Higanbana.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/higanbana/Higanbana.java); classe `jp.aquafactory.apprenticecodex.spell.higanbana.Higanbana`.
- **Registro comprovado:** `SpellRegistry.reg("higanbana", Higanbana::new)`; entrada distinta de escola, registry e documento.
- **Localização de parâmetros:** conservar as fórmulas, constantes, tempo, mana, configurações e advertências da seção `Exact source coefficients` desta própria ficha; conferir na classe qualquer setter de entidade/efeito, sem presumir que o campo possa ser alterado externamente.
- **Atributos/modificadores:** como addon do Iron's, `AbstractSpell` resolve spell power/custo e escola conforme seu contrato exato; parâmetros como raio, alvos e projéteis podem depender da classe acima ou de helpers/entidades *provider-owned*. Sua mutabilidade por perk está **CONDICIONADA** a evento/API/adapter validado na versão exata.
- **Causalidade e proteção:** associar progressão ao cast original; não premiar projétil, dano indireto, summon ou recast como outro cast automaticamente. Nenhum teste de alteração de runtime, Survival ou hook foi conduzido por esta ficha.
- **Proveniência:** fonte no commit 0.9.7.1 `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Metadados e localizadores factuais; nenhuma cópia de implementação ou asset upstream.
