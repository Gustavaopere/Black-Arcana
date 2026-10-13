# Mana Transcription

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mana_transcription`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Long
- **Cooldown:** 4 s
- **Resource:** Iron's mana + provider-required player XP/operation item
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseManaCost = 500`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 100 ticks`
- effective cast time is explicitly forced to the spell's own cast time rather than being shortened through the normal override path.

## Two provider-owned operation modes

`ManaTranscriptionLogic` resolves one of two modes from the held items:

1. **EXTRACTION** — extracts one eligible enchantment from the main-hand item and writes it into an enchanted book using the required offhand book medium.
2. **RESET** — consumes an accepted dedicated offhand medium to reset prior anvil-work/repair cost on the main-hand item.

The exact required XP is calculated by provider logic from the current held-item state. The spell surfaces current/required XP and the selected/randomized target operation to the player before completion.

## Transaction/anti-swap behavior

Before cast start the provider:

- resolves the operation;
- verifies sufficient XP;
- randomly locks one candidate when multiple enchantments are eligible for extraction;
- snapshots/locks the main-hand and offhand operation state into cast data.

Every server cast tick verifies that the player's hands still match the locked operation. Swapping the relevant item cancels casting.

On completion the provider resolves the operation again and requires it to match the locked resolution before spending XP or mutating items.

## Extraction settlement

On successful extraction:

- required XP is removed;
- the selected enchantment is removed from the target item;
- the target's repair cost is advanced using vanilla anvil repair-cost progression;
- the offhand operation item is converted/filled into the resulting enchanted book.

## Repair-cost reset settlement

On successful reset:

- required XP is removed;
- target repair cost is set to zero;
- the dedicated operation item is consumed outside Creative mode.

These are provider-owned transactional mutations. Black Arcana must never consume a second XP/item/mana payment or repeat the enchantment mutation after observing the cast.

## What it does

Provider guide semantics match the source: channel mana and experience through items in both hands to transcribe an enchantment onto an unwritten Book and Quill, or use a compatible catalyst to remove prior anvil work.

## Acquisition

Registered through Iron's spell registry. Exact scroll/loot availability remains part of the provider-wide acquisition audit.

## Deduplication

Occupies the **high-cost magical enchantment extraction / repair-cost reset** utility niche. Black Arcana should not add an equivalent forbidden enchantment-transfer spell without materially different risk, provenance and transaction semantics.

## Confidence

`SOURCE-PINNED SPELL + SERVER TRANSACTION PATH / EXACT XP FORMULA + RESET ITEM TAG INVENTORY + FULL RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:mana_transcription` → `SpellRegistry.reg("mana_transcription", ManaTranscription::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.manatranscription.ManaTranscription`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/manatranscription/ManaTranscription.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.
