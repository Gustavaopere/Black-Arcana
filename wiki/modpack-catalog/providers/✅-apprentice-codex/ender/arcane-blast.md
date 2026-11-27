# Arcane Blast

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:arcane_blast`
- **Iron's school:** Ender
- **Levels:** 1–10
- **Minimum rarity:** Common
- **Cast type:** Long
- **Cooldown:** 1 s
- **Resource:** Iron's mana
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode coefficients

- `baseSpellPower = 40`
- `spellPowerPerLevel = 5`
- `baseManaCost = 20`
- `manaCostPerLevel = 4`
- `castTime = 30 ticks`

Raw damage before the provider config multiplier:

`spellPower / 10`

Effective range:

`16 + 4 * spellPower / 10` blocks.

Both damage and range therefore respond to actual Ender spell power, not only nominal spell level.

## Provider behavior

The server raycasts from the caster eye using a narrow `0.1` width and accepts only provider-valid combat targets. A successful hit uses Apprentice's Codex `ARCANE_BLAST` damage and then applies/increments **Arcane Charge** on the caster for `200 ticks`.

Arcane Charge amplifier is capped by this cast path at `2`, producing up to three charge tiers (`0..2`). The effect is provider state later consumed by Arcane Beam.

The public guide describes the spell as an internal arcane explosion/beam-like strike that accelerates mana circulation, bypasses armor and is ineffective against the provider's demonic targets. Armor bypass and demon eligibility were not demonstrated in the inspected bytecode and are not promoted as static facts; exact demon-tag membership remains provider data/runtime authority.

## Causality

One successful Arcane Blast is one provider hit plus one Arcane Charge state mutation. Black Arcana must not count the charge application as a second offensive cast/proc identity.

## Acquisition

Registered through Iron's spell registry. Exact survival scroll/loot/crafting availability for the 1.0.1.1 artifact remains part of the provider-wide acquisition audit.

## Deduplication

Occupies the **fast direct Ender/arcane hit that builds a short-lived charge resource for another spell** niche.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:arcane_blast` → construtor de `jp.aquafactory.apprenticecodex.spell.arcaneblast.ArcaneBlast`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** Server raycast from caster eye with `RAYCAST_WIDTH=0.1` and `CombatTools.isValidCombatTarget` → accepted hit applies `DamageTypes.ARCANE_BLAST` via `CombatTools.applyDamage` → on accepted hit only, `ARCANE_CHARGE` is created for `200` ticks at amplifier `0` or incremented to `min(amplifier+1,2)` → Arcane Beam later consumes that provider state.

**Constantes/cálculo:** Declared coefficients: `baseSpellPower=40`, `spellPowerPerLevel=5`, `baseManaCost=20`, `manaCostPerLevel=4`, `castTime=30`, COMMON, Long, cooldown `1.0`; damage `power/10 * DamageMultiplierKey.ARCANE_BLAST`; reach `16+4*power/10`; charge amplifier cap `2`.

**Limites:** Installed damage multiplier, demon-tag membership, effective config and physical QA remain `NÃO VERIFICADOS`. One hit plus one charge mutation is one root action, not two offensive casts.

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
