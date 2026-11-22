# Gazing Pearl — escrita SavedData, lambdas JVM e IOUtilities (NeoForge 21.1.248)

**Estado:** ⚠️ parcial, com recorte transitivo de engine distribuída SHA-exato; não certifica o item nem um hook. `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION` e provider `OPEN`. **Esta ponte de persistência não constitui novo spell, cast, buff ou raiz semântica.**

## Autoridade e proveniência

**Provider:** Alex's Caves Continued `alexscaves`, JAR registrado na modlist física sibling `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. O publisher 1.0.10 previamente auditado tem SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; **o arquivo instalado do usuário não foi copiado ou comparado byte a byte**.

**Engine real de referência:** Minecraft 1.21.1, NeoForge **21.1.248**, Java 21. O [workflow nativo #45020412060](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45020412060), após o diagnóstico de localização da classe, executou `--installServer` com instalador Maven SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`. Bibliotecas verificadas: overlay `neoforge-21.1.248-server.jar` (5.675.624 bytes, SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`) e Minecraft SRG `server-1.21.1-20240808.144430-srg.jar` (14.246.609 bytes, SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`).

**Diferença de empacotamento confirmada:** `DimensionDataStorage` e `SavedData` vieram do overlay NeoForge; `net.neoforged.neoforge.common.IOUtilities` não está nesses dois JARs, mas foi localizada **uma única vez** no `libraries/net/neoforged/neoforge/21.1.248/neoforge-21.1.248-universal.jar` (3.551.268 bytes; SHA-256 `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`), classe SHA-256 `3c4cfda19b620562486ca18af3d7c095c94a54c31d1028bf8e5d9860952e115a`. Nenhum código foi executado pela auditoria: os dados vêm de classfile/constant pool e `javap` com checagens de estrutura e hash.

[Evidência ZIP #14753915176](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45020412060/artifacts/14753915176), `report.json` **27.045 bytes**, SHA-256 `5ee461aef0690a5180d0824f900ac6793e03eb0ceb65a0cf0dc0ce8787c9be16`. [Probe somente leitura](../../../../docs/qa/neoforge_211248_gazing_pearl_ioworker_lambda_probe.py), [manifesto SHA-exato](EXACT-NEOFORGE-211248-GAZING-PEARL-IOWORKER-ABI.json), [checker fail-closed](../../../../docs/qa/neoforge_211248_gazing_pearl_ioworker_lambda_checks.py) e [workflow](../../../../.github/workflows/neoforge-211248-gazing-pearl-ioworker-discovery.yml). A aprovação da **CI integral da HEAD final** é gate separado da extração inicial.

## 1. Chamada do cache → SavedData

`DimensionDataStorage.save():void`, class SHA `6316f03f8ff914c9d7f26fd91359ae98af449f7894e423a2209144e7181e3993`, Code SHA `4d9b55ddd4b2504d1c2eaf7d22331d9aba3e1c8bbfe71aa7bed8891b6ba2ab6b`, possui **6 instruções**. Carrega `cache` @1, cria um `BiConsumer` por `invokedynamic` @5 (CP **#223**, `BootstrapMethods[2]`) e chama `Map.forEach` @10. O bootstrap `LambdaMetafactory.metafactory` liga explicitamente o adaptador `REF_invokeVirtual` (kind 5) `DimensionDataStorage.lambda$save$1(String,SavedData):void`, Code SHA `aa760c83dab616be2f763436b8a90b1932f9e5c0cb526c9a069773595eac0127`.

`lambda$save$1` possui **10 instruções**. Guarda `SavedData != null` em @1 (ramo null→@17); em caso não nulo solicita `getDataFile(key)` @7, lê `registries` @11 e invoca `SavedData.save(File,Provider)` @14. Isso delimita um percurso **por entrada cacheada não nula**; não existe filtro de nome ligado especificamente à Gazing Pearl dentro do dispatcher genérico.

## 2. SavedData → função de escrita

`SavedData.save(File,HolderLookup.Provider):void`, class SHA `b55a20a77d7f3d4a69c7af79240d6bf14cfa4c7536414a70543030631b265310`, Code SHA `17391efcb49f300ec019d10d3c6ff49376ce4b821ce2f2823b579955241f44b5`, **32 instruções**. Reaproveita o contrato de [dirty/cache/load auditado](EXACT-NEOFORGE-211248-GAZING-PEARL-SAVEDDATA-ABI.md): `isDirty` @1, `ifeq` @4→62; quando verdadeiro, prepara a cópia NBT e cria `Runnable` por `invokedynamic` @49 (CP **#44**, `BootstrapMethods[0]`). Este bootstrap `LambdaMetafactory.metafactory` vincula o `REF_invokeVirtual` (kind 5) `SavedData.lambda$save$0(CompoundTag,File):void`.

O `Runnable` tem **12 instruções**, Code SHA `5119fbfa785c735cdb023b9ece9f39b71c409ebb2896e5b34798d12a6f994e60`. Solicita `File.toPath` @2 e `IOUtilities.writeNbtCompressed(CompoundTag,Path)` @5. Há **handler JVM para `java/io/IOException`**, protegido no intervalo de offsets **[0,8)** e iniciado em @11, que solicita `LOGGER.error("Could not save data {}",...)` @19 e termina em @24. Este fluxo prova **chamada de escrita e captura de IOException**, não que arquivo válido foi persistido. Exceções não abrangidas pelo handler (por exemplo, `RuntimeException`) exigem verificação separada.

`SavedData.save(File,Provider)` chama `IOUtilities.withIOWorker(Runnable)` @54 e, em seguida, `setDirty(false)` @59. A própria sobrecarga de `SavedData.save(CompoundTag,Provider)` continua **abstrata e implementada por subclasses**; não misturar assinatura abstrata e rotina de envio ao worker.

## 3. IOUtilities — agendamento assíncrono, sem bloqueio no método

`IOUtilities`, campo estático `saveDataTasks:CompletableFuture`, `<clinit>` com **18 instruções**, Code SHA `0bb043d2461fc95dc8ed4154dbc1065e036c38343f2b289fb52de2fe3ed6790c`: solicita `CompletableFuture.completedFuture(null)` @28 e armazena em `saveDataTasks` @31.

`withIOWorker(Runnable):void` tem **6 instruções**, Code SHA `f160c3418e9acf857b202582af5a798a0f2dfa22a2bd069b2c49e4154553bf42`:

- `getstatic saveDataTasks` @0 recupera o estágio anterior;
- `Util.ioPool()` @4 fornece um `ExecutorService`;
- `CompletableFuture.thenRunAsync(Runnable,Executor)` @7 cria o próximo estágio dependente;
- `putstatic saveDataTasks` @10 armazena o `CompletableFuture` retornado; `return` @13.

**Conclusão estática estrita:** o worker usa encadeamento assíncrono de `CompletableFuture` e **não invoca `join`, `get` ou outro bloqueio direto nesse corpo de seis instruções**. Portanto, a chamada em `SavedData.save` pode retornar após o agendamento, antes de o arquivo ser gravado. O indicador `dirty` é solicitado como falso após a chamada de agendamento, e a própria lambda de escrita captura `IOException` e registra erro. **Não foi observada** nesta cadeia uma confirmação da tarefa concluída antes de limpar dirty nem uma marcação automática dirty=true quando a escrita falha.

Isso é uma **possível lacuna de durabilidade/recuperação** a validar em condições reais, **não evidência de perda de dados** no servidor do usuário. Para concluir comportamento de arquivo atômico, concorrência e falha no pool, ainda são necessárias as implementações efetivas de `IOUtilities.writeNbtCompressed`, primitivas NIO, efeitos de ModLauncher/mixins e testes físicos.

## 4. Consequências para a Gazing Pearl

O grafo publicado e identificado permanece: `GazingPearlItem.acInventoryTick → ACWorldData.get(Level) → ACPlatform.computeIfAbsent → DimensionDataStorage.computeIfAbsent`; no salvamento do mundo, `DimensionDataStorage.save → lambda$save$1 → SavedData.save(File) → lambda$save$0 → IOUtilities.writeNbtCompressed`, intermediado por `withIOWorker`. O caller `ACWorldData.get` solicita `setDirty()` em resultado não nulo, mas a rotina de consulta não comprova gravação imediata nem resultado após reinício.

**Targeting, dano/tipo, AOE, projétil, custo de mana, duração e cooldown:** N/A no worker (infraestrutura de persistência). Identificação por UUID, tooltip, cor HSB, ticks, receita e condições de aquisição são tratadas separadamente na [ficha Gazing Pearl](items/gazing-pearl.md), não reclassificadas como magias. Nenhum evento/callback mutador por player/Perk/Mastery foi certificado; Black Arcana mantém autoridade do runtime e RPG Skill Tree permanece provider de progressão.

## 5. Limitações e próximos gates

O universo de objetos do mod permanece `OPEN`; a Gazing Pearl segue **⚠️ PARCIAL**. Este estudo **não** executou o jogo, o Java ModLauncher do usuário, o `IOUtilities.writeNbtCompressed`, a sincronização client/server, a migração e a persistência/recuperação do arquivo `alexscaves_world_data.dat`, nem comparou os bytes de mod instalado com o JAR publisher. A ordem de chamadas pode divergir de comportamento final caso outra transformação intercepte o código distribuído.

Ainda faltam auditoria de `writeNbtCompressed` e operações relacionadas (backup/temporário, exception, atomic move), QA física após crash e reinício, modpacks reais, sync de `CUSTOM_DATA` e demais consumidores de Deep One reputation. **Sem hook seguro real: `NO_MUTATION`/fail-closed; sem aumento de fichas certificadas, raízes, perks, QA ou Stage.**
