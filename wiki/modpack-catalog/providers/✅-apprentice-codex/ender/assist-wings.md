# Assist Wings

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:assist_wings`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 100`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 0`
- allowed air-jump count: `1 + spellLevel` = **2 / 3 / 4** for levels 1–3

The vertical impulse uses:

`0.6 + caster jumpBoostPower`

rather than spell power.

## Lifecycle and authority

The provider stores the number of completed air jumps in server spell data. Touching ground resets the bounded air-jump counter. The spell also maintains an owner-linked wing entity with removal grace.

When mounted, the spell fails for arbitrary vehicles. It has explicit provider integration for **Hoverride Broom** and lets the broom own the movement application after server validation.

For a player not riding that broom, the server owns spell-state mutation and sends a dedicated player packet for the vertical jump so ordinary server velocity correction does not overwrite client horizontal motion.

## What it does

The guide describes a jump/air-mobility aid with limited mid-air reuses and fall-safety behavior. The 1.0.1.1 bytecode additionally proves the bounded jump counter and special broom path.

## Causality

Repeated air jumps belong to one provider spell mechanic/state family. RPG/Black Arcana must not award progression per movement tick or duplicate the provider's jump impulse.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **bounded reusable air-jump / wing-assist mobility** niche.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:assist_wings` → construtor de `jp.aquafactory.apprenticecodex.spell.assistwings.AssistWings`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** `checkPreCastConditions` rejects arbitrary mounts except an authorized Hoverride Broom → ground or broom-near-ground permits an attempt, airborne requires `doneJump < getJumpCount(level)` → `onCast` delegates to `broom.acceptServerAssistWingsJump` when mounted, otherwise applies the jump and sends `SyncAssistWingsJumpPacket` → `AssistWingsWingEntity.tickOnServer` tracks the owner, resets the counter on ground and removes the wing after `REMOVAL_GRACE_TICKS=10`.

**Constantes/cálculo:** Declared coefficients: `baseSpellPower=100`, `spellPowerPerLevel=100`, `baseManaCost=20`, `manaCostPerLevel=0`, `castTime=0`, RARE, Instant, cooldown `0.0`; allowed air jumps `1+level` (2/3/4); vertical impulse `0.6+caster.jumpBoostPower`. Fall protection is blocked when a held item belongs to `ASSIST_WINGS_ONLY_JUMP_ITEMS`.

**Limites:** Effective config, broom compatibility, server/client prediction, relog, stuck wing, water, antimagia, other fall-protection providers and physical QA remain `NÃO VERIFICADOS`. Repeated jumps are one provider mobility mechanic.

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
