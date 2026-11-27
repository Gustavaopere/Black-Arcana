# Otherworld Lens

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:otherworld_lens`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Continuous
- **Cooldown:** 5 s
- **Resource:** Iron's mana
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode config

- `baseManaCost = 35`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 300 ticks`
- fixed targeting/placement range: **8 blocks**
- marked incompatible with the provider's Chargecast Staffbow path.

## Server-authoritative placement/session

The spell only accepts a `ServerPlayer`. Before casting it:

1. resolves a pending block target within 8 blocks;
2. requires a valid hit block + face and air at the placement side;
3. runs `OtherworldLensTargetSafety.validate(...)`;
4. stores validated target data as cast data.

During server pre-cast, the target is validated again before the temporary lens block is placed. A provider session UUID then links player, lens position and viewed target.

Every server cast tick validates the active session. The spell cancels if the player is too far away (`KEEP_RANGE_SQ=144.0`, i.e. 12 blocks), the lens disappears, the lens is replaced, or another provider validation fails. Placement range remains the distinct 8-block value. Cast completion always closes the session with a provider-owned end reason.

## What it does

Provider guide semantics: conjures an unstable crystal lens from another world. Looking through it reveals the world as though viewed from behind the lens surface. The lens only persists while concentration is maintained, and obstructions can prevent a valid placement/session.

This is a temporary, validated remote-viewing surface—not a persistent portal.

## Authority and deduplication

This directly overlaps Black Arcana Divination. Black Arcana must not create a second camera/session state or independently place/remove the same lens. A future bridge should observe the provider session only through a legitimate boundary and preserve its server-validated target and cleanup rules.

## Acquisition

Registered through Iron's spell registry. Exact scroll/loot acquisition remains in the provider-wide acquisition audit.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:otherworld_lens` → construtor de `jp.aquafactory.apprenticecodex.spell.otherworldlens.OtherworldLens`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** `ServerPlayer` only → `IClientBlockTargetingSpell` target within `8` blocks → `OtherworldLensTargetSafety.validate` (block/face/air plus server raycast recheck) → lens block placement → `OtherworldLensSessionManager` UUID links caster, dimension, lens position and viewed target → every server tick revalidates the session → provider-owned end reason closes it and removes only the owned lens block.

**Constantes/cálculo:** Declared coefficients: `baseManaCost=35`, `manaCostPerLevel=0`, `baseSpellPower=0`, `castTime=300`, LEGENDARY, Continuous, cooldown `5.0`. Placement range is `8`; `KEEP_RANGE_SQ=144.0` (`12²`) is the distinct session-retention radius.

**Limites:** Claims, chunk unload, crash cleanup, NBT persistence, client view rendering, effective config and server+client QA remain `NÃO VERIFICADOS`. This is a temporary validated remote-viewing surface, not a second Black Arcana divinity/portal.

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
