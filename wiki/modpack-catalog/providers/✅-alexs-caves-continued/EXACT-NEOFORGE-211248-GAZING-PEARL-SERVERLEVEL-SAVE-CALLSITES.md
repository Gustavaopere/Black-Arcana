# Gazing Pearl — cadeia JVM de save e shutdown até `waitUntilIOWorkerComplete` (NeoForge 21.1.248)

**Estado:** ⚠️ **auditoria estática e read-only de engine distribuída**, sem certificação do objeto. `alexscaves:gazing_pearl` mantém `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; universo do provider `OPEN`. Esta cadeia não cria novo cast, feitiço, efeito ou objeto mágico, nem altera contagens.

## 1. Procedência

- **Modpack:** Minecraft 1.21.1, NeoForge **21.1.248**, Java 21. Alex's Caves Continued **1.0.10**, mod ID `alexscaves`, JAR declarado `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 físico declarado `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` (modlist sibling). Paridade byte-a-byte com a instância real **não verificada**; nenhum client/server real foi iniciado.
- **Distribuição auditada:** instalador NeoForge 21.1.248 SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`; server overlay SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359` (1.603 classfiles), Minecraft server SRG SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71` (6.148 classfiles), NeoForge universal SHA-256 `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5` (1.492 classfiles).
- **Dois censos SHA-exatos sobre os mesmos 9.243 classfiles**, com referências tipadas do constant pool separadas de instruções JVM reais:
  1. `ServerLevel.save(ProgressListener,boolean,boolean)` — relatório `report.json` **45.105 bytes**, SHA-256 `70ea6910ab39cf59d2c3b1a3347aa54d09dbdfe98f65dee42356c555c23ec4b8`.
  2. `MinecraftServer.saveAllChunks(boolean,boolean,boolean)` — relatório `saveallchunks_report.json` **68.068 bytes**, SHA-256 `979f36eee46e8848216ad8429208627a68a4ae18654dd1073c9bf1ff5b562708`.
- **Descoberta reproduzível:** [workflow GitHub #45067244452](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45067244452) e [artefato #14772170804](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45067244452/artifacts/14772170804). Sonda: [`docs/qa/neoforge_211248_serverlevel_save_callsite_probe.py`](../../../../docs/qa/neoforge_211248_serverlevel_save_callsite_probe.py). Manifesto: [`EXACT-NEOFORGE-211248-GAZING-PEARL-SERVERLEVEL-SAVE-CALLSITES.json`](EXACT-NEOFORGE-211248-GAZING-PEARL-SERVERLEVEL-SAVE-CALLSITES.json); [checker causal](../../../../docs/qa/neoforge_211248_serverlevel_save_callsite_checks.py), [teste adversarial](../../../../docs/qa/neoforge_211248_serverlevel_save_callsite_negative.py), [workflow](../../../../.github/workflows/neoforge-211248-serverlevel-save-callsites.yml). O selo final depende da CI da **HEAD final**, distinta do workflow de descoberta.

## 2. Identidades de métodos e consumidores diretos

A varredura identifica **callers na distribuição auditada**, não todas as classes potencialmente transformadas/adicionadas por mods e ModLauncher.

| Alvo | JAR | Método caller | Offset JVM | Comportamento observado |
|---|---|---|---:|---|
| `ServerLevel.save(ProgressListener,ZZ)V` | Overlay | `MinecraftServer.saveAllChunks(ZZZ)Z` | @82 | `invokevirtual` depois de montar argumentos/skip de noSave |
| Mesmo | Minecraft SRG | `MinecraftServer.saveAllChunks(ZZZ)Z` | @82 | Equivalente estrutural, Code SHA diferente da versão overlay |
| Mesmo | NeoForge universal | `GenerationTask.lambda$acceptChunkResult$5()V` | @7 | Chama com terceiro argumento = true; `ServerLevel.save` pula o corpo |
| `MinecraftServer.saveAllChunks(ZZZ)Z` | Overlay | `MinecraftServer.saveEverything(ZZZ)Z` | @16 | Encaminha seus três booleans sem substituição |
| Mesmo | Overlay | `MinecraftServer.stopServer()V` | @224 | Chama com **(false, true, false)** |
| Mesmo | Minecraft SRG | `saveEverything(ZZZ)Z` e `stopServer()V` | @16 / @224 | Dois consumidores equivalentes na build SRG |
| Mesmo | NeoForge universal | Nenhum caller direto | — | Resultado restrito a este JAR |

**Hashes da classe concreta MinecraftServer:** overlay SHA-256 `3f1b7a260a249ae836d9d71bf0a0fe7575b62aff48f2b8fac10dd06aaa9efd2f`; SRG SHA-256 `b2c008639af4ff9a4c108494ecab7ec4d4c89a228fd461b7eeb76d51f424ce52`. O selo fixa também SHA de Code/instruções e contagens para os **sete métodos** observados entre os dois relatórios; não mistura offsets de outras versões.

## 3. Caminho de `stopServer` distribuído

O método `net.minecraft.server.MinecraftServer.stopServer():void` no overlay, Code SHA-256 `6dae566c783e0299191ddefbd767276b0af2c62dc4f065361632e2d17d919430`, tem **136 instruções JVM**. Sequência causal selecionada:

1. @27–31: solicita `ServerConnectionListener.stop()`. @34–36: escreve `isSaving=true`. @39–68: quando existe player list, chama `saveAll()` e `removeAll()`.
2. @82–120: itera os níveis; para cada nível não nulo, executa `iconst_0` @116 e `putfield ServerLevel.noSave` @117. Isso **limpa a flag** `noSave` dos níveis percorridos.
3. @123–217: solicita verificações/ticks de chunks e aguarda ciclo de tickets com `waitUntilNextTick()`, conforme as condições do loop do método; não foi avaliada duração real ou garantia de terminação.
4. @220–224: carrega `aload_0`, `iconst_0`, `iconst_1`, `iconst_0` e `invokevirtual MinecraftServer.saveAllChunks(ZZZ)Z`. Os três argumentos são **(false, true, false)** nessa chamada estática de shutdown.
5. @261–279: publica `LevelEvent.Unload` e solicita `ServerLevel.close()`; @301–319: limpa `isSaving` e solicita fechamento de recursos e do acesso ao armazenamento. Isso estabelece **ordem de solicitações do bytecode**, não comprova que as ações terminem corretamente em execução física.

No SRG, `stopServer()V` também chama `saveAllChunks(ZZZ)Z` @224, mas tem **129 instruções** e Code SHA-256 distinto. O caminho de NeoForge **overlay** prevalece para os detalhes dos eventos Forge; não inferir equivalência byte-a-byte.

## 4. Encaminhamento dos três booleans

`MinecraftServer.saveAllChunks(ZZZ)Z` (overlay, Code SHA-256 `141333cba3001dc03409adc7b92e5fe800e7e1f3c33b9badda4cd09fe6f9ce66`, 93 instruções) faz:

- @63 passa `ProgressListener=null`; @64 passa **o segundo parâmetro booleano da função** (`iload_2`) sem transformá-lo para o segundo parâmetro de `ServerLevel.save`.
- @65–81 calcula o terceiro booleano de `ServerLevel.save`: lê `ServerLevel.noSave` @67; se for falso, resulta em 0. Se for verdadeiro, lê o terceiro parâmetro de `saveAllChunks` @73; quando este é **falso**, o argumento de skip resulta em 1; se verdadeiro, resulta em 0. A expressão equivalente é `noSave && !arg3`.
- @82 chama `ServerLevel.save(null,arg2,noSave && !arg3)`. @91–162 trata world border, dados do mundo e escreve world-data tag; @165–238 contém log adicional quando o segundo parâmetro é verdadeiro. Esses últimos passos não comprovam, por si, atomicidade ou durabilidade do nível.
- Para o `stopServer` acima, os argumentos são `saveAllChunks(false,true,false)`. Como a rotina limpou `noSave` nos níveis não nulos, o `ServerLevel.save` chamado pela engine é **`save(null,true,false)`**, no percurso estático normal sem exceções/intervenções.

A [auditoria anterior dos consumidores de I/O](EXACT-NEOFORGE-211248-GAZING-PEARL-IOWORKER-CALLSITES-ABI.md) comprovou que o `ServerLevel.save` efetivo do **overlay** rejeita o corpo quando seu terceiro parâmetro é verdadeiro (@6–7) e, quando o segundo é verdadeiro, chama `IOUtilities.waitUntilIOWorkerComplete():void` @94 após solicitar `saveLevelData`, `ServerChunkCache.save`, `entityManager.saveAll` e publicar `LevelEvent.Save`. O método da [auditoria IOUtilities](EXACT-NEOFORGE-211248-GAZING-PEARL-WRITE-NBT-ABI.md) chama `CompletableFuture.join()` sobre a cadeia `saveDataTasks`, mas `join()` não é prova de sucesso de escrita, arquivo fisicamente persistido ou tolerância a falha de energia.

## 5. Outros caminhos e limites

- `MinecraftServer.saveEverything(ZZZ)Z` chama `PlayerList.saveAll()`, encaminha seus três argumentos sem alteração para `saveAllChunks(ZZZ)Z` @16 e limpa `isSaving` no fluxo normal e no handler; os **callers de saveEverything e seus valores de argumentos** não foram explorados neste recorte.
- `GenerationTask.lambda$acceptChunkResult$5()` no universal invoca `ServerLevel.save(null,false,true)` @7; o último `true` faz o corpo de save retornar. Não conta como chamada que execute gravação do nível ou espera de I/O nesse método.
- Os dois censos usam classes **distribuídas**; não incluem classes pós-transformação, outros mods, injeções, handlers de eventos, snapshots de disco, estado do servidor, erros de I/O, cronologia real do `CompletableFuture`, conteúdos de `alexscaves_world_data.dat` ou manipulação manual do processo.
- **PENDENTE:** validar com QA física server save/stop/restart, arquivos NBT reais antes/depois, recuperação pós-crash, arquivo íntegro e coerência da reputação Deep One por UUID, paridade do JAR físico, ModLauncher/mixins e hooks legítimos (se existirem). A verificação de que `stopServer()` **sempre é invocado**, de que todos os ramos concluem e de que um worker não termina excepcionalmente não foi feita.

**Interoperabilidade e perks:** a reputação dos Deep Ones permanece **authority do provider**. Uma cadeia de persistência da engine não constitui hook mutador de reputação. Black Arcana não escreve nem altera bytes NBT do provider; RPG Skill Tree só poderá integrar gate/perk com boundary real e auditado, sem novo pipeline de save, conflito de owner ou duplicação. **`NO_MUTATION` / fail-closed.**

**Estados e contadores:** `static_contract=NOT_CERTIFIED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; provider `OPEN`; nenhum objeto novo, nenhuma promoção a ✅, nenhum progresso ou índice numérico alterado.
