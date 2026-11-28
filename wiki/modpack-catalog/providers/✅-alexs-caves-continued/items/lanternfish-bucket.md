# Lanternfish Bucket

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21. Modlist sibling #19; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45653331096/job/139343330423), HEAD `b5bc7f2d5f70fe485036dc7e79285fa96ae7867b`, duas saídas idênticas de 335.054 bytes, SHA-256 `a9afad89d2771265dfbb4f86c2981bba8d204943e053d4364af82af69c5a7f41`. [Dossiê](../EXACT-MARINE-FISH-MOTH-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:lanternfish_bucket`; owner `ModFishBucketItem`; factory `ACItemRegistry.lambda$static$80`, Code SHA-256 `890937e2190ba7e244b6f1dc3c35740b4af2802b9096780d845497837ba47581`. [Registro](../systems/item-registry.md). Transporte/liberação de entidade. Descrição interpretativa do binário. Modelo `assets/alexscaves/models/item/lanternfish_bucket.json`, SHA-256 `64a2ccfbda89984d68eeb71707ebc909628451db9b176c6150a4f89facedb87a`, apenas apresentação.

Factory referencia ACEntityRegistry.LANTERNFISH; fluido supplier via `lambda$static$79` no bootstrap @7, corpo ainda não examinado; craftRemainder BUCKET.

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


## Continuação individual — evidências reaproveitadas e coleta preparada

Base Black Arcana `90be29b5fc21c1a357e545809c8057fa3625119b`, modlist sibling `b05e2536461bc0a9c526dc47a38e3b9af62d941c` (#001 NeoForge 21.1.250, #019 publisher 1.0.10). Releitura dos logs [45653331096/job 139343330423](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45653331096/job/139343330423): factory $80, 33 bytes de Code / 13 instruções, instruction SHA-256 `2727e115dce63cbe14f4cae6499205cac3d129c6dd03f31b725b377cbce78af2`, LANTERNFISH @4, fluid bootstrap #10 @7 -> $79, BUCKET @19/craftRemainder @22, stacksTo(1) @26, construtor ModFishBucketItem @29. O registro de item comprova também LANTERNFISH_BUCKET -> FluidContainerDispenseItemBehavior @267 no setup; não é o mesmo binding de Gossamer @330.

### Reuso causal restrito à classe compartilhada e engine distribuída

A ficha [Gossamer Worm Bucket](gossamer-worm-bucket.md) registra duas auditorias da mesma classe ModFishBucketItem e NeoForge 21.1.250 ([schema 3](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46072668781/job/140753053471), dois relatórios SHA-256 `41d1a0a171c156db71dc32b8035eee812f01d36ae39146d41ed7fdcbc8a3dfdb`, 1.848.274 bytes). Para Lanternfish, a identidade da factory $80 comprova a mesma classe construída; suas rotas próprias de spawn, não a identidade/atributos do animal, podem ser reutilizadas. Reutilização do downstream de BucketItem/MobBucketItem e Bucketable é condicional à resolução do fluido e à declaração/linhagem do animal; nenhuma transferência de certificado.

- A inserção solicitada por EntityType.spawn usa addFreshEntityWithPassengers void, sem agregar retorno booleano do manager. Recusa por EntityJoinLevelEvent ou UUID duplicado é possível no engine distribuído. Não contar ENTITY_PLACE, ITEM_USED ou referência criada como receipt de inserção.
- A rota nativa do dispenser compartilhado recebe a stack, solicita emptyContents, em sucesso invoca checkExtraContent e retorna novo BUCKET; em falha solicita fallback de DefaultDispenseItemBehavior. Não atribuir ao jogador um summon sem evidência. Não repetir, reembolsar ou debitar por inferência.
- CUSTOM_DATA lido via ACCompat.getOrCreateTag é cópia, não gravação; ENTITY_DATA é outro canal. FishBucketTag foi comprovado para Gossamer, NÃO para Lanternfish. Persistência específica, mobInteract, alvo de captura, NBT e dimensões ainda exigem projeção individual.

### Sonda publisher-only

[Script](../../../../../docs/qa/alexscaves_1010_lanternfish_bucket_probe.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-lanternfish-bucket.yml) preparados no commit `0e5052df83d67876269d06f96cf921b08edafdeb` e `77533d3e2e924f1f3c886d795a51ebc46b804af5`. Reutilizam pins de item/registry/class roster e helpers existentes. A sonda exige a sequência de registro LANTERNFISH, deriva o tipo da entidade pelo handle de construtor real, resolve fluido $79, projeta linhagem publisher e corpos pertinentes ao transporte/persistência/atributos, registra censo tipado e recursos data/ com ID exato ou basename. Dois replays determinísticos, orçamento e self-test de recurso exato. Não materializa outra vez a distribuição engine para os consumidores já demonstrados; não confundir com prova de dispatch integral. Sem nova medição local do publisher (DNS indisponível no container nesta sessão).

Resultado da coleta: PENDENTE. Sem promoção de ledger, índices ou hook; sem nova raiz. A certificação depende da interpretação dos corpos específicos e reconciliação com as fronteiras engine previamente demonstradas, incluindo a auditoria complementar do Gossamer em curso. `STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.
