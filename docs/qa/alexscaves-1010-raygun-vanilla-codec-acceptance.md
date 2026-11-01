# Raygun — fronteira do ItemStack opcional vanilla 1.21.1 (não é homologação NeoForge)

## Autoridades e limitação

- **Provider instalado:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, mod ID `alexscaves` (modlist física do sibling). O recorte do helper sombreado está no [manifesto exato do provider](../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-RAYGUN-ITEMSTACK-HELPER-1.0.10.json).
- **Loader instalado:** NeoForge `21.1.248`. A classe Minecraft transformada por esse loader **não foi inspecionada** neste recorte.
- **Fonte nova, separada:** JAR *client* oficial Mojang **Minecraft 1.21.1**, SHA-1 `30c73b1c5da787909b2f73340419fdf13b9def88` (26.836.906 bytes), mapa oficial SHA-1 `2244b6f072256667bcd9a73df124d6c58de77992` (9.598.610 bytes). Versão e downloads vieram da metadata oficial do launcher; a CI confere hash/tamanho antes de executar o `javap` Java 21. O binário é consultado, **não** publicado.
- **Selo reprodutível:** [EXACT-MOJANG-1211-ITEMSTACK-STREAM-ABI.json](../wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-MOJANG-1211-ITEMSTACK-STREAM-ABI.json) e [probe read-only](minecraft_1211_itemstack_optional_stream_probe.py).

O mapping Mojang identifica `net.minecraft.world.item.ItemStack` como `cuq.class` (SHA-256 `a34b9141828bd62fa74ad6a5d3b9b47a81df18b4a86866827c8f73d3ab97f901`) e `OPTIONAL_STREAM_CODEC` como campo `h`. O `<clinit>` instancia `cuq$1` em `@120` e atribui `h @127`; a classe codec possui SHA-256 `b67408499e6a5f8edd5120e1bffa67c6e0c50f68658d5d098c4813beebbadfc2`.

## Comportamento estático comprovado apenas no vanilla

| Contrato binário | Observação do JAR vanilla 1.21.1 | Limite |
| --- | --- | --- |
| Contagem de leitura | Método anônimo `a(Lwk;)Lcuq;`: chama `wk.l:()I @1`, testa `ifgt @6` e usa `ItemStack.EMPTY @9` no ramo não positivo | Os nomes `wk`, `jm` e `kn` foram resolvidos via mapping como `RegistryFriendlyByteBuf`, `Holder` e `DataComponentPatch`. O valor máximo e rejeição de valores fora do domínio não foram avaliados |
| Decodificação não vazia | `StreamCodec.decode @17` para item/holder; `getstatic kn.c @26` e `StreamCodec.decode @30` para patch de componentes; instancia `ItemStack @40/@48` | Os limites internos do stream codec de `DataComponentPatch` e do registry codec não foram analisados |
| Escrita da stack | Branch `ifeq @4`, `wk.c:(I) @9/@19`, item `StreamCodec.encode @31`, patch `kn.c @36` e `StreamCodec.encode @47` | Não valida a legitimidade da stack recebida pelo servidor |
| Fonte provider | `PacketBufferUtils.readItemStack` usa o campo simbólico `ItemStack.OPTIONAL_STREAM_CODEC` do ambiente NeoForge (PR #998) | **Não basta** para afirmar identidade binária entre o vanilla e a classe Minecraft transformada pelo NeoForge `21.1.248` |

O codec do vanilla é tratado aqui como **corroboração da fronteira de serialização**, e não como a última autoridade do runtime instalado. Não inferir que esses branches constituam saneamento da tag do Raygun, autenticação de `entityId`, validação de `ChargeUsed`/`UseTime`, antirreplay ou limite geral de NBT.

## Plano de aceite pendente

| ID | Prova requerida | Situação |
| --- | --- | --- |
| VC-01 | Inspecionar `ItemStack.OPTIONAL_STREAM_CODEC` na **classe Minecraft mesclada e transformada** da instalação NeoForge 21.1.248; registrar checksums e diferenças em relação ao vanilla | ⚠️ PENDING — fonte vanilla não substitui runtime |
| VC-02 | Analisar versão efetiva do `DataComponentPatch.STREAM_CODEC`, `ByteBufCodecs` e limite de componentes/bytes/profundidade da stack no contexto exato | ⚠️ NOT_VERIFIED |
| VC-03 | Observar aceitação/rejeição controlada de stack vazia, quantidade inválida, NBT grande, patch desconhecido e buffers malformados em cliente e servidor do modpack (sem entregar pacotes hostis a servidores externos) | ⚠️ NOT_TESTED |
| VC-04 | Demonstrar que dados C2S não podem atualizar uma entidade/item fora da autoridade do remetente; checar mão principal, secundária, troca de mão, reenvio e jogador remoto | ⚠️ NOT_VERIFIED / NOT_TESTED |
| VC-05 | Validar `ChargeUsed`/`UseTime` server-owned, limits, custo nativo, ausência de duplicação de dano/uso e compatibilidade com perks | ⛔ NO_MUTATION até contrato e QA apropriados |
| VC-06 | Somente depois dos sete eixos de evidência certificados, reavaliar contrato estático e índices do provider; Stage e QA física são independentes | ⚠️ NOT_CERTIFIED |

Não marcar nenhuma linha física como PASS pela auditoria de bytecode ou CI. O Black Arcana não usa o payload recebido como autoridade de targeting, item, custo ou mundo. A política D006/D008/D035 permanece aplicável.

**Estados preservados:** `Raygun = ⚠️ parcial/condicionado`; `static_perk_certification=NOT_CERTIFIED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`. Nenhuma alteração de runtime, certificados, números globais ou Stage.
