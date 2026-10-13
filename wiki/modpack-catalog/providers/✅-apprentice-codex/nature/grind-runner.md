# Grind Runner

- **Provider:** Apprentice's Codex
- **Registry ID:** `apprenticecodex:grind_runner`
- **School:** Nature
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 20 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 20`
- `manaCostPerLevel = 5`
- `castTime = 100 ticks / 5 s`
- summon targeting range: **8 blocks**
- ground search below candidate: **4 blocks**
- summon drop height: **4 blocks** over **5 ticks**.

Raw combat damage:

`2 * spellPower / 100`

then multiplied by `DamageMultiplierKey.GRIND_RUNNER`.

Item processing rate:

`8 * spellPower / 100 items/s`, then optional Craftsman's Delight process-speed modifier.

Launch speed:

`0.9 + 0.05 * spellPower / 100`.

## Placement and release

The wheel cannot be summoned without valid ground. Candidate position is derived from target entity hit, block face or maximum look range, then the provider raycasts downward and requires a real collision surface.

On cast completion/cancellation, launch sustain time is derived from actual elapsed channel time:

`min(30, elapsedCastTicks / 2)`.

The wheel entity then owns travel, damage and item-processing behavior.

## Create compatibility

Provider guide semantics state that when Create is present, supported item grinding is handled as if processed by Crushing Wheels or a Millstone. That is a provider-native optional compatibility seam and must not be replaced with a second Black Arcana/Create processing pipeline.

## What it does

Summons an arcane wheel to grind entities and supported items, then releases it forward. The launched wheel can also hit the caster according to provider guide semantics.

## Deduplication

Occupies the **summoned grinder / item processing / released damaging wheel** niche.

## Confidence

`SOURCE-PINNED SPELL + SUMMON/GROUND/LAUNCH PARAMETERS / WHEEL PROCESSING + EXACT CREATE RECIPE BRIDGE QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:grind_runner` → `SpellRegistry.reg("grind_runner", GrindRunner::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.grindrunner.GrindRunner`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/grindrunner/GrindRunner.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
