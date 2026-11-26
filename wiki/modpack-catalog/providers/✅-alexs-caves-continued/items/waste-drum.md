# Waste Drum

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Item de bloco; sem nova raiz semântica certificada.

## Identidade e evidência

`alexscaves:waste_drum`; `RadioactiveOnDestroyedBlockItem`; Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-RADIOACTIVE-ITEMS-1.0.10.md). [Prova original](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45750603107/job/139677193397), 232.851 bytes SHA-256 `b8fd8880d0f888ee137a436ec0aa81ea7916c6e6883acc0237d2915525499c97`; [prova suplementar](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45793839880/job/139819307102), 1.106.955 bytes SHA-256 `52f90cc908f4e775a29711454c2a58a411dc491116020680d77eaf553a299709`; HEAD `e992226c0d80b5d6393e0a99de49d185c406a807`; dois replays idênticos de cada. Sem dump físico instalado novo.

ACBlockRegistry class SHA `b4de04f32f6e1d92eeda55480b8480f7ed69f3813164f330f49d0eced202e54c`; <clinit> Code SHA `d4e20fc9df025209351d92f78283942e0817358a21a30b62c4b68dc9d93f082a`: literal waste_drum @2192, supplier de bloco @2195, selector 5 @2200, registerBlockAndItem(String,Supplier,int) @2201, Field WASTE_DRUM:Ljava/util/function/Supplier; @2204. Helper Code SHA `d1a0bd80dc6b33272d28f317f10161bc4fbacda2d8b41529fe2a53d82141f32c`: registra bloco @5, recebe supplier de bloco, passa selector + supplier a getBlockSupplier @15, registra item com mesmo nome @18. getBlockSupplier Code SHA `0491a61abf0d322efcd2b927a9d55591d5f25a2f094e9d386121b5ad3ed45b68`: switch 5 -> @87, invokedynamic @88 ligado a lambda$getBlockSupplier$441. Factory Code SHA `6659fa766f94d238df90308e900913b9bb93b1edc19ea32f34b4f3a90b6e425f`: blockItemProperties @5, rate 0.01F @8, construtor @11. Vínculo declarativo, sem prova de registry transformado.

## Irradiação por inventário

Herdado de RadioactiveBlockItem (extends BlockItemWithSupplier), class SHA `1c769a4b64f0e4b3b9a2f5589bfc44ce3e27ec46c616b447d4e1359ffb21bd4b`, construtor Code SHA `668113e6779d9bb2128c47dc5f1b7210561d219af9d6fef79715ba835d2562af`. acInventoryTick(ItemStack,Level,Entity,boolean)V, 73 instruções, Code SHA `a98c07b15db89b72116500877e23e3f95db45ec8223dfeaa00fb76980bacc47d`. Servidor, entidade LivingEntity, Player não criativo, ausência de IRRADIATED; boolean selected não lido. Comparação float nextFloat() < count×0.01F×(1−HazmatArmorItem.getWornAmount(carrier)/4F); sem clamp explícito. Stack de 1, zero peças: 1% nominal por chamada elegível. [Hazmat](hazmat-mask.md) contador 0..4 por identidade e slot. addEffect(MobEffectInstance(IRRADIATED,1800)) @138 (amp0 default), retorno ignorado, mensagem visual posterior @160/163. Não consulta vizinhos ou tag de resistência explicitamente; sem dano direto, shrink, mana, cooldown ou XP. [Irradiated](../effects/irradiated.md) e [Radiation](../damage-types/radiation.md) são consumidores separados. Não confundir amp0 com dano periódico. Estado do efeito pela engine; sem NBT próprio demonstrado.

## Destruição e mundo

RadioactiveOnDestroyedBlockItem class SHA `853e1f6318cfaa2c97ab27955e6b068e4e5f34ab94f4354092233e69bc502f24`, construtor Code SHA `e1e5d733c7751a8bb39d327cb52e4c272a84e1e7c211af5ea84d834434afa25d`. onDestroyed(ItemEntity,DamageSource)V, 82 instruções, Code SHA `34f73b931946ae63544f4cbe9e35d1bd10fcab90f25b000bbdc54b98bc8b8881`: chama super @3; retorna se DamageSource.isCreativePlayer ou item já removido (@10/@17); discard @21. Cria AreaEffectCloud no x/y/z do item @44, sem owner setado nesse corpo, partícula GAMMAROACH @60, cor 7853582 @66. IRRADIATED 9600 ticks amp1 @92/95; radius2F @100, duration12000 @107, waitTime0 @112, radiusPerTick=-getRadius()/getDuration() float @117–127. Solicita addFreshEntity @135, retorno ignorado; solicita Level.explode @165 no x,y+0.5,z, parâmetro power1.8F, ExplosionInteraction.BLOCK; sem prova de dano final, raio efetivo ou autor da explosão. Nenhuma guarda explícita de lado/claims/PvP nesse corpo. Discard, cloud e explode não formam transação comprovada. Alvos, reapplication delay, redução real de duração/raio e descarte da nuvem dependem de AreaEffectCloud/engine; não inferir aplicação de 9600 ticks a cada vítima.

## Integração e validação

Sem hook mutador verificado. Não duplicar aplicação de status, consumo, cloud, descarte, explosão ou XP; não alterar proteção Hazmat global. Perks de exposição e mitigação são apenas possibilidades conceituais. WorldEffectPolicy deve preservar autoridade de Black Arcana sem presumir interceptação do provider. Pendências: ACBlockRegistry.blockItemProperties, BlockItemWithSupplier/placement, bloco específico, recipes/loot/tags transitivos, stack defaults, dispatch real, aceitação de addEffect, multiplayer e persistência, callback efetivo de destruição, área de efeito e explosão, owner e proteção de região. Contrato parcial; não certificar por identidade isolada. QA física NOT_TESTED.

## Evidência complementar: fronteiras de exposição, recursos e engine

O dispatcher certificado [Ticking Item](../systems/ticking-item.md) liga ItemStack.inventoryTick à interface nativa e encaminha a entidade portadora e selected; não converte seleção em condição de irradiação. O certificado das quatro identidades [RadioactiveItem](../EXACT-RADIOACTIVE-CONSUMER-CENSUS-1.0.10.md) fixa a mesma lógica Code SHA do acInventoryTick, mas NÃO certifica o placement ou o bloco correspondente. A proteção Hazmat vale para o coeficiente do produtor, não concede imunidade global. O risco por chamada é nominal; não calcular probabilidade por segundo supondo frequência/stack constantes ou independência após o primeiro efeito. A modlist atual confirma NeoForge 21.1.250. Custo de crafting, colocação e exposição são caminhos distintos.

Fronteira externa oficial 21.1.250: [selo](../EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json) identifica o patch ItemEntity.hurt que, no ramo health<=0, chama ItemStack.onDestroyed(this,damageSource) antes de discard. IItemStackExtension encaminha para getItem().onDestroyed(itemEntity,damageSource); o override de Waste Drum recebe a fonte. Não se prova o despacho transformado nem cada rota de descarte, e discard por si não deve ser tratado como dano letal.

Nuvem: [engine distribuída](../EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md) e [geometria](../EXACT-INK-BOMB-IMPACT-21.1.250.md) fixam width=2r/height=.5, busca LivingEntity dentro da AABB, filtro de distância horizontal <=r, isAffectedByPotions, gates de aplicabilidade e victims com delay nominal 20. Seleção a cada cinco ticks ativos, registro de cooldown antes do addEffect; instância customizada copiada sem a redução aplicada a efeitos de poção-base nesse ramo. O produtor Waste Drum usa waitTime=0, r=2, duração=12000, step=float32(-2/12000) e IRRADIATED amp1/9600. Modelo isolado: soma float32 recorrente r'=float32(r+step), sem alterações on-use/interrupção, primeira atualização com r<0.5 após 9001 reduções (r≈0.49994206), antes do limite temporal de 12000. É número de atualizações modeladas, não idade física garantida. O descarte por raio precede setRadius e busca nesse tick. Cloud não recebe owner explícito; persistência guarda timers, raio, particle, potion_contents e owner quando presente, não mapa victims. Explosão power 1.8 e cloud têm fronteiras distintas; nenhum dano ou raio de destruição efetivo inferido.

Advancement stop_nuclear_furnace_meltdown (SHA `ae6d3f12a76838420c21771f1f6731cbe5e882c627f9fd73f0669caaea329baa`) usa waste_drum como ícone, não prova que o item seja requisito ou causa do trigger.

Os recursos acima foram relidos no log SHA-exato da prova suplementar (job 139819307102). Limites de bloco colocado e consumidores não enumerados permanecem explícitos. `NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.


## Resultado do censo causal — #1240

[Run 45903382213/job 140194260474](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45903382213/job/140194260474): sete checks e dois relatórios byte-idênticos de 227.057 bytes SHA-256 `9708b284726f23dded9e4ad5268296f5ae437bd7aa115ea1bf62e7bc0abdd7a2`, 1.563 JSONs. [Dossiê](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-1.0.10.md) · [Selo por ID](../EXACT-BLOCK-RESOURCE-ATTRIBUTION-SEAL-1.0.10.json).

`BlockItemWithSupplier` class SHA-256 `07a1c41d7b895e55e6c25c1dcb749703bed3c4a289592c958b4567a85a567d20`, quatro métodos próprios. `getBlock()` Code `34958b1e4ad3d0a7c35384b798190647caca05f7aac8bc9d6258af91b9393083` resolve supplier @4. `canFitInsideContainerItems()` Code `5fba881bd1a026278faca1b4a5a9eb6fc3eec8fed13571f9f16df3681035445e` retorna falso apenas para ShulkerBoxBlock; o bloco específico desta ficha não pertence a essa classe. `onDestroyed(ItemEntity)` Code `226813dc8af7ac6358213a35838f56fb39d5d9e717acb039d331303489bc9a46` somente no ramo ShulkerBoxBlock limpa CONTAINER @25 e solicita ItemUtils.onContainerDestroyed @41 se conteúdo anterior não nulo. `ACBlockRegistry.blockItemProperties()` Code `26961a0e9ab5a59780758d47ec0512a60c5ac8d3deab1d9982f6421393181e81` cria Item.Properties sem override. [Defaults 21.1.250](../EXACT-ITEM-ENTITY-DEFAULTS-21.1.250.md): stack nominal 64, sem durabilidade explícita. O uso/placement genérico e a execução após transformação não foram comprovados neste recorte.

**Bloco colocado:** supplier lambda$static$154 Code `30cee093ea59043530072e12988396b7eeedfe0d935aac68d4b630139c4df39e` instancia WasteDrumBlock (class SHA `9f185182d50f9ace844a8327bc9237640adaa70b32b95735d6234ceae75a31b8`, 6/6 métodos), extends Block. strength 3.5F, som SCRAP_METAL, FACING default NORTH; getStateForPlacement @8/11/14 usa direção oposta a getNearestLookingDirection, rotate/mirror ajustam FACING. Não há override próprio de contato/explosão no bloco; destruição de ItemEntity permanece caminho distinto. 

Consumidores observados: NuclearFurnaceBlockEntity.tick @793–808 testa canFitInResultSlot(stack,4), @844–855 cria outra stack após ramo de barrelTime; BrainiacEntity.PickupBarrelGoal.isValidTarget @11–22 compara bloco na posição não nula, BrainiacEntity.dropEquipment @23–37 pede spawn de item condicionado por shouldDropBlocks; TremorzillaEntity.mobInteract @30–44 compara stack com asItem no ramo !isTame; registerGoals @110 insere item no array de objetivo; tick @3214 é BlockParticleOption cliente. Renderers e JEI não são resultados de gameplay. Ferromagnetic block/item tags, raycat_sleeps_on e galena crystallization (via tag) são caminhos de integração, não garantem atração, sono, cristalização ou dano. Necessária auditoria integral desses consumidores e de world safety antes de certificar.

**Fieldrefs do registry neste recorte:**

| Owner/método | Offset | Opcode | Code SHA-256 |
|---|---:|---|---|
| `ThrownWasteDrumEntityRenderer.render` | 199 | `getstatic` | `58a0d6857b4cf2c7d556e81da572d14c3ab794fae3e14c8fe20df0b6eee9f757` |
| `BrainiacBackBarrelLayer.render` | 120 | `getstatic` | `ccc03afe7c9979daa431cedbe6800f1eb43cf00a9623f9ca2374af301219bee8` |
| `NuclearFurnaceRecipeCategory.setRecipe` | 95 | `getstatic` | `ab7932e66cc36902383baf46ad7171408e3b2807e44773cd6d2c47c5207162f2` |
| `ACBlockRegistry.<clinit>` | 2204 | `putstatic` | `d4e20fc9df025209351d92f78283942e0817358a21a30b62c4b68dc9d93f082a` |
| `NuclearFurnaceBlockEntity.tick` | 793 | `getstatic` | `7a4ceaf1732f7423d0041531e1310c4f54e19317c4c5fd45f3011bc65eb2f2f1` |
| `NuclearFurnaceBlockEntity.tick` | 844 | `getstatic` | `7a4ceaf1732f7423d0041531e1310c4f54e19317c4c5fd45f3011bc65eb2f2f1` |
| `BrainiacEntity$PickupBarrelGoal.isValidTarget` | 11 | `getstatic` | `71c620f72a07525dacda3022b40a45a2d527701960671cb4d73d0d372206d12a` |
| `BrainiacEntity.dropEquipment` | 23 | `getstatic` | `a4d82afdbc333fcbab4f8bfbeab6cfd5750f5d08cf51d047218f564c7afd4c8f` |
| `TremorzillaEntity.mobInteract` | 30 | `getstatic` | `066e9d6d6927ee7d1c5f70722329856ac3df8b5a4a6f1831756f7485cd9eabf2` |
| `TremorzillaEntity.registerGoals` | 110 | `getstatic` | `36b12278d2793a72073efd211439367c9c11de278f4e6f6fa98547e0c06f0cbf` |
| `TremorzillaEntity.tick` | 3214 | `getstatic` | `de5ac1743a5711b29c50c50a519dd3df346d8e887544af72ec4a8f28873f7745` |
| `ACCreativeTabRegistry.lambda$static$10` | 841 | `getstatic` | `4a6ee5775221aa148147d7baedc4aa322f92ac71ff99476dccb039250004171e` |
| `ACCreativeTabRegistry.lambda$static$8` | 4 | `getstatic` | `f2bbaa648ab9f12380b4ceceeed6e4da53680426601d3f32515519e614b7477f` |

**Atribuição completa de referências literais/possíveis tags no recorte data/:**

| Recurso | Caminho JSON / relação | SHA-256 |
|---|---|---|
| `data/alexscaves/advancement/alexscaves/stop_nuclear_furnace_meltdown.json` | `["display","icon","id"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `ae6d3f12a76838420c21771f1f6731cbe5e882c627f9fd73f0669caaea329baa` |
| `data/alexscaves/advancement/alexscaves/tame_tremorzilla.json` | `["display","icon","id"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `c6833f5fe81d3119d3b816654a51a37c17a87fae08e4445fb9b56a37744f5733` |
| `data/alexscaves/loot_table/blocks/waste_drum.json` | `["pools",0,"entries",0,"name"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `5cb7972f440fdcac2ad056338fc559b988eefdae98a2645a006307a20f6eba99` |
| `data/alexscaves/loot_table/chests/toxic_ruins.json` | `["pools",0,"entries",8,"name"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `2bb1a858fc213060eb83765487b0f91093c81b7d53b7913364b1265571d3ffe3` |
| `data/alexscaves/recipe/waste_drum.json` | `["result","id"]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `b5cdde5c8cbbbe0ae634c77784bef704f2533736d9c6415a46e2870a40006062` |
| `data/alexscaves/tags/block/ferromagnetic_blocks.json` | `["values",5]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `250cf29361aba28c02ec0706b11bc2d48780bc6d7aafd189a5372fde4a53a3f0` |
| `data/alexscaves/tags/block/raycat_sleeps_on.json` | `["values",1]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `0d337411d9951d91ee83614cb159fb718e30716e59b61630870272531ca18cb9` |
| `data/alexscaves/tags/item/ferromagnetic_items.json` | `["values",4]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `d56b9514fe890d6b4eb1e256fd418683e7ec9aeb7032592168671f6851548dbf` |
| `data/alexscaves/tags/item/galena_gauntlet_crystallization_items.json` | `["values",0]` · POTENTIAL_ITEM_TAG_REFERENCE | `a66bc2d0071dac61445130165f3acbd050694a8613113d47293237557167fd05` |
| `data/minecraft/tags/block/mineable/pickaxe.json` | `["values",68]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `99e22d2a271e04796bc030a61f34273b8f1c5f14723c167dcd3b0c97501ed030` |
| `data/minecraft/tags/block/needs_stone_tool.json` | `["values",24]` · DIRECT_ID_REGISTRY_CONTEXT_REQUIRED | `25c340d57a0e318082610740495630260f10dfea29abf425953b31dfc42e8620` |

**Estado:** NOT_CERTIFIED / NO_MUTATION / NOT_TESTED; as lacunas indicadas acima não foram promovidas.
