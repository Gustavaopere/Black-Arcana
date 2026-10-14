# Magic Spear

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:magic_spear`
- **Iron's school:** Fire
- **Levels:** 1–5
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 0.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 600`
- `spellPowerPerLevel = 300`
- `baseManaCost = 30`
- `manaCostPerLevel = 30`
- `castTime = 0`
- assisted-aim/lock-on range: **64 blocks**

Raw impact/blast damage is `spellPower / 100`, then multiplied by `DamageMultiplierKey.MAGIC_SPEAR`.

## Missile lifecycle

The exact missile entity establishes:

- release phase: **5 ticks**;
- boost speed: **2.2 blocks/tick**;
- homing turn cap: **5 degrees/tick**;
- maximum life before burst/discard: **120 ticks**;
- impact blast radius: **1.5 blocks**;
- burst visual phase: **14 ticks**;
- anti-magic susceptibility: Counterspell/anti-magic converts it to a visual burst without applying blast damage.

The spell alternates launch side on successive casts and can acquire a provider-valid target within the assisted-aim range. Homing only continues while that target remains valid and in the same level.

## What it does

The provider guide describes a magical spear/missile launched toward the target in line of sight. It homes toward that target and bursts on impact, damaging nearby valid combat targets.

The blast uses provider combat-target filtering and normal knockback semantics. It does not become a Black Arcana projectile or proc source merely because a future integration observes the hit.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **rapid Fire homing missile + compact AoE burst** niche. Black Arcana Chaos/Fire should not duplicate this with a differently colored tracking projectile.

## Confidence

`SOURCE-PINNED SPELL + MISSILE ENTITY / PACK CONFIG MULTIPLIER + FULL RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Código da implementação:** [`MagicSpear.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/magicspear/MagicSpear.java); classe `jp.aquafactory.apprenticecodex.spell.magicspear.MagicSpear`.
- **Registro comprovado:** `SpellRegistry.reg("magic_spear", MagicSpear::new)`; entrada distinta de escola, registry e documento.
- **Localização de parâmetros:** conservar as fórmulas, constantes, tempo, mana, configurações e advertências da seção `Exact source coefficients` desta própria ficha; conferir na classe qualquer setter de entidade/efeito, sem presumir que o campo possa ser alterado externamente.
- **Atributos/modificadores:** como addon do Iron's, `AbstractSpell` resolve spell power/custo e escola conforme seu contrato exato; parâmetros como raio, alvos e projéteis podem depender da classe acima ou de helpers/entidades *provider-owned*. Sua mutabilidade por perk está **CONDICIONADA** a evento/API/adapter validado na versão exata.
- **Causalidade e proteção:** associar progressão ao cast original; não premiar projétil, dano indireto, summon ou recast como outro cast automaticamente. Nenhum teste de alteração de runtime, Survival ou hook foi conduzido por esta ficha.
- **Proveniência:** fonte no commit 0.9.7.1 `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Metadados e localizadores factuais; nenhuma cópia de implementação ou asset upstream.
