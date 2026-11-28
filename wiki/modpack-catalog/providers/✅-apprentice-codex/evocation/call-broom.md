# Call Broom

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:call_broom` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | sem interface adicional declarada |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `RARE` |
| Níveis declarados | 1 (`setMaxLevel(1)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `1.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=20`, `manaCostPerLevel=0`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.callbroom.CallBroom` |
| Auxiliares da mesma raiz | `CallBroomDeploymentManager`, `CallBroomDeploymentEvents`, `BroomCurioSupport`, `BroomDeploymentState` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("call_broom", CallBroom::new)` |
| Config | `RARE`, nível 1, cooldown `1.0`, `EVOCATION_RESOURCE`, `setAllowCrafting(false)`, `allowLooting()=false` |
| Coeficientes | <init>: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=20`, `manaCostPerLevel=0`, `castTime=20` |
| Validação | `CallBroomDeploymentManager.validate`: brooma Curio único, jogador não passageiro, entidade não ocupada |
| Distância | `RECALL_DISTANCE=8.0`, `RECALL_DISTANCE_SQR=64.0` |
| Recuperação | `findOwnedBrooms` varre `server.getAllLevels()`; `shouldRecall` considera dimensão, posse, `isVehicle()` e `matchesEquippedDeployment` |
| Eventos | `CallBroomDeploymentEvents` chama `onLogin`/`onLogout`/`onBroomRemoved` |

Bytecode: scratch/javap1011_evocation10.txt (`javap -classpath <JAR> -p -s -c`, 61 classes, EXIT=0, SHA-256 `B872A0B86732D7EAE026532ED358AD9BBDFB7B1D7BCFCA2C6B35F13EADD9A2D5`); decompilação de apoio: scratch/evocation10_sources.txt (44 fontes Vineflower 1.12.0, SHA-256 `BCAF5695AA5346DABC0D976D8EBFA327B7622570230DE48B4330396876448387`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `checkPreCastConditions` valida via `CallBroomDeploymentManager.validate(serverPlayer)` e recusa com `not_found_broom` ou `cannot_recall_mounting` conforme a falha.
2. Para jogador não servidor, exige `!player.isPassenger()` e `BroomCurioSupport.findUniqueEquippedBroom(player).isPresent()`.
3. `onCast` chama `CallBroomDeploymentManager.execute(player)`: com `Action.RECALL`, chama `broom.recallWithoutItem()`; com `Action.SUMMON`, cria a brooma a partir do item Curio, define dono, nome, move para a posição do jogador, adiciona à dimensão e inicia montaria.
4. `BroomDeploymentState.setDeployedEntity(stack,uuid)` amarra o item à entidade; falha ao montar reverte com `recallWithoutItem()`.
5. `shouldRecall` recolhe a brooma se o dono morreu, mudou de dimensão, está a mais de `8.0` blocos (`64.0` ao quadrado) ou se o item equipado não corresponde à entidade.
6. Login/logout e remoção da entidade limpam o estado; nenhuma segunda brooma é criada quando já existe uma não ocupada.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Alvo | Item-brooma único equipado como Curio |
| Recolha | `64.0` (distância²) ≈ `8.0` blocos |
| Dimensões | Varredura em `server.getAllLevels()` |
| Ocupação | `isVehicle()` recusa recall/summon |
| Spawn | Posição exata do jogador, yaw do jogador, sem pitch |
| Montaria | `player.startRiding(broom,true)` |

## 5. Resultado

- A magia recupera ou invoca a brooma existente; não cria objeto semântico novo por entidade.
- O vínculo é bidirecional: UUID no item (`BroomDeploymentState`) e dono/nome na entidade.
- A montaria é imediata; falha de montaria resulta em `recallWithoutItem()` e nenhum estado pendente.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `0` (sem escalonamento de poder) | constante |
| Mana/cooldown/cast | `20` / `1.0` s / `20` ticks | host + config **NÃO VERIFICADA** |
| Recall | `8.0` blocos (`64.0` ao quadrado) | distância do dono |
| Unicidade | Uma brooma equipada, uma entidade implantada | estado do Curio |

## 7. Possibilidades de perks

- **A — atributo nativo:**mana/cooldown respondem ao `AbstractSpell`; poder não altera a brooma.
- **B — evento verificado:** login/logout/remoção são manutenção de estado, sem modificação de parâmetros.
- **C — adapter condicionado:** mudar a distância de recall, permitir múltiplas broomas ou substituir o Curio exigiria alterar manager, estado do item e eventos. **CONDICIONADO**.
- **D — sem hook demonstrado:** não há contract seguro para transformar o recall em teleporte de grupo ou ignorar `isVehicle()`. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`um cast → validação do Curio → recall da brooma em qualquer dimensão ou summon com montaria imediata → limpeza nos eventos`.


## 9. Concepção de nova magia

Assinatura ocupada: "recall/summon de montaria única vinculada a Curio". Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, coeficientes 0/0/20/0/20, `allowCrafting=false`, `allowLooting=false`, constantes 8/64, varredura em todas as dimensões e gates de passageiro/ocupação confirmados no bytecode 1.0.1.1.
- ⚠️ multiplicador/mana efetivos e comportamento em portais/montaria PvP não certificados.
- ⚠️ `physical_qa=NOT_TESTED`: sem servidor Survival, PvP, portais, montarias, recast em combate real ou teleportes.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

- `8.0`/`64.0` são a mesma grandeza em unidades diferentes (distância e distância²).
- A busca cobre todas as dimensões via `server.getAllLevels()`.
- A brooma não pode ser recolhida se estiver ocupada ou se o jogador estiver passageiro.
- Nenhum ponto de mutação segura demonstrado; manter fail-closed.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
