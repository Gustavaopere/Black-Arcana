# Marine Snow

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (`alexscaves`) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21. Modlist sibling #19; publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45653331096/job/139343330423), HEAD `b5bc7f2d5f70fe485036dc7e79285fa96ae7867b`, duas saídas idênticas de 335.054 bytes, SHA-256 `a9afad89d2771265dfbb4f86c2981bba8d204943e053d4364af82af69c5a7f41`. [Dossiê](../EXACT-MARINE-FISH-MOTH-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:marine_snow`; owner `MarineSnowItem`; factory `ACItemRegistry.lambda$static$90`, Code SHA-256 `d385d5b08e71c8ae683c30c5f0402acecbcb5ec0b6f13d0e33c25bbf57cdf7ba`. [Registro](../systems/item-registry.md). Insumo de crescimento/recuperação e duplicação de blocos aquáticos. Descrição interpretativa do binário. Modelo `assets/alexscaves/models/item/marine_snow.json`, SHA-256 `179f4314608e9b3f7b8351759bc30e0a1641620c978e909f568e9daf31e4451c`, apenas apresentação.

## Ativação, efeitos e parâmetros

useOn inicializa mapas; scanForWater verifica FluidTags.WATER no bloco clicado ou em uma posição adjacente de cada Direction. Sem água retorna PASS. O alvo é o bloco clicado. GROWS_INTERACTIONS contém 20 pares de corais mortos → vivos (TUBE, BRAIN, BUBBLE, FIRE, HORN × bloco, planta, fan, wall fan); copia propriedades compatíveis e solicita setBlockAndUpdate @152. DUPLICATES_INTERACTIONS contém 25 entradas (20 corais vivos, SPONGE → WET_SPONGE, WET_SPONGE → WET_SPONGE, anêmonas DUSK/TWILIGHT/MIDNIGHT); nextInt(2)==0 pede ItemEntity no click location, addFreshEntity @254. A flag de interação é ajustada antes do sorteio. MUSSEL com MUSSELS < 5 recebe pedido de +1 via setBlockAndUpdate @334. Retornos de alteração/inserção descartados. Se flag de interação, evento 1505 no lado não cliente; shrink(1) fora de creative @382 e sidedSuccess. Não há guarda explícita de lado antes dos pedidos de alteração de mundo. Não equiparar solicitação a sucesso.

## Custos, estado e integração

Uma unidade solicitada mesmo quando sorteio não produz entidade. Mapas estáticos lazy, sem estado per-player demonstrado; stack e bloco sob autoridade nativa. Sem dano, projétil, AOE de combate, mana, cooldown ou duração próprios demonstrados. Aquisição, componentes efetivos e comportamento com player nulo não fechados. Perks conceituais: chance de duplicação, crescimento, custo. WORLD_SAFETY_BLOCKED: não reexecutar useOn, alterar mapa/estado/drop ou creditar Mastery antes de validar claims, callbacks, lado, aceitação e limites. Investigar engine Item, proteção de bloco, fluido, propriedades e eventual reutilização da stack armazenada no mapa.

## Localizadores de evidência

Classfile SHA-256 `b7515b5195e7ae5f1aa4f82fb2fb9e93faa339ad3a754ea62313ce438db46526`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>()V` | 6 | `8be36d6241481f2aa744705cb8bf58543a3d2d603628b0a2626b73949973458c` |
| `useOn(Lnet/minecraft/world/item/context/UseOnContext;)Lnet/minecraft/world/InteractionResult;` | 169 | `dec29a166ca2ab5e84b8f78f3c35d157e9403a293a0e97c167cc3a73adbcf206` |
| `scanForWater(Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/core/BlockPos;)Z` | 35 | `ddd9d511d51511cf1831277df3c24e98fb1def06784b82327e63ccf71adf384d` |
| `initGrowth()V` | 16 | `73f1070a2c895ae97a6af0f4decd7e2f989b511b89cd328904986e17f0bc4c83` |
| `lambda$initGrowth$1(Ljava/util/HashMap;)V` | 213 | `0740caf393748346c5690ac6b98376eb85788337d545fc6f3b03b1645976d71f` |
| `lambda$initGrowth$0(Ljava/util/HashMap;)V` | 101 | `6329ada9dbdbe900f68e49a6134a370eb63c6ca3149014b96be32441baafd95f` |


## Continuação downstream — autoridade e limites do efeito no mundo

Base Black Arcana `81dbec3021492e8862b36bb6bbb844d956d742d9`, modlist sibling `b05e2536461bc0a9c526dc47a38e3b9af62d941c`, #001 NeoForge 21.1.250 e #019 Alex's Caves 1.0.10. Licowitch Radiant Essence permanece reservado ao PR #1240; Marine Snow é o próximo item livre. Releitura do replay de 45653331096/job 139343330423 confirmou os pivôs abaixo.

- useOn: verificação água @25/28; GROWS_INTERACTIONS @33 e containsKey @40, ramo cresce com flag true @48, percorre propriedades existentes do novo estado e testa hasProperty no estado original @110, getValue @123/setValue @126, solicita setBlockAndUpdate @152, descarta booleano @155. Ramo exclusivo de crescimento, não também sorteio de duplicação.
- DUPLICATES_INTERACTIONS @159/166, flag true @174 ANTES de nextInt(2) @184; ifne @189 segue ao assentamento. getOrDefault @202 fornece a stack do mapa (sem chamada de copy na rota observada), passada ao construtor ItemEntity @243 nas coordenadas do click, addFreshEntity @254 e pop @257. Investigar se o construtor/campos/synched data mantêm alias com o mapa e se merge/tick podem alterá-lo; não afirmar duplicação efetiva de recurso ou bug confirmado.
- Mussel: identidade @273, MUSSELS @280/getValue @283 e limite 5 @292/293, flag true @296, incremento 1 @323/setValue @328/setBlockAndUpdate @334 com pop. Evento de mundo 1505 @364 somente se !isClientSide; player @368/isCreative @371 sem guarda de null local; shrink(1) @382. Ausência de guarda local não exclui autorização/validação upstream, mas invocação sintética sem player não é segura. Mesmo ramo de débito quando sorteio falha ou solicitação de alteração/entidade é negada; efeitos e assentamento não constituem receipt atômico.
- scanForWater: primeiro estado clicado @1/7, depois Direction.values @15 e BlockPos.relative @43/BlockGetter.getFluidState @46 com FluidTags.WATER @54. É uma consulta de condições de adjacência, não AOE de efeito; não estender ao entorno por perk sem boundary.
- initGrowth testa ambos os mapas @0/6 e, se algum null, instancia os dois com Util.make @21/38 e handles lambda$initGrowth$0/$1. Mapas compartilhados não devem ser alterados por perk global.

### Coleta preparada

[Sonda](../../../../../docs/qa/alexscaves_1010_marine_snow_world_probe.py), commit `8af07c191194d9f0f614abbd92e764549abd49a4`; [workflow](../../../../../.github/workflows/alexscaves-1010-marine-snow-world.yml), commit `11bce6c84961e22931407cc6f9f8cf3dac56260d`. Mantém pins publisher e seis Code hashes, materializa engine distribuída 21.1.250, projeta ItemStack.useOn/ServerPlayerGameMode.useItemOn e candidatos de hooks, contexto/estado/propriedades, Level.setBlock e callbacks de chunk, Mussel/corais, ItemEntity e inserção. Censo de Fieldref e referências tipadas do publisher, recursos JSON data/ com ID literal ou basename, sem presumir ausência transitiva. Duas reproduções determinísticas, orçamento e testes de filtro. Seletores sem declaração nominal não equivalem a ausência de comportamento. Resultado PENDENTE; não promove ficha/ledger ou runtime.

`STATIC_DISCOVERY_ONLY / NOT_CERTIFIED / WORLD_SAFETY_BLOCKED / NO_MUTATION / NOT_TESTED`.


## Primeira coleta distribuída aprovada — engine e recursos

[Run 46096220025/job 140828043452](https://github.com/Gustavaopere/Black-Arcana/actions/runs/46096220025/job/140828043452), HEAD `144d631ac3c772f2ba1a7487845bca7e526b0c61`: job específico success; dois relatórios byte-idênticos de 1.495.767 bytes SHA-256 `2e1ac9e56b431c4fa09708669e9cc6ec40cb91dbfa7adaff89f664d7ed4c0d7a`, 25 owners. Publisher 1.0.10, distribuições NeoForge 21.1.250 pinadas; sem jogo ou QA física. Todos os valores abaixo são do recorte estático.

### Autoridade upstream e liquidação

- ServerPlayerGameMode.useItemOn(ServerPlayer,Level,ItemStack,InteractionHand,BlockHitResult)InteractionResult Code `fefe429707ec85aee6cb3fc60ff4195fc77b98366a76655dd23d0c79c6c309b6`: bloco habilitado @24, CommonHooks.onRightClickBlock @41, cancelamento @48/56, ramo spectator @64–99, UseOnContext @109, tri-state de item/bloco e uso prioritário do bloco @265/317. Rota de item @344–449 considera stack vazia, cooldown externo e decisão de evento; creative preserva count @397/405/413, não creative usa @422. Critério ITEM_USED_ON_BLOCK @443 depende de consumesAction, não do sucesso de duplicação.
- ItemStack.useOn(UseOnContext)InteractionResult Code `e7886e663416c88730e1989a19d6c5a89168ad30ffae605fd6fb940113523d81`: UseItemOnBlockEvent(ITEM_AFTER_BLOCK) @11/post @14, cancelamento @24/31; no servidor CommonHooks.onPlaceItemIntoWorld @49, no cliente onItemUse @62. Não chamar MarineSnowItem.useOn diretamente para contornar estas camadas.
- CommonHooks.onPlaceItemIntoWorld Code `3cb4d3ad6f02ee91bef502b0e98b79cb97aa947fa3313ca96e7cd524f348a30e`: se player não nulo sem mayBuild, exige CAN_PLACE_ON e AdventureModePredicate @33/61; guarda contagem/componentes @78/84, captura snapshots condicionada ao item @101, chama Item.useOn @115; onPlayerDestroyItem condicional @134. Se resultado consumesAction, copia snapshots e dados pós-uso, restaura count/componentes anteriores @184/190, publica onMultiBlockPlace @218 ou onBlockPlace @251 quando quantidade de snapshots corresponde; recusa gera FAIL @261 e reversão via BlockSnapshot.restore @314. Sem recusa restaura dados pós-uso @332/338 e solicita onPlace/markAndNotifyBlock @408/435 e awardStat @454. Não há prova de rollback integral de entidades, efeitos externos ou callbacks do modpack. O caso de duplicação não cria por si snapshot de bloco; não extrapolar cancelamento de bloco a inserção de ItemEntity.
- Level.setBlockAndUpdate Code `6f01df666d51aa44e11f79a4f02ef92ce7ecd43abdd05d6140b99617c5cb7a52` solicita flags 3. Level.setBlock(pos,state,flags) Code `b295c48f8f79b1617e1fd50d89f2e605253cc4f87fbd87a35e06877e7eb7efe8` delega com limite de updates 512. Overload de quatro argumentos Code `9e3984e61f8b1a55a0347e9f8da9b7d8e173ce5c79dcaa8a8b32561d16db13d3`: recusa fora da altura e debug server, captura snapshot se habilitada, LevelChunk.setBlockState @124, se retorno null remove snapshot e false; caso contrário markAndNotifyBlock @173 quando não há snapshot. markAndNotifyBlock Code `53c34b0a84ac8d624172b994abff3e056e2bf1364bbca09998edc68bf3932609` testa estado atual, flags e limite, solicita update/neighbor shapes e onBlockStateChange. Não é garantia de bloco permanecer após física, callbacks, coral death ou claims.
- Para inserção de drop, a rota distribuída já confirmada nos contratos Depth Charge/Gossamer inclui ServerLevel.addFreshEntity -> manager, EventJoinLevel/UUID com possibilidade de recusa; o retorno é descartado pelo MarineSnowItem @257. Prova de inserção não é prova de pickup ou de persistência.

### Stack de duplicação — alias potencial, não bug físico confirmado

ItemEntity.<init>(Level,DDD,ItemStack)V Code `5bfb596cc62f0b648b9055e387b8d7a965cffb744f597621ab2be881d94ab60f` delega ao overload com velocidade, Code `b15677b5e1e526b924bc61c367c85315abd78a3fe555b7ff9ae1c92e9d8118e1`, que chama setItem @30 com stack recebida e lê lifespan. Não há copy nessa rota. setItem Code `da3a80913def6b75a5cad8eb866ac9495587917babc51a713241389d8d07fac0` entrega stack a SynchedEntityData.set @8; getItem Code `ed33328bed3a873349a466eedf37884e3891bfff05a6fab2b890d2d3805172e0` lê SynchedEntityData.get @7. SynchedEntityData.set(accessor,value) Code `12fd7498c7ba0008a2903a883550c442eb5b6ba71015ae4b93574ee2cf34fbd4` delega com force=false; overload Code `45e7c6a8e3307673e19d7d300196780d32fa7fc0cd0c6898821d4d31c5c62d81` testa ObjectUtils.notEqual, chama DataItem.setValue @26 e notifica dirty. Getter Code `400a6fb3402a9936f6674d0677e005c8c83dbbfc47f48f8503f5c89fcf3f4512` devolve DataItem.getValue @5. Ainda fechar corpo de DataItem, pickup e outras mutações de stack.

ItemEntity.merge(ItemStack,ItemStack,int) Code `95e64024c49b36a08c5325fedd4c0a7403989f077b8dc248d949114d2c051e75`: limita tamanho e cria cópia com count aumentado, shrink da stack doadora @35. Overloads Code `7a798ec766efdc888bdcd49c3c35bacdec4953937db963e053c241967a5eec57` / `e206a7d2e5bda1d04a531b1cc70d7744d0573472513e948fe0ea2a8c808b0913` escrevem receiver, ajustam age/pickup delay e descartam doador vazio. tryToMerge Code `25df79a8b14a7f186d3afbb975773a3ccf011c788dd7e6a31ebed61d01f100cb` exige target igual e areMergable, escolhe por count. tick Code `13ccfc705f3f1a98f324f3e5db83c72ec3df099d51704e57eda7ba72d4852b1b` permite onEntityItemUpdate, descarta vazio, merge server-side e onItemExpire. Se alias for confirmado na DataItem, consumo por merge/pickup pode alterar protótipo compartilhado; requer prova direta, não assumir exploit, nem autorizar reexecução para compensar.

### Mexilhões — limites e lifecycle

MusselBlock class SHA `2c91380410cb45f26bf6b0d29b4d5758f8922b23a8728919771fd94d69bcaeb0`. <clinit> Code `d995d3554d1d7b0cff8f7df331c8328f788bfdf081ededa969ddedae41481729` declara MUSSELS IntegerProperty [1,5], WATERLOGGED e FACING. Construtor Code `daefc68297af2dbe2befbbf92f9a17c5228719b2799015ed44f013c5d4555c45` default FACING=UP/MUSSELS=1/WATERLOGGED=true, randomTicks, no collision. canSurvive Code `c0b9c8f9dabcb445c24632a710066aab155b7233454ab23bc31a9884b7c114bd` exige face de suporte robusta; updateShape Code `0be6e63cf28668480c0bf216288669833d2d70d28c6bf775e6956f0358805a35` agenda fluido quando waterlogged e retorna AIR se perder suporte no lado relevante. getStateForPlacement Code `39f072a531b89da46268666d2fe1f373b2fbba5f0d1adede9df08598f4627602` incrementa mexilhão existente até 5, senão usa fluido WATER/face clicada. getFluidState Code `8c82c2094529fad147bf1da2be297bfe50aa90bc94347cd6aae027ab09c40d8e` fornece fonte WATER se waterlogged. randomTick Code `e6fd37de990c14278286a543b1fb60091d00206ae6de615fdb95ccc2a259e289`: gate nextInt(20)==0 e suporte ACTagRegistry.GROWS_MUSSELS; abaixo de 5 incrementa, no limite tenta espalhar por offset aleatório (-3..2 em cada eixo), condiciona água/mexilhão waterlogged e faces robustas. Este lifecycle autônomo não é AOE imediato do Marine Snow nem autorização para alterar randomTicks.

### Recursos e aquisição declarativa

Censo de 1555 classfiles localizou três candidatos tipados/Fieldref: ACItemRegistry, MarineSnowItem e ACCreativeTabRegistry. Não demonstra ausência de consumidores indiretos. Quatro recursos data/ com referência literal ou basename:
- advancement marine_snow SHA `c9f246f6c458a18056003fd749877e8dbc67a1476824bbc8deec5da66bc85cb0`: inventory_changed, parent abyssal_bucket; observa posse, não efeito aceito.
- loot abyssal_ruins SHA `7542b7b2a0c95b8cb49fb498ebb06ed4d02c25ca68b22debcfd651e902599b96`: pool rolls 8–10, Marine Snow peso 12 e quantidade 2–8 por seleção. Não é chance de 12%.
- loot gameplay/sea_pig_digestion SHA `b08eb3c3736baa89879e51dcf4a967f5a4599446cf9b581033c81d94ee8808a6`: uma seleção; pesos muck=2, pearl=1, marine_snow=15; quantidade 1–2. Nominal 15/18 = 5/6 por roll sem modificadores externos; execução do produtor ainda não comprovada.
- recipe pearl_from_gazing_pearl SHA `663ecb4f1b80e92a251e541e6a9b2c312efecccfd322f959d81ecc2e8b4e14d2`: shapeless, Gazing Pearl + Marine Snow -> Pearl x1. Consome insumo, não o produz. Não localizar receita produtora no censo literal não é prova de inexistência transitiva.

### Coleta complementar preparada
Schema 2 commit `aca742723cd45cd6491948e6c5d38765aabc00ef`: adiciona DataItem.setValue/getValue, ItemEntity.playerTouch/areMergable, inventário e stacks, CommonHooks.onRightClickBlock e onItemUse, callsites Fieldref e candidatos Sea Pig pelo literal de loot/roster de classes; seleção de métodos não certifica todos os produtores por si. Busca demonstrar o assentamento e o alias diretamente, além de aquisição causal. Sem execução local de jogo ou promoção. Mantidos `NOT_CERTIFIED / WORLD_SAFETY_BLOCKED / NO_MUTATION / NOT_TESTED`.
