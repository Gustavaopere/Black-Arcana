# Sense Evil

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:sense_evil`
- **Iron's school:** Holy
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 10 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 50`
- `baseManaCost = 70`
- `manaCostPerLevel = 25`
- `castTime = 0`

Detection range:

`16 + 16 * spellPower / 100` blocks.

The scan volume is a cube centered on the caster bounding-box center, with half-extent equal to calculated range plus half caster height.

## Exact detection behavior

On a ServerPlayer cast, the provider takes a snapshot and sends only the resulting highlight records to that player.

Entity candidates:

- living and alive;
- not the caster;
- either configured by the provider's highlight manager or recognized by `UndeadTools.isUndead(...)`.

Spawner candidates:

- only `SpawnerBlockEntity` instances in the detection box;
- their current `SpawnData` and weighted `SpawnPotentials` are inspected for configured/undead entity types;
- configured variants take precedence over generic undead classification.

## Bounded performance contract

Spawner scanning iterates the chunk coordinates overlapping the detection box but calls `getChunkNow(...)`. **Unloaded chunks are skipped and never synchronously loaded by the spell.** Within loaded chunks it examines the existing block-entity map.

This is a useful design reference for Black Arcana Divination: bounded, cast-triggered snapshots are acceptable; global/per-tick world scans are not.

## What it does

Provider guide semantics: detects nearby unholy beings, highlights them even without line of sight, and can identify devices/spawners that create such entities.

## Authority/deduplication

This is a direct Divination overlap. Black Arcana must not run a second nearby-undead/spawner scan after observing Sense Evil. Any progression observer should use the original provider cast rather than count each highlighted target as a separate magical action.

## Confidence

`SOURCE-PINNED SPELL + ENTITY/SPAWNER SNAPSHOT / CLIENT HIGHLIGHT RENDER + DATAPACK VARIANT CONTENT QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:sense_evil` → `SpellRegistry.reg("sense_evil", SenseEvil::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.senseevil.SenseEvil`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/senseevil/SenseEvil.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
