# Defaults de componentes, builder de entidade Ink Bomb e codec de receita — 21.1.250

**DISCOVERY_ONLY / NO_MUTATION**. Publisher Alex's Caves Continued 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. Modlist #019, Minecraft 1.21.1, Java 21, distribuição oficial NeoForge 21.1.250. Não é observação física.

## Evidência prévia reutilizada

- Run [45471957912](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45471957912/job/138721970278), relatório 1.956.222 bytes SHA-256 `5a5c4a201604224306a2b5cded87cb82523bce8cf0e82aaf998954125afe0c65`. Item$Properties.<init> Code `91fd20ff4ac88d8a1516a2bd89ed6c288a6546839db4a268fb15d30671e879f3` inicializa requiredFeatures e canRepair=true, não escreve tamanho de stack. buildAndValidateComponents Code `ce196929d6466b4ddf1d652d18a7827b1e79831f5bfd93997d81f874a5975b10` delega buildComponents @1 e validateComponents @6. Default de componentes não pode ser inferido apenas do construtor.
- Run [45478837398](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45478837398/job/138746190157), relatório 658.305 bytes SHA-256 `1a4dc80b88f1484d3a059ddfb3782ec7c5299452c9923cf30244a27e155c645e`. ItemStack.lambda$static$3 Code `dc6750c881e2b856e770b6292081224e4048a6cbea15468efcffb0cd4e04c226` projeta count com intRange(1,99) e orElse(1) @38. Isso isoladamente não prova que o serializer shapeless usa esse codec.
- Run [45473794747](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45473794747), 178.620 bytes SHA-256 `534c8c6a7534d203d994ea1e4f4948b03c5a0ed01c79a5d97aa6a5eb2fdf79c2`: factory ACEntityRegistry.lambda$static$43 Code `5f095071ddceb4d09df9169080fcd8cda9d0fdbe185340560e692aa7b63d0fe7`, categoria MISC, sized(0.6F,0.6F), setShouldReceiveVelocityUpdates(true), setUpdateInterval(1), sem argumento explícito de trackingRange. Não atribuir valores default até localizar o builder.

## Sonda nova

`docs/qa/alexscaves_1010_item_entity_defaults_250_probe.py` reutiliza pins de oito classes e sete Code hashes prévios (três engine, quatro registry). Seleciona Item$Properties.buildComponents, Item, ItemStack, builder/mapa de componentes, EntityType$Builder, EntityType, ShapelessRecipe$Serializer e quatro factories. Os métodos candidatos não são afirmações de APIs; a declaração e Code vêm do JAR. A projeção de DataComponents.<clinit> fixa os quatro pivôs de escrita e uma janela limitada de 100 instruções anteriores à escrita de COMMON_ITEM_COMPONENTS, não pretende descrever toda a inicialização. A sonda não chama métodos da engine; workflow exige duas execuções idênticas. Primeiro resultado observado abaixo.

Escopo útil para as fichas Ink Bomb/Glow Ink Bomb, default de componentes, aquisição de Hot Chocolate Bottle. Sem mudança de fichas concorrentes, certificado, runtime, hook ou QA.

## Evidência reproduzida

[Run 45517751804, job 138881481661](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45517751804/job/138881481661): 12 classes e 58 métodos executáveis, duas saídas idênticas de 322.625 bytes, SHA-256 `448111136166191329351f06376741dc040bb6a6ee9f8f624ae8b915d5fae944`. O workflow agora exige esse selo; CI do novo HEAD necessária.

- DataComponents.<clinit> Code `1f3ab98f9eca8afb8378e6dceae0ee03f35f4be09cc7f5cc133b2c89199042be`: COMMON_ITEM_COMPONENTS construído @811–874; MAX_STACK_SIZE=64 @814–822; lore, enchantments e attribute_modifiers vazios, repair_cost=0, rarity COMMON. Sem DAMAGE/MAX_DAMAGE nesse mapa. Item$Properties.buildComponents retorna o mapa comum quando não há builder; factory das duas variantes usa propriedades sem overrides. Valor nominal, não registro/stack efetivos.
- EntityType$Builder.<init> Code `113f390bad1f8bc3df187fc92973eb49b693d52504f09bc0ff65467ffbf326e8`: tracking bruto 5 @23, intervalo bruto 3 @28. Factory Ink Bomb substitui dimensão por 0,6×0,6, solicita supplier de update=1 e velocidade=true. build encaminha campos e suppliers; getters delegam aos suppliers. Não equiparar tracking a alcance de combate nem declarar valor efetivo do supplier sem projetar o corpo.
- ShapelessRecipe$Serializer.lambda$static$8 Code `0a3472c8f9da332d2116732999d107f9ca6bda43a9d4a2258c6d404e982db24f`: result via ItemStack.STRICT_CODEC @45. lambda$static$6 rejeita lista vazia ou acima de maxHeight×maxWidth. A ligação do codec estrito ao corpo de count permanece pendente. Nenhuma aceitação física de receita, hook ou certificado novo.

## Ligação efetivamente observada

[Run 45525743293, job 138908485876](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45525743293/job/138908485876), HEAD `9c49cd0ca0f776b9906e4f7de86847f2e0548aec`: selo anterior reproduzido (322.625 bytes); relatório adicional de 380.596 bytes SHA-256 `aab3ae48b827b010a92197e8c0c56bc9be8cbb35cadb1e8c0809a9542cc5bcdb`, 69 métodos distintos, duas execuções idênticas. O workflow exige agora ambos os hashes e tamanhos.

| Corpo | Code SHA-256 | Contrato distribuído |
|---|---|---|
| EntityType.defaultTrackingRangeSupplier | `940c8e76d6e4850d223eb734aa8924b449670a45f0da5ce5ef637e41cccdd07d` | lê clientTrackingRange @1 |
| EntityType.defaultUpdateIntervalSupplier | `0acda5776f4f42254683c9eebba76280a652f72391d27436cf55b83dc1c3902a` | lê updateInterval @1 |
| EntityType$Builder.lambda$setUpdateInterval$1 / lambda$setTrackingRange$2 / lambda$setShouldReceiveVelocityUpdates$3 | `5cbd9da63c8139da8b77e3a93548191c896e8a377e500f7e81913317750a2935` | retornam argumento capturado; não leem configuração da entidade |
| ItemStack.<clinit> | `c4db5c18b82da9e5db534aecd001ef195d1064345f9d253f6fca104d0c22b4d0` | bootstrap @21 -> lambda$static$4; lazyInitialized @26 -> CODEC @29; CODEC @43 -> validateStrict handle @46 -> validate @51 -> STRICT_CODEC @56 |
| ItemStack.lambda$static$4 | `16b0461124b984e237d09b45c5ff6eedd5b3efccf89d1df853cb114cc6115dc9` | bootstrap @0 -> lambda$static$3 -> RecordCodecBuilder.create @5 |
| ItemStack.validateStrict | `328d49ea44b178e9a6a61494ad654ca41b58fc7d538101894e22e3adc8d01cd2` | validateComponents @4; erro retorna resultado mapeado; count>getMaxStackSize rejeita; demais success |
| ItemStack.validateComponents | `421ab393a8e152d0cccec03b7791d697a8f130d8030bdeddf1f61b30294cb0d8` | MAX_DAMAGE com MAX_STACK_SIZE>1 rejeitado; verifica contagem de itens não vazios no CONTAINER contra stack máxima |

**Conclusão estática:** ambas Ink Bombs usam tracking nominal 5, intervalo 1 e velocity updates true pelo builder/supplier observado; não converter 5 em alcance efetivo de rede ou ataque. ShapelessRecipe.Serializer usa STRICT_CODEC; o codec base contém count em [1,99], orElse(1), components opcional EMPTY. Portanto o resultado declarativo da receita Hot Chocolate Bottle, que omite count, tem quantidade padrão 1, sujeita à validação de componentes e stack máxima nominal 16. Não é prova de crafting efetivo, datapack carregado ou execução física. `NO_MUTATION`.
