# Anchor Blink

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:anchor_blink`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Crafting:** disabled
- **Looting:** disabled
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 200`
- `baseManaCost = 80`
- `manaCostPerLevel = 0`
- `castTime = 10 ticks`
- effective cast time deliberately ignores cast-time reduction
- raw dagger damage: `spellPower / 100 * providerDamageMultiplier`
- projectile speed: `1.8`
- maximum anchor-establishment range: `min(128, 16 * spellPower / 100)` blocks

At the one registered level and default spell power, the bytecode-derived maximum anchor range is **64 blocks** before external spell-power modifiers.

## Item prerequisite

The cast requires the generated **Spell-Sided Edge mirror** in the off hand. If the mirror is absent, provider pre-cast validation fails with an action-bar message.

The spell is explicitly non-craftable/non-lootable and is therefore an item-bound capability rather than an ordinary survival scroll.

## Cast and anchor lifecycle

On successful server cast, the provider spawns an owner-linked `AnchorBlinkDaggerEntity`, stores damage and maximum range, and launches it along the caster's look direction.

The public guide describes a short-lived anchor behavior: after the reverse-edge dagger embeds, the caster can satisfy the provider jump condition to blink near it within roughly three seconds. Casting also deactivates the provider's Edge Dancer state.

The post-impact teleport safety/placement flow is owned by the dagger/anchor event path and is traced in the 1.0.1.1 bytecode in the causal-engineering section below; its runtime behavior remains `NÃO VERIFICADO`.

## Causality

Dagger throw, anchor establishment, teleport and Edge Dancer cleanup belong to one provider interaction chain. Black Arcana must not add a second teleport settlement or treat the eventual blink as a fresh provider cast.

## Deduplication

Occupies the **item-bound thrown anchor dagger followed by short-window positional blink** niche.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:anchor_blink` → construtor de `jp.aquafactory.apprenticecodex.spell.anchorblink.AnchorBlink`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** Item-gated cast spawns an owner-linked `AnchorBlinkDaggerEntity` → dagger stores damage/range and flies along look direction → impact creates an active anchor → provider jump input resolves it → `resolveTeleportDestination` checks border, standing hitbox and fluids → `Utils.handleSpellTeleport` moves the player → `POST_BLINK_PROTECTION_TICKS=40` and anchor/entity cleanup.

**Constantes/cálculo:** Declared coefficients: `baseSpellPower=400`, `spellPowerPerLevel=200`, `baseManaCost=80`, `manaCostPerLevel=0`, `castTime=10`, EPIC, Long, cooldown `30.0`, non-craftable/non-lootable; `getEffectiveCastTime` ignores reduction. Dagger damage is `power/100 * providerMultiplier`, speed `1.8`, anchor range `min(128,16*power/100)`; `MAX_FLIGHT_TICKS=160`, `IMPACT_LIFETIME_TICKS=60`.

**Limites:** Claims, cross-dimension, chunk unload, teleport canceled by another provider, PvP protection semantics, effective config and physical QA remain `NÃO VERIFICADOS`. Throw, anchor, blink and Edge Dancer cleanup are one root.

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
