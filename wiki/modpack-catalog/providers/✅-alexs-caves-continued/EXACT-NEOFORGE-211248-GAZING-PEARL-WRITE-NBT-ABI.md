# Gazing Pearl — IOUtilities.writeNbtCompressed, atomicWrite e recuperação de arquivo (NeoForge 21.1.248)

**Escopo:** ⚠️ evidência técnica transitiva **estática e read-only**, exclusivamente dos bytes **distribuídos** oficialmente com NeoForge 21.1.248 / Minecraft 1.21.1. O objeto `alexscaves:gazing_pearl` continua `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, provider `OPEN`. A rotina de arquivo não constitui novo cast/objeto mágico.

## Autoridade, artefatos e rastreabilidade

- **Mod instalado declarado:** Alex's Caves Continued `1.0.10`, mod ID `alexscaves`, modlist sibling `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 declarado `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. O publisher auditado tem SHA256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; comparação byte-a-byte com a cópia física do modpack **NOT_VERIFIED**.
- **Distribuição:** instalador Maven `neoforge-21.1.248-installer.jar` SHA256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`; bibliotecas oficiais `neoforge-21.1.248-server.jar` 5.675.624 bytes SHA256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359` e `server-1.21.1-20240808.144430-srg.jar` 14.246.609 bytes SHA256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`.
- **Classe efetiva do recorte:** `net/neoforged/neoforge/common/IOUtilities` no `neoforge-21.1.248-universal.jar`, 3.551.268 bytes, SHA256 `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`; `IOUtilities.class` SHA256 `3c4cfda19b620562486ca18af3d7c095c94a54c31d1028bf8e5d9860952e115a`, Java class major `65`. A interface `IOUtilities$WriteCallback` SHA256 `788ce7628d40835cc3b061e231efbc43e0366eb16c2f334143bf43fa6bac4618` contém `write(OutputStream):void` como método abstrato.
- **Descoberta:** [workflow #45047273632](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45047273632), [artefato #14764335789](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45047273632/artifacts/14764335789), `report.json` **64.358 bytes**, SHA256 `fa32022e12085683d0d4fe5f85e9e9ab15a979d1901f47ae2229f77849687092`. [Sonda](../../../../docs/qa/neoforge_211248_gazing_pearl_write_nbt_compressed_probe.py), [manifesto de 14 métodos SHA-exatos](EXACT-NEOFORGE-211248-GAZING-PEARL-WRITE-NBT-ABI.json), [checker causal](../../../../docs/qa/neoforge_211248_gazing_pearl_write_nbt_compressed_checks.py) e [workflow](../../../../.github/workflows/neoforge-211248-gazing-pearl-write-nbt-compressed.yml). Verificar os testes finais na HEAD da PR antes de declarar gate verde.

**Classe e universo interno:** todos os **14 métodos declarados** de `IOUtilities` foram levantados com nomes, descritores, flags, Code SHA256, instruction SHA256, offsets JVM, handlers e limite de tamanho. Isso fecha apenas o **recorte do classfile distribuído**, não os consumidores, o carregador ou a engine toda.

## 1. Grafo nativo da serialização comprimida

`IOUtilities.writeNbtCompressed(CompoundTag,Path):void` tem 5 instruções, Code SHA256 `272d495a87ec57b2aefdc0d24d2183cf6e7aed795473296a9b4373c295d58ef9`. Seu `invokedynamic` @2 é o `CONSTANT_InvokeDynamic#88` → `BootstrapMethods[1]` → `LambdaMetafactory.metafactory` → `REF_invokeStatic lambda$writeNbtCompressed$1`, cujo destino tipado recebe `CompoundTag, OutputStream`; `atomicWrite(Path,WriteCallback)` é invocado @7. A função não grava diretamente no destino.

A lambda `lambda$writeNbtCompressed$1(CompoundTag,OutputStream):void` (22 instruções; Code SHA256 `59552640fb080b54d00774eafec82e587ea590fb0f3a533341277837282245c2`) cria um `BufferedOutputStream` @0–5, solicita `NbtIo.writeCompressed(CompoundTag,OutputStream)` @11, fecha buffer @15 e usa handlers `Throwable` para fechamento/suppressed. A implementação interna de `NbtIo.writeCompressed` **não foi incluída neste recorte**; não se afirma que o arquivo físico é válido ou recarregável.

`IOUtilities.writeNbt(CompoundTag,Path)` também usa a mesma ponte `atomicWrite`, porém com `CONSTANT_InvokeDynamic#96` → `BootstrapMethods[2]` → `lambda$writeNbt$2`, que invoca a variante NBT não comprimida. Não misturar os dois caminhos.

## 2. atomicWrite — temporário, force e rename

`IOUtilities.atomicWrite(Path,WriteCallback):void`, 76 instruções; Code SHA256 `4243612c391911a78edd3bdc7b463eeb56e153347aff8d3b2cc77b992ff384bb`, instruction SHA256 `c55fc94ab58f0edf170e4e9a5d4d7d77fbe611b233817937d2a0873ee21996d3`. Offsets relevantes:

| Offset | Instrução JVM observada | Alcance demonstrado |
|---|---|---|
| @1, @7, @12 | `Path.getParent`, `getFileName`, `toString` | Constrói argumentos da localização do arquivo temporário |
| @17, @23 | string `.neoforge-tmp`; `Files.createTempFile(parent,filename,suffix,...)` | Solicita arquivo temporário no diretório pai do destino; falha de criação pode propagar antes do escopo de cleanup |
| @31, @39, @47 | `FileChannel.open`, `CloseShieldOutputStream.wrap`, `WriteCallback.write` | Faz o callback escrever no canal da cópia temporária |
| @53, @54 | `iconst_1`; `FileChannel.force(true)` | Solicita flush do arquivo e metadados pelo canal antes do rename, sem prova de durability da entrada do diretório |
| @101, @105 | `StandardCopyOption.ATOMIC_MOVE`; `Files.move(temp,dest,ATOMIC_MOVE)` | Primeiro solicita move atômico |
| @112, @121, @125 | handler de `AtomicMoveNotSupportedException`; `REPLACE_EXISTING`; novo `Files.move` | Se move atômico não for suportado, usa substituição comum; portanto **atomicidade universal não comprovada** |
| @132, @134, @141, @150 | handler de `Exception`; `Files.deleteIfExists(temp)`; suppressed; `athrow` | Em erros do escopo protegido, tenta remover o temporário e propaga a exceção; erro de exclusão não encobre o original |

**Handlers verificados:** `Throwable` [35,57)→68 e [74,78)→81 para fechamento do canal; `AtomicMoveNotSupportedException` [93,109)→112; `Exception` [27,129)→132 e [133,138)→141 para cleanup/suppressed. A opção de abertura da classe é `WRITE` @6 e `TRUNCATE_EXISTING` @12 do `<clinit>` — aplicada ao **arquivo temporário já criado**, não prova truncamento in-place do destino original.

**Limites importantes:** Java NIO e a implementação do `FileSystemProvider` decidem o resultado do move, inclusive quando já existe um destino. `FileChannel.force(true)` solicita persistência do canal, mas não equivale a garantia independente de fsync da pasta, conclusão após falha de energia ou commit transacional do arquivo substituído. Não existe medição física de durabilidade ou crash neste recorte.

## 3. Tarefas assíncronas e possível propagação de falha

Os [callbacks anteriores de SavedData](EXACT-NEOFORGE-211248-GAZING-PEARL-IOWORKER-ABI.md) comprovaram `SavedData.save(File,Provider)` → `IOUtilities.withIOWorker(Runnable)` → `CompletableFuture.thenRunAsync(Util.ioPool)`; `SavedData.save` solicita `setDirty(false)` após agendar, antes de confirmar o término da escrita.

Nesta classe, `waitUntilIOWorkerComplete():void` (7 instruções) lê `saveDataTasks` @0, chama `CompletableFuture.join()` @3 e substitui a referência por `completedFuture(null)` @8–11. **A existência do método não prova que esse método seja chamado em fechamento, stop, crash, troca de dimensão ou salvamento do mundo.** Não foi feita busca exaustiva por callsites externos dele.

No ramo de erro `atomicWrite` repropaga `Exception`, e a lambda de `SavedData.save` captura especificamente `IOException` e faz log. Uma falha efetiva de I/O pode, portanto, ser registrada após a chamada que limpou `dirty`; **isso é uma hipótese causal de risco de persistência**, não comprovação de corrupção, rollback ou perda de reputação no modpack real. Falhas não capturadas em tarefas de `CompletableFuture` exigem auditoria adicional.

Os métodos nativos `tryCleanupTempFiles`, `tryListTempFiles`, `cleanupTempFiles` e `createPredicate` foram incluídos no inventário de 14 métodos, incluindo tratamento de `IOException` e `Files.find/deleteIfExists` quando executados. **Não há demonstração de que sejam invocados automaticamente por `atomicWrite` após toda falha ou em um reinício**; não atribuir a eles garantias de recuperação que seu callsite não mostrou.

## 4. Estados, integração e pendências

O storage `alexscaves_world_data` do Overworld e o `getDeepOneReputation(UUID)` foram observados previamente no JAR publisher `1.0.10`. Esta investigação da engine é compartilhada por muitos SavedData e não descobre novo encantamento, cast ou consumidor específico de perks. Targeting, hitbox, dano, AOE, projéteis, mana, duração, cooldown e scaling **N/A** para essa infraestrutura (ver [Gazing Pearl](items/gazing-pearl.md) para os efeitos do item).

Sem hook real e seguro, Black Arcana não assume autoridade sobre gravação mutadora do estado de Alex's Caves; RPG Skill Tree fornece apenas progressão/gates por contratos reais. **`NO_MUTATION` / fail-closed**, nenhum `src/`, nenhuma Stage, nenhum índice/contador promovido.

**Pendências verificáveis:** bytecode exato de `NbtIo.writeCompressed`, eventual intervenção do `FileSystemProvider`, callsites de `waitUntilIOWorkerComplete`, classe após ModLauncher/mixins, paridade byte-a-byte do JAR físico, arquivo `alexscaves_world_data.dat` real antes/depois de save e após reinício/crash, integridade NBT, sincronização do ItemStack/tooltip e comportamento do provider com o modpack. `physical_qa=NOT_TESTED` e `static_contract=NOT_CERTIFIED` persistem.
