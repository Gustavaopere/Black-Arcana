# Arcane Blast

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:arcane_blast`
- **Iron's school:** Ender
- **Levels:** 1–10
- **Minimum rarity:** Common
- **Cast type:** Long
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 40`
- `spellPowerPerLevel = 5`
- `baseManaCost = 20`
- `manaCostPerLevel = 4`
- `castTime = 30 ticks`

Raw damage before the provider config multiplier:

`spellPower / 10`

Effective range:

`16 + 4 * spellPower / 10` blocks.

Both damage and range therefore respond to actual Ender spell power, not only nominal spell level.

## Provider behavior

The server raycasts from the caster eye using a narrow `0.1` width and accepts only provider-valid combat targets. A successful hit uses Apprentice's Codex `ARCANE_BLAST` damage and then applies/increments **Arcane Charge** on the caster for `200 ticks`.

Arcane Charge amplifier is capped by this cast path at `2`, producing up to three charge tiers (`0..2`). The effect is provider state later consumed by Arcane Beam.

The public guide describes the spell as an internal arcane explosion/beam-like strike that accelerates mana circulation, bypasses armor and is ineffective against the provider's demonic targets. Exact demon-tag membership remains provider data/runtime authority.

## Causality

One successful Arcane Blast is one provider hit plus one Arcane Charge state mutation. Black Arcana must not count the charge application as a second offensive cast/proc identity.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 survival scroll/loot/crafting availability remains part of the provider-wide acquisition audit.

## Deduplication

Occupies the **fast direct Ender/arcane hit that builds a short-lived charge resource for another spell** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT DAMAGE+RANGE+CHARGE PATH / PACK CONFIG MULTIPLIER + DEMON ELIGIBILITY + RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:arcane_blast` → `SpellRegistry.reg("arcane_blast", ArcaneBlast::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.arcaneblast.ArcaneBlast`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/arcaneblast/ArcaneBlast.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia de perks — cadeia causal exata

- **`ArcaneBlast`** implementa `ICastHighlightSpell` com raycast `RAYCAST_WIDTH=0.1`, filtro `CombatTools.isValidCombatTarget`, e `getRange = 16+4*getSpellPower(level,caster)/10`.
- **Dano:** `getDamage=(getSpellPower/10)*DamageMultiplierKey.ARCANE_BLAST`, aplicado por `CombatTools.applyDamage` com `DamageTypes.ARCANE_BLAST`. Não prosseguir com charge se o hit não for aceito.
- **Carga ao acertar:** `ARCANE_CHARGE` é criado com duração `200` ticks, amplificador `0`, ou aumentado para `min(amplifier+1,2)` se já ativo.
- **Perks:** power altera dano **e alcance simultaneamente**; stack de carga tem cap próprio 2, e o consumo posterior pelo Arcane Beam é outra fase do mesmo provider. Não tratar charge como novo cast.

**Confiança:** source auditado do commit fixado 0.9.7.1; hooks externos de mutação e teste em Survival permanecem pendentes.
