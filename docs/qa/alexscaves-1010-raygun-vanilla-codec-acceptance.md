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

## Plano de aceite pendente

| ID | Prova requerida | Situação |
| --- | --- | --- |
| VC-01 | Inspecionar `ItemStack.OPTIONAL_STREAM_CODEC` na distribuição oficial NeoForge 21.1.248 e na classe final carregada/transformada com o modpack | ⚠️ **Distribuição de servidor SHA-exata INSPECIONADA**, mas bytes carregados pelo ModLauncher/transformações do modpack **NOT_OBSERVED**; falta comparação de runtime |
| VC-02 | Analisar versão efetiva do `DataComponentPatch.STREAM_CODEC`, `ByteBufCodecs` e limite de componentes/bytes/profundidade da stack no contexto exato | ⚠️ NOT_VERIFIED |
| VC-03 | Observar aceitação/rejeição controlada de stack vazia, quantidade inválida, NBT grande, patch desconhecido e buffers malformados em cliente e servidor do modpack (sem entregar pacotes hostis a servidores externos) | ⚠️ NOT_TESTED |
| VC-04 | Demonstrar que dados C2S não podem atualizar uma entidade/item fora da autoridade do remetente; checar mão principal, secundária, troca de mão, reenvio e jogador remoto | ⚠️ NOT_VERIFIED / NOT_TESTED |
| VC-05 | Validar `ChargeUsed`/`UseTime` server-owned, limits, custo nativo, ausência de duplicação de dano/uso e compatibilidade com perks | ⛔ NO_MUTATION até contrato e QA apropriados |
| VC-06 | Somente depois dos sete eixos de evidência certificados, reavaliar contrato estático e índices do provider; Stage e QA física são independentes | ⚠️ NOT_CERTIFIED |

Não marcar nenhuma linha física como PASS pela auditoria de bytecode ou CI. O Black Arcana não usa o payload recebido como autoridade de targeting, item, custo ou mundo. A política D006/D008/D035 permanece aplicável.

**Estados preservados:** `Raygun = ⚠️ parcial/condicionado`; `static_perk_certification=NOT_CERTIFIED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`. Nenhuma alteração de runtime, certificados, números globais ou Stage.
