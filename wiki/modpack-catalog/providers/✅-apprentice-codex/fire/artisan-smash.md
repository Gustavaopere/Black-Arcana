# Artisan Smash

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:artisan_smash`
- **Iron's school:** Fire
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 900`
- `spellPowerPerLevel = 400`
- `baseManaCost = 40`
- `manaCostPerLevel = 20`
- `castTime = 30 ticks`
- projectile speed seeded by spell: **1.5**

Raw damage:

`spellPower / 100`

then multiplied by `DamageMultiplierKey.ARTISAN_SMASH`.

Splash radius:

`min(2 + spellPower / 600, 8)` blocks.

## What it does

The spell summons a magical grenade launcher, charges, and fires an explosive shell on successful cast completion. The launcher is released without firing if the cast is cancelled.

Provider guide semantics state that the shell blasts a wide area but **does not destroy terrain or item entities**, while still being capable of hitting the caster. That non-griefing explosive identity is provider-owned.

## Equipment interaction

The spell implements the provider's Magi Agent Suit affected-spell contract. The suit may change interruptibility/attack-spell handling. Those are Apprentice's Codex equipment semantics, not RPG Skill Tree perks and not Black Arcana casting authority.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **charged summoned grenade launcher / scalable Fire splash without terrain destruction** niche. Black Arcana should not recreate an equivalent explosive shell merely as a Chaos spell unless its mechanics and risk/world-safety identity are materially distinct.

## Confidence

`SOURCE-PINNED SPELL / SUMMONED LAUNCHER + SHELL SEMANTICS / PACK CONFIG MULTIPLIER + FULL RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Código da implementação:** [`ArtisanSmash.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/artisansmash/ArtisanSmash.java); classe `jp.aquafactory.apprenticecodex.spell.artisansmash.ArtisanSmash`.
- **Registro comprovado:** `SpellRegistry.reg("artisan_smash", ArtisanSmash::new)`; entrada distinta de escola, registry e documento.
- **Localização de parâmetros:** conservar as fórmulas, constantes, tempo, mana, configurações e advertências da seção `Exact source coefficients` desta própria ficha; conferir na classe qualquer setter de entidade/efeito, sem presumir que o campo possa ser alterado externamente.
- **Atributos/modificadores:** como addon do Iron's, `AbstractSpell` resolve spell power/custo e escola conforme seu contrato exato; parâmetros como raio, alvos e projéteis podem depender da classe acima ou de helpers/entidades *provider-owned*. Sua mutabilidade por perk está **CONDICIONADA** a evento/API/adapter validado na versão exata.
- **Causalidade e proteção:** associar progressão ao cast original; não premiar projétil, dano indireto, summon ou recast como outro cast automaticamente. Nenhum teste de alteração de runtime, Survival ou hook foi conduzido por esta ficha.
- **Proveniência:** fonte no commit 0.9.7.1 `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Metadados e localizadores factuais; nenhuma cópia de implementação ou asset upstream.
