# Tamers Pocket

**Estado do contrato:** ✅ `COMPLETE_PERK_READY` — `STATIC_TECHNICAL_CATALOG_ONLY` · `SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `mutation=NO_MUTATION` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`.

> O ✅ cobre exclusivamente a documentação estática SHA-exata deste objeto. Não homologa hook mutador, execução no pack, configuração efetiva, universo integral do provider nem QA físico.

## 1. Identidade e proveniência

| Campo | Valor verificado |
|---|---|
| Provider | Apprentice's Codex |
| Mod ID | `apprenticecodex` |
| Registry ID | `apprenticecodex:tamers_pocket` |
| Host | Iron's Spells 'n Spellbooks (`AbstractSpell`) |
| Interfaces | `ICastDataSerializable` via `TamersPocketCastData`; `TamersPocketState` e `TamersPocketSync` pertencem à mesma raiz |
| Escola | `SchoolRegistry.EVOCATION_RESOURCE` (Evocation) |
| Raridade mínima declarada | `UNCOMMON` |
| Níveis declarados | 1 (`setMaxLevel(1)`) |
| Tipo de cast | `LONG` |
| Cooldown declarado | `4.0 s` |
| Recurso | Mana do Iron's (`baseManaCost=50`, `manaCostPerLevel=0`) |
| JAR exato | `apprentice_codex-1.0.1.1-mc1.21.1.jar` |
| SHA-256 do JAR | `9C5244E75DBCA95BDAF48A85F0C189F8456149D1220BAD5FF339A86BCE04AC86` |
| SHA-1 do JAR | `A3F9C73EBD77D15B7E77AE14F4D0F695FEC3B7CF` |
| Ambiente | Minecraft 1.21.1 · NeoForge · Java 21 (JDK 21.0.12 na inspeção) |
| Classe de implementação | `jp.aquafactory.apprenticecodex.spell.tamerspocket.TamersPocket` |
| Auxiliares da mesma raiz | `TamersPocketCastData`, `TamersPocketCastMode`, `TamersPocketState.StoredPet`, `TamersPocketSync`, `CodexSpellStateTypeRegister.TAMERS_POCKET_STATE` |
| Evidência compartilhada | [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md) |

As versões 0.9.7.1 e 1.0.1 permanecem como histórico; nenhum valor foi reaproveitado sem confirmação no artefato físico 1.0.1.1. Os coeficientes declarados não são os valores efetivos instalados: mana, cooldown, spell power, nível, raridade e multiplicadores do host permanecem `NÃO VERIFICADOS` (`AbstractSpell` lê `SpellConfigManager`, atributos, Curios e eventos).

## 2. Localizadores para o Codex

| Elemento | Localizador |
|---|---|
| Registro | `SpellRegistry.reg("tamers_pocket", TamersPocket::new)` |
| Config | `UNCOMMON`, nível 1, cooldown `4.0`, `EVOCATION_RESOURCE` |
| Coeficientes | <init>: `baseSpellPower=0`, `spellPowerPerLevel=0`, `baseManaCost=50`, `manaCostPerLevel=0`, `castTime=20` |
| Alcance | `getRange()=8.0`; usado em `raycastFromEye(...,0.5,...)` e `boundingBox.inflate(8.0)` |
| Modos | `WITHDRAW_SINGLE`, `WITHDRAW_AREA`, `DEPLOY` calculados em `buildCastData` |
| Deploy Y | `DEPLOY_Y_OFFSETS={0,1,-1,2,-2}`; `findDeployPositions` prioriza `dot(horizontal,forward)*100 - dist² - |yOffset|` |
| Estado | `TamersPocketState`: `storedPets`, `clientSyncedStoredPetCount`, `StoredPet(entryId, entityTypeId, entityData, storedGameTime, displayName)` |
| Cura no deploy | `heal(max(0, (gameTime - storedGameTime)/1200))` |
| Sincronia | `TamersPocketSync.syncToClient(player)` após guardar/remover pets |

Bytecode: scratch/javap1011_evocation7.txt (`javap -classpath <JAR> -p -s -c`, 94 classes, EXIT=0, SHA-256 `AF225F42FA1A0295D7339542D49620FBA0D0BE6599147EEDF69B75744730DB41`); decompilação de apoio: scratch/evocation7_sources.txt (46 fontes Vineflower 1.12.0, SHA-256 `05090319D9206171C8C4C38ED1A33479F0F1313F9135B5D70146F5559EB80DB1`). Constantes e fórmulas decisivas foram confrontadas com o bytecode; em divergência, o bytecode prevalece.

## 3. Casting / execução

1. `checkPreCastConditions` exige `ServerPlayer` e chama `buildCastData`.
2. `buildCastData` prioriza `findLookTarget`: raycast de `8.0` blocos com raio `0.5`, filtrado por `isOwnedPetBy`; sucesso gera `WITHDRAW_SINGLE` com o UUID.
3. Sem alvo olhado, lê `TamersPocketState`: se `storedCount<=0`, procura pets próprios em `boundingBox.inflate(8.0)`, ordena por distância e gera `WITHDRAW_AREA`; falha envia `no_pets`.
4. Com pets armazenados, `findDeployPositions` varre X/Z de `-range..range` com `dist²<=range²`, os cinco offsets Y, filtra `isSafeDeployPosition` e ordena por prioridade; falha envia `no_safe_place`.
5. `onCast` aplica `withdrawLockedPets` ou `deployStoredPets` conforme o modo; `NONE` não faz nada.
6. `withdrawLockedPets` localiza a entidade por UUID no servidor, exige dono, captura tipo/NBT/tempo/nome, ejeta passageiros, descarta a entidade e grava no estado.
7. `deployStoredPets` usa `EntityType.loadEntityRecursive`, reatribui o dono, adiciona com passageiros, cura conforme tempo armazenado e remove as entradas com sucesso; `onServerCastComplete` limpa o cast data.

## 4. Targeting / geometria

| Propriedade | Valor e consumidor |
|---|---|
| Modo single | Pet olhado em raycast de `8.0` blocos, raio `0.5`, `isOwnedPetBy` |
| Modo área | Pets próprios em `boundingBox.inflate(8.0)`, vivos e ordenados por distância |
| Modo deploy | Posições seguras em X/Z até `8.0`, Y em `{0,1,-1,2,-2}`; exige volume `3×3×3` de ar, suporte (bloco sólido ou água) e AABB `inflate(1.0)` livre; prioridade `dot(horizontal,forward)*100 - dist² - |yOffset|*6`; reserva AABB `inflate(1.0)` sem sobreposição |
| Filtro de dono | `isOwnedPetBy` no pre-cast e novamente no saque; `ensureOwnedByCaster` no deploy |
| Armazenamento | `StoredPet` com UUID próprio, tipo, `saveWithoutId`, tempo de jogo e nome opcional |
| Cura | `+1` por `1200` ticks armazenados, sem teto declarado no código |
| Persistência | `TamersPocketState` em `CodexSpellData`, com contagem sincronizada ao cliente |

## 5. Resultado

- Não causa dano, cura direta, status, projétil ou knockback (`N/A` com justificativa: teleporte/armazenamento de pets).
- `WITHDRAW_SINGLE` e `WITHDRAW_AREA` descartam entidades e gravam NBT; `DEPLOY` recria entidades e aplica cura passiva proporcional ao tempo.
- `deployStoredPet` só remove a entrada se `tryAddFreshEntityWithPassengers` e `ensureOwnedByCaster` tiverem sucesso.
- `clientSyncedStoredPetCount` separa a contagem exibida no cliente da lista real no servidor.

## 6. Scaling e caps

| Parâmetro | Fórmula literal | Unidade / ownership |
|---|---|---|
| Spell power | `0 + 0*(level-1)`; nenhuma fórmula consulta poder |
| Alcance | `8.0` blocos para raycast e área de pets |
| Modos | 3 (`WITHDRAW_SINGLE`, `WITHDRAW_AREA`, `DEPLOY`) |
| Offsets Y | `{0,1,-1,2,-2}` |
| Cura no deploy | `max(0, (gameTime - storedGameTime)/1200)` pontos |
| Mana | `50 + 0*(level-1)` declarado; efetivo **NÃO VERIFICADO** |
| Cooldown | `4.0` s declarado |
| Cast time | `20` ticks (`CastType.LONG`) |

## 7. Possibilidades de perks

- **A — atributo nativo:** nenhum parâmetro responde a poder; alcance e offsets são constantes.
- **B — evento verificado:** `TamersPocketSync` é sincronia de estado, não hook de modificação.
- **C — adapter condicionado:** mudar alcance, offsets ou cura exigiria substituir `TamersPocket`/`TamersPocketState` com risco de perda ou duplicação de pets. **CONDICIONADO**.
- **D — sem hook demonstrado:** nenhuma API segura para alterar o número de pets ou a cura sem corromper estado persistido. **NO_MUTATION** / fail-closed.

- `mutating_hook = NOT_VERIFIED`; `mutation = NO_MUTATION` (fail-closed).

## 8. Causalidade

`pre-cast escolhe modo → cast guarda ou deploya pets → estado persistido em CodexSpellData → sincronia ao cliente → limpeza do cast data`.


## 9. Concepção de nova magia

Assinatura ocupada: bolso que guarda e recoloca pets próprios com cura proporcional ao tempo. Nenhuma implementação foi realizada.

## 10. Verificação e pendências

- ✅ identidade/hash, construtor `0/0/50/0/20`, alcance `8.0`, três modos, offsets Y, prioridade de deploy, cura `/1200`, NBT de `StoredPet` e sincronia confirmados no bytecode 1.0.1.1.
- ⚠️ mana/cooldown efetivos, comportamento real de `isSafeDeployPosition`, dono de pets modulares e sobrevivência a restart permanecem `NÃO VERIFICADOS`.
- ⚠️ `physical_qa=NOT_TESTED`: sem Survival, montarias, portais, reload ou duplicação de pets observada.
- ⚠️ Universo integral do provider não encerrado; homologação integral permanece `NOT_CERTIFIED`.


## Localizadores para Codex — resumo operacional

Assinatura ocupada: bolso que guarda e recoloca pets próprios com cura proporcional ao tempo. Nenhuma implementação foi realizada.

- Consultar [`EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md`](../EXACT-TECHNICAL-CONTRACTS-1.0.1.1.md).
