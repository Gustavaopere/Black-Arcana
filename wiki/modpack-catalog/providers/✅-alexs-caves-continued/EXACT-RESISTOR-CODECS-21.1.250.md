# Resistor Shield — codecs de componentes e encantamentos efetivos (NeoForge 21.1.250)

## Identidade e reprodução

- Publisher: alexscaves-1.0.10-neoforge+1.21.1.jar, 75.279.314 bytes; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`.
- Distribuição oficial NeoForge 21.1.250: installer `0e47a91ba2139a8db4bf7627af081f7b5789b508bb039ee8dea1272b79693d60`; server `1808fab692dc44b2d474295d1cdd9f1fe8a7dceab4f594210873646fafdf1359`; SRG `26ca9c40d7e1681190b428583c38816852218e78df3f8bdb60a59a78503aec71`; universal `1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956`.
- [Run 45478837398](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45478837398), job 138746190157, artefato 14960312659; relatório 658.305 bytes, SHA-256 `1a4dc80b88f1484d3a059ddfb3782ec7c5299452c9923cf30244a27e155c645e`. 131 registros semânticos em 22 owners. O primeiro run 45477912720 falhou porque o método efetivo não é declarado em ItemStack: a busca foi corrigida para considerar as interfaces e extensões, sem relaxar a exigência de um corpo observado.
- Probe `docs/qa/alexscaves_1010_resistor_codecs_250_probe.py`, workflow `.github/workflows/alexscaves-1010-resistor-codecs-250.yml`. A coleta de classes nested candidatas não significa auditoria integral de todas elas. O inicializador de ByteBufCodecs possui projeção limitada aos sites selecionados.

## Transporte

| Corpo observado | Code SHA-256 | Contrato distribuído |
|---|---|---|
| ItemStack$1.decode | `2598630c64d3f0a6a844a485cb490c688d5a6134267123207d971f26fddd2c4c` | readVarInt @1; count<=0 retorna EMPTY @9; holder codec @17, patch @30, construtor @48. |
| ItemStack$1.encode | `0c0542fc7e345f0d3074722a48f4fc3ba6f278ae0b80af46ccbefaabc692a8ea` | stack vazia escreve 0; senão count @21, holder @33 e asPatch @46 -> encode @49. |
| ItemStack$2.decode | `bf606eb1bd00697b8e6965e1993ab47f48bdcf9350f11aaedc31bc412ec33896` | OPTIONAL_STREAM_CODEC; rejeita vazio por DecoderException. |
| ItemStack$2.encode | `f3f487899397232d22b656bef720935c1f5d46804769fce9452d9a90bbfc209e` | rejeita vazio por EncoderException; delega ao codec optional. |
| DataComponentPatch$1.decode | `d76938dd090b435e004ad7bd1757b042c89d7b813448ea3a10a85550360931c0` | dois VarInts; ambos zero -> EMPTY; capacidade inicial limitada por Math.min(...,65536), não prova limite total de entradas; laços separados: tipos + valores com Optional.of, tipos removidos Optional.empty. |
| DataComponentPatch$1.encode | `5b8802884e35a9510e7290548bd463f12d457fb97f58c6980779d7b69219c56f` | conta presentes/removidos, escreve ambos e em seguida os grupos; valor presente usa codec do próprio tipo, removido transmite tipo. |
| PatchKey.valueCodec | `050cb33d65fc20c1820fd114d2bde0c0a28765f03278fb201a786ac6b24abda7` | removed -> Codec.EMPTY.codec; demais -> type.codecOrThrow. |

## CUSTOM_DATA

DataComponents.lambda$static$0 (Code `0b9817868c28885fcda466c67c8e3a50a4c4d70a42ebc39d6c783042221aa187`) registra CustomData.CODEC via persistent; não chama networkSynchronized nesse corpo. DataComponentType.Builder.build (Code `0b26f0b1487146dff8a90079bc7c35b3f5d5e6ea949bcc0037a682b97b5bb100`) usa streamCodec explícito ou fallback lambda$build$0 -> ByteBufCodecs.fromCodecWithRegistries(codec). Não confundir com CustomData.STREAM_CODEC, que existe e é construído com COMPOUND_TAG.map.

CustomData.<clinit> (Code `61789e93e1de4c97d6c81c5f09b254e1da6225bb65557c9e3984d4de7aaf361a`) combina CompoundTag.CODEC e TagParser.AS_CODEC via withAlternative, xmap para CustomData, CODEC_WITH_ID separado via validate. NbtAccounter.create e unlimitedHeap usam profundidade 512; unlimitedHeap recebe Long.MAX_VALUE. Não inferir que toda rota de CUSTOM_DATA usa quota ilimitada, nem equivalência byte a byte entre codecs distintos. O relatório cobre referências, não teste de round-trip físico ou pacotes transformados.

## Durabilidade e encantamentos

- IItemStackExtension.getAllEnchantments (Code `62fe211295ef711e36898365cac4ad9fb40730bd21da18f33d405fac960c2987`): self -> Item.getAllEnchantments @16 -> EventHooks.getAllEnchantmentLevels @28. Default IItemExtension.getAllEnchantments (Code `2e0a700b9d7421062c67e9eeefa085303560e0d28a1dc464153491b97ca669bc`) lê getTagEnchantments.
- IItemStackExtension.getEnchantmentLevel chama Item.getEnchantmentLevel e EventHooks.getEnchantmentLevelSpecific; default ItemExtension consulta getTagEnchantments/getLevel. A leitura efetiva não é equivalente à leitura direta do tag.
- EnchantmentHelper.runIterationOnItem (Code `6b686fb46d4be3e95586bb5c6bb1e36bee35163ee19054efbff9a2ccc86cc30e`): usa ENCHANTMENTS ou EMPTY; se CommonHooks.resolveLookup(ENCHANTMENT) não nulo, substitui pela consulta getAllEnchantments; visita pares holder/nível. Outra overload com entidade/slot tem matchingSlot. Não projetar essa guarda para a primeira.
- processDurabilityChange (Code `89a14566218ef8a9b87dd342bc5e6c6fc148253f4fcfb2a95c2ba2fd7ff275b9`) acumula MutableFloat e retorna intValue. Enchantment.modifyDurabilityChange delega ITEM_DAMAGE -> modifyItemFilteredCount -> getEffects/itemContext/applyEffects. A lambda recebe nível, random do ServerLevel e valor anterior -> EnchantmentValueEffect.process -> setValue. O resultado depende dos efeitos/condições/eventos e nível efetivo; débito solicitado pelo escudo não é débito garantido.

## Limites

Não é prova de filtros individuais completos de applyEffects ou listeners de EventHooks; não prova codecs de todas as nested classes, persistência real, aceitação de pacotes, PvP/claims ou transformações. Nenhum hook mutador autorizado. Estado: static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; mutation=NO_MUTATION; magic_roots_delta=0.
