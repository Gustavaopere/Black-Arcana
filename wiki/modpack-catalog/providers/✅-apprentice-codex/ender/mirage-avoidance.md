# Mirage Avoidance

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:mirage_avoidance` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.EPIC` |
| Níveis | 1 (`DefaultConfig.setMaxLevel(1)`) |
| Tipo de cast | `CastType.INSTANT` |
| Cooldown declarado | `3.0` s |
| Recurso | Mana do Iron's (`baseManaCost=50`, `manaCostPerLevel=0`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.mirageavoidance.MirageAvoidance` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("mirage_avoidance", MirageAvoidance::new)` |
| Config | `MirageAvoidance.config` (`EPIC`, nível 1, cooldown `3.0`) |
| Coeficientes | `MirageAvoidance.<init>()`: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=50`, `manaCostPerLevel=0`, `castTime=0` |
| Gate de cast | `MirageAvoidance.checkPreCastConditions(...)`: exige `Player` e `!MirageAvoidanceEvents.isInputLocked(player)`; recusa com action bar `ui.apprenticecodex.during_effect` |
| Duração exibida | `MirageAvoidance.getDuration(boolean supported)` → `supported ? 20 : 15` ticks |
| `onCast` | grava `startGameTime`, `activeUntilGameTime = gameTime + (supported ? 22 : 25)`, `invulnerableUntilGameTime = gameTime + getDuration(supported)`, `movementForward`, `movementStrafe`, sincroniza e chama `spawnStartupPulse` |
| Suporte | `ProtectionSpellSupporter.isEquippedBy(player)` alterna 25/15 → 22/20 ticks |
| Estado | `capability.codexspelldata.spellstates.MirageAvoidanceState` |
| Eventos | `jp.aquafactory.apprenticecodex.spell.mirageavoidance.MirageAvoidanceEvents` (`onPlayerTick(Pre/Post)`, `onLivingIncomingDamage`, `isInputLocked`, `rejectServerInputCastIfLocked`, `applyMovement`) |
| Cliente | `MirageAvoidanceClientController` (`MovementInputUpdateEvent`, `InteractionKeyMappingTriggered`, `MouseScrollingEvent`, `MouseButton.Pre`) |
| Sync | `MirageAvoidanceSync.syncToClient(...)` |
| Pulse | `Networks.sendToTrackingEntityAndSelf(player, new HeavenlyFistPulsePacket(center, 1.0F))`, centro em `player.getY()+0.1` |
| Som/animação | `SoundRegistry.MIRAGE`, `SpellAnimations.SELF_CAST_TWO_HANDS` |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSpell` resolve mana/cooldown/nível; `castTime=0`, `CastType.INSTANT`.
2. `checkPreCastConditions` exige `Player` e nega cast enquanto `isInputLocked` (com mensagem vermelha ao `ServerPlayer`).
3. No servidor, `onCast` lê `SpellMovementInput.recent(serverPlayer).normalizedOrBackward()` (cliente sem servidor usa `Input(-1,0)`), calcula `supported = ProtectionSpellSupporter.isEquippedBy(player)`, grava estado capability com `activeUntil = +22/+25` e `invulnerableUntil = +20/+15`, sincroniza ao cliente e emite `HeavenlyFistPulsePacket` raio `1.0`.
4. `MirageAvoidanceEvents` sanitiza tempos persistidos, desativa em expiração/morte/montaria, cancela dano apenas na janela de invulnerabilidade e bloqueia interações/casts de input enquanto ativo.
5. `MirageAvoidanceClientController` zera impulse de movimento, up/down/left/right/jump/shift e cancela interações, scroll e botão de mouse (ação `1`) enquanto `isActive()`.

## 4. Timing e geometria

| Propriedade | Valor e consumidor |
|---|---|
| Estado ativo (base) | `EFFECT_DURATION_TICKS=25` (1,25 s); `SLIDE_TICKS=18` |
| Estado ativo (suportado) | `SUPPORTED_EFFECT_DURATION_TICKS=22`; usado em `activeUntilGameTime` quando `ProtectionSpellSupporter` está equipado |
| Invulnerabilidade (base) | `INVULNERABLE_TICKS=15` (0,75 s) |
| Invulnerabilidade (suportada) | `SUPPORTED_INVULNERABLE_TICKS=20`; retornado por `getDuration(true)` |
| Freeze inicial | `FREEZE_TICKS=2`; `applyMovement` só atua para `elapsedTicks >= 2` |
| Fim da recuperação vulnerável | `VULNERABLE_RECOVERY_START_TICK=20`; slide em `2 <= tick < 20` |
| Velocidade horizontal | `RUN_SPEED_PER_TICK=0.42`, escalada por `1 - slideTick/18` (`slideTick=clamp(elapsed-2,0,18)`) |
| Queda lenta | `SLOW_FALL_SPEED=-0.08`; `y` é limitado inferiormente a `-0.08` durante o slide |
| Reset de `fallDistance` | `shouldResetFallDistance`: `elapsedTicks >= 2 && < 20` |
| Pulse inicial | raio `1.0`, centro em `player.y + 0.1` |

**Delta corrigido neste lote:** o ficha histórica registrava apenas `25/15` ticks; o JAR `1.0.1.1` contém também os ramos `22/20` quando `ProtectionSpellSupporter` está equipado (`SUPPORTED_EFFECT_DURATION_TICKS`, `SUPPORTED_INVULNERABLE_TICKS` e uso direto de `22` em `onCast`).

## 5. Resultado

- `onLivingIncomingDamage` cancela dano somente se `invulnerableUntilGameTime > gameTime`.
- Os handlers de interação (`AttackEntityEvent`, `EntityInteract`, `EntityInteractSpecific`, `LeftClickBlock`, `RightClickBlock`, `RightClickItem`) são bloqueados por `isInputLocked`.
- `rejectServerInputCastIfLocked` bloqueia casts de input no servidor e envia o aviso de efeito em andamento.
- `PersistentGameTimeSanitizer` repara `activeUntil` e `invulnerableUntil` persistidos; esses ticks são sanitização, não extensão de duração.

Todos os efeitos pertencem a uma única ativação; não são procs defensivos independentes.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `0 + 0*(level-1)` | sem escalonamento |
| Mana | `50 + 0*(level-1)` | Iron's mana, default declarado |
| Duração base | `25` ativo / `15` invulnerabilidade | ticks |
| Duração suportada | `22` ativo / `20` invulnerabilidade | ticks; depende de `ProtectionSpellSupporter` |
| Cooldown | `3.0` s | `DefaultConfig` |
| Corredor de slide | `2 <= tick < 20`, `18` ticks | providers `FREEZE_TICKS`/`SLIDE_TICKS` |

A condição de suporte é equipamento de item; o efeito exato do curador de equipamento dependente não foi estendido além do que o bytecode mostra.

## 7. Possibilidades de perks

- **A — atributo nativo:** mana/cooldown via `AbstractSpell`; contrato do host, não hook de mutação deste objeto.
- **B — evento verificado:** `PlayerTickEvent`, `LivingIncomingDamageEvent` e eventos de input são observadores/canceladores do provider; a existência deles **não** autoriza mudar janelas de i-frame, speed de slide ou input lock.
- **C — adapter condicionado:** alterar 15/20 ticks ou 0.42 exigiria substituir `MirageAvoidanceEvents.applyMovement` e a janela de dano com contrato de sanitização e sincronização. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API segura comprovada para estender invulnerabilidade, alterar o gate de input ou remover o lock sem quebrar a session do provider. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → um estado capability com janela de efeito/i-frame → tick de movimento + input lock + cancelamento de dano → expiração/sanitização`.

Black Arcana não deve criar segundo i-frame, segundo lock de input nem pagar Mastery por tick de slide.

## 9. Concepção de nova magia

Assinatura ocupada: "esquiva instantânea curta com janela de i-frame e deslizamento travado". Uma magia original precisaria de semântica materialmente distinta (por exemplo, deslocamento sem lock de input ou sem i-frame) para não duplicar esta identidade. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, constantes de timing base e suportada, input lock, cancelamento de dano, sanitização e pulse confirmados no bytecode 1.0.1.1.
- ⚠️ Configuração efetiva e multiplicadores instalados não lidos.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente/servidor Survival, PvP, reconexão, replay de packet, game-time reset ou equipamento de suporte real.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- `getDuration(boolean)` retorna `15`/`20`, não 25/22; 25/22 são o estado ativo gravado em `onCast`.
- A janela de dano é sempre a de `invulnerableUntilGameTime`, nunca a de `activeUntilGameTime`.
- `isInputLocked` sanitiza antes de consultar; não assumir estado persistido cru.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
