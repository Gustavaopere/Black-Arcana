# Gazing Pearl — SavedData/DimensionDataStorage no servidor NeoForge 21.1.248

**Status do recorte:** 🟡 auditoria técnica transitiva **read-only** da engine distribuída. A ficha individual `alexscaves:gazing_pearl` continua **⚠️ PARCIAL**. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`. Não constitui spell, cast, novo efeito, hook mutador ou raiz semântica.

## Identidade e cadeia de autoridade

- **Mod:** Alex's Caves Continued `1.0.10`, mod ID `alexscaves`, JAR listado fisicamente como `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 da modlist sibling `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. O JAR publisher anteriormente auditado tem SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; paridade com a cópia instalada continua **NOT_VERIFIED**.
- **Engine exata da build:** `Minecraft 1.21.1` / `NeoForge 21.1.248` / Java 21, como `gradle.properties` da `main`. O workflow descarrega o **instalador oficial** do Maven NeoForge, SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`, executa `--installServer` e compara as bibliotecas distribuídas: `neoforge-21.1.248-server.jar` de **5.675.624 bytes**, SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`, e `server-1.21.1-20240808.144430-srg.jar` de **14.246.609 bytes**, SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`.
- **Fonte precisa do classfile:** em todos os três owners abaixo, a classe foi encontrada no **overlay NeoForge**, e não escolhida por fallback ao SRG. Esses são bytes da **distribuição oficial instalada em ambiente isolado**, não a classe depois de patches adicionais, mixins ou execução via ModLauncher no modpack do usuário.
- **Evidência:** [workflow #45016249706](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45016249706), [artifact #14751558128](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45016249706/artifacts/14751558128), `report.json` com **64.217 bytes**, SHA-256 `8a16f6041ad4f917295d8d757a531f449c307bcde6cc31d6f5af4da925b847ac`. [Probe](../../../../docs/qa/neoforge_211248_gazing_pearl_saveddata_engine_probe.py), [manifesto SHA-exato](EXACT-NEOFORGE-211248-GAZING-PEARL-SAVEDDATA-ABI.json), [checker fail-closed](../../../../docs/qa/neoforge_211248_gazing_pearl_saveddata_engine_checks.py) e [workflow](../../../../.github/workflows/neoforge-211248-gazing-pearl-saveddata-engine.yml). O checker e seus testes negativos ainda dependem da **CI da HEAD final**; a execução inicial certificou apenas a extração.

## 1. Fábrica de SavedData — configuração e null DataFixTypes

`net/minecraft/world/level/saveddata/SavedData$Factory`, class SHA-256 `46cf90d6ca49802a7a4fb4a2ef63686e209893b4b4128bf044ec82a6d861d8dc`, 3 campos (`constructor:Supplier`, `deserializer:BiFunction`, `type:DataFixTypes`), 8 métodos declarados, 4 corpos selecionados.

A versão oficial possui dois construtores: `Factory(Supplier,BiFunction)` (6 instruções), que fornece literalmente `null` ao construtor de 3 argumentos em @3–4, e `Factory(Supplier,BiFunction,DataFixTypes)` (12 instruções), que atribui os três campos @6/@11/@16. Os acessores `deserializer()` e `type()` devolvem os campos armazenados sem mutação. Isso corrobora a compatibilidade do `ACPlatform.computeIfAbsent` do publisher com a factory de 3 parâmetros, fornecendo `DataFixTypes=null`.

Não inferir a partir da assinatura que outro `Function` da ponte de Alex's Caves seja utilizado: seu corpo nativo já foi mostrado como não carregando o segundo argumento.

## 2. DimensionDataStorage — cache e fallback

`net/minecraft/world/level/storage/DimensionDataStorage`, class SHA-256 `6316f03f8ff914c9d7f26fd91359ae98af449f7894e423a2209144e7181e3993`, 5 campos (`LOGGER`, `cache`, `fixerUpper`, `registries`, `dataFolder`), 12 métodos declarados, **7 corpos selecionados**.

| Método | Offset JVM comprovado | Consequência estritamente estática |
|---|---|---|
| `computeIfAbsent(Factory,String)` — 20 instruções | `get` @3, `ifnull` @8→13, `Supplier.get` @17 e `set(name,new)` @31 | Se `get` devolver objeto não nulo, retorna-o; caso contrário cria instância e a coloca no cache |
| `get(Factory,String)` — 29 instruções | `cache.get` @5, `ifnonnull` @15; `cache.containsKey` @23 e `ifne` @28→57 | Se a chave já está no mapa com valor `null`, não tenta reler arquivo nesse `get` |
| `get(Factory,String)` | `Factory.deserializer` @33, `Factory.type` @37, `readSavedData` @41 e `cache.put(name,result)` @51 | Em cache miss real, faz uma tentativa de carga e memoriza seu resultado, inclusive `null`; o wrapper `computeIfAbsent` então cria um novo valor se continuar nulo |
| `set(String,SavedData)` — 7 instruções | `cache.put` @6 | Registra apenas o objeto no cache; o corpo desse `set` não solicita `setDirty` |
| `save()` — 6 instruções | `Map.forEach` @10 | Encaminha os objetos do mapa ao consumer sintético; o corpo da lambda de `save()` **não foi auditado** neste recorte |
| `getDataFile(String)` — 8 instruções | criação de `File` e concatenação dinâmica @9 | Resolve caminho relativo ao `dataFolder`; o sufixo de concatenação requer análise separada do bootstrap |
| `readSavedData(...)` — 33 instruções | existência de arquivo @9; `readTagFromDisk` @29; `getCompound("data")` @39; `BiFunction.apply` @46 | Carrega NBT pelo nome e entrega o composto `data` ao deserializador junto com `registries` |

**Falha de leitura:** `readSavedData` possui handler `java/lang/Exception` que cobre offsets **0–54**, inicia em **@58**, registra erro e retorna `null` @73–74. Em seguida, o `computeIfAbsent` que invocou `get` pode construir e registrar objeto novo. Isso representa **risco de perda de estado preexistente se um arquivo inválido vier a ser substituído depois**, mas não há prova de que qualquer arquivo real foi corrompido, nem de sobrescrita efetivamente ocorrida.

## 3. DataFixTypes, NBT e fluxo de I/O

`DimensionDataStorage.readTagFromDisk(String,DataFixTypes,int)` possui **97 instruções**, Code SHA `fa08c2c79a1bfe904b94fdc1491ce7f51a2e350648693ca2a8fa08427e2d2230`. Escolhe a via NBT comprimida (`NbtIo.readCompressed` @51, com `NbtAccounter.unlimitedHeap` @48) ou não comprimida (`NbtIo.read` @72). **O campo DataFixTypes da factory é testado em @107–108**: `ifnull → @139` pula `DataFixTypes.update` @131. Assim, o `null` entregue pelo adaptador de Alex's Caves **não produz chamada ao DataFixer nesse ramo JVM**. Isso não equivale a validar compatibilidade de um save antigo concreto.

O mesmo método invoca `IOUtilities.withIOWorker` @210 após leitura e antes do retorno @215. O [dossiê da implementação distribuída do worker](EXACT-NEOFORGE-211248-GAZING-PEARL-IOWORKER-ABI.md) demonstrou que `withIOWorker(Runnable)` usa `CompletableFuture.thenRunAsync(Util.ioPool)` sem aguardar diretamente o término. **Isso não prova a conclusão nem a durabilidade dessa leitura/escrita**; a semântica das tarefas específicas permanece separada.

## 4. SavedData — dirty, serialização e ordem de escrita

`net/minecraft/world/level/saveddata/SavedData`, class SHA-256 `b55a20a77d7f3d4a69c7af79240d6bf14cfa4c7536414a70543030631b265310`, 2 campos (`LOGGER`, `dirty:boolean`), 8 métodos declarados, **4 corpos executáveis selecionados** e uma declaração abstrata, `save(CompoundTag,HolderLookup.Provider):CompoundTag`, **sem atributo JVM `Code`**. A implementação concreta desse método é responsabilidade da subclasse como `ACWorldData`; não confundir a declaração abstrata com a sobrecarga de arquivo.

- `isDirty():boolean` devolve o campo `dirty` @1; `setDirty()` chama `setDirty(true)` @2; `setDirty(boolean)` grava o campo @2.
- `save(File,HolderLookup.Provider)` possui **32 instruções**. Em @1 lê `isDirty`; se falso, `ifeq` @4→62 evita todo o corpo da serialização. Caso verdadeiro, solicita o `save(CompoundTag,Provider)` virtual @27, coloca seu resultado sob a chave NBT `data` @30, adiciona `DataVersion` atual @35 e prepara uma cópia `CompoundTag.copy` @40.
- No mesmo ramo, chama `IOUtilities.withIOWorker` @54 para agendar um `Runnable` de escrita e **somente depois** solicita `setDirty(false)` @59. O [recorte SHA-exato das lambdas e do worker](EXACT-NEOFORGE-211248-GAZING-PEARL-IOWORKER-ABI.md) demonstra `CompletableFuture.thenRunAsync` e a captura/log de `IOException` pelo `Runnable`, mas a conclusão e a durabilidade do I/O após crash continuam **NOT_VERIFIED**. O método `save(File,Provider)` não possui handler próprio de exceção no classfile verificado.

Relacionando com o [dossiê ACWorldData](EXACT-GAZING-PEARL-WORLDDATA-1.0.10.md): `ACWorldData.get(Level)` solicita `setDirty()` em leituras com storage não nulo. Esse sinal é relevante para o ciclo posterior de `SavedData.save`, mas **não demonstra quantas vezes o servidor gravou** nem autoriza escrita de perks.

## Limites, targeting, integração e QA

Esta é uma cadeia de persistência do mundo, não um efeito ofensivo. Dano, tipo de dano, hitbox, AOE, projéteis, mana, duração e cooldown **N/A** para a infraestrutura; a identificação por UUID, limiares de reputação, guardas de lado servidor, receita e snapshot de ItemStack pertencem à ficha [Gazing Pearl](items/gazing-pearl.md). O storage global fica associado à chave `alexscaves_world_data` no Overworld segundo o caller publisher; nenhum arquivo `data/alexscaves_world_data.dat` foi aberto nesta auditoria.

O [guia oficial NeoForge Saved Data da série 1.21.1](https://docs.neoforged.net/docs/1.21.1/datastorage/saveddata/) também descreve `setDirty` e `computeIfAbsent`. Entretanto, este dossiê prioriza **classfiles distribuídos com hash exato**, e não exemplos genéricos ou código de outra versão.

**Pendente para uma conclusão mais abrangente:** o [worker e as duas lambdas sintéticas de `save` foram auditados na distribuição oficial](EXACT-NEOFORGE-211248-GAZING-PEARL-IOWORKER-ABI.md), e o [corpo de `IOUtilities.writeNbtCompressed`/`atomicWrite` também foi analisado na distribuição](EXACT-NEOFORGE-211248-GAZING-PEARL-WRITE-NBT-ABI.md). Ainda faltam garantias físicas do filesystem, política de exceções não-IOException e execução do pool, `NbtIo.writeCompressed`, dataversions e verificação com modloader carregado, outros transforms, bytes do JAR físico, layout real, reinício/rollback, sincronização dos componentes/tooltip e QA em cliente/servidor com modpack. Sem hook real e seguro, **NO_MUTATION/fail-closed**; não houve incremento dos contadores de progresso ou promoção da Gazing Pearl.
