# Anchor Blink

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:anchor_blink`
- **Iron's school:** Ender
- **Levels:** 1
- **Minimum rarity:** Epic
- **Cast type:** Long
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Crafting:** disabled
- **Looting:** disabled
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 400`
- `spellPowerPerLevel = 200`
- `baseManaCost = 80`
- `manaCostPerLevel = 0`
- `castTime = 10 ticks`
- effective cast time deliberately ignores cast-time reduction
- raw dagger damage: `spellPower / 100 * providerDamageMultiplier`
- projectile speed: `1.8`
- maximum anchor-establishment range: `min(128, 16 * spellPower / 100)` blocks

At the one registered level and default spell power, the source-derived maximum anchor range is **64 blocks** before external spell-power modifiers.

## Item prerequisite

The cast requires the generated **Spell-Sided Edge mirror** in the off hand. If the mirror is absent, provider pre-cast validation fails with an action-bar message.

The spell is explicitly non-craftable/non-lootable and is therefore an item-bound capability rather than an ordinary survival scroll.

## Cast and anchor lifecycle

On successful server cast, the provider spawns an owner-linked `AnchorBlinkDaggerEntity`, stores damage and maximum range, and launches it along the caster's look direction.

The public guide describes a short-lived anchor behavior: after the reverse-edge dagger embeds, the caster can satisfy the provider jump condition to blink near it within roughly three seconds. Casting also deactivates the provider's Edge Dancer state.

Exact post-impact teleport safety/placement is owned by the dagger/anchor event path and remains separate from the spell-class coefficients above.

## Causality

Dagger throw, anchor establishment, teleport and Edge Dancer cleanup belong to one provider interaction chain. Black Arcana must not add a second teleport settlement or treat the eventual blink as a fresh provider cast.

## Deduplication

Occupies the **item-bound thrown anchor dagger followed by short-window positional blink** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT ITEM GATE+DAMAGE+PROJECTILE+RANGE / IMPACT-ANCHOR TELEPORT SAFETY+3s WINDOW INTERNALS+RUNTIME QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:anchor_blink` → `SpellRegistry.reg("anchor_blink", AnchorBlink::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.anchorblink.AnchorBlink`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/anchorblink/AnchorBlink.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — 0.9.7.1 (audit de source, 2026-10-13)

**Prova rastreável:** [`anchorblink/AnchorBlink.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/anchorblink/AnchorBlink.java) · [`anchorblink/AnchorBlinkDaggerEntity.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/anchorblink/AnchorBlinkDaggerEntity.java) · [`anchorblink/AnchorBlinkEvents.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/anchorblink/AnchorBlinkEvents.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, mod ID `apprenticecodex`. Identidade e versão do JAR são da modlist física; **não há prova de equivalência de cada corpo de método com o JAR compilado**.

### Sequência causal e parâmetros de execução

- **Cast original:** `AnchorBlink` é a única root registrada. O `AnchorBlinkDaggerEntity` conserva UUID do proprietário, dano, alcance, estado de impacto, game time e vetor de impacto. O `tick()` descarta o projétil em até `MAX_FLIGHT_TICKS=160` ticks em voo; após impacto, expira em `IMPACT_LIFETIME_TICKS=60` ticks. O efeito de aproximação/teleporte não constitui nova root de spell.
- **Admissão do blink:** `tryBlink(ServerPlayer)` resolve `ACTIVE_ANCHORS` pelo UUID do jogador, verifica a **mesma dimensão**, procura a entidade pelo ID atual e exige `isImpacted()`; remove um registro inválido. Se a âncora estiver apta, `tryBlinkOwner` calcula uma posição aprovada antes de executar o teleporte via `Utils.handleSpellTeleport`.
- **Escolha de destino:** `resolveTeleportDestination` examina deslocamentos para frente/trás, altura e lateral em sequência finita. `canStandAt` exige posição dentro do world border, ausência de colisão na hitbox de `Pose.STANDING` e fluidos vazios em todos os block states atravessados pelo volume. Se nenhuma posição passa, retorna vazio e não teleporta. **A rotina local não é prova de permissão de claims ou de segurança de qualquer mod externo.**
- **Pós-teleporte:** reseta `fallDistance`, emite som, registra `POST_BLINK_PROTECTION_TICKS=40` e remove âncora/entidade. `isProtectedFromEnemyDamage` só aceita proteção ativa, mesma dimensão e origem considerada hostil por `CombatTools.canBeHostileToMe`; não é imunidade global a todas as fontes.
- **Boundary:** não emitir dois recibos de cast/Mastery para o arremesso e o salto. Estado `ACTIVE_ANCHORS`/`DAMAGE_PROTECTIONS` é local ao addon; testar desconexão, mudança de dimensão, unload, teleporte cancelado por outro provider, PvP e reconstrução de entidade antes de perks de mobilidade.

### Perfil para integração de perks e QA

- **A / stats e rank:** ler apenas os atributos declarados no host Iron's e os state objects que o addon expõe; stat dinâmica e duração efetiva exigem ambiente, item e configuração. Nenhuma alteração de mana/cooldown do Iron's por Black Arcana.
- **B / causalidade:** uma ação primária `apprenticecodex:anchor_blink`; filhos, efeitos retardados, limpeza ou automação pertencem à raiz do provider. Sem `cast UUID`/contrato de retorno validado, o BA e RPG não devem inferir reward do resultado observado.
- **C/D / segurança:** ⛔ adapter de Mastery/perks enquanto inexistir contrato seguro. ⚠️ QA: servidor real, replay, NBT/relog, cross-dimension, compat opcional, ordenação e anti-double-processing. Não houve GameTest do provider nesta auditoria.
- **Clean-room:** análise factual e documentação próprias; código upstream não foi incorporado.

[Matriz causal desta etapa](../PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md).
