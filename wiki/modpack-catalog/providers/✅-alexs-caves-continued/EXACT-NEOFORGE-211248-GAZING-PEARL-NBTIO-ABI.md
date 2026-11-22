# Gazing Pearl — NbtIo.writeCompressed e fallback de strings no NeoForge 21.1.248

**Escopo:** auditoria técnica **somente estática**, read-only, da distribuição oficial NeoForge `21.1.248` / Minecraft `1.21.1` / Java 21. O objeto `alexscaves:gazing_pearl` permanece **⚠️ PARCIAL**: `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, provider `OPEN`. Esta sonda cobre a infraestrutura de serialização, **não cria magias, itens semânticos, perks nem hooks**.

## 1. Autoridade e evidência reproduzível

**Provider:** Alex's Caves Continued, mod ID `alexscaves`, versão `1.0.10`, JAR físico declarado no sibling `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. O publisher auditado anteriormente tem SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`; **paridade da cópia instalada do usuário NOT_VERIFIED**.

**Distribuição engine:** instalador Maven `neoforge-21.1.248-installer.jar` SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`; `neoforge-21.1.248-server.jar` de **5.675.624 bytes**, SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`; `server-1.21.1-20240808.144430-srg.jar` de **14.246.609 bytes**, SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`. A sonda procura os owners em ambos, com precedência do overlay oficial.

**Identidade dos classfiles realmente selecionados:**
- `net/minecraft/nbt/NbtIo`: class SHA-256 `6c124951f395280964900afe4c0c2a550d4808901c3362519806202fd48024d0`, `NEOFORGE_OVERLAY`, **22 declarações**, campo `SYNC_OUTPUT_OPTIONS`; **8 métodos com corpo JVM** auditados diretamente, cada um com descritor, Code SHA, instruction SHA, offsets e handlers.
- `net/minecraft/nbt/NbtIo$StringFallbackDataOutput`: class SHA-256 `0dd70203d2a454f6cf95ab854640062e39d0372cdf2665c734aa16b4fd7847ba`, `NEOFORGE_OVERLAY`, superclasse `net/minecraft/util/DelegateDataOutput`, **2 métodos concretos** auditados.

**Execução de descoberta aprovada:** [workflow #45055281886](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45055281886), [artefato #14767252409](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45055281886/artifacts/14767252409), `report.json` de **44.730 bytes**, SHA-256 `02a7b6c89e8b704189f40f4979b85a334e212dd8aa2be5cb24bfecdb311f33f3`. Ver também [sonda JVM](../../../../docs/qa/neoforge_211248_gazing_pearl_nbtio_compressed_probe.py), [manifesto SHA-exato](EXACT-NEOFORGE-211248-GAZING-PEARL-NBTIO-ABI.json), [checker fail-closed](../../../../docs/qa/neoforge_211248_gazing_pearl_nbtio_compressed_checks.py) e [workflow](../../../../.github/workflows/neoforge-211248-gazing-pearl-nbtio-compressed.yml). **A aprovação da CI completa da HEAD final é um gate separado desta coleta.**

## 2. Contrato do compressor — sobrecarga exata

O callsite já verificado em [IOUtilities](EXACT-NEOFORGE-211248-GAZING-PEARL-WRITE-NBT-ABI.md) chama precisamente `NbtIo.writeCompressed(CompoundTag,OutputStream):void`, não a sobrecarga `(CompoundTag,Path)`.

| Código e offset JVM | Comportamento demonstrável na distribuição |
|---|---|
| `createCompressorStream(OutputStream):DataOutputStream` — 11 instruções; `new GZIPOutputStream` @8, init @13, `BufferedOutputStream` @16 e `DataOutputStream` @19 | Envolve o `OutputStream` recebido em `GZIPOutputStream`, buffer e saída tipada, nessa ordem de construção |
| `writeCompressed(CompoundTag,OutputStream)` — 24 instruções, Code SHA `4e40b3d0af785b83eab4b9ebe9373ecfe34ac33368dd5572f701c107714fec81` | Solicita `createCompressorStream` @1, `write(CompoundTag,DataOutput)` @7 e `DataOutputStream.close` @15 |
| `write(CompoundTag,DataOutput)` — 4 instruções, Code SHA `85675cda32d432eadcea901432f5b6b7cd5d746a2fbc58bddd992ead373acc35` | Encaminha @2 para `writeUnnamedTagWithFallback(Tag,DataOutput)` |
| `writeUnnamedTagWithFallback` — 7 instruções, Code SHA `229bbc701566bb153dc9716a4bafd2f9e9b91576049e383eb751a4ed709658e0` | Instancia o wrapper `NbtIo$StringFallbackDataOutput` @1/@6 e o encaminha ao `writeUnnamedTag` @9 |
| `writeUnnamedTag(Tag,DataOutput)` — 14 instruções | Lê `Tag.getId` @2; escreve tipo por `DataOutput.writeByte` @7; para ID diferente de zero solicita nome UTF vazio @24 e delega ao método virtual `Tag.write` @31 |

O `writeCompressed(CompoundTag,OutputStream)` usa handlers `Throwable` para fechamento e `addSuppressed` no caso de erro durante o close; o handler cobre intervalos JVM **[5,10)→21** e **[26,30)→33**. Isso mostra o **protocolo de fechamento**, não que escrita em disco tenha sido concluída. Não foi provada garantia física de flush de disco pela API de compressão.

**Sobrecarga diferente:** `writeCompressed(CompoundTag,Path)` tem Code SHA `9710e409f4bf8006f6f7471937d0e6493eb8960246bb4d542d5fb96a75e19afc`, **43 instruções**, cria `Files.newOutputStream` e buffer próprios; não substitui a cadeia `IOUtilities.atomicWrite` aqui documentada. `write(CompoundTag,Path)` (sem compressão) também é método separado. O manifesto preserva seus hashes para evitar confusão de overload.

## 3. Comportamento exato de NbtIo$StringFallbackDataOutput

O wrapper tem construtor `(DataOutput)` de 4 instruções, Code SHA `405f81f0b51683db4ab14a729fb164a2c889439967d0bfe6248ebe8183a4873d`: invoca `DelegateDataOutput.<init>(DataOutput)` @2.

O método `writeUTF(String):void` tem 12 instruções, Code SHA `bef73de317c11cdb18b016eaf07520ab2129b80325dd627a21787d14803d4b66` e handler **`java/io/UTFDataFormatException`** delimitado por **[0,5)→8**.

- @2: solicita `DelegateDataOutput.writeUTF(String)` com a string original;
- @8: captura `UTFDataFormatException` se lançada dentro do intervalo protegido;
- @9–12: chama `Util.logAndPauseIfInIde("Failed to write NBT String",Throwable)`;
- @16–18: carrega uma string literal vazia do constant pool `#21` e solicita `DelegateDataOutput.writeUTF("")`.

**Consequência causal limitada:** sob a condição da exceção específica, o valor originalmente solicitado pode ser substituído por **string vazia** na serialização. O método de fallback não comprova que alguma string do armazenamento `alexscaves_world_data` acionou esse ramo, nem define por si só o tamanho máximo de uma string. A implementação concreta de `DelegateDataOutput`, `CompoundTag.write` e demais `Tag.write` virtuais exige exame separado para fechar contratos internos de serialização.

## 4. Integração da cadeia já auditada

A cadeia técnica estabelecida, sem equivaler a efeito mágico, é:

`ACWorldData.get(Level)` → `ACPlatform.computeIfAbsent` → `DimensionDataStorage.computeIfAbsent` → `SavedData`. No salvamento, `DimensionDataStorage.save` → `SavedData.save(File,Provider)` → `IOUtilities.withIOWorker` (agendamento `CompletableFuture.thenRunAsync`) → `SavedData.lambda$save$0` → `IOUtilities.writeNbtCompressed` → `IOUtilities.atomicWrite` → **`NbtIo.writeCompressed(CompoundTag,OutputStream)`** → escrita de `Tag` para um `DataOutputStream` GZIP.

O [dossiê de escrita temporária](EXACT-NEOFORGE-211248-GAZING-PEARL-WRITE-NBT-ABI.md) já demonstrou `Files.createTempFile` (`.neoforge-tmp`), `FileChannel.force(true)`, tentativa `Files.move(ATOMIC_MOVE)` e fallback `REPLACE_EXISTING` quando `AtomicMoveNotSupportedException`. **A nova observação de NbtIo não prova atomicidade universal, fsync do diretório ou durabilidade/recovery física.** A existência de `waitUntilIOWorkerComplete` não demonstra um caller de shutdown.

**Interoperabilidade:** nenhum hook seguro de alteração de reputação de Deep Ones foi confirmado. O Black Arcana não assume a persistência mutadora do provider; RPG Skill Tree permanece sibling de progressão/perks sem controlar o estado do mundo. `NO_MUTATION` / fail-closed.

**Parâmetros mágicos (dano, AOE, alcance, duração, cooldown, custos, targeting, scaling):** N/A para o codec NBT. A ficha [Gazing Pearl](items/gazing-pearl.md) continua sendo o único objeto individual deste recorte, sem novo spell ou raiz semântica.

## 5. Pendências verificáveis e critérios de segurança

**Não observado:** cópia física do JAR do usuário, bytes de classe transformados por ModLauncher, arquivo `data/alexscaves_world_data.dat` antes/depois da gravação e após reinício, aceitação do reload, recuperação sob erro/energia, comportamento do filesystem provider, integridade concreta de `CompoundTag.write`/`Tag.write`, consumo e efeitos de StringFallback com dados reais, rede e sync de ItemStack, caller de `waitUntilIOWorkerComplete` ao encerrar o servidor e QA nativa do modpack.

**Nenhum percentual, Stage, hook, perk, contrato certificado ou runtime é promovido por esta coleta.** Permanecem `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION` e universo `OPEN`.
