# Quick Arms

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:quick_arms`
- **Iron's school:** Lightning
- **Levels:** 1–5
- **Minimum rarity:** Common
- **Cast type:** Instant + recast weapon lifecycle
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 20`
- `baseManaCost = 75`
- `manaCostPerLevel = 20`
- `castTime = 0`
- summoned/recast lifetime: **60 ticks / 3 s**
- range: **24 blocks**
- initial firing standby: **20 ticks**

Raw shot damage:

`4 * spellPower / 100`

then multiplied by `DamageMultiplierKey.QUICK_ARMS`.

Maximum activation count:

`min(16, 2 + round(4 * spellPower / 100))`

## Recast lifecycle

The initial cast summons a handgun and seeds range/standby/damage. Recasts are rejected until the weapon reports that it can fire, and a recast cannot proceed if the weapon entity has disappeared.

At every valid shot, damage is recalculated from the caster's current spell power before the provider entity fires. The source explicitly does this so temporary Focus Staffbow recast power is reflected correctly.

## What it does

Provider guide semantics: summons a magical handgun and allows rapid repeated shots for a short period.

All repeated handgun shots belong to the same provider recast lifecycle. They are not new Black Arcana cast intents.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **short-duration magical handgun / rapid bounded recast** niche. Black Arcana should not add an equivalent conjured sidearm unless its domain and lifecycle are materially different.

## Confidence

`SOURCE-PINNED SPELL + RECAST WEAPON / PACK CONFIG MULTIPLIER + ENTITY SHOT QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:quick_arms` → `SpellRegistry.reg("quick_arms", QuickArms::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.quickarms.QuickArms`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/quickarms/QuickArms.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
