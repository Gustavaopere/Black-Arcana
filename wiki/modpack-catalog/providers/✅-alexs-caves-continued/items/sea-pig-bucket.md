# Sea Pig Bucket

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21. Modlist sibling #19; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45653331096/job/139343330423), HEAD `b5bc7f2d5f70fe485036dc7e79285fa96ae7867b`, duas saídas idênticas de 335.054 bytes, SHA-256 `a9afad89d2771265dfbb4f86c2981bba8d204943e053d4364af82af69c5a7f41`. [Dossiê](../EXACT-MARINE-FISH-MOTH-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:sea_pig_bucket`; owner `ModFishBucketItem`; factory `ACItemRegistry.lambda$static$88`, Code SHA-256 `fc3ae35eecabc8a02f3f04ab286e47880a5b1f2742409b6101bd83a9ebca3072`. [Registro](../systems/item-registry.md). Transporte/liberação de entidade. Descrição interpretativa do binário. Modelo `assets/alexscaves/models/item/sea_pig_bucket.json`, SHA-256 `c6bbb41ba5899fa67e41113c291c2d0205073c0fce4456023c87b9e7c0e51d39`, apenas apresentação.

Factory referencia ACEntityRegistry.SEA_PIG; fluido supplier via `lambda$static$87` no bootstrap @7, corpo ainda não examinado; craftRemainder BUCKET.

## Ativação, efeitos, targeting e estado

ModFishBucketItem extends MobBucketItem; construtor resolve suppliers EntityType e Fluid, fornece BUCKET_EMPTY_FISH e stacksTo(1), guarda supplier de entidade. checkExtraContent exige ServerLevel, chama spawnFish @15 e solicita GameEvent.ENTITY_PLACE @25. spawnFish chama EntityType.spawn @24 com stack, Player nulo, posição, MobSpawnType.BUCKET e flags true/false. Se retorno implementa Bucketable, ACCompat.getOrCreateTag da stack → loadFromBucketTag @50 e setFromBucket(true) @58. addExtraAttributes @67 ocorre fora desse ramo; seu corpo próprio e appendHoverText são no-op. SweetishFishBucketItem é subclass direta e exige ficha/análise própria. Uma solicitação de spawn por execução; sem raio, AOE, dano, duração, scaling, comando ou vínculo de invocador próprios demonstrados.

## Custos, integração e limites

Custo final, retorno do balde, aquisição, captura, aceitação de spawn, restauração de componentes e fluido dependem da engine e do EntityType individual. Não inferir consumo ou captura pelo callback de soltura. MobBucketItem controla o uso herdado. Investigar save/load de Bucketable, dispensers, proteções de mundo e o supplier de fluido. NO_MUTATION: não duplicar entidade, reexecutar checkExtraContent, atribuir owner de summon ou creditar Mastery por tentativa. Não é nova magia de invocação.

## Localizadores de evidência

Classfile SHA-256 `9d22e586625f298993fbbf86b59ff2369cc3dccd9a9115b23d52778ed4c112dc`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Ljava/util/function/Supplier;Ljava/util/function/Supplier;Lnet/minecraft/world/item/Item$Properties;)V` | 16 | `224e2c3aaea571fa844d2996289b095aefd92c68998d23270ce802f918d7eef4` |
| `appendHoverText(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/Item$TooltipContext;Ljava/util/List;Lnet/minecraft/world/item/TooltipFlag;)V` | 1 | `149488d869cbef080602a371ab0d39d97af103fb726aaeb02ccd36c06f494e5d` |
| `checkExtraContent(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/core/BlockPos;)V` | 15 | `9afd208eba966e70dffc5385cd7ea9cfe66cc0b4cbe2d5629ff94fee058eb89b` |
| `spawnFish(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/core/BlockPos;)V` | 32 | `bd106b4cdeed0c33da4a95b9fe241ce074bebe0f7404a8d863d9ded5a9233945` |
| `addExtraAttributes(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;)V` | 1 | `149488d869cbef080602a371ab0d39d97af103fb726aaeb02ccd36c06f494e5d` |
