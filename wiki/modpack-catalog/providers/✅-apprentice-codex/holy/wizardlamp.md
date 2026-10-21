# Wizardlamp

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:wizardlamp`
- **Iron's school:** Holy
- **Levels:** 1
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 0.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source config

- `baseSpellPower = 0`
- `spellPowerPerLevel = 0`
- `baseManaCost = 50`
- `manaCostPerLevel = 0`
- `castTime = 0`
- placement range: **6 blocks**
- Chargecast Staffbow incompatible.

## Targeting and placement

The spell captures client target intent but resolves/validates the requested placement against its 6-block range and server world state.

If normal server raycast misses a block, the provider preserves the air-placement behavior by using the 6-block ray endpoint. If a client-requested position is outside range, it is clamped back to the range boundary before final placement validation.

A valid position must:

- be inside world bounds;
- contain a replaceable block state;
- support survival of the Wizardlamp lantern state.

On placement, the lantern is marked waterlogged when the target fluid is water. Placement itself uses `BlockTools.tryPlaceBlockByEntity(...)`, preserving provider/loader interaction checks.

## What it does

Provider guide semantics: summons and places a magical lantern that illuminates the surrounding area. It can be placed within reach without a conventional support block and remains in place without support.

## World-effect authority

Wizardlamp placement is a provider-owned world effect. A Black Arcana integration must not place/remove another lantern or settle a second resource/world policy transaction after the provider succeeds.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **floating/waterloggable magical lantern placement** niche, adjacent but not identical to Mage Light's torch placement.

## Confidence

`SOURCE-PINNED SPELL + TARGET CLAMP + PLACEMENT / PACK PROTECTION-MOD QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:wizardlamp` → `SpellRegistry.reg("wizardlamp", Wizardlamp::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.wizardlamp.Wizardlamp`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/wizardlamp/Wizardlamp.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — utilidades, persistência e recursos (2026-10-14)

**Registry:** `apprenticecodex:wizardlamp`. **Proveniência source:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e` (versão declarada 0.9.7.1); classes e helpers: [Wizardlamp.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/wizardlamp/Wizardlamp.java); [WizardlampLanternBlock.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/wizardlamp/WizardlampLanternBlock.java); [WizardlampLanternBlockEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/wizardlamp/WizardlampLanternBlockEntity.java).

**Cadeia causal no código-fonte:** Wizardlamp.checkPreCastConditions resolve posição server-validated e guarda WizardlampCastData; onCast reutiliza a posição ou revalida, calcula WATERLOGGED quando o fluido é água e só liquida placement via BlockTools.tryPlaceBlockByEntity. WizardlampLanternBlockEntity é uma BlockEntity simples sem ticker implementado no source fixado, não uma job loop nem cast adicional por tick.

**QA prioritário pendente:** Handoff de target cliente para servidor, waterlogged/reload, claims/BlockTools, placement negado e persistência do bloco sem owner/pagamento extra.

**Governança:** o host Iron's controla cast/mana/recast; o addon controla o estado/efeito/custo especializado verificado. Um pulso, dano periódico, bloco, item gerado, job tick, cast visual ou cast derivado não é uma identidade semântica nova nem gatilho de Mastery/XP automático. Black Arcana não reprocessa recursos, eventos, mutação do mundo ou callback dos providers. ⚠️ Source-level não comprova bytecode idêntico/config efetiva/teste físico. ⛔ Nenhum contrato de RPG Skill Tree perks/Mastery homologado: fail-closed.
