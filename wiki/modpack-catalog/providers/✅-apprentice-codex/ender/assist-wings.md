# Assist Wings

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:assist_wings`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Rare
- **Cast type:** Instant
- **Cooldown:** 0 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

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

The guide describes a jump/air-mobility aid with limited mid-air reuses and fall-safety behavior. The current source additionally proves the bounded jump counter and special broom path.

## Causality

Repeated air jumps belong to one provider spell mechanic/state family. RPG/Black Arcana must not award progression per movement tick or duplicate the provider's jump impulse.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **bounded reusable air-jump / wing-assist mobility** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT JUMP COUNT+IMPULSE+SERVER STATE / FALL-SAFETY EDGE CASES + SABLE/BROOM PHYSICAL QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:assist_wings` → `SpellRegistry.reg("assist_wings", AssistWings::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.assistwings.AssistWings`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/assistwings/AssistWings.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — lote persistente 0.9.7.1

**Evidência source-located:** [`assistwings/AssistWings.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/assistwings/AssistWings.java) · [`assistwings/AssistWingsWingEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/assistwings/AssistWingsWingEntity.java). Source declarado `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, alinhado à release 0.9.7.1. **Não há demonstração de equivalência dos corpos de métodos compilados no JAR da modlist**, nem GameTest provider-native neste dossiê.

### Sequência e ownership

- **Admissão do salto:** `AssistWings.checkPreCastConditions` recusa montaria que não seja `HoverrideBroomEntity` autorizada por `broom.canUseAssistWings(player)`. Em solo ou broom próxima de pouso permite tentar; no ar, `ASSIST_WINGS_STATE.doneJump < getJumpCount(spellLevel)` é verificado quando o provider oferece state. Esse número de saltos não é uma quantidade de casts BA.
- **Execução:** `AssistWings.onCast` usa `broom.acceptServerAssistWingsJump` quando montado. O estado reusa uma `AssistWingsWingEntity` existente vinculada ao caster ou instancia outra e grava `localEntityId`; reinicia grace, zera `doneJump` no solo e incrementa quando airborne. Para não montado aplica `applyJump` e sincroniza `SyncAssistWingsJumpPacket` para visualização cliente.
- **Controle por tick:** `AssistWingsWingEntity.tickOnServer` descarta wing sem owner `Player`, acompanha posição das costas, possui `REMOVAL_GRACE_TICKS=10` e encerra sessão ao pousar/encostar em água após grace. `applyFallProtection` zera `fallDistance` **somente quando** não existe item em main/offhand pertencente à tag `ASSIST_WINGS_ONLY_JUMP_ITEMS`; essa proteção é limitada, não uma imunidade a todo dano.
- **QA:** confirmar broom compatível, mounts alheios, server-client prediction, relog, stuck wing, salto múltiplo, água, antimagia e outro provider de fall protection. O próprio addon detém jump, wing, counters e estado.

### Integração com perks e QA

O evento original `apprenticecodex:assist_wings` já está catalogado. Spawn, processamento por tick, efeitos atrasados, partículas, loot, custo e cleanup pertencem ao Iron's/Apprentice's. **⛔** Não há adapter RPG Skill Tree de Mastery/perks com contrato testado; Black Arcana não cria segundo cast, segundo recurso ou efeito substituto do addon. **⚠️** Dados físicos de métodos, configuração, Survival, multiplayer/claims, save/reload e ordem intermod seguem pendentes. Stage 06.05 não é promovido.

[Engenharia source-level da etapa](../PERK-ENGINEERING-MATRIX-PERSISTENT-0.9.7.1.md).
