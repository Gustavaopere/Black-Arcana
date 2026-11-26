# Unrefined Waste

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Item de bloco; sem nova raiz semântica certificada.

## Identidade e evidência

`alexscaves:unrefined_waste`; `RadioactiveBlockItem`; Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-RADIOACTIVE-ITEMS-1.0.10.md). [Prova original](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45750603107/job/139677193397), 232.851 bytes SHA-256 `b8fd8880d0f888ee137a436ec0aa81ea7916c6e6883acc0237d2915525499c97`; [prova suplementar](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45793839880/job/139819307102), 1.106.955 bytes SHA-256 `52f90cc908f4e775a29711454c2a58a411dc491116020680d77eaf553a299709`; HEAD `e992226c0d80b5d6393e0a99de49d185c406a807`; dois replays idênticos de cada. Sem dump físico instalado novo.

ACBlockRegistry class SHA `b4de04f32f6e1d92eeda55480b8480f7ed69f3813164f330f49d0eced202e54c`; <clinit> Code SHA `d4e20fc9df025209351d92f78283942e0817358a21a30b62c4b68dc9d93f082a`: literal unrefined_waste @2321, supplier de bloco @2324, selector 4 @2329, registerBlockAndItem(String,Supplier,int) @2330, Field UNREFINED_WASTE:Ljava/util/function/Supplier; @2333. Helper Code SHA `d1a0bd80dc6b33272d28f317f10161bc4fbacda2d8b41529fe2a53d82141f32c`: registra bloco @5, recebe supplier de bloco, passa selector + supplier a getBlockSupplier @15, registra item com mesmo nome @18. getBlockSupplier Code SHA `0491a61abf0d322efcd2b927a9d55591d5f25a2f094e9d386121b5ad3ed45b68`: switch 4 -> @80, invokedynamic @81 ligado a lambda$getBlockSupplier$440. Factory Code SHA `97cdb48022a1d0e97196956a30d852cc346aad92de1c88cc8f6590109bfd71f3`: blockItemProperties @5, rate 0.001F @8, construtor @11. Vínculo declarativo, sem prova de registry transformado.

## Irradiação por inventário

Herdado de RadioactiveBlockItem (extends BlockItemWithSupplier), class SHA `1c769a4b64f0e4b3b9a2f5589bfc44ce3e27ec46c616b447d4e1359ffb21bd4b`, construtor Code SHA `668113e6779d9bb2128c47dc5f1b7210561d219af9d6fef79715ba835d2562af`. acInventoryTick(ItemStack,Level,Entity,boolean)V, 73 instruções, Code SHA `a98c07b15db89b72116500877e23e3f95db45ec8223dfeaa00fb76980bacc47d`. Servidor, entidade LivingEntity, Player não criativo, ausência de IRRADIATED; boolean selected não lido. Comparação float nextFloat() < count×0.001F×(1−HazmatArmorItem.getWornAmount(carrier)/4F); sem clamp explícito. Stack de 1, zero peças: 0.1% nominal por chamada elegível. [Hazmat](hazmat-mask.md) contador 0..4 por identidade e slot. addEffect(MobEffectInstance(IRRADIATED,1800)) @138 (amp0 default), retorno ignorado, mensagem visual posterior @160/163. Não consulta vizinhos ou tag de resistência explicitamente; sem dano direto, shrink, mana, cooldown ou XP. [Irradiated](../effects/irradiated.md) e [Radiation](../damage-types/radiation.md) são consumidores separados. Não confundir amp0 com dano periódico. Estado do efeito pela engine; sem NBT próprio demonstrado.

## Destruição e mundo

Não há override próprio onDestroyed na classe RadioactiveBlockItem. Não transferir nuvem/explosão do subclass Waste Drum para este item. Efeitos do bloco colocado, quebra, interações, propriedades, custo e placement herdado não auditados nesta ficha.

## Integração e validação

Sem hook mutador verificado. Não duplicar aplicação de status, consumo, cloud, descarte, explosão ou XP; não alterar proteção Hazmat global. Perks de exposição e mitigação são apenas possibilidades conceituais. WorldEffectPolicy deve preservar autoridade de Black Arcana sem presumir interceptação do provider. Pendências: ACBlockRegistry.blockItemProperties, BlockItemWithSupplier/placement, bloco específico, recipes/loot/tags transitivos, stack defaults, dispatch real, aceitação de addEffect, multiplayer e persistência, comportamento do bloco no mundo. Contrato parcial; não certificar por identidade isolada. QA física NOT_TESTED.

## Evidência complementar: fronteiras de exposição, recursos e engine

O dispatcher certificado [Ticking Item](../systems/ticking-item.md) liga ItemStack.inventoryTick à interface nativa e encaminha a entidade portadora e selected; não converte seleção em condição de irradiação. O certificado das quatro identidades [RadioactiveItem](../EXACT-RADIOACTIVE-CONSUMER-CENSUS-1.0.10.md) fixa a mesma lógica Code SHA do acInventoryTick, mas NÃO certifica o placement ou o bloco correspondente. A proteção Hazmat vale para o coeficiente do produtor, não concede imunidade global. O risco por chamada é nominal; não calcular probabilidade por segundo supondo frequência/stack constantes ou independência após o primeiro efeito. A modlist atual confirma NeoForge 21.1.250. Custo de crafting, colocação e exposição são caminhos distintos.

Receitas furnace/uranium_shard_blasting.json e furnace/uranium_shard_smelting.json (SHA-256 `3655bc694c8f900b9e9001651fe3da845328ce0741581354f42950ae9a5cb1b7` e `eadb37b66ecdaf22c44bc45c4fdb28f3a9816a97b23252afa57ca6eabecd16ac`): ambas declaram ingrediente unrefined_waste, resultado uranium_shard, 100 ticks e XP 1.0. A duração igual nos dois tipos é do recurso, não convenção presumida do vanilla. Transformar insumo altera identidade e não duplica cast, efeito ou XP. Sem inferir comportamento do bloco colocado.

Os recursos acima foram relidos no log SHA-exato da prova suplementar (job 139819307102). Limites de bloco colocado e consumidores não enumerados permanecem explícitos. `NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.


## Resultado do censo causal — #1240

[Run 45903382213/job 140194260474](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45903382213/job/140194260474): sete checks e dois relatórios byte-idênticos de 227.057 bytes SHA-256 `9708b284726f23dded9e4ad5268296f5ae437bd7aa115ea1bf62e7bc0abdd7a2`, 1.563 JSONs. [Dossiê](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-1.0.10.md) · [Selo por ID](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-SEAL-1.0.10.json).

`BlockItemWithSupplier` class SHA-256 `07a1c41d7b895e55e6c25c1dcb749703bed3c4a289592c958b4567a85a567d20`, quatro métodos próprios. `getBlock()` Code `34958b1e4ad3d0a7c35384b798190647caca05f7aac8bc9d6258af91b9393083` resolve supplier @4. `canFitInsideContainerItems()` Code `5fba881bd1a026278faca1b4a5a9eb6fc3eec8fed13571f9f16df3681035445e` retorna falso apenas para ShulkerBoxBlock; o bloco específico desta ficha não pertence a essa classe. `onDestroyed(ItemEntity)` Code `226813dc8af7ac6358213a35838f56fb39d5d9e717acb039d331303489bc9a46` somente no ramo ShulkerBoxBlock limpa CONTAINER @25 e solicita ItemUtils.onContainerDestroyed @41 se conteúdo anterior não nulo. `ACBlockRegistry.blockItemProperties()` Code `26961a0e9ab5a59780758d47ec0512a60c5ac8d3deab1d9982f6421393181e81` cria Item.Properties sem override. [Defaults 21.1.250](../EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md): stack nominal 64, sem durabilidade explícita. O uso/placement genérico e a execução após transformação não foram comprovados neste recorte.

**Efeito adicional no bloco colocado — distinto de inventário.** Supplier lambda$static$163 Code `88f6a8b0ca9d1745667ce7f2923c9902471ff372fe891e480df068a2dc3de39d` instancia UnrefinedWasteBlock (class SHA `72f6127bc522cd40553bdffb919ea42ce4870273cf92282efe533aaed67a046a`, 11/11 métodos), extends FallingBlockWithColor (SHA `de17b8426736df4bdb494111279c53ddf61b5c0db981af04cf22b87c679c6b64`, 3/3, extends FallingBlock). strength .5F, luz 3, emissive true, dustColor 60928; collision shape box(0.1,0.1,0.1,15.9,14,15.9) em unidades 1/16 bloco, visual e support full block. `entityInside` Code `dae1b651c6bfafb537b8a61157d58ae7996f37c71aa06699343736110c887a34` exige LivingEntity @2 e ausência de RESISTS_RADIATION no tipo @26. Solicita setDeltaMovement(vx×0.9,vy,vz×0.9) @49 e addEffect(IRRADIATED,4000 ticks, amp0 default) @78; retorno ignorado. Não há guarda explícita de servidor, Hazmat, creative, efeito existente, dano direto, owner ou cooldown nesse corpo. A cada callback elegível, não necessariamente a cada tick físico; não confundir forma de colisão com raio de aura. Amp0 não executa tick periódico próprio, mas pode bloquear heal por consumidor de presença. AnimateTick nextInt(2)==0 e face vizinha não oclusiva ou não sólida seleciona GAMMAROACH/HAZMAT_BREATHE; apenas apresentação. FallingBlockWithColor.codec delega unsupportedBlockCodec; não inferir persistência de entidade caindo.

Fieldrefs de gameplay: NuclearFurnaceBlockEntity.destroyWhileCritical @18 lê default state após currentWaste=0; AcidFluidType.onVaporize @150 solicita setBlockAndUpdate @164 e descarta retorno; TremorzillaEntity.createEggBeddingBlockState @0–14 retorna default state. Esses são caminhos de produção/uso distintos, não provas de resultado. Receita de Waste Drum referencia UNREFINED_WASTE e há receita própria e loot, listados abaixo. Pendentes corpos completos de consumidores, falling block e world safety. Perks de velocidade, duração do status, resistência e exposição de inventário têm fronteiras diferentes; não alterar tag global nem duplicar callbacks.

**Fieldrefs do registry neste recorte:**

| Owner/método | Offset | Opcode | Code SHA-256 |
|---|---:|---|---|
| `ACBlockRegistry.<clinit>` | 2333 | `putstatic` | `d4e20fc9df025209351d92f78283942e0817358a21a30b62c4b68dc9d93f082a` |
| `NuclearFurnaceBlockEntity.destroyWhileCritical` | 18 | `getstatic` | `e354ae78664f5167d9de96453ae69aab7127eecfbcd41f80bba944538cca575c` |
| `AcidFluidType.onVaporize` | 150 | `getstatic` | `3065c4ada2540a1fcb0443062ea37a42b189618dd00468280c16a8d8925ab872` |
| `TremorzillaEntity.createEggBeddingBlockState` | 0 | `getstatic` | `f0560e61af0b64a782ae929e838e59b56a484e445593f5ae11c56c0dac02aaac` |
| `ACCreativeTabRegistry.lambda$static$10` | 916 | `getstatic` | `4a6ee5775221aa148147d7baedc4aa322f92ac71ff99476dccb039250004171e` |

**Atribuição completa de referências literais/possíveis tags no recorte data/:**

| Recurso | Caminho JSON / relação | SHA-256 |
|---|---|---|
| `data/alexscaves/loot_table/blocks/unrefined_waste.json` | `["pools",0,"entries",0,"name"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `a905215e2de34cbd75862b4d181c3b8513def796a19c713013771ba2733c3b70` |
| `data/alexscaves/recipe/furnace/uranium_shard_blasting.json` | `["ingredient","item"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `3655bc694c8f900b9e9001651fe3da845328ce0741581354f42950ae9a5cb1b7` |
| `data/alexscaves/recipe/furnace/uranium_shard_smelting.json` | `["ingredient","item"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `eadb37b66ecdaf22c44bc45c4fdb28f3a9816a97b23252afa57ca6eabecd16ac` |
| `data/alexscaves/recipe/unrefined_waste.json` | `["result","id"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `12be3df081d4158df0b1d984cb90921b95e5d5301853677dc2de5f3a0952c332` |
| `data/alexscaves/recipe/waste_drum.json` | `["key","U","item"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `b5cdde5c8cbbbe0ae634c77784bef704f2533736d9c6415a46e2870a40006062` |
| `data/alexscaves/worldgen/configured_feature/unrefined_waste_replace_mud.json` | `["config","targets",0,"state","Name"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `a0560578c70d161ff0b66c8d791d2b2ef9dc0783de57cb11ac57be6cbb8ea1f1` |
| `data/minecraft/tags/block/mineable/shovel.json` | `["values",1]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `4e5ec0ebe7259c65a96dd89934e0a54d91c082e3ae0c154486e3314d1760dff2` |

**Estado:** NOT_CERTIFIED / NO_MUTATION / NOT_TESTED; as lacunas indicadas acima não foram promovidas.
