# Graced Rain

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:graced_rain`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 15`
- `manaCostPerLevel = 5`
- `castTime = 400 ticks / 20 s`
- target range: **16 blocks**

Heal amount seeded into the cloud:

`2 * spellPower / 100`

The spell UI displays healing per second as `healAmount * 2`; exact cloud heal cadence is owned by `GracedRainCloudEntity`.

Effect radius:

`1 + floor(spellPower / 200)` blocks.

Growth interval:

`max(1, 5 - round(spellPower / 100))` ticks.

## Target/anchor modes

At cast start the spell can:

- attach the cloud to a valid living target;
- anchor it to a validated block target;
- otherwise anchor it around the resolved target position.

Block anchoring is validated before creating the cloud; invalid anchor geometry rejects placement rather than spawning an unmanaged effect.

## What it does

Provider guide semantics: summons a rain cloud with healing power; entities under it recover health and nearby vegetation is nourished/grown.

The cloud entity owns healing/growth cadence and release lifecycle. One cloud tick affecting many entities/plants remains child behavior of one provider cast.

## Provider modifier

The spell implements the provider's Craftsman's Delight affected-spell contract. Any bonus is provider-owned and must not be duplicated as an external process/healing modifier without a real bridge.

## Deduplication

Occupies the **anchored/following healing + plant-growth cloud** niche.

## Confidence

`SOURCE-PINNED SPELL + CLOUD CONFIG / EXACT HEAL-GROWTH ENTITY CADENCE + RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:graced_rain` → `SpellRegistry.reg("graced_rain", GracedRain::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.gracedrain.GracedRain`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/gracedrain/GracedRain.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — mundo, channel e defesa (2026-10-14)

**ID causal:** `apprenticecodex:graced_rain` — uma magia Iron's-native; ticks/jobs/entidades/impactos são efeitos-filhos, nunca um novo cast.

**Source pin:** [GracedRain.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/gracedrain/GracedRain.java); [GracedRainCloudEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/gracedrain/GracedRainCloudEntity.java).

**Cadeia verificada em source:** GracedRain coloca cloud seguindo entidade ou ancorada a bloco; GracedRainCloudEntity.tickOnServer descarta quando não resolve owner compatível, acompanha follow target e só chama tryGrowPlant se há anchorBlockPos e intervalo. applyFollowEffect a cada FOLLOW_EFFECT_INTERVAL_TICKS cura alvos normais e usa CombatTools.applyDamage para inverted-heal/harm; bônus de aging depende do equipamento Craftsman's Delight.

**QA prioritário (não executado):** Growth e claims/bonemeal de outros mods, múltiplas clouds, owner/target unload, workload da AABB e PvP.

**Boundary:** mana/casting Iron's e efeitos Apprentice's; nenhuma segunda liquidação/XP/Mastery por Black Arcana; contrato RPG sem hook comprovado: ⛔ fail-closed. ⚠️ Sem prova de bytecode do JAR instalado, config nem QA físico.
