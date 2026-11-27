# Auto Magnet

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:auto_magnet`
- **Iron's school:** Ender
- **Levels:** 1–5
- **Minimum rarity:** Common
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 25`
- `baseManaCost = 40`
- `manaCostPerLevel = 10`
- `castTime = 0`
- collection range: `8 + 4 * (spellLevel - 1)` = **8 / 12 / 16 / 20 / 24 blocks**
- collection mana charge: `10` by default, or `0` when the provider server config disables collection mana cost

## Provider behavior

The cast toggles `AutoMagnetFamiliarManager` on the server. Crouching selects **REVERSE** collection mode; normal casting selects **NORMAL** mode. The provider sends the resolved mode back as action-bar presentation.

The public guide describes an owner-following magnet that gathers dropped items/XP while respecting inventory behavior. The 1.0.1.1 bytecode verifies the two-tick collection loop and the orbit parameters; final inventory insertion and XP pickup are delegated to vanilla/host and remain `NÃO VERIFICADOS`.

## Resource authority

The ongoing collection mana cost is provider-owned. Black Arcana must not impose an additional mana/strain payment merely because Auto Magnet collected an item, nor infer a cast/progression event from each collected stack or XP orb.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **toggleable owner-following item/XP magnet with normal/reverse modes** niche.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:auto_magnet` → construtor de `jp.aquafactory.apprenticecodex.spell.automagnet.AutoMagnet`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** Cast toggles `AutoMagnetFamiliarManager` on the server; crouch selects `REVERSE`, otherwise `NORMAL` → `AutoMagnetFamiliarEntity.tickOnServer` checks `getCollectionMode().canCollect(owner.isCrouching())` and runs `collectNearbyDrops` every `COLLECT_INTERVAL_TICK=2` → item pass filters owner-recent drops and inventory fit, charges collection mana once per batch through `tryConsumeCollectMana` → XP orb pass moves orbs to owner feet without calling `tryConsumeCollectMana` in that loop.

**Constantes/cálculo:** Declared coefficients: `baseSpellPower=100`, `spellPowerPerLevel=25`, `baseManaCost=40`, `manaCostPerLevel=10`, `castTime=0`, COMMON, Instant, cooldown `0.0`; collection range `8+(level-1)*4`; `getCollectMana()` returns `0.0` or `10.0` per `AutoMagnetServerConfig.disableCollectManaCost` (default `false`); familiar orbit `1.4`, height `1.2`, angular speed `0.06981317007977318`.

**Limites:** The XP pass does not prove final pickup or external pickup events; inventory insertion is left to vanilla/host. Effective config, installed mana channels, full inventory, duplicate familiars, chunk unload, logout, Botania compat and physical QA remain `NÃO VERIFICADOS`.

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
