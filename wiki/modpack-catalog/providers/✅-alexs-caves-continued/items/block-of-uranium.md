# Block Of Uranium

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Item de bloco; sem nova raiz semântica certificada.

## Identidade e evidência

`alexscaves:block_of_uranium`; `RadioactiveBlockItem`; Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-RADIOACTIVE-ITEMS-1.0.10.md). [Prova original](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45750603107/job/139677193397), 232.851 bytes SHA-256 `b8fd8880d0f888ee137a436ec0aa81ea7916c6e6883acc0237d2915525499c97`; [prova suplementar](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45793839880/job/139819307102), 1.106.955 bytes SHA-256 `52f90cc908f4e775a29711454c2a58a411dc491116020680d77eaf553a299709`; HEAD `e992226c0d80b5d6393e0a99de49d185c406a807`; dois replays idênticos de cada. Sem dump físico instalado novo.

ACBlockRegistry class SHA `b4de04f32f6e1d92eeda55480b8480f7ed69f3813164f330f49d0eced202e54c`; <clinit> Code SHA `d4e20fc9df025209351d92f78283942e0817358a21a30b62c4b68dc9d93f082a`: literal block_of_uranium @2292, supplier de bloco @2295, selector 4 @2300, registerBlockAndItem(String,Supplier,int) @2301, Field BLOCK_OF_URANIUM:Ljava/util/function/Supplier; @2304. Helper Code SHA `d1a0bd80dc6b33272d28f317f10161bc4fbacda2d8b41529fe2a53d82141f32c`: registra bloco @5, recebe supplier de bloco, passa selector + supplier a getBlockSupplier @15, registra item com mesmo nome @18. getBlockSupplier Code SHA `0491a61abf0d322efcd2b927a9d55591d5f25a2f094e9d386121b5ad3ed45b68`: switch 4 -> @80, invokedynamic @81 ligado a lambda$getBlockSupplier$440. Factory Code SHA `97cdb48022a1d0e97196956a30d852cc346aad92de1c88cc8f6590109bfd71f3`: blockItemProperties @5, rate 0.001F @8, construtor @11. Vínculo declarativo, sem prova de registry transformado.

## Irradiação por inventário

Herdado de RadioactiveBlockItem (extends BlockItemWithSupplier), class SHA `1c769a4b64f0e4b3b9a2f5589bfc44ce3e27ec46c616b447d4e1359ffb21bd4b`, construtor Code SHA `668113e6779d9bb2128c47dc5f1b7210561d219af9d6fef79715ba835d2562af`. acInventoryTick(ItemStack,Level,Entity,boolean)V, 73 instruções, Code SHA `a98c07b15db89b72116500877e23e3f95db45ec8223dfeaa00fb76980bacc47d`. Servidor, entidade LivingEntity, Player não criativo, ausência de IRRADIATED; boolean selected não lido. Comparação float nextFloat() < count×0.001F×(1−HazmatArmorItem.getWornAmount(carrier)/4F); sem clamp explícito. Stack de 1, zero peças: 0.1% nominal por chamada elegível. [Hazmat](hazmat-mask.md) contador 0..4 por identidade e slot. addEffect(MobEffectInstance(IRRADIATED,1800)) @138 (amp0 default), retorno ignorado, mensagem visual posterior @160/163. Não consulta vizinhos ou tag de resistência explicitamente; sem dano direto, shrink, mana, cooldown ou XP. [Irradiated](../effects/irradiated.md) e [Radiation](../damage-types/radiation.md) são consumidores separados. Não confundir amp0 com dano periódico. Estado do efeito pela engine; sem NBT próprio demonstrado.

## Destruição e mundo

Não há override próprio onDestroyed na classe RadioactiveBlockItem. Não transferir nuvem/explosão do subclass Waste Drum para este item. Efeitos do bloco colocado, quebra, interações, propriedades, custo e placement herdado não auditados nesta ficha.

## Integração e validação

Sem hook mutador verificado. Não duplicar aplicação de status, consumo, cloud, descarte, explosão ou XP; não alterar proteção Hazmat global. Perks de exposição e mitigação são apenas possibilidades conceituais. WorldEffectPolicy deve preservar autoridade de Black Arcana sem presumir interceptação do provider. Pendências: ACBlockRegistry.blockItemProperties, BlockItemWithSupplier/placement, bloco específico, recipes/loot/tags transitivos, stack defaults, dispatch real, aceitação de addEffect, multiplayer e persistência, comportamento do bloco no mundo. Contrato parcial; não certificar por identidade isolada. QA física NOT_TESTED.

## Evidência complementar: fronteiras de exposição, recursos e engine

O dispatcher certificado [Ticking Item](../systems/ticking-item.md) liga ItemStack.inventoryTick à interface nativa e encaminha a entidade portadora e selected; não converte seleção em condição de irradiação. O certificado das quatro identidades [RadioactiveItem](../EXACT-RADIOACTIVE-CONSUMER-CENSUS-1.0.10.md) fixa a mesma lógica Code SHA do acInventoryTick, mas NÃO certifica o placement ou o bloco correspondente. A proteção Hazmat vale para o coeficiente do produtor, não concede imunidade global. O risco por chamada é nominal; não calcular probabilidade por segundo supondo frequência/stack constantes ou independência após o primeiro efeito. A modlist atual confirma NeoForge 21.1.250. Custo de crafting, colocação e exposição são caminhos distintos.

Receita shaped, nove uranium para um bloco (SHA-256 `99771f9748bf1ae78015ebb3925edfeebc2a77a3911c2ae8f9bdb1e5ae70e071`); receita shapeless de retorno, um bloco para nove uranium (`1917b3f4af98eb1d27c449c30d13756de10288313f89adfdfa50bffc678e3249`). Loot de bloco declara um roll e entrada do próprio item (`57cbb67895d67a34ba717e1c8f586c8209ba8dc43babddecc90afbeb8043e857`). Tags c:storage_blocks/uranium dos registries item e block têm o mesmo payload (SHA-256 `d7add0ba72b543411eeb285f314b141a9195dd054e3e6e76bd31f66cdac80dd8`), mas não são intercambiáveis. A compressão muda número de itens no inventário; a taxa nominal por unidade não é multiplicada por nove pela rotina de RadioactiveBlockItem. Não presumir que quebrar/colocar o bloco propaga o efeito do inventário.

Os recursos acima foram relidos no log SHA-exato da prova suplementar (job 139819307102). Limites de bloco colocado e consumidores não enumerados permanecem explícitos. `NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.


## Resultado do censo causal — #1240

[Run 45903382213/job 140194260474](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45903382213/job/140194260474): sete checks e dois relatórios byte-idênticos de 227.057 bytes SHA-256 `9708b284726f23dded9e4ad5268296f5ae437bd7aa115ea1bf62e7bc0abdd7a2`, 1.563 JSONs. [Dossiê](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-1.0.10.md) · [Selo por ID](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-SEAL-1.0.10.json).

`BlockItemWithSupplier` class SHA-256 `07a1c41d7b895e55e6c25c1dcb749703bed3c4a289592c958b4567a85a567d20`, quatro métodos próprios. `getBlock()` Code `34958b1e4ad3d0a7c35384b798190647caca05f7aac8bc9d6258af91b9393083` resolve supplier @4. `canFitInsideContainerItems()` Code `5fba881bd1a026278faca1b4a5a9eb6fc3eec8fed13571f9f16df3681035445e` retorna falso apenas para ShulkerBoxBlock; o bloco específico desta ficha não pertence a essa classe. `onDestroyed(ItemEntity)` Code `226813dc8af7ac6358213a35838f56fb39d5d9e717acb039d331303489bc9a46` somente no ramo ShulkerBoxBlock limpa CONTAINER @25 e solicita ItemUtils.onContainerDestroyed @41 se conteúdo anterior não nulo. `ACBlockRegistry.blockItemProperties()` Code `26961a0e9ab5a59780758d47ec0512a60c5ac8d3deab1d9982f6421393181e81` cria Item.Properties sem override. [Defaults 21.1.250](../EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md): stack nominal 64, sem durabilidade explícita. O uso/placement genérico e a execução após transformação não foram comprovados neste recorte.

**Bloco colocado:** supplier lambda$static$161 Code `039886b00152eeaeb98c1a20c5bd4dc7c99f786a8bedb9ba54b87b0c31dfdb8b` instancia UraniumFullBlock (class SHA `8146d2e9cd72977191d12039f00792fa9bb9b1c44ff8cc0fb1d9ac34817d8e51`, extends RotatedPillarBlock; 4/4 métodos). Construtor strength 3.5F, cor LIGHT_GREEN, som URANIUM, luz 4 via lambda$new$0 e emissiveRendering true via lambda$new$1. animateTick Code `7a8f43d993c7b487d79a0620f28582068d9a6a151f056eeec8b51753a54f1440` tem ramo nextInt(80)==0 com som local central, volume .5F, pitch .8F+.4F×nextFloat; ramo nextInt(13)==0 solicita partícula PROTON. Não há callback próprio de contato, dano ou status no bloco. O único Fieldref de gameplay/presentation fora dos registries é TremorzillaEntity.tick @3189, sob ramo cliente, construindo BlockParticleOption; não é consumo/ataque. Gloomoth light-source tag identifica consumidor de AI ainda não projetado; não inferir atratividade ou distância. Receita nuclear_bomb menciona a tag de armazenamento, no contexto de item, não o tag de bloco. Mantém pendência de placement e consumidor Gloomoth.

**Fieldrefs do registry neste recorte:**

| Owner/método | Offset | Opcode | Code SHA-256 |
|---|---:|---|---|
| `ACBlockRegistry.<clinit>` | 2304 | `putstatic` | `d4e20fc9df025209351d92f78283942e0817358a21a30b62c4b68dc9d93f082a` |
| `TremorzillaEntity.tick` | 3189 | `getstatic` | `de5ac1743a5711b29c50c50a519dd3df346d8e887544af72ec4a8f28873f7745` |
| `ACCreativeTabRegistry.lambda$static$10` | 886 | `getstatic` | `4a6ee5775221aa148147d7baedc4aa322f92ac71ff99476dccb039250004171e` |

**Atribuição completa de referências literais/possíveis tags no recorte data/:**

| Recurso | Caminho JSON / relação | SHA-256 |
|---|---|---|
| `data/alexscaves/loot_table/blocks/block_of_uranium.json` | `["pools",0,"entries",0,"name"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `57cbb67895d67a34ba717e1c8f586c8209ba8dc43babddecc90afbeb8043e857` |
| `data/alexscaves/recipe/block_of_uranium.json` | `["result","id"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `99771f9748bf1ae78015ebb3925edfeebc2a77a3911c2ae8f9bdb1e5ae70e071` |
| `data/alexscaves/recipe/nuclear_bomb.json` | `["key","B","tag"]` · POTENTIAL_BLOCK_TAG_REFERENCE | `94b861eaf1860011598df08221f3ccc8e8eb41485bd6cba07eb605364e4d081c` |
| `data/alexscaves/recipe/nuclear_bomb.json` | `["key","B","tag"]` · POTENTIAL_ITEM_TAG_REFERENCE | `94b861eaf1860011598df08221f3ccc8e8eb41485bd6cba07eb605364e4d081c` |
| `data/alexscaves/recipe/uranium_from_block.json` | `["ingredients",0,"item"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `1917b3f4af98eb1d27c449c30d13756de10288313f89adfdfa50bffc678e3249` |
| `data/alexscaves/tags/block/gloomoth_light_sources.json` | `["values",12]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `9aeda81133fcd264d5968a8cf77ce272e2d0645d07d0a7752642cc8bf767a866` |
| `data/c/tags/block/storage_blocks/uranium.json` | `["values",0]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `d7add0ba72b543411eeb285f314b141a9195dd054e3e6e76bd31f66cdac80dd8` |
| `data/c/tags/item/storage_blocks/uranium.json` | `["values",0]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `d7add0ba72b543411eeb285f314b141a9195dd054e3e6e76bd31f66cdac80dd8` |
| `data/minecraft/tags/block/mineable/pickaxe.json` | `["values",75]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `99e22d2a271e04796bc030a61f34273b8f1c5f14723c167dcd3b0c97501ed030` |
| `data/minecraft/tags/block/needs_iron_tool.json` | `["values",2]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `5fc249e25f5b3b98b6783ba19be2fba34cc6eee1f1b7829156e41054c22dd8cf` |

**Estado:** NOT_CERTIFIED / NO_MUTATION / NOT_TESTED; as lacunas indicadas acima não foram promovidas.
