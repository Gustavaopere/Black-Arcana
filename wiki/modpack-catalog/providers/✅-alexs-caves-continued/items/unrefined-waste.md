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
