# Gazing Pearl — serializers concretos Tag.write / CompoundTag.write (NeoForge 21.1.248)

**Estado: ⚠️ PARCIAL — infraestrutura estática SHA-exata, não certificação do objeto.** `alexscaves:gazing_pearl` continua `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; universo do provider `OPEN`. Esta coleta **não adiciona um cast, uma magia, um hook ou um contrato de perk**.

## 1. Fonte física, rastreabilidade e escopo

- **Mod de origem:** Alex's Caves Continued `alexscaves` **1.0.10**, Minecraft 1.21.1 / NeoForge / Java 21. A modlist do sibling registra `alexscaves-1.0.10-neoforge+1.21.1.jar` (#19; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`). O JAR publisher previamente auditado tinha SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A cópia local instalada **não foi confrontada byte a byte** com aquele publisher.
- **Engine distribuída:** instalador oficial NeoForge `21.1.248`, SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`; overlay `neoforge-21.1.248-server.jar` de 5.675.624 bytes, SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`; `server-1.21.1-20240808.144430-srg.jar` de 14.246.609 bytes, SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`.
- **Coleta exata:** [workflow de descoberta #45058410553](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45058410553), [artefato report.json #14768342779](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45058410553/artifacts/14768342779), **71.642 bytes**, SHA-256 `c80b30aaac9a243f83af59c581800bb565653adc7fc7d1ada4a6b14546667351`. Nenhum JAR foi commitado ou enviado como artefato.
- **Reprodução:** [probe Python](../../../../docs/qa/neoforge_211248_gazing_pearl_tag_writer_probe.py), [manifesto exato](EXACT-NEOFORGE-211248-GAZING-PEARL-TAG-WRITERS.json), [checker de ABI, offsets e instruções](../../../../docs/qa/neoforge_211248_gazing_pearl_tag_writer_checks.py), [11 testes adversariais](../../../../docs/qa/neoforge_211248_gazing_pearl_tag_writer_negative.py) e [workflow de CI](../../../../.github/workflows/neoforge-211248-gazing-pearl-tag-writers.yml). O relatório contém os corpos de instruções **somente** dos métodos selecionados; o manifesto preserva roster SHA, identidades e hashes de método. O sucesso da coleta acima **não substitui a CI completa da HEAD final**.

| Owner distribuído | Origem | SHA-256 classfile | Métodos JVM selecionados |
|---|---|---|---|
| `net/minecraft/nbt/Tag` | Minecraft SRG | `2e5fb1c98da5019e49f1b6805daf7564f980d83cc1ae0bfc3d8723f336a546ca` | 2 declarações abstratas, sem corpo |
| `net/minecraft/nbt/CompoundTag` | NeoForge overlay | `93a9643a11aa61b666871cadeb14be32ff4f813bf97b05951bae389bada15fe6` | `getId`, `write`, `writeNamedTag` |
| `net/minecraft/nbt/ListTag` | NeoForge overlay | `b9f4d0b453362a71e82e05af6190509694c781e688feee51fe9b6e74f38abb84` | `getId`, `write` |
| `net/minecraft/nbt/IntTag` | Minecraft SRG | `0245c8d0134ebd88f1b484c90f72c7a3ace51ae858bde385e0436439d3c95077` | `getId`, `write` |
| `net/minecraft/nbt/IntArrayTag` | Minecraft SRG | `8894d67d9f0e9c27b2df9971c685b7cd3dc0696d1c3b2c295fd180773f222088` | `getId`, `write` |
| `net/minecraft/nbt/StringTag` | NeoForge overlay | `4c177a1d925f5645ece0d34ab51a438ec247b02f9ddc805945db49ea8d5be110` | `getId`, `write` |

## 2. Grafo de escrita comprovado em JVM

A [auditoria anterior de NbtIo](EXACT-NEOFORGE-211248-GAZING-PEARL-NBTIO-ABI.md) estabeleceu `NbtIo.writeUnnamedTag` → `Tag.write(DataOutput)`. A nova coleta confirma o **contrato concreto do `CompoundTag.write`** e quatro implementações de payload, mas não todos os subtipos possíveis de `Tag`.

1. **`CompoundTag.write(DataOutput):void`** — 27 instruções; Code SHA-256 `396856bee5be76314f84a366ffe6419e963856ae0e62c8428d8aadf9ca9f096d`. Carrega `tags:Map`, obtém `keySet()` @4, percorre o iterador (guarda `hasNext` @16), lê a chave e o `Map.get` correspondente, delega `writeNamedTag` @53 a cada entrada e termina escrevendo o **byte zero**: `iconst_0` @60 → `DataOutput.writeByte` @61. **Não há ordenação explícita das chaves** nesse método; ordem estável não é inferida.
2. **`CompoundTag.writeNamedTag(String,Tag,DataOutput):void`** — 14 instruções; Code SHA `167e7d7de97ad5a44ab62e8a1fa5a31f1b5180bf263f65c1ab24888f57c374df`. Obtém `Tag.getId` @2, escreve o ID com `DataOutput.writeByte` @7; o teste `ifeq` @18 **encerra** quando ID = 0; caso contrário escreve o **nome** via `DataOutput.writeUTF` @23 e delega o **valor** por chamada interface `Tag.write` @30. Portanto, **a própria chave** passa pela rota UTF sujeita ao wrapper já auditado em NbtIo.
3. **`ListTag.write(DataOutput):void`** — 41 instruções; Code SHA `5f47c238639b72fc0e018b24925f45c38f146887793a003bcedba4a060da6c5a`. Se lista vazia, grava `type=0` **no próprio campo de instância** @14; se não vazia, lê `list[0].getId` @34 e grava em `type` @39. Em seguida escreve `type` como byte @47, `size` como inteiro @62 e cada elemento via `Tag.write` @98, **sem nome/ID individual para cada entrada**. O ajuste em memória do campo `type` durante escrita **não** significa mutação da reputação de mundo nem hook Black Arcana.
4. **`IntTag.write`** — cinco instruções; `DataOutput.writeInt(data)` @5. **`IntArrayTag.write`** — 26 instruções; escreve `arraylength` @5 via `writeInt` @6 e cada `int` @37. A associação de qualquer campo UUID concreto a `IntArrayTag` exige uma prova separada de seu produtor; **não está demonstrada apenas por estes writers**.
5. **`StringTag.write`** — cinco instruções; delega `DataOutput.writeUTF(data)` @5. No percurso `NbtIo.writeCompressed` já certificado como infraestrutura, `NbtIo$StringFallbackDataOutput.writeUTF` pode gravar `""` se ocorrer `UTFDataFormatException`. **A ocorrência dessa exceção no `DeepOneReputations` real não foi observada.**
6. **`Tag`** é uma interface com `getId():byte` e `write(DataOutput):void` abstratos (flags JVM 1025), não um único corpo genérico de escrita; o dispatcher virtual exige examinar os subtipos efetivamente produzidos. A amostra de cinco subtipos acima **não equivale ao universo de todas as Tags**.

Todos os métodos concretos selecionados acima vieram com **zero handlers de exceção declarados no próprio Code**; isso não elimina falhas ou handlers nos chamadores/implementações do `DataOutput`.

## 3. Fronteiras de persistência, integração e QA

A relação causal até aqui documentada é `ACWorldData.acSave` → `SavedData.save` → `IOUtilities.writeNbtCompressed` → `NbtIo.writeCompressed` → `NbtIo.writeUnnamedTag` → `CompoundTag.write` → `writeNamedTag` → `Tag.write` concreto. Esta relação prova **solicitações de serialização no bytecode distribuído**, não que um snapshot específico de reputação tenha sido corretamente escrito, sincronizado com disco, recarregado ou preservado após reinício/crash.

**Dados de reputação:** a Gazing Pearl apenas consulta um retrato do `ACWorldData` e o apresenta no item. `DeepOneReputations` permanece armazenamento externo ao Black Arcana. Alterar bytes serializados, NBT da stack ou temporização não constitui ponto autorizado de perk para mudar reputação, IA dos Deep Ones, dano, targeting, buffs, Mastery ou XP. **Sem hook mutador nativo e seguro: `NO_MUTATION` / fail-closed.** N/A para alcance, cooldown, dano, geometria, custos ou projéteis próprios deste codec.

**Falta verificar:** todas as implementações `Tag.write` atingíveis por dados reais; `CompoundTag.putUUID`/produtor preciso do tipo NBT de UUID; limites/propagação de `DelegateDataOutput.writeUTF`; callers concretos de `waitUntilIOWorkerComplete` no shutdown; bytes reais do `alexscaves_world_data.dat`; leitura após restart, paridade ModLauncher transformada, proteção contra corrupção e QA real cliente/servidor do modpack. O inventário e índice **não aumentam** por esta auditoria de infraestrutura.

## 4. Critérios de certificação e testes

A coleta `report.json` é reproduzível com JDK 21 e os dois JARs oficiais checksum-exatos, via workflow linkado acima. O checker confronta classe, roster, assinaturas, métodos, hashes e **22 pontos de instrução/ramo**; o teste adversarial forja os 11 pivôs críticos, **recalcula os hashes apresentados no relatório e no manifesto falso**, e exige rejeição explícita por `JVM opcode drift`. Isso verifica a capacidade de detecção de alterações nos pivôs monitorados, **não testa persistência física nem conclui a certificação da Gazing Pearl**.

**Status final de escopo:** `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, `provider_universe_closed=false`.
