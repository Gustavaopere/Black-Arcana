# Palette Shift

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:palette_shift`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode config

- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 0`
- `setAllowCrafting(false)`
- `requiresLearning() = false`

## Preconditions and effect

Casting is allowed only while a **Pastel Staff** is held in either hand. Otherwise the provider rejects the cast and sends an action-bar error.

A successful cast applies `Palette Reception` for **600 ticks / 30 s**.

Provider guide semantics: this is a latent Pastel Staff spell that makes the staff receive the color/affinity of the **next** spell cast. Palette Shift cannot color the staff by itself.

## Acquisition

This is an item-bound latent spell, not a normal craftable spell-scroll path. `setAllowCrafting(false)` and `requiresLearning=false` are exact bytecode facts in the 1.0.1.1 artifact; other provider-internal ways the Pastel Staff exposes it remain owned by the item implementation.

## Deduplication

Occupies the **staff attunement / next-spell affinity capture** niche. It should not be interpreted as a generic Black Arcana school-conversion mechanic.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:palette_shift` → construtor de `jp.aquafactory.apprenticecodex.spell.paletteshift.PaletteShift`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** `PaletteShift.checkPreCastConditions` requires a Pastel Staff in mainhand or offhand → `onCast` applies `PALETTE_RECEPTION` for `600` ticks → `PaletteShiftReceptionEvent` runs at `EventPriority.HIGHEST`, ignores Palette Shift itself and, when a staff is modified, removes the reception and cancels the next cast that supplied the school/color.

**Constantes/cálculo:** Declared coefficients: `baseManaCost=50`, `manaCostPerLevel=0`, `baseSpellPower=0`, `castTime=0`, LEGENDARY, Instant, cooldown `30.0`; `setAllowCrafting(false)`, `requiresLearning()=false`, HiddenFromEldritchResearch.

**Limites:** Hook ordering against other `SpellPreCastEvent` handlers, two-hand behavior, other mods' school colors, re-login/expiry, effective config and physical QA remain `NÃO VERIFICADOS`. The canceled next spell is not a second successful Black Arcana cast.

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
