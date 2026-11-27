# Spectral Wing

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:spectral_wing`
- **Iron's school:** Eldritch
- **Levels:** 1
- **Minimum rarity:** Legendary
- **Cast type:** Instant
- **Cooldown:** 2 s
- **Resource:** Iron's mana
- **Binary pin:** SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes
- **Historical source provenance:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (0.9.7.1; documental only, not the certification baseline)

## Exact 1.0.1.1 bytecode config

- `baseManaCost = 150`
- `manaCostPerLevel = 0`
- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `castTime = 0`

Initial launch constants:

- horizontal look-direction scale: **0.75**;
- minimum vertical launch speed: **1.05**;
- start grace: **10 ticks**.

Recast boost constants:

- forward boost speed: **2.75**;
- added upward speed: **0.22**;
- spin visual duration: **10 ticks**;
- visual wing-effect refresh: **20 ticks**.

## Preconditions

The exact spell rejects casting when:

- caster is not a player;
- an Elytra is equipped in the chest slot;
- Iron's Angel Wings effect is active;
- player is in water/bubble or swimming.

## What it does

First cast launches the player, starts fall-flying and activates provider-owned Spectral Wing state. Recasting while that spell-started state is active applies a strong look-direction boost instead of starting a second independent wing state.

Provider guide semantics state that the wings disappear when landing or touching water. The state/lifecycle is owned by Apprentice's Codex capability/event code.

## Authority and safety

This is not Black Arcana flight state. Black Arcana must not mirror velocity, cooldown or active-state bookkeeping in a second mobility controller. Any future stamina/progression observation must preserve the provider's single server-authoritative activation identity.

## Acquisition

Registered through Iron's spell registry. Exact scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **launch → glide → recast directional surge** mobility niche. A Black Arcana movement spell should not clone this sequence merely with different wing particles.

## Confidence

`SHA_EXACT_BINARY_BEHAVIOR 1.0.1.1 / STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / physical_qa=NOT_TESTED / config efetiva e QA físico pendentes`

## Localizadores e certificação — JAR 1.0.1.1

- **Artefato:** `apprentice_codex-1.0.1.1-mc1.21.1.jar`; SHA-256 `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86`; SHA-1 `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF`; 11.870.671 bytes.
- **Registro/identidade:** `apprenticecodex:spectral_wing` → construtor de `jp.aquafactory.apprenticecodex.spell.spectralwing.SpectralWing`; pacote e classe confirmados no inventário e no bytecode do JAR físico.
- **Evidência primária:** `javap -classpath <JAR> -p -s -c`/`-v` (`scratch/javap1011.txt`, `scratch/javap1011_v.txt`) e decompilação Vineflower 1.12.0 (`scratch/vf_apprentice1011/`). Síntese auditável: [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
- **Leitura para perks:** usar somente os fluxos, constantes e consumidores desta ficha. Evento, setter, callback ou estado provider-owned não é promovido a hook mutador sem ponto de chamada, consumidor do valor alterado e restrições de execução demonstrados.
- **Contrato:** host Iron's controla casting/mana/cooldown; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana não duplica custo, hit, estado ou efeito. Sem hook comprovado: **⚠️ condicionado/fail-closed**.
- **Pendências:** configuração efetiva do pack, canais herdados de `AbstractSpell`, multiplicadores de dano instalados e QA físico/Survival. O source 0.9.7.1 permanece apenas histórico; equivalência com o JAR não é assumida.

## Engenharia causal — ancoragem 1.0.1.1

**Fluxo verificado:** `SpectralWing.checkPreCastConditions` rejects non-player, elytra, Angel Wings and water/swim conflicts → first cast activates provider spectral-wing state, fall-flying and launch → recast while that state is active applies directional boost → `SpectralWingFlightEvent` maintains visual/fall state and deactivates on water after `WATER_DEACTIVATE_GRACE_TICKS=4`, landing, mount, ladder or incompatible flight.

**Constantes/cálculo:** Declared coefficients: `baseManaCost=150`, `manaCostPerLevel=0`, `baseSpellPower=0`, `castTime=0`, LEGENDARY, Instant, cooldown `2.0`. `LAUNCH_HORIZONTAL_SPEED=0.75`, `LAUNCH_VERTICAL_SPEED=1.05`, `BOOST_SPEED=2.75`, `BOOST_UPWARD_SPEED=0.22`, `BOOST_SPIN_TICKS=10`, `VISUAL_EFFECT_DURATION_TICKS=20`, `START_GRACE_TICKS=10`.

**Limites:** Interaction with external flight/gravity mods, state sync/relogin/death, dimension changes, effective config and client/modpack flight QA remain `NÃO VERIFICADOS`. No second mobility controller may mirror provider state.

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
