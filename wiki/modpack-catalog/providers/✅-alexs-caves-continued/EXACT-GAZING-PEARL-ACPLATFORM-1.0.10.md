# Gazing Pearl — ponte de armazenamento ACPlatform / SavedData (publisher 1.0.10)

**Estado:** ⚠️ **CONTRATO TRANSITIVO ESTÁTICO PARCIAL**, sem promoção da Gazing Pearl. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · universo do provider `OPEN`. O mecanismo é infraestrutura de persistência, **não** outro cast, spell, perk ou raiz semântica.

## Identidade, autoridade e reprodução

- **Provider:** Alex's Caves Continued, mod ID `alexscaves`, Minecraft 1.21.1 / NeoForge / Java 21. A modlist física no sibling `Gustavaopere/neoforge-rpg-skilltree` identifica `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. JAR publisher lido: **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 1.555 classfiles. **Não** houve confronto direto de bytes da cópia instalada.
- **Owner nativo:** `com/github/alexmodguy/alexscaves/server/misc/ACPlatform`, class SHA-256 `662a4d2593fe515ed8790bad06d8184d1eb921423033dfd11b3b44142dedc3e6`; superclass `java/lang/Object`, 3 fields e 43 métodos declarados. Entre as classes cujo nome contém "platform", a sonda não encontrou outro owner declarando um método `computeIfAbsent`.
- **Relatório 1:** [workflow #45011716885](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45011716885), artifact [#14749664289](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45011716885/artifacts/14749664289), 23.609 bytes de JSON SHA-256 `7c682ff2db8d675d31af75cbd213779aca2f5923d73777ae7b09bf1abc7b901c`.
- **Relatório ampliado canônico:** [workflow #45011825823](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45011825823), artifact [#14750315491](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45011825823/artifacts/14750315491), `report.json` de **36.169 bytes**, SHA-256 `c50ddcc8cb7f9ee327802642c9d940db600c9dac20a50217bb8345faf6e0265b`. A [sonda read-only](../../../../docs/qa/alexscaves_1010_gazing_pearl_acplatform_probe.py) reconcilia SHA/tamanho e o inventário dos 1.555 classfiles; o [manifesto de contratos](EXACT-GAZING-PEARL-ACPLATFORM-1.0.10.json) e o [checker fail-closed](../../../../docs/qa/alexscaves_1010_gazing_pearl_acplatform_checks.py) são o gate de reprodução desta PR (requer CI final própria).

## Corpo exato — ACPlatform.computeIfAbsent

**Signature JVM:** `(DimensionDataStorage, Function, Function, Supplier, String) -> SavedData`, retornando `Lnet/minecraft/world/level/saveddata/SavedData;`. Método público estático, **11 instruções**, Code SHA-256 `66492d422ecbe213c0fc8b337f300693b25341c69690610806b86b906c4e78b3`, instruction SHA-256 `625899b736db7a61455db4301becd6996444ea6f58c897da47084cb7a44a3903`.

**Fluxo causal pinado:**

| Offset JVM | Operação observada | Implicação estritamente estática |
|---:|---|---|
| 0–1 | Lê `DimensionDataStorage` e instancia `SavedData.Factory` | O wrapper atua como ponte para o sistema de SavedData |
| 5 | `aload_3` | Passa o `Supplier` de criação |
| 6–7 | `aload_1` + `invokedynamic` gerando `BiFunction` | O loader utiliza a **primeira** `Function` |
| 12–13 | `aconst_null` + `SavedData.Factory.<init>(Supplier,BiFunction,DataFixTypes)` | O argumento `DataFixTypes` da fábrica é **null**; não comprova todas as migrações externas |
| 16–18 | Recebe o argumento String da posição local 4 e invoca `DimensionDataStorage.computeIfAbsent(Factory,String)` | A chave de armazenamento é preservada para a engine |
| 21 | `areturn` | Devolve o `SavedData` encaminhado pela engine |

**Discrepância da assinatura nativa:** o corpo **não contém nenhum acesso a `aload_2`**, portanto a **segunda `Function` fornecida ao helper fica sem uso direto nessa build**. Isto não demonstra bug por si: `ACWorldData` mantém uma implementação de `save`/`acSave` própria, e o comportamento total de `DimensionDataStorage` depende da engine. Não utilizar a segunda função como suposto hook de serialization/perks.

### Lambda adaptadora da carga

`ACPlatform.lambda$computeIfAbsent$1(Function,CompoundTag,HolderLookup.Provider) -> SavedData`: **5 instruções**, Code SHA-256 `5cbb0594bcb4ff83d01c6b409af2de04871b173a69c6ec087c18f4e6f44af60e`, instruction SHA-256 `664d874cd05f359896963334f4c5b3cf81137b1723d2aa4e500aa717979df553`. Em @0–2 passa o `CompoundTag` recebido a `Function.apply`, em @7 faz `checkcast SavedData` e retorna em @10. **Não lê o `HolderLookup.Provider` da posição local 2.** O `invokedynamic` do wrapper tem tipo compatível com essa adaptação; **o BootstrapMethods/MethodHandle de vinculação não foi auditado individualmente neste recorte**, e a compatibilidade de assinaturas não deve ser tratada como prova independente de vinculação.

### Consumidores diretos do helper

O censo de métodos tipados em **1.555 classfiles** encontrou apenas **dois owners** invocando esse descriptor. Estes são os consumidores **deste helper exato** no publisher, não o universo completo de chamadas indiretas, engine ou reflection:

| Caller | Class SHA-256 | Corpo/offset e armazenamento |
|---|---|---|
| `ACWorldData.get(Level)` | `ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5` | 27 instruções, Code SHA `bd22587b8dbae8d2faae621a1df5bdbd1e454ce2741779f3f38cac48b5163893`; chave `alexscaves_world_data` @39, call @41 e `setDirty` @53 quando retorno não nulo |
| `CitadelServerData.get(MinecraftServer)` | `f279444fc992c88734aac6bdb65810eb43ed1095a5aa562203d78141181273fa` | 19 instruções, Code SHA `756553ae00384d97e15bad1ee171e05655d5a39bc46c87ef3f9b2f7a78e76404`; chave `alexscaves_citadel_world_data` @29, call @31 e `setDirty` @39 |

**Isolamento de contexto:** `CitadelServerData` compartilha o helper genérico, porém **não** é uma segunda raiz de reputação nem consumidor direto da Gazing Pearl. A cadeia comprovada da pérola segue `GazingPearlItem.acInventoryTick → ACWorldData.get → ACPlatform.computeIfAbsent → DimensionDataStorage.computeIfAbsent` e, quando há instância válida, `ACWorldData.getDeepOneReputation(UUID)`.

## Referência de engine e efeitos delimitados

A [documentação oficial NeoForge **1.21–1.21.1**](https://docs.neoforged.net/docs/1.21.1/datastorage/saveddata/) define `DimensionDataStorage.computeIfAbsent` como consulta/criação/carregamento de `SavedData` por `Factory` e nome; os dados ficam no diretório `data` da dimensão pertinente. A mesma documentação define `setDirty` como aviso de alteração necessário para salvar, **não** garantia de escrita síncrona imediata. O [Javadoc da engine para 1.21.1](https://lexxie.dev/neoforge/1.21.1/net/minecraft/world/level/storage/DimensionDataStorage.html) confirma a assinatura `computeIfAbsent(SavedData.Factory,String)` e tipos de armazenamento.

Portanto, **a chave candidata esperada** no Overworld para o owner reputacional é `alexscaves_world_data` (arquivo `data/alexscaves_world_data.dat`, condicionado ao layout da instância e à engine). **A presença física, conteúdo, durabilidade de escrita, comportamento de erros de I/O, migração e carregamento pós-reinício não foram testados** nesta instância. O fato de `ACWorldData.get` solicitar `setDirty` após consulta não prova alteração de reputação nem eficácia final de gravação; pode indicar trabalho adicional de serialização, mas não houve medição.

## Parâmetros, efeitos, hooks, pendências

- **Dano/tipo, AOE, projétil, duração, mana, cooldown, targeting ofensivo:** **N/A** para esta ponte de armazenamento. O UUID do portador pertence ao caller Gazing Pearl, **não** ao método `computeIfAbsent`.
- **Key de SavedData, Supplier/loader e contexto servidor:** observados; a operação de armazenamento não certifica permissões de escrita por player, prevenção de replay, PvP/claims, sync de stack ou ownership.
- **Clean-room:** apenas signatures, offsets, hashes e observações comportamentais para interoperabilidade. Não transferir código de terceiros, nem reimplementar a classe no runtime Black Arcana.
- **Próximas provas:** inspecionar o `BootstrapMethods` de `invokedynamic` para vinculação exata; contrato da engine efetiva NeoForge 21.1.248 e `SavedData.Factory`; semântica de `ACPlatform.computeIfAbsent` em mundos/saves e errors; sincronização de `ItemStack` com `CUSTOM_DATA`, render/tooltip client, QA física em modpack e reprodução do JAR efetivamente instalado. Sem hook real e seguro por usuário, **NO_MUTATION / fail-closed**.

**Status final do recorte:** método local conhecido, mas **Gazing Pearl ⚠️ parcial**, `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; provider `OPEN`, nenhuma raiz ou contagem aumentada.
