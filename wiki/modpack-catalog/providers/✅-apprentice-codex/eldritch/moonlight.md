# Moonlight

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:moon_light`
- **Iron's school:** Eldritch
- **Levels:** 1–3
- **Minimum rarity:** Legendary
- **Cast type:** Long
- **Cooldown:** 8 s
- **Resource:** Iron's mana
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode coefficients

- `baseSpellPower = 1200`
- `spellPowerPerLevel = 900`
- `baseManaCost = 120`
- `manaCostPerLevel = 30`
- `castTime = 40 ticks`
- cannot be interrupted
- standby visual starts from a 10-tick base delay, scaled against effective cast duration

Raw damage:

`spellPower / 100`

then multiplied by `DamageMultiplierKey.MOON_LIGHT`.

Attack distance by spell level:

`8 + (spellLevel - 1) * 8` blocks.

## What it does

The spell summons a Moonlight katana during the charge and, on successful completion, performs the blade slash plus a separate spatial charge-cut entity over the configured distance.

Provider guide semantics describe the flash-cut as rending space and severing both magical effects on the target and spellcasting itself. The cast is explicitly uninterruptible.

The provider's katana/charge-cut entities own exact hit, dispel/interruption and damage causality. Black Arcana must not apply a second anti-magic settlement when observing the same hit.

## Acquisition

Registered through Iron's spell registry. Exact scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **uninterruptible Eldritch flash-cut / long spatial slash / magic-effect and casting disruption** niche. Black Arcana anti-magic must remain mechanically distinct and must not rebrand this provider spell.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:moon_light` → construtor de `jp.aquafactory.apprenticecodex.spell.moonlight.MoonLight`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** `MoonLight` charge/standby → `MoonLightKatanaEntity` slash → `MoonLightChargeCutEntity` segment advances over the verified process duration with `damagedEntityIds` guard → `MoonLightCounterspellEffect` only after an accepted hit. The katana, spatial cut and counterspell are one semantic root.

**Constantes/cálculo:** Declared coefficients: `baseSpellPower=1200`, `spellPowerPerLevel=900`, `baseManaCost=120`, `manaCostPerLevel=30`, `castTime=40`, LEGENDARY, Long, cooldown `8.0`, uninterruptible. Raw damage is `spellPower/100 * DamageMultiplierKey.MOON_LIGHT`; reach is `8+(level-1)*8`. Standby starts from `STANDBY_START_DELAY_TICK=10`, scaled by effective cast duration.

**Limites:** Effective school/mana/cooldown/power channels, the installed `MOON_LIGHT` multiplier, third-party counterspell ordering, duplicate katana/cut settlement and Survival/PvP QA remain `NÃO VERIFICADOS`.

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
