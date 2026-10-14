# Spectral Wing

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:spectral_wing`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 2 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseManaCost = 150`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 0`

Initial launch constants:

- horizontal look-direction scale: **0.75**;
- minimum vertical launch speed: **1.05**;
- start grace: **10 ticks**.

Recast boost constants:

- forward boost speed: **2.75**;
- added upward speed: **0.22**;
- spin visual duration: **10 ticks**;
- visual wing-effect refresh: **20 ticks**.

## Preconditions

The exact spell rejects casting when:

- caster is not a player;
- an Elytra is equipped in the chest slot;
- Iron's Angel Wings effect is active;
- player is in water/bubble or swimming.

## What it does

First cast launches the player, starts fall-flying and activates provider-owned Spectral Wing state. Recasting while that spell-started state is active applies a strong look-direction boost instead of starting a second independent wing state.

Provider guide semantics state that the wings disappear when landing or touching water. The state/lifecycle is owned by Apprentice's Codex capability/event code.

## Authority and safety

This is not Black Arcana flight state. Black Arcana must not mirror velocity, cooldown or active-state bookkeeping in a second mobility controller. Any future stamina/progression observation must preserve the provider's single server-authoritative activation identity.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **launch → glide → recast directional surge** mobility niche. A Black Arcana movement spell should not clone this sequence merely with different wing particles.

## Confidence

`SOURCE-PINNED SPELL + STATE ENTRY CONSTANTS / STATE-EXIT EVENT + FULL CLIENT/MODPACK FLIGHT QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:spectral_wing` → `SpellRegistry.reg("spectral_wing", SpectralWing::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.spectralwing.SpectralWing`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/spectralwing/SpectralWing.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — utilidades, persistência e recursos (2026-10-14)

**Registry:** `apprenticecodex:spectral_wing`. **Proveniência source:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1); classes e helpers: [SpectralWing.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/spectralwing/SpectralWing.java); [SpectralWingFlightEvent.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/spectralwing/SpectralWingFlightEvent.java).

**Cadeia causal no código-fonte:** SpectralWing.checkPreCastConditions exige Player sem conflito de wings nem contato inicial com água. onCast ativa estado SPECTRAL_WING_STATE e dá impulso/fallFlying, ou reaplica boost e launchGrace no recast. SpectralWingFlightEvent.onPlayerTick (server Pre) mantém visual/fallDistance, inicia fallFlying quando válido e desativa por água após WATER_DEACTIVATE_GRACE_TICKS=4, pouso após grace, montaria/escada/voo incompatível; remove efeito e reseta estado quando termina.

**QA prioritário pendente:** Concorrência de elytra/voo/mods de gravidade, deactivation/morte/relogin e restauro de fallFlying, dimensão, sincronização de estado e PvP.

**Governança:** o host Iron's controla cast/mana/recast; o addon controla o estado/efeito/custo especializado verificado. Um pulso, dano periódico, bloco, item gerado, job tick, cast visual ou cast derivado não é uma identidade semântica nova nem gatilho de Mastery/XP automático. Black Arcana não reprocessa recursos, eventos, mutação do mundo ou callback dos providers. ⚠️ Source-level não comprova bytecode idêntico/config efetiva/teste físico. ⛔ Nenhum contrato de RPG Skill Tree perks/Mastery homologado: fail-closed.
