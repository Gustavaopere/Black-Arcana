# Remote Eye

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:remote_eye` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Escola | `SchoolRegistry.ENDER_RESOURCE` (Ender) |
| Raridade mínima | `SpellRarity.EPIC` |
| Níveis | 1–3 (`DefaultConfig.setMaxLevel(3)`) |
| Tipo de cast | `CastType.INSTANT` |
| Cooldown declarado | `30.0` s |
| Recurso | Mana do Iron's (`baseManaCost=80`, `manaCostPerLevel=25`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.remoteeye.RemoteEye` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1.

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("remote_eye", RemoteEye::new)` |
| Config | `RemoteEye.config` (`EPIC`, nível 3, cooldown `30.0`) |
| Coeficientes | `RemoteEye.<init>()`: `baseSpellPower=100`, `spellPowerPerLevel=30`, `baseManaCost=80`, `manaCostPerLevel=25`, `castTime=0` |
| Duração | `RemoteEye.getDuration(int,LivingEntity)` → `40 + round(40*power/100)` ticks |
| Gate de dimensão | `RemoteEye.checkPreCastConditions(...)`: `!ApprenticeCodexServerConfig.isRemoteEyeDimensionAllowed(level.dimension().location())` → mensagem `ui.apprenticecodex.spell.dimension_not_allowed` e falha |
| `onCast` | grava `activeUntilGameTime`, `activeDurationTicks`, `anchorX/Y/Z`, `anchorYaw`, `anchorPitch` em `REMOTE_EYE_STATE`; sincroniza ao `ServerPlayer` |
| Constante de reparo | `PERSISTED_STATE_REPAIR_MAX_ACTIVE_TICKS=600` |
| Estado | `capability.codexspelldata.spellstates.RemoteEyeState` |
| Tick de sessão | `jp.aquafactory.apprenticecodex.spell.remoteeye.RemoteEyeBodyControlEvent.onPlayerTick(Post)`, `isActive`, `sanitizePersistentGameTimes`, `anchorBody`, `deactivate` |
| Reparo | `PersistentGameTimeSanitizer.repairPersistedFutureUntil(gameTime, activeUntil, activeDurationTicks>0 ? activeDurationTicks : 600)` |
| Sync | `RemoteEyeSync.syncToClient(...)` |
| Som | `SoundRegistry.REMOTE_PREPARE` |
| Limpeza | handlers de `LivingDeathEvent`, `PlayerLoggedInEvent`, `PlayerRespawnEvent`, `PlayerChangedDimensionEvent` |

Bytecode: `scratch/javap1011_ender10.txt` (`javap -classpath <JAR> -p -s -c`, `EXIT=0`, SHA-256 `0095E23B21918E38B4BD7D6C47DA8C3503753F0F988C00AB04A786060E2C50E5`); decompilação: `scratch/ender10_sources.txt` (SHA-256 `F3953EB8FCFB793EC501694E054E3C3CBE187E557B09B6CF158828692A97A645`).

## 3. Casting / execução

1. `AbstractSpell` resolve mana/cooldown/nível; `castTime=0`, `CastType.INSTANT`.
2. `checkPreCastConditions` rejeita dimensões não permitidas pela config no lado servidor.
3. `onCast` calcula `duration = 40 + round(40*power/100)` e grava no capability: `activeUntilGameTime = gameTime + duration`, `activeDurationTicks = duration`, âncora XYZ e âncora de yaw/pitch do casador; sincroniza ao cliente se `ServerPlayer`.
4. `RemoteEyeBodyControlEvent.onPlayerTick(Post)` sanitiza horizontes persistidos, testa `activeUntilGameTime > gameTime`, e exige `player.isAlive() && !player.isPassenger()`; caso contrário `deactivate` reseta e sincroniza.
5. Enquanto ativo, `anchorBody` repõe o corpo na âncora e na rotação registrada. `deactivate` só atua quando `activeUntilGameTime != 0`.

Valores efetivos de mana/cooldown e configuração de dimensão **NÃO VERIFICADOS**.

## 4. Estado e geometria

| Propriedade | Valor e consumidor |
|---|---|
| Duração | `40 + round(40*power/100)` ticks; nominal **80 / 92 / 104 ticks (4 / 4,6 / 5,2 s)** nos níveis 1–3 sem modificadores |
| Âncora | XYZ + yaw/pitch capturados no cast; `POSITION_EPSILON_SQ=1.0E-6` para detectar divergência |
| Reparo de save antigo | limite `600` ticks quando `activeDurationTicks <= 0`; é sanitização, não extensão de duração |
| Corpo | `anchorBody` chama `setPos(anchor)`, `setYRot`, `setXRot`, `setYHeadRot`, `setYBodyRot`, zera `yRotO`/`xRotO`, `fallDistance`, `setDeltaMovement(Vec3.ZERO)`, `xOld/yOld/zOld`, `hasImpulse=false`, `hurtMarked=true` |
| Persistência | `RemoteEyeState` no capability do Codex, sincronizado via `RemoteEyeSync` |

O corpo real permanece no mundo e é alvo de dano. A visualização/câmera do cliente não é autoridade de teleporte nem de deslocamento remoto.

## 5. Resultado

- Limpeza em expiração, morte (`LivingDeathEvent`), login, respawn e troca de dimensão.
- `sanitizePersistentGameTimes` reescreve `activeUntilGameTime` e sincroniza a correção quando há divergência.
- O provider descreve um modo de observação destacado; a colisão/UX da câmera pertence ao cliente do provider e não foi certificada nesta análise.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `100 + 30*(level-1)` | float; `getSpellPower` do host aplica atributos/multiplicadores |
| Mana | `80 + 25*(level-1)` | Iron's mana |
| Duração | `40 + round(40*power/100)` | ticks; responde a spell power |
| Gate | `ApprenticeCodexServerConfig.isRemoteEyeDimensionAllowed(...)` | config do servidor; conteúdo **NÃO VERIFICADO** |
| Cooldown | `30.0` s | `DefaultConfig` |
| Reparo | `600` ticks | somente para estado legado sem duração registrada |

## 7. Possibilidades de perks

- **A — atributo nativo:** spell power/mana/cooldown via `AbstractSpell`; a duração responde indiretamente ao spell power.
- **B — evento verificado:** `PlayerTickEvent.Post` e os handlers de ciclo de vida são observadores do provider; não autorizam alterar âncora, duração base ou a imobilização do corpo.
- **C — adapter condicionado:** mudar o modo de observação exigiria contrato com `RemoteEyeBodyControlEvent`/`RemoteEyeSync`, câmera do cliente e sanitização de estado. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há API segura comprovada para transformar o olho remoto em possessão, teleporte ou segunda sessão de observação. **NO_MUTATION / fail-closed**.
- `mutating_hook = NOT_VERIFIED`.

## 8. Causalidade

`um cast → um estado de observação com âncora e expiração → imobilização do corpo até limpeza`.

Há sobreposição semântica direta com Familiars & Divination do Black Arcana. Um recurso BA equivalente exigiria distinção demonstrável (ownership/privacidade de alvo ou contrato noético diferente), não apenas VFX diverso. Black Arcana não deve consumir câmera do cliente como autoridade de provider.

## 9. Concepção de nova magia

Assinatura ocupada: "observação remota temporária com corpo imobilizado e âncora persistida". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ Identidade/hash, coeficientes, fórmula de duração, gate de dimensão, âncora, limpeza e reparo confirmados no bytecode 1.0.1.1.
- ⚠️ Configuração efetiva de dimensão e comportamento de câmera/colisão no cliente não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem cliente/servidor Survival, reconexão, replay de save, cross-dimension, dano ao corpo ou PvP.
- ⚠️ Universo integral do provider não encerrado.

## Localizadores para Codex — resumo operacional

- `PERSISTED_STATE_REPAIR_MAX_ACTIVE_TICKS=600` não é a duração da spell; é teto de reparo de estado antigo.
- `anchorBody` imobiliza o corpo; não é um teleporte e não move a câmera por autoridade de servidor.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.
- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
