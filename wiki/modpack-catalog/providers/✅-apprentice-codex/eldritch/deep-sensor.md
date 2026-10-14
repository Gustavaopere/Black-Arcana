# Deep Sensor

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:deep_sensor`
- **Iron's school:** Eldritch
- **Levels:** 1–3
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 100 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 60`
- `manaCostPerLevel = 20`
- `castTime = 0`
- fixed sensing range: **24 blocks**
- effect duration: `round(spellPower * 6)` ticks

## What it does

A successful cast applies the provider's `Sense Sensor` effect to the caster.

Provider guide semantics: while active, the player senses nearby vibrations through walls in a Sculk Sensor-like way and sees visual cues whose color communicates distance: red is nearer, blue is farther. The effect suppresses vibrations caused by the player's own movement, but does **not** suppress item use, block placement or block breaking.

This is a perception/sensing capability, not a generic wallhack contract. The provider owns which vibration events become cues and how they are rendered.

## Acquisition

Registered through Iron's spell registry. Exact scroll/loot acquisition remains in the provider-wide acquisition audit.

## Deduplication

Directly overlaps Black Arcana Divination. A Black Arcana vibration-sensing spell that merely highlights through walls would duplicate Deep Sensor unless it has materially different information semantics, costs/risks and targeting constraints.

## Confidence

`SOURCE-PINNED SPELL + PROVIDER GUIDE / EFFECT EVENT FILTERING + FULL CLIENT RENDER QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:deep_sensor` → `SpellRegistry.reg("deep_sensor", DeepSensor::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.deepsensor.DeepSensor`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/deepsensor/DeepSensor.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — fechamento das nove fichas (2026-10-14)

**Source:** [`deepsensor/DeepSensor.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/deepsensor/DeepSensor.java) · [`deepsensor/SenseSensorVibrationEvent.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/deepsensor/SenseSensorVibrationEvent.java).

- **Efeito e silêncio:** `DeepSensor.onCast` aplica `SENSE_SENSOR` por `round(spellPower*6)` ticks. `SenseSensorVibrationEvent.onVanillaGameEvent` cancela uma lista explícita de `VanillaGameEvent` (por exemplo STEP, SWIM, HIT_GROUND, ELYTRA_GLIDE, ENTITY_DAMAGE) originados por uma `LivingEntity` com o efeito, antes do dispatch dos ouvintes de vibração; não equivale a silenciar todos os game events.
- **Observações em memória:** um `SensorState` por `ServerPlayer` UUID mantém listener dinâmico com raio **24**; exclui vibrações próprias e mantém `DeepSensorObservationBuffer`: **40 ticks** de retenção, máximo **64** registros internos e **8** exibidos, dedup por UUID de fonte ou BlockPos. Packet `DeepSensorObservationsPacket` sincroniza ao caster quando a seleção visível muda.
- **Cleanup:** hooks de troca de dimensão, logout, morte e perda de efeito removem listener/buffer; `DeepSensorClientDisplay` limpa cache se level ou player muda e representa direções, não uma fonte de dano. QA: silêncio de sculk/Warden, memória sob vibrações densas, limites e desync entre clientes.

🟡 Dossiê causal source-level; ⚠️ equivalência bytecode/JAR/config, PvP/claims e QA Survival/dedicated pendentes; ⛔ sem adapter Mastery/perks real. Black Arcana não apropria casts, mana ou efeitos do provider.
