# Mage Light

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:mage_light`
- **Iron's school:** Holy
- **Levels:** 1
- **Minimum rarity:** Uncommon
- **Cast type:** Instant
- **Cooldown:** 0.5 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 25`
- `baseManaCost = 20`
- `manaCostPerLevel = 0`
- `castTime = 0`
- Chargecast Staffbow incompatible.

Normal placement range:

`max(0, min(8 * spellPower / 100, configuredMaxRange))`

The hard maximum is provider server config, mirrored client-side through the provider's Mage Light config state. The exact pack config value remains runtime/config QA.

## Placement authority

The spell validates a block target before cast, stores the resolved placement position in cast data and then attempts placement through the provider's `BlockTools.tryPlaceBlockByEntity(...)` path.

The source respects replacement/survival checks and does not simply trust client coordinates. A successful cast places `MAGE_LIGHT_TORCH`, plays placement audio and emits particles.

Provider guide semantics: summons and places a magical torch that lights the area and does not require an ordinary supporting block.

## Integration/world safety

This is an Apprentice's Codex world effect settled by provider placement helpers. Black Arcana must not place a duplicate torch or charge a second world-effect transaction after observing the provider cast. Black Arcana-originated world effects remain governed by its own `WorldEffectPolicy`.

## Acquisition

Registered through Iron's spell registry. Exact 0.9.7.1 scroll/loot availability remains in the provider-wide acquisition audit.

## Deduplication

Occupies the **cheap magical light placement** niche. A second generic BA light-orb/torch spell needs a materially different persistent/domain role to justify itself.

## Confidence

`SOURCE-PINNED SPELL + SERVER PLACEMENT / PACK MAX-RANGE CONFIG + FULL PROTECTION-MOD QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:mage_light` → `SpellRegistry.reg("mage_light", MageLight::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.magelight.MageLight`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/magelight/MageLight.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

## Engenharia causal aprofundada — mundo, channel e defesa (2026-10-14)

**ID causal:** `apprenticecodex:mage_light` — uma magia Iron's-native; ticks/jobs/entidades/impactos são efeitos-filhos, nunca um novo cast.

**Source pin:** [MageLight.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/magelight/MageLight.java); [MageLightTorchBlock.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/magelight/MageLightTorchBlock.java); [MageLightTorchBlockEntity.java](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/magelight/MageLightTorchBlockEntity.java).

**Cadeia verificada em source:** MageLight.checkPreCastConditions escolhe target do MageLightCastContext ou resolve e guarda MageLightCastData; onCast coloca exclusivamente por BlockTools.tryPlaceBlockByEntity. resolveCastTarget valida pending client target por BlockTargetingHelper.validateTarget com alcance limitado ou raycast fallback, e exige posição substituível/sobrevivência do bloco. MageLightTorchBlockEntity não tem ticker próprio: não tratar um bloco colocado como job recorrente.

**QA prioritário (não executado):** Proteções/claims no BlockTools efetivo, target packet, falha de placement, reload e casting remoto/dispenser.

**Boundary:** mana/casting Iron's e efeitos Apprentice's; nenhuma segunda liquidação/XP/Mastery por Black Arcana; contrato RPG sem hook comprovado: ⛔ fail-closed. ⚠️ Sem prova de bytecode do JAR instalado, config nem QA físico.
