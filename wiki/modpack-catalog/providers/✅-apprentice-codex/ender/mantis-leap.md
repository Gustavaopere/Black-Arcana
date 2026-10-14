# Mantis Leap

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mantis_leap`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Long
- **Cooldown:** 8 s
- **Interruptible:** no
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 1200`
- `spellPowerPerLevel = 400`
- `baseManaCost = 70`
- `manaCostPerLevel = 15`
- `castTime = 25 ticks`
- damage before provider multiplier: `spellPower / 100`
- targeting/leap range: `min(32, spellPower / 100)` blocks
- leap arc height: `1.5`
- minimum leap duration: `10 ticks`
- target stop distance baseline: `1 block`

Leap timing per block:

`max(0.25, 2.5 - spellPower / 800)` ticks/block.

## Server/client movement contract

The server resolves the authoritative leap destination and stores start, target, duration, arc height and linked blade entity state. The client runs the same formula predictively to reduce correction jitter; the blade slash remains server-owned.

If a valid leap cannot start, the summoned blade slashes immediately. If the leap starts, the provider retains the weapon for the post-leap slash path.

The source explicitly preserves completion-time spell-power/Focus Staffbow modifiers in the weapon's damage state.

## What it does

The guide describes summoning magical blades and leaping toward the line-of-sight target, with a slash and no cast interruption. It is a movement+attack transaction, not two independent player casts.

## Causality

Leap movement and the associated blade strike share one Mantis Leap causal identity. Black Arcana/RPG must not reward one event for movement completion and another as if the slash were a separately initiated cast.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **uninterruptible targeted leap into a provider-owned summoned-blade attack** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT RANGE+DAMAGE+LEAP CURVE+SERVER AUTHORITY / COLLISION-ENDPOINT+CLIENT CORRECTION+PACK RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:mantis_leap` → `SpellRegistry.reg("mantis_leap", MantisLeap::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.mantisleap.MantisLeap`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/mantisleap/MantisLeap.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — ofensiva/movimento (2026-10-14)

**Source:** [`mantisleap/MantisLeap.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/mantisleap/MantisLeap.java) · [`mantisleap/MantisLeapMovementEvent.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/mantisleap/MantisLeapMovementEvent.java).

- **Estado e autoridade:** `startLeap` grava duração, origem, destino, `bladeEntityId` em `MANTIS_LEAP_STATE`; `onPlayerTick` calcula a trajetória no cliente e servidor; `finalizeLeap(...,!isClientSide)` só permite a lâmina atacar do lado autoritativo.
- **Watchdog/landing:** após **4 ticks** sem avanço mínimo, o movimento finaliza. `findSafeLandingPosition` testa offsets por `level.noCollision`, porém retorna o **destino original** se nenhum servir. `deactivate` restaura gravidade e zera estado; janela pós-salto de **20 ticks** cancela somente ataques de fonte `Mob` no `LivingIncomingDamageEvent`.
- **QA:** colisão, fall damage, client correction, PvP, restart e invulnerabilidade. `MantisLeapBladeEntity.slash` usa flag `slashed` para bloquear segundo corte. Movimento e dano têm uma causa.

🟡 Source-level causal; ⚠️ bytecode do JAR, config e QA modpack/Survival não certificados; ⛔ RPG perks/Mastery sem adapter homologado. Iron's e Apprentice's mantêm mana/casting/efeitos; Black Arcana não duplica runtime.
