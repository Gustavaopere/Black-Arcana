# Mana Transcription

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mana_transcription`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Long
- **Cooldown:** 4 s
- **Resource:** Iron's mana + provider-required player XP/operation item
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode config

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

Provider guide semantics are compatible with the 1.0.1.1 bytecode flow: channel mana and experience through items in both hands to transcribe an enchantment onto an unwritten Book and Quill, or use a compatible catalyst to remove prior anvil work.

## Acquisition

Registered through Iron's spell registry. Exact scroll/loot availability remains part of the provider-wide acquisition audit.

## Deduplication

Occupies the **high-cost magical enchantment extraction / repair-cost reset** utility niche. Black Arcana should not add an equivalent forbidden enchantment-transfer spell without materially different risk, provenance and transaction semantics.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:mana_transcription` → construtor de `jp.aquafactory.apprenticecodex.spell.manatranscription.ManaTranscription`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** `ServerPlayer` → `ManaTranscriptionLogic` resolve `EXTRACTION`/`RESET` from the held main/offhand pair → XP check → resolution and hand state locked in `ManaTranscription$ManaTranscriptionCastData` → every server cast tick revalidates the hands → `onCast` re-resolves and requires a match before `giveExperiencePoints(-requiredXp)` and the provider-owned enchantment/book or repair-cost mutation.

**Constantes/cálculo:** Declared coefficients: `baseManaCost=500`, `manaCostPerLevel=0`, `baseSpellPower=0`, `spellPowerPerLevel=0`, `castTime=100`, cooldown `4.0`, LEGENDARY, Long. `getEffectiveCastTime` deliberately forces the spell's own cast time. The required XP is produced by provider logic from the held-item state and is not promoted here to an unsupported fixed constant.

**Limites:** The source pin 0.9.7.1 is historical; this flow is reanchored in the 1.0.1.1 bytecode/decompilation. Atomicity of XP + item mutation after crash/failure, effective config, inherited mana/cooldown channels and physical QA remain `NÃO VERIFICADOS`. No second XP/item/mana settlement may be added.

## Estado da certificação

- `claim_scope`: `STATIC_TECHNICAL_CATALOG_ONLY`
- `evidence_grade`: `SHA_EXACT_BINARY_BEHAVIOR`
- `version`: `1.0.1.1`
- `artifact_sha256`: `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`
- `artifact_sha1`: `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`
- `mutating_hook`: `NOT_VERIFIED`
- `physical_qa`: `NOT_TESTED`
- `implementation_in_main`: `NOT_APPLICABLE`
- **Resultado:** ✅ contrato técnico estático reancorado; ⚠️ hook mutador, config efetiva, canais herdados e QA físico permanecem pendentes; ⛔ sem homologação para perks/Mastery.
