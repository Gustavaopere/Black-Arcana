# Arcane Beam

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:arcane_beam`
- **Iron's school:** Ender
- **Levels:** 1–5
- **Minimum rarity:** Rare
- **Cast type:** Continuous
- **Cooldown:** 12 s
- **Resource:** Iron's mana
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode coefficients

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

The guide describes a continuous piercing arcane beam whose damage is enhanced by circulated mana/Arcane Charge, bypasses armor and is ineffective against demonic beings. Those guide claims about armor and demon eligibility were not demonstrated in the inspected bytecode and are not promoted as static facts; exact target filtering remains provider/runtime authority.

## Causality

Repeated beam damage callbacks belong to one continuous provider cast. A future progression/hazard observer must deduplicate by the cast/session rather than treating every beam tick as a new cast.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **continuous long-range Ender beam consuming a charge built by Arcane Blast** niche.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:arcane_beam` → construtor de `jp.aquafactory.apprenticecodex.spell.arcanebeam.ArcaneBeam`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** First server cast tick creates an owner-linked `ArcaneBeamEntity` near the eye and stores its UUID in `BeamCastData` → continuous ticks reorient and reclip the beam against blocks → `ArcaneBeamEntity.tick` calls `damageHitTarget` when `tickCount % 5 != 0` (4 in 5 ticks) → cast completion or cancellation discards the beam and removes Arcane Charge.

**Constantes/cálculo:** Declared coefficients: `baseSpellPower=200`, `spellPowerPerLevel=100`, `baseManaCost=5`, `manaCostPerLevel=5`, `castTime=60`, RARE, Continuous, cooldown `12.0`; range `32`, radius `0.25`; base damage `(1+power/100)*providerMultiplier`; charge bonus `round((power-100)/30)*(amplifier+1)` percent. The correct package is `spell.arcanebeam`; `spell.arcanabeam` does not exist.

**Limites:** The 4-in-5 cadence is a static bytecode fact, not measured DPS. Per-cast victim dedup was not demonstrated in the inspected method; installed multiplier, config, claims/clip, interruption and Survival QA remain `NÃO VERIFICADOS`.

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
