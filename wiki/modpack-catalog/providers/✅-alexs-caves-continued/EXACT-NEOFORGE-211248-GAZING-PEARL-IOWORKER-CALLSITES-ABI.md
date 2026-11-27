# Gazing Pearl — consumidores de `waitUntilIOWorkerComplete` no NeoForge 21.1.248

**Estado: ⚠️ recorte estático da engine, não certificação individual.** O objeto `alexscaves:gazing_pearl` segue com `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. O provider continua `OPEN`. Esta análise não conta novas raízes mágicas nem altera runtime, progressão, mana ou perks.

## Evidência e delimitação

- **Provider:** Alex's Caves Continued `alexscaves` 1.0.10, JAR físico declarado `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` conforme modlist sibling. Publisher anteriormente examinado SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Não foi provada a paridade byte-a-byte com a instalação física do usuário.
- **Engine:** Minecraft 1.21.1, NeoForge 21.1.248, Java 21. Instalador oficial SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`. `neoforge-21.1.248-server.jar`: 5.675.624 bytes, SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`; `server-1.21.1-20240808.144430-srg.jar`: 14.246.609 bytes, SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`; `neoforge-21.1.248-universal.jar`: 3.551.268 bytes, SHA-256 `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`.
- **Descoberta:** [run #45062154362](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45062154362), [artefato #14770385280](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45062154362/artifacts/14770385280), `report.json` 22.710 bytes, SHA-256 `54411e230dbf04fe72faedae3b96e513524739a4592d1c56646d48e797cc1725`. [Sonda de censo read-only](../../../../docs/qa/neoforge_211248_ioworker_completion_callsite_probe.py), [manifesto SHA-exato](EXACT-NEOFORGE-211248-GAZING-PEARL-IOWORKER-CALLSITES-ABI.json), [checker causal](../../../../docs/qa/neoforge_211248_ioworker_completion_callsite_checks.py) e [workflow](../../../../.github/workflows/neoforge-211248-ioworker-completion-callsites.yml). A primeira tentativa de censo falhou por um limite de tamanho de classe inadequado à classe legítima `BlockStateData`; o limite foi corrigido e a segunda coleta passou. Isso **não** altera a integridade dos hashes da distribuição.

O censo percorreu **9.243 classfiles** distribuídos nos três arquivos: 1.603 do overlay, 6.148 do Minecraft SRG e 1.492 do universal. Primeiro verificou referências tipadas `CONSTANT_Methodref`/`InterfaceMethodref` exatas; depois desassemblou **somente classes candidatas** e cruzou operandos reais `invoke*` com índices de constant pool. Foram encontrados **dois candidatos/duas chamadas diretas**, ambos no overlay. Nenhuma referência exata foi encontrada nos outros dois JARs. Isso **não** constitui censo da totalidade do classpath do ModLauncher, mods do pack, mixins ou classes transformadas.

## Consumidores concretos, condições e ordem

| Classe de caller | Método/descriptor | Classfile SHA-256 | Code SHA-256 | Offset da chamada |
|---|---|---|---|---|
| `net/minecraft/server/level/ServerLevel` | `save(ProgressListener,boolean,boolean):void` | `19b42e51848fd27df3683dacf694baa5126ee9f0665f12afdc65f82493a1e5a3` | `9d5744651dacb59b8108ef18fc0088c11a594561476feb28f6f20fe025617706` | `invokestatic #1324` @94 |
| `net/minecraft/util/worldupdate/WorldUpgrader` | `work():void` | `f0349c7a436bb8216c5c4d0ab06c0bdb15a6181bfc8f80a1289413eff551bd97` | `45f2cc76455e13cde6d0c4b2c3d391c86986d68c43ee37a19437e6de1f13d8b6` | `invokestatic #213` @74 |

### 1. `ServerLevel.save`

O método tem 42 instruções JVM, instruction SHA-256 `cf0feca69062c125ba9dd7ba62b0e5df908692a2d2d69e7a4d1b86589d4377a9`. Seu **terceiro argumento posicional** (índice local 3) é testado por `ifne 97` @7: quando verdadeiro, o corpo de salvamento salta direto ao `return` @97. Quando não salta, solicita `saveLevelData()` @27, `ServerChunkCache.save(boolean)` @49, escolhe `entityManager.saveAll()` ou `autoSave()` conforme o **segundo booleano** (índice local 2; ramo @53), e publica `LevelEvent.Save` @84. Depois, `iload_2` @90 + `ifeq 97` @91 condicionam a chamada `IOUtilities.waitUntilIOWorkerComplete()` @94.

**Interpretação causal limitada:** a chamada existe em salvamentos que passam por esse método, **não** no ramo de skip, e só é alcançável quando o segundo booleano é verdadeiro. A mera presença desse método não prova os valores enviados por `MinecraftServer`, nem que toda rotina de desligamento execute essa trajetória ou que o `CompletableFuture.join()` conclua durabilidade física. Identificar os callers e parâmetros de `ServerLevel.save` no encerramento é um **próximo recorte distinto**.

### 2. `WorldUpgrader.work`

O método possui 45 instruções JVM, instruction SHA-256 `865b2ae2f5b08879062c0ff0b7d71c9818d5c1ae7a0a78bf3d745f170c008b43`. Depois das rotinas de atualização de entidades, POIs e chunks, solicita `overworldDataStorage.save()` @71, chama **diretamente** `IOUtilities.waitUntilIOWorkerComplete()` @74 e registra a duração da otimização, terminando com `finished=true` @103. Não foi identificada guarda condicional local entre @71 e @74 no corpo observado; exceções, intervenção de outros mods e execução real não foram testadas.

Esse caminho é **atualização/otimização do mundo**, não é por si prova da política de shutdown normal do servidor.

## Relação com Gazing Pearl, hooks e persistência

A cadeia de dados anterior estabeleceu `ACWorldData` → `SavedData` → `DimensionDataStorage` → `IOUtilities.withIOWorker` → `NbtIo.writeCompressed` → `CompoundTag.write` e suas implementações. Este recorte acrescenta **dois consumidores estáticos** do método de espera, já auditado anteriormente em `IOUtilities` como `saveDataTasks.join()` e reset da referência. A espera pode reduzir a distância entre *agendamento* e *conclusão do future* quando o ramo é atingido, mas **não comprova arquivo válido, flush do diretório, atomicidade universal, recuperação após crash, chamada em todo stop, nem sincronização de estado de reputação ao cliente**. Falhas assíncronas e seus efeitos requerem observação própria.

Nenhuma instrução identificada constitui ponto de modificação autorizado para perks. Não alterar `ACWorldData`, não interceptar `ServerLevel.save` para simular progresso e não contabilizar XP por leitura da Gazing Pearl. O Black Arcana mantém autoridade apenas sobre seu runtime mágico; integrações externas continuam `NO_MUTATION` / fail-closed.

**Evidência posterior:** o [censo estático de `MinecraftServer.saveAllChunks`/`stopServer`](EXACT-NEOFORGE-211248-GAZING-PEARL-SERVERLEVEL-SAVE-CALLSITES.md) verificou que o bytecode distribuído chama `saveAllChunks(false,true,false)` durante `stopServer` e encaminha `save(null,true,false)` a `ServerLevel.save`, atingindo a espera @94 no percurso estático sem exceções. **Pendências para conclusão individual:** execução física do shutdown, outros JARs/mixins, bytes pós-ModLauncher, `alexscaves_world_data.dat` em save/restart, QA cliente/servidor no pack, API/hooks reais e demais dependências individuais de Gazing Pearl. `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` e provider `OPEN`.