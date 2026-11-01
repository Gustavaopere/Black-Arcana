# Raygun — fronteira do ItemStack opcional vanilla 1.21.1 (não é homologação NeoForge)

## Autoridades e limitação

- **Provider instalado:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, mod ID `alexscaves` (modlist física do sibling). O recorte do helper sombreado está no [manifesto exato do provider](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-ITEMSTACK-HELPER-1.0.10.json).
- **Loader instalado:** NeoForge `21.1.248`. A classe Minecraft transformada por esse loader **não foi inspecionada** neste recorte.
- **Fonte nova, separada:** JAR *client* oficial Mojang **Minecraft 1.21.1**, SHA-1 `30c73b1c5da787909b2f73340419fdf13b9def88` (26.836.906 bytes), mapa oficial SHA-1 `2244b6f072256667bcd9a73df124d6c58de77992` (9.598.610 bytes). Versão e downloads vieram da metadata oficial do launcher; a CI confere hash/tamanho antes de executar o `javap` Java 21. O binário é consultado, **não** publicado.
- **Selo reprodutível:** [EXACT-MOJANG-1211-ITEMSTACK-STREAM-ABI.json](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-MOJANG-1211-ITEMSTACK-STREAM-ABI.json) e [probe read-only](minecraft_1211_itemstack_optional_stream_probe.py).

O mapping Mojang identifica `net.minecraft.world.item.ItemStack` como `cuq.class` (SHA-256 `a34b9141828bd62fa74ad6a5d3b9b47a81df18b4a86866827c8f73d3ab97f901`) e `OPTIONAL_STREAM_CODEC` como campo `h`. O `<clinit>` instancia `cuq$1` em `@120` e atribui `h @127`; a classe codec possui SHA-256 `b67408499e6a5f8edd5120e1bffa67c6e0c50f68658d5d098c4813beebbadfc2`.

## Comportamento estático comprovado apenas no vanilla

| Contrato binário | Observação do JAR vanilla 1.21.1 | Limite |
| --- | --- | --- |
| Contagem de leitura | Método anônimo `a(Lwk;)Lcuq;`: chama `wk.l:()I @1`, testa `ifgt @6` e usa `ItemStack.EMPTY @9` no ramo não positivo | Os nomes `wk`, `jm` e `kn` foram resolvidos via mapping como `RegistryFriendlyByteBuf`, `Holder` e `DataComponentPatch`. O valor máximo e rejeição de valores fora do domínio não foram avaliados |
| Decodificação não vazia | `StreamCodec.decode @17` para item/holder; `getstatic kn.c @26` e `StreamCodec.decode @30` para patch de componentes; instancia `ItemStack @40/@48` | Os limites internos do stream codec de `DataComponentPatch` e do registry codec não foram analisados |
| Escrita da stack | Branch `ifeq @4`, `wk.c:(I) @9/@19`, item `StreamCodec.encode @31`, patch `kn.c @36` e `StreamCodec.encode @47` | Não valida a legitimidade da stack recebida pelo servidor |
| Fonte provider | `PacketBufferUtils.readItemStack` usa o campo simbólico `ItemStack.OPTIONAL_STREAM_CODEC` do ambiente NeoForge (PR #998) | **Não basta** para afirmar identidade binária entre o vanilla e a classe Minecraft transformada pelo NeoForge `21.1.248` |

O codec do vanilla é tratado aqui como **corroboração da fronteira de serialização**, e não como a última autoridade do runtime instalado. Não inferir que esses branches constituam saneamento da tag do Raygun, autenticação de `entityId`, validação de `ChargeUsed`/`UseTime`, antirreplay ou limite geral de NBT.


## Evidência adicional — distribuição oficial de servidor NeoForge 21.1.248 (PR #1000)

O [manifesto SHA-exato da distribuição NeoForge](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NEOFORGE-211248-ITEMSTACK-SERVER-ABI.json) e o [probe limitado](neoforge_211248_itemstack_server_codec_probe.py) acrescentam uma fonte binária distinta do cliente Mojang vanilla: instalador **oficial** NeoForge `21.1.248`, obtido com checksum Maven SHA-256 `68eeab77059ba53df1812f1afa5bf530ab2566a3cdcd5f924aa6e71be42e410c`, executado por `--installServer` na CI. O classfile resultante está no JAR `neoforge-21.1.248-server.jar` com SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359` e tamanho 5.675.624 bytes.

| Classe/método | Evidência compilada na distribuição 21.1.248 | Limitação |
| --- | --- | --- |
| `net.minecraft.world.item.ItemStack` | `ItemStack.class` SHA-256 `072cd6887595d3f928a3a1a9605662ff547fe3201d6b6d713a43bfd2719f1a13`; `OPTIONAL_STREAM_CODEC` atribuído em `@127` | Binário de distribuição, não classe final transformada pelo ModLauncher |
| `ItemStack$1` | SHA-256 `414239d4c913a25cda60a8fc9e6f41661d7939dc9f9f6f4e23f0731468c46925` | Nenhum cliente/multiplayer ou patch de outros mods exercitado |
| Leitura | `RegistryFriendlyByteBuf.readVarInt @1`; `ifgt @6 → @13`; `ItemStack.EMPTY @9`; `ITEM_STREAM_CODEC.decode @17`; `DataComponentPatch.STREAM_CODEC.decode @30` | Nenhum máximo de quantidade, tamanho, componentes ou profundidade comprovado no codec delegado |
| Escrita | `ifeq @4 → @16`; `writeVarInt @9/@21`; `ITEM_STREAM_CODEC.encode @33`; `PatchedDataComponentMap.asPatch @46`; `DataComponentPatch.STREAM_CODEC.encode @49` | Não comprova validação de dados C2S pelo servidor |

Os hashes das classes da distribuição NeoForge diferem dos hashes do JAR vanilla ofuscado (mapeamento/empacotamento distintos); **não usar essa desigualdade, isoladamente, para inferir mudança funcional**. O corpus sela os 15 callsites relevantes e preserva `jvm_modlauncher_class_loaded=NOT_OBSERVED` / `neoforge_modpack_runtime_transformations=NOT_OBSERVED`.

A inspeção da classe entregue pelo instalador é avanço parcial de VC-01, mas **não fecha VC-01**. Permanecem necessários um levantamento da classe efetivamente carregada, avaliação específica dos codecs do patch de componentes, limites efetivos e QA física em cliente/servidor do modpack. `NOT_CERTIFIED` · `NO_MUTATION`.

## VC-02 — DataComponentPatch.STREAM_CODEC na distribuição NeoForge 21.1.248

Nova prova SHA-exata do **JAR oficial distribuído** `neoforge-21.1.248-server.jar` (SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`). O [manifesto do componente](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NEOFORGE-211248-COMPONENT-PATCH-ABI.json) sela a classe `DataComponentPatch.class` (SHA-256 `24f57ec112e9f3ec1e8db754e9014b5b02e2f2c6283f13fbffd27fb90be8d263`) e a classe anônima concreta do `STREAM_CODEC`, `DataComponentPatch$1.class` (SHA-256 `d98b1334116457aea1f6b174e9f0760e6897d965eda58b7f57865bd1e5427880`). O campo estático é atribuído em `@49` após instanciar `$1 @42`.

| Caminho compilado do codec $1 | Evidência e interpretação limitada |
| --- | --- |
| Decodificação, duas contagens | `RegistryFriendlyByteBuf.readVarInt @1/@6`; `ifne @11/@15` retorna `DataComponentPatch.EMPTY` quando ambas são zero |
| Capacidade **inicial** do mapa | Soma das contagens `iadd @24`, constante `int 65536 @33`, `Math.min @35` e `Reference2ObjectArrayMap.<init>(I) @38`. **65.536 limita a capacidade inicial escolhida para alocação, NÃO constitui limite máximo de componentes admitidos.** Os laços continuam vinculados às contagens lidas |
| Componentes acrescentados | Laço com teste `if_icmpge @49`, `DataComponentType.STREAM_CODEC.decode @56`, codec específico do tipo via `DataComponentType.streamCodec @68` e `StreamCodec.decode @74` |
| Componentes removidos | Segundo laço `if_icmpge @108`, `DataComponentType.STREAM_CODEC.decode @115`, `Optional.empty @129` |
| Codificação | `writeVarInt` das contagens, `DataComponentType.STREAM_CODEC`, e chamada `encodeComponent` que delega ao codec específico |

A evidência não comprova validação de contagens negativas, limite máximo agregado de bytes/componentes, profundidade de NBT, exceções em buffers malformados ou compatibilidade das transformações do ModLauncher. O papel de `Math.min(65536)` foi verificado pela sequência das instruções, sem afirmar que não existam controles em outras camadas. Não extrapolar para autorização do `entityId`, modificação de `ChargeUsed`/`UseTime`, exploração ou QA física.

**VC-02: parcialmente analisado na distribuição, ainda `NOT_VERIFIED` quanto a limites efetivos.** Conservam-se `NO_MUTATION`, `NOT_CERTIFIED` e `physical_qa=NOT_TESTED`.
## Plano de aceite pendente

| ID | Prova requerida | Situação |
| --- | --- | --- |
| VC-01 | Inspecionar `ItemStack.OPTIONAL_STREAM_CODEC` na distribuição oficial NeoForge 21.1.248 e na classe final carregada/transformada com o modpack | ⚠️ **Distribuição de servidor SHA-exata INSPECIONADA**, mas bytes carregados pelo ModLauncher/transformações do modpack **NOT_OBSERVED**; falta comparação de runtime |
| VC-02 | Analisar `DataComponentPatch.STREAM_CODEC`, `ByteBufCodecs` e limites de componentes/bytes/profundidade no contexto exato | ⚠️ **Decoder `$1` da distribuição 21.1.248 INSPECIONADO**; `65536` é capacidade inicial do mapa, não cap de componentes; codecs delegados, limites de segurança e runtime modpack **NOT_VERIFIED** |
| VC-03 | Observar aceitação/rejeição controlada de stack vazia, quantidade inválida, NBT grande, patch desconhecido e buffers malformados em cliente e servidor do modpack (sem entregar pacotes hostis a servidores externos) | ⚠️ NOT_TESTED |
| VC-04 | Demonstrar que dados C2S não podem atualizar uma entidade/item fora da autoridade do remetente; checar mão principal, secundária, troca de mão, reenvio e jogador remoto | ⚠️ NOT_VERIFIED / NOT_TESTED |
| VC-05 | Validar `ChargeUsed`/`UseTime` server-owned, limits, custo nativo, ausência de duplicação de dano/uso e compatibilidade com perks | ⛔ NO_MUTATION até contrato e QA apropriados |
| VC-06 | Somente depois dos sete eixos de evidência certificados, reavaliar contrato estático e índices do provider; Stage e QA física são independentes | ⚠️ NOT_CERTIFIED |

Não marcar nenhuma linha física como PASS pela auditoria de bytecode ou CI. O Black Arcana não usa o payload recebido como autoridade de targeting, item, custo ou mundo. A política D006/D008/D035 permanece aplicável.

**Estados preservados:** `Raygun = ⚠️ parcial/condicionado`; `static_perk_certification=NOT_CERTIFIED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`. Nenhuma alteração de runtime, certificados, números globais ou Stage.


## Inspeção da delegação `CUSTOM_DATA`/NBT — NeoForge 21.1.248 (PR #1002)

A [sonda de descoberta de delegates](neoforge_211248_custom_data_delegate_probe.py)
e seu [manifesto de referências SHA-exatas](../../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-NEOFORGE-211248-CUSTOM-DATA-DELEGATE-ABI.json)
ampliam VC-02 **sem repetir** os 29 pivôs selados no codec `DataComponentPatch$1`.
A [execução read-only de descoberta no GitHub Actions](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41358213129)
identificou duas fontes distintas da instalação oficial:

- `neoforge-21.1.248-server.jar`, SHA-256 `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`, contém o overlay compilado `ByteBufCodecs.class` (SHA-256 `a5c5cc1792471d16fb8780c4c6b01f65cbcb6cbe5105318541c0d054b58e418c`).
- `server-1.21.1-20240808.144430-srg.jar`, SHA-256 `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`, contém `CustomData.class` (SHA-256 `23463cf7238fbd2b9ff5bb11bb4a5466fcc06137e89f65d199fe31b7b7d451c9`) e `DataComponents.class` (SHA-256 `fee338af2dbe21bd35781275b01752b72e9178b4314b9d574934a0cddc464716`).

A seleção estreita registra `DataComponents.bootstrap(Registry)` com
`getstatic CUSTOM_DATA @0` e quatro métodos fornecedores de `NbtAccounter`
na classe `ByteBufCodecs`: `lambda$fromCodecWithRegistries$9`,
`lambda$fromCodec$4`, `lambda$static$1` e `lambda$static$0`.
Em cada um desses quatro métodos, a sequência observada é
`ldc2_w long 2097152l @0` seguida de
`NbtAccounter.create(J) @3`. O literal equivale numericamente a **2 MiB**
e é argumento de um factory de accounting de NBT nessas quatro funções;
**não** constitui, isoladamente, limite de tamanho da mensagem Raygun,
garantia de profundidade máxima ou prova de qual desses caminhos o
`CUSTOM_DATA` da mensagem percorre.

O classfile SRG de `CustomData` tem 26 métodos; a seleção de referências
`StreamCodec`/`ByteBufCodecs` não encontrou método correspondente.
Isso é **ausência de match no filtro restrito**, não demonstração de
ausência de codec em outros registries/rotas. O overlay inspecionado é
ainda uma distribuição, não a classe final com transformações do
ModLauncher/modpack. Nenhum pacote malformado foi enviado, nenhum hook mutador
foi testado e nenhuma vulnerabilidade é afirmada.

**VC-02 permanece ⚠️ parcial.** Próximo gate: ligar o componente
`CUSTOM_DATA` ao codec realmente selecionado pela entrada do registry;
em seguida auditar os limites do ramo concreto e as permissões do
receiver em ambiente real. `NO_MUTATION`, `NOT_CERTIFIED`,
`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; nenhum
contador de catálogo, certificado ou Stage promovido.
