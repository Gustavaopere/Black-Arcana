# Arcane Beam

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:arcane_beam`
- **Iron's school:** Ender
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 200`
- `spellPowerPerLevel = 100`
- `baseManaCost = 5`
- `manaCostPerLevel = 5`
- `castTime = 60 ticks`
- beam range: `32 blocks`
- beam width configured at spawn: `0.25`

Base beam damage before the provider config multiplier:

`1 + spellPower / 100`

Arcane Charge bonus percentage per stored charge tier is derived from:

`round((spellPower - 100) / 30) * (chargeAmplifier + 1)`

and multiplies the beam's base damage by `1 + bonus/100`.

## Cast lifecycle

On the first server cast tick, the provider creates an owner-linked `ArcaneBeamEntity`, positions it near the caster eye and stores its UUID in serializable cast data. During the continuous cast, the server moves/reorients the entity and recomputes beam length against the world.

When the cast completes or is cancelled, the beam entity is discarded and the caster's **Arcane Charge** effect is removed. The charge is therefore provider-owned transient state, not a Black Arcana resource.

## What it does

The guide describes a continuous piercing arcane beam whose damage is enhanced by circulated mana/Arcane Charge, bypasses armor and is ineffective against demonic beings. Exact target filtering and demon eligibility remain provider authority.

## Causality

Repeated beam damage callbacks belong to one continuous provider cast. A future progression/hazard observer must deduplicate by the cast/session rather than treating every beam tick as a new cast.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **continuous long-range Ender beam consuming a charge built by Arcane Blast** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT BEAM RANGE+DAMAGE+CHARGE CONSUMPTION / ENTITY COLLISION CADENCE + PACK MULTIPLIER + RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:arcane_beam` → `SpellRegistry.reg("arcane_beam", ArcaneBeam::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.arcanebeam.ArcaneBeam`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/arcanebeam/ArcaneBeam.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
