# Combustion Jet

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:combustion_jet`
- **Iron's school:** Fire
- **Levels:** 1–5
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 200`
- `baseManaCost = 30`
- `manaCostPerLevel = 10`
- `castTime = 0`
- fixed range: **10 blocks**

Raw damage:

`1 + spellPower / 100`

then multiplied by `DamageMultiplierKey.COMBUSTION_JET`.

Burn duration:

`max((spellLevel - 1) * 40, 10)` ticks.

## Exact heat-wave geometry/lifecycle

The exact wave entity establishes:

- travel speed: **2.25 blocks/tick**;
- wave width: **9 blocks**;
- wave height: **1 block**;
- wave depth: **1.5 blocks**;
- explicit horizontal knockback strength: **1.0**;
- fixed maximum travel distance seeded as 10 blocks by the spell;
- each target UUID is affected at most once by a wave instance;
- block collision is evaluated through a narrow central collision volume so the wide visual/damage wave is not trivially erased by side geometry;
- anti-magic susceptibility is provider-owned.

The damage call itself uses no automatic knockback, after which the wave applies its own directional knockback. This is one provider-owned settlement and must not be double-processed.

## What it does

Provider guide semantics: emits a broad heat wave in the view direction. Fire-resistant targets cannot receive the intended heat damage according to provider semantics, but the spell still attempts to push targets back. Successfully affected living targets receive the configured burn duration.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot/recipe availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **broad Fire force-wave / burn / directional knockback** niche. This is especially relevant to Chaos design: a generic red force blast is not distinct merely because Black Arcana calls it Chaos.

## Confidence

`SOURCE-PINNED SPELL + WAVE ENTITY / PACK CONFIG MULTIPLIER + FIRE-IMMUNITY RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Código da implementação:** [`CombustionJet.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/combustionjet/CombustionJet.java); classe `jp.aquafactory.apprenticecodex.spell.combustionjet.CombustionJet`.
- **Registro comprovado:** `SpellRegistry.reg("combustion_jet", CombustionJet::new)`; entrada distinta de escola, registry e documento.
- **Localização de parâmetros:** conservar as fórmulas, constantes, tempo, mana, configurações e advertências da seção `Exact source coefficients` desta própria ficha; conferir na classe qualquer setter de entidade/efeito, sem presumir que o campo possa ser alterado externamente.
- **Atributos/modificadores:** como addon do Iron's, `AbstractSpell` resolve spell power/custo e escola conforme seu contrato exato; parâmetros como raio, alvos e projéteis podem depender da classe acima ou de helpers/entidades *provider-owned*. Sua mutabilidade por perk está **CONDICIONADA** a evento/API/adapter validado na versão exata.
- **Causalidade e proteção:** associar progressão ao cast original; não premiar projétil, dano indireto, summon ou recast como outro cast automaticamente. Nenhum teste de alteração de runtime, Survival ou hook foi conduzido por esta ficha.
- **Proveniência:** fonte no commit 0.9.7.1 `305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`. Metadados e localizadores factuais; nenhuma cópia de implementação ou asset upstream.

## Engenharia causal aprofundada — utilidades, persistência e recursos (2026-10-14)

**Registry:** `apprenticecodex:combustion_jet`. **Proveniência source:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1); classes e helpers: [CombustionJet.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/combustionjet/CombustionJet.java); [CombustionJetWaveEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/combustionjet/CombustionJetWaveEntity.java).

**Cadeia causal no código-fonte:** CombustionJet.onCast cria CombustionJetWaveEntity com origem/owner, direção, dano, burnDuration e maxTravelDistance. CombustionJetWaveEntity.tick limita deslocamento ao range, verifica colisão de bloco, aplica danos apenas ao segmento percorrido, descarta em colisão/limite; affectEntities resolve multipart e usa victimUuids para um único hit por entidade na mesma onda. affectEntity também aplica knockback/fire conforme o fluxo próprio da wave, sem segunda mana.

**QA prioritário pendente:** Perfuração/oclusão e claims, marcação de vítima no reload de projétil, fogo/knockback quando dano é negado, anti-magic, ownership e velocidade sob sobrecarga.

**Governança:** o host Iron's controla cast/mana/recast; o addon controla o estado/efeito/custo especializado verificado. Um pulso, dano periódico, bloco, item gerado, job tick, cast visual ou cast derivado não é uma identidade semântica nova nem gatilho de Mastery/XP automático. Black Arcana não reprocessa recursos, eventos, mutação do mundo ou callback dos providers. ⚠️ Source-level não comprova bytecode idêntico/config efetiva/teste físico. ⛔ Nenhum contrato de RPG Skill Tree perks/Mastery homologado: fail-closed.
