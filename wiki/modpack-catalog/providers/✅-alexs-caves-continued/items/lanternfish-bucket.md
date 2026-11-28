# Lanternfish Bucket

**Estado:** ✅ contrato técnico estático individual de transporte, delimitado; candidato à integração na main após CI. `STATIC_TECHNICAL_CATALOG_ONLY / mutating_hook=NOT_VERIFIED / runtime_dispatch=NOT_VERIFIED / perk_certification=NOT_CERTIFIED / physical_qa=NOT_TESTED / NO_MUTATION`. Não constitui nova raiz semântica certificada. Estados NOT_CERTIFIED nas etapas históricas abaixo descrevem a coleta, não a decisão estática final.

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

[Script](../../../../../docs/qa/alexscaves_1010_lanternfish_bucket_probe.py) e [workflow](../../../../../.github/workflows/alexscaves-1010-lanternfish-bucket.yml) preparados no commit `0e5052df83d67876269d06f96cf921b08edafdeb` e `77533d3e2e924f1f3c886d795a51ebc46b804af5`. Reutilizam pins de item/registry/class roster e helpers existentes. A sonda exige a sequência de registro LANTERNFISH, deriva o tipo da entidade pelo handle de construtor real, resolve fluido $79, projeta linhagem publisher e corpos pertinentes ao transporte/persistência/atributos, registra censo tipado e recursos data/ com ID exato ou basename. Dois replays determinísticos, orçamento e self-test de recurso exato. Não materializa outra vez a distribuição engine para os consumidores já demonstrados; não confundir com prova de dispatch integral. Sem nova medição local do publisher; prova obtida pelo runner remoto. A indisponibilidade de DNS local não foi testada nesta revisão.

Resultado da coleta: PENDENTE. Sem promoção de ledger, índices ou hook; sem nova raiz. A certificação depende da interpretação dos corpos específicos e reconciliação com as fronteiras engine previamente demonstradas, incluindo a auditoria complementar do Gossamer em curso. `STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.


## Primeira coleta individual aprovada — identidade, captura e persistência

[Run 46094200839/job 140821723742](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46094200839/job/140821723742), HEAD `10415ff3dde24aeeef59b6c91bc43546e7938a52`: job específico success; duas saídas idênticas de 144.928 bytes, SHA-256 `659f4e28dd43f66f3fd6949d9589d14604f50a8fc831d58868d84bbd22be23f0`. Publisher pinado, 1555 classes e 1563 JSON data/. Sem execução de jogo; sem certificado por herança.

### Registro, geometria e atributos
- ACItemRegistry.lambda$static$79()Fluid Code `17ddd17374a6af404edd3800059ef59916e856e35318f410ae35626c71e4da88` retorna Fluids.WATER @0. A factory do item $80 já selada entrega esse handle.
- ACEntityRegistry.<clinit> DEF_REG @636, literal lanternfish @639, bootstrap #152 @642, register @647 e LANTERNFISH @650. Handle resolve lambda$static$36()EntityType, Code `b1724b692eb8aeaef2c2dd9e12725e90659324091c4ed839e95ddb00e9fa6538`: construtor LanternfishEntity(EntityType,Level) por bootstrap #79; WATER_AMBIENT @5, sized(0.5F,0.4F) @17, id @23/build @26; sem setter de tracking/intervalo explícito no corpo.
- LanternfishEntity class SHA `10e48544cd4a543a0b0a1195ea8490d035a841555d3af5efb24d03d1f19da33f`, estende WaterAnimal, implementa Bucketable. Construtor Code `c159ee6dc2037d21f029d4bcf01f01a309e652d9aedf8985ecefd32e0b83079b`: circleSpeed=1F, fishPitch/prevFishPitch=0F, baitballCooldown recebe expressão com RandomSource.nextInt(100), circleTime=0, maxCircleTime=300, groupSize=1, LanternfishMoveControl e malus WATER=0. Não converter valores em velocidade efetiva, duração garantida ou atributo de conjurador.
- createAttributes Code `28a635657a59fe35bd82ed6c1024f91ddb7272875f9c8e28ceb479b74767780b`: Monster.createMonsterAttributes @0, MOVEMENT_SPEED=0.15D @9 e MAX_HEALTH=2D @18. São bases declaradas na factory de atributos, não garantia de binding/runtime ou HP atual após carga.

### Captura e retorno
mobInteract Code `a108290676d869fc0626387f7a35be505e5efa977041e11fd20005154494cea1`: Bucketable.bucketMobPickup @3, WaterAnimal.mobInteract @9, Optional.orElse @12; fallback ancestral é avaliado avidamente. A rota distribuída 21.1.250, já projetada na ficha Gossamer, exige Items.WATER_BUCKET e isAlive, solicita som, captura, createFilledResult(flag false), substituição de mão, FILLED_BUCKET server-side e descarte. O getter individual getBucketItemStack Code `e786e5bb885f4b819dbdc9c637f698d99f49a7499ff100a415a9c6600fe2d3e6` cria ItemStack do supplier LANTERNFISH_BUCKET; getPickupSound Code `020664486aaf05d848952a0018f4266b5b305439b2de85c2c1791f1ffa333eb3` retorna BUCKET_FILL_FISH. Não vincular ao owner de summon. A identidade da classe e do fluido permite reusar os consumidores comuns da engine (não a certificação de outro objeto).

### Persistência individual
- defineSynchedData Code `3424e254d3625b57203a93a68332ebc58fa587fceca765b07c76bd5c9fe1ce8b` define FROM_BUCKET=false após super; fromBucket Code `60cd160f918ea8fdfd5ccd4201f329b8f19b9c0cf2fe2092eaee97d66d9768e5`, setFromBucket Code `9b912993bd34384efae539fc33fa6f6fa671b0a6539f819fc905aa5faaf762e7` operam SynchedEntityData.
- saveToBucketTag Code `b17437a6fcea59e8f0d44aa61a4f7dd256c8d9199b2db040bf2aa43685147bb8`: nome condicional @12, CompoundTag/asOutput @33, addAdditionalSaveData @36, CUSTOM_DATA via getOrCreateTag @40, FishBucketTag @49 e setTag @55. loadFromBucketTag Code `57798f5c1094228d2ccd6baebfa3c0e0ac436d30ee8dc71e236818619e745d39`: se contém FishBucketTag, getCompound/asInput @25/readAdditionalSaveData @28; sempre setAirSupply(2000) @35. Não é duração de status ou garantia de respiração.
- addAdditionalSaveData Code `4647abf95f74e86567c0cf72866b23c6e101689efd39f70513b427314b0c45ed` e readAdditionalSaveData Code `b5e897f42ae4b20bdb941db027f42ebc0c067eaea1179dda5fb960119f34849e` delegam a WaterAnimal e escrevem/leem FromBucket; não escrevem explicitamente groupSize, leader ou timers próprios. Sem prova de persistência total de estado de escola, posição/UUID e lifecycle. requiresCustomPersistence Code `16fb8bc0367f15560f6aab163c450b5150d525879a2d8cefb9e30cfde107d049` = super || fromBucket; removeWhenFarAway Code `d8bd82adf2c92c105d8d9b03d60f44bf1ccea6d2feea21bd4a743cb7db98c38b` = !fromBucket && !hasCustomName. Não equivale a invulnerabilidade.
- finalizeSpawn Code `049864daae1de1522e2f0aa60923b0dba443ca3f0ef4e0707691b225a73aeaa7`: ramo groupData null cria GroupData @10, se não nulo lê groupLeader @24/chama createAndSetLeader @27; doInitialPosing @40 só com NATURAL @32/35; delega WaterAnimal.finalizeSpawn @49. BUCKET não executa essa pose; não transportar regras de formação natural para soltura. Falta fechar a autoria/estado da escola e os consumidores diretos de groupData.

### Recursos distribuídos
Censo de 1563 JSON data/, 11 hits exatos por ID/filename. Apenas abyssal_bucket contém ID de balde; os IDs alexscaves:lanternfish nos demais recursos são resolvidos conforme tipo de registry, não equivalem ao balde.
- Advancement abyssal_bucket SHA `09a9db7a36ccab1e5f017868b465e1e2a1ba07721dbc06a4e1d63e46be02c61b`: inventory_changed e grupo de requisitos alternativos de quatro buckets; não é gate de captura/uso nem receipt de Mastery.
- Bioma abyssal_chasm SHA `541769de5d56ef890e0b20fb317a6602f1ac32ca0d87c949ef5bbba5fd74d830`: water_ambient peso 100, grupos 15–20; regras de spawn e configuração efetiva externas não observadas. Não equivale à quantidade de soltura do balde.
- Loot de morte lanternfish SHA `84cd2c0811fb27b3dd6b5948fccd6533cc1e93a48d2cb2b15f7c37b781e5f835`: um roll, item lanternfish e furnace_smelt condicional on_fire. Loot de baú abyssal_ruins SHA `7542b7b2a0c95b8cb49fb498ebb06ed4d02c25ca68b22debcfd651e902599b96`: peixe item, peso 12, count 1–2; não balde. Sushi, receitas de cozimento, tags item fishes/raw_meats referem peixe como item, não custo de transporte. Tag entity_type seafloor_denizens SHA `8f688e5ac71562265abe6ab76c0ad339318709e1a774ec382b926ee2f137f6f5` contém tipo lanternfish; comentário de recurso não prova consumidor efetivo. Nenhuma receita/loot direta do balde no recorte literal; não excluir tags indiretas, loot modifiers ou datapacks.
- Censo tipado: nove owners, incluindo entity, registry, render/model e classes internas GroupData, JoinSchoolGoal, LanternfishMoveControl, SwimInSchoolGoal. Não equivale a callsites executados.

### Coleta complementar preparada
Schema 2 no commit `752741d01f3eb5087c97b92f5da6dcebd4b5a084` mantém os pins acima e acrescenta corpos próprios de groupData, limites de escola, tick/airSupply e consumers JoinSchoolGoal/SwimInSchoolGoal; orçamento finito, sem execução. Não promover até interpretar saída e reusar (quando concluídas) as fronteiras comuns de liquidação do Gossamer. Não confundir atributo de mob com escala de dano de um cast. Sem hook, QA física, ledger ou índices. `STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`.


## Segunda coleta aprovada — estado de cardume e lifecycle próprio

[Run 46094534407/job 140822758163](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46094534407/job/140822758163), HEAD `f4119b4e208cb602e23f067c78703d884adca334`: job específico success, duas saídas de 398.523 bytes SHA-256 `c8e493ad2c6a692b61f62fec73e2f4f31c1e36f1911e70fed8e41a01fd66f007`, schema 2. Pins de entidade/fluido/factory e três classes de escola verificados. Sem jogo, sem afirmação de CI final do HEAD posterior.

### Cardume — limites nominais, estado não transportado explicitamente
- getMaxGroupSize Code `de35150e24150e8208c82ef524cd41667de4ba7abacbe7bfaef5eba4fc4531b6` retorna 20; getMaxSpawnClusterSize Code `d213d42b55d9646f9176cbe3a35c7f86f5129c3eb3f9a8cf24cf0a40dd6d78ee` delega ao anterior; isMaxGroupSizeReached Code `42ca1f85243342bd41983ab86f2235408fa46ded7466d4525196f66b9dbb5f3e` retorna false. Não tratar 20 como clamp universal de todas as rotas.
- isGroupLeader Code `0af01cbbe94e945d39daabe4058833bedcc65e3109e7a7eea0a79aec201a4122` = groupSize>1; hasGroupLeader Code `6f5b5cabf90a4203f36cc02e916546463c50b7fdb4dfeeb44c3a66786261ace7` exige referência não nula e líder vivo. canGroupGrow Code `fff92554322392a85c93b4dc133e71450e63856e92ad47f13fc9377e3a2b4856` exige isGroupLeader e groupSize<getMaxGroupSize. increase/decrease Code `44ba8f289e9fd8cf22f90e6cc1f45a1641b9402c58d56b824a02165957915b9e` / `4d760bf7f10328b87f73a6fb4b7d2ef5a34fb3f7d18382a01446fa4d83cd209f` somam/subtraem 1 sem clamp local.
- createAndSetLeader Code `f92c851664af4ee758aa8fc97a32cd2e76215582edadc06ab3dfb0b4ba2adce9` escreve groupLeader @2 e chama increaseGroupSize no líder @6; leaveGroup Code `4ecf4f6b37e94ebcfdd7f844d5c81d8bc44f002860a5d0765f4f8882630e5087` decrementa líder não nulo @11 e limpa referência @16. GroupData.<init> Code `8d1dc0f647dcc32588ab1c954b0b8cecaeee2a9aafa32395f5b6f687c6b5b5cb` passa 0.05F ao construtor ancestral e armazena groupLeader. No spawn do balde, grupo recebido pela factory é nulo no caminho engine projetado; não inferir reprodução, summon múltiplo ou preservação de vínculo de líder.
- inRangeOfGroupLeader Code `ffb1e1cceb8e8b6ff544ebf3088b00a708ee8449113775c3069f4346b0b518a8`: distância quadrada <=121D (11 blocos nominais). moveToGroupLeader Code `f2c37b7b95ddc343f95ab6835cef92df91b9ed13e575ea5620057e259e3e54ce`: se hasGroupLeader, solicita navigation.moveTo nas coordenadas do líder com argumento 1D. Distância de IA, não targeting de captura/cast.
- registerGoals Code `86f3da20b7265f86f138ba1ca6d94378ba1a01f7116e485e06277ca604287e94`: prioridades 0 SwimInSchoolGoal, 1 JoinSchoolGoal, 2 RandomLookAroundGoal, 3 LookAtPlayerGoal com 6F. JoinSchoolGoal.canUse Code `eb624d0360556cca00d90f1fef2357135e418a16cac6293510784cab14eea93e`: não inicia se líder ou circulando, aceita líder atual, verifica temporizador e busca LanternfishEntity em AABB expandida 8D por eixo. Filtra candidato canGroupGrow ou sem líder, e chama createFromStream com candidatos sem líder; corpo de createFromStream não projetado neste recorte. canContinueToUse Code `43b3c7e921bcc0f467e64f1fdce7a0c4f382b908323e972f59ff5629cfbd19b7` requer líder válido, distância e !isCircling; stop Code `8aedbdd53f7af6171931958435a025202de6f181cf9a84940f792733deccd8f0` chama leaveGroup. tick Code `059af56262497994225213c009738e972a4d68f71e47bb97585265cd97a58856` solicita recálculo de caminho no delay ajustado de 10. Não atribuir frequência exata de execução do goal sem scheduler.
- SwimInSchoolGoal.tick Code `813a41360db794d8ab0dcd5811842eec6ea609b63fd589a4fee7a12b8ef57236`: condições e consumidores de circlePos/time/maxTime/speed, orbitAroundPos e navigation.moveTo; líder redefine cooldown=100+nextInt(150), maxCircleTime=100+nextInt(200), circleDistance=1+nextFloat()*1.5F e circleSpeed=0.75F+nextFloat()*0.5F; seguidor copia circlePos/time/maxTime do líder e sorteia distância/speed/direção. Estado não é explicitamente salvo por addAdditionalSaveData do animal. Não chamar esses delays de cooldown de item. orbitAroundPos Code `c44c7b2e55b3f696702662ddf99dc3ddbf3c8d366ad91f085762d45469a110b4` e findSwimToPos Code `cd52efea24b7e4bb53dddf39486342a3b82e314088f6251905b52679a754ec99` selecionam trajetória e ponto aquático, não dano/AOE. Escopo não fecha toda a IA.
- handleAirSupply(I)V Code `4f307edf27f7ee64141bbdddf8e2758d83b9fd6064ad6377aa3a64a64596fc83`: vivo fora de água/bubble, setAirSupply(input-1) @18, se getAirSupply==-20, seta 0 e solicita hurt(dryOut,2F) @44; caso contrário ao ramo externo, setAirSupply(200) @55. Assim 2000 escrito após carga não é duração garantida; água pode redefinir o valor para 200. Dano de ressecamento do mob, não dano causado pelo uso do balde. tick Code `37c26a33aa2b5cc2b18d36bc35689adb9dbd59c38a7f08ead2082cbbec9bc430` inclui flop fora de água e decremento baitballCooldown quando positivo; não é efeito de perk ou cast.

### Reuso adicional da engine
Schema 5 do Gossamer [run 46094303735/job 140822035239](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46094303735/job/140822035239) confirma dois relatórios de 2.379.853 bytes SHA-256 `c9275d19e66b94acf68bd21caa9e18387a95e7eb813bea806fdb9850ac12d8c2`, mesma engine 21.1.250 e classe ModFishBucketItem. Attributes.BLOCK_INTERACTION_RANGE default declarado 4.5D, min 0, max 64, consumidor raycast usa valor efetivo; CommonHooks.onPlayerTossEvent admite cancelamento e ignora booleano de inserção, Stack/Inventory/CompoundTag têm fronteiras descritas na ficha Gossamer branch correspondente. Reusar evidências de engine exata, não certificação por analogia.

### Disposição do contrato delimitado
Identidade, ativação/captura/soltura, parâmetros, targeting, custo e retorno, estado e integração de transporte têm evidência suficiente para revisão individual; mana, cooldown de item, dano ofensivo, AOE, cast time e summon de combate próprios são N/A nesse recorte. IA integral de cardume (incluindo createFromStream e movimento), consumidores de tags externos, mutação de atributos, QA física e valores efetivos não estão certificados. Não confundir transporte com certificado integral do animal. A promoção do ledger/crosswalk será reconciliada com os PRs #1255 e #1257; por enquanto `NOT_CERTIFIED / NO_MUTATION / NOT_TESTED`. Nenhuma nova raiz.


## Certificação individual — escopo de captura e transporte

| Eixo | Evidência delimitada |
|---|---|
| identity | Factory $80/$79, registry $36, LanternfishEntity e modelo SHA-exatos. |
| behavior | Captura individual, soltura compartilhada com identidade comprovada, dispenser, callbacks e recusa de engine; estado de cardume separado. |
| parameters | Stack nominal 1, dimensões 0.5x0.4, HP 2, movimento 0.15, ar 2000 restaurado e dryOut próprio da entidade; ausência de cast/dano/AOE próprios. |
| targeting | Captura em entidade viva com water bucket; raycast de bloco por atributo e permissões da engine exata; cardume não targeting de item. |
| costs | Captura, consume/creative, retorno de balde e descarte; loot de peixe não balde; boundaries compartilhados comprovados. |
| integration | FishBucketTag individual, FromBucket, CUSTOM_NAME/ENTITY_DATA, grupo/líder não gravados explicitamente, recusa de spawn e toss; NO_MUTATION. |
| validation | Schema 2 run 46094534407/job 140822758163, dois relatórios 398523 bytes SHA-256 c8e493ad2c6a692b61f62fec73e2f4f31c1e36f1911e70fed8e41a01fd66f007; engine schema 5 comprovada em run 46094303735. |

Certificado individual registrado no ledger da branch consolidada, não na main até merge. N/A: mana, cast time, cooldown de item, dano/AOE ofensivos e owner de summon de combate não pertencem à ação de transporte comprovada; valores efetivos, IA integral, mutação, runtime e QA física seguem separados. Não reemitir callbacks, inventário, entidades ou Mastery. `STATIC_TECHNICAL_CATALOG_ONLY / NO_MUTATION / NOT_VERIFIED / NOT_TESTED`.
