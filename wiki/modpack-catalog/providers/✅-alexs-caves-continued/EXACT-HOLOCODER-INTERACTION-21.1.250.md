# Holocoder — ingresso de interação, blocos e liquidação de inventário (21.1.250)

**DISCOVERY_ONLY / NO_MUTATION.** Publisher Alex's Caves 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`, 75.279.314 bytes; NeoForge 21.1.250, Minecraft 1.21.1, Java 21. Modlist #001/#019. Sem runtime transformado.

Reusa [ingresso publisher](EXACT-HOLOCODER-INGRESS-1.0.10.md), [representação recursiva](EXACT-HOLOCODER-ENTITY-LOAD-21.1.250.md) e [downstream](EXACT-FOUR-ITEMS-DOWNSTREAM-21.1.250.md). Captura chama addItem/drop após shrink, sem guarda explícita local de lado; ramo de consumo do projetor tem outra fronteira. O listener publisher e as classes de representação não comprovam o caminho de packet ou a liquidação do inventário.

A sonda `docs/qa/alexscaves_1010_holocoder_interaction_250_probe.py` fixa quatro classes e três Code hashes prévios, pins de distribuição, seleção delimitada do ingresso server de entidade/bloco, dispatch e eventos, Player/Inventory/ItemStack/ItemEntity e callbacks publisher. Nomes candidatos são filtros a confirmar no JAR, não APIs presumidas. Nested classes de packets e listener são descobertas da distribuição, com seleção de métodos por declarações. Duas saídas idênticas obrigatórias. Primeiro resultado observado abaixo; extensão selecionada após a leitura do report, ainda pendente. Não afirma autorização efetiva de player, conservação da stack, proteção dos dados ou aceitação física.

Ficha Holocoder permanece parcial; nenhum novo certificado, hook ou raiz.

## Replay inicial e resultados

[Run 45534885854, job 138938941949](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45534885854/job/138938941949): 67 métodos declarados, 62 executáveis, 20 owners com métodos; 550.666 bytes SHA-256 `5b143587795e92f53ff1777e7351097056f4b266f18298a12d8bdea700ad09df`, replay idêntico. Revisão inicial 06d7039e36054307395e91109a7daabc9d1eb752. Este selo histórico não é digest do probe ampliado.

| Corpo e Code SHA-256 | Resultado |
|---|---|
| ServerGamePacketListenerImpl.handleInteract `bc9e55d839cea173759c32149b6c1ae2f6ff03dc2c5416168b1131b70d431bcf` | ensureRunningOnSameThread @9; getTarget @22; setShiftKeyDown @41; alvo não nulo e world border @56; canInteractWithEntity(AABB,1D) @76 (dconst_1 @75); dispatch @93 |
| Player.canInteractWithEntity(AABB,D) `d50b4eb3745e7beeef985fab825b21cf33d5cacb50a7402dd5a5aa18364cf856` | distância quadrada do olho à AABB < (entityInteractionRange + margem)^2; atributo lido de ENTITY_INTERACTION_RANGE |
| ServerGamePacketListenerImpl.handleUseItemOn `55869d14c53bd30689d6299a8c75ba5405b2db6e30836a1a420c5466726180b4` | item enabled; canInteractWithBlock @88; tolerância coordenadas de hit 1.0000001D; altura, posição aguardada, mayInteract @206; gameMode.useItemOn @229 |
| ServerPlayerGameMode.useItemOn `fefe429707ec85aee6cb3fc60ff4195fc77b98366a76655dd23d0c79c6c309b6` | CommonHooks.onRightClickBlock @41 e cancelamento; spectator, item first, tri-state useBlock, useItemOn @265, fallback main hand, cooldown/creative na rota item useOn |
| BlockStateBase.useItemOn `2579c564edf3cecce683b652c3cc5281c776c78b8b910b762c3e9f68f5a16716` | UseItemOnBlockEvent fase BLOCK, cancelamento antes de Block.useItemOn @83 |
| Player.interactOn `91c17cc96b0a5a8c18f80e5832f0aa21d8b394263f39ab80310e620c1d13ac8a` | spectator anterior; CommonHooks.onInteractEntity @30, resultado não nulo retorna antes da interação nativa e restauração instabuild |
| Inventory.add(ILItemStack) `537ef561768bbce8d07322489e48bb88172711595ab50e6f3c0ed377c0c4c0c1` | stack vazia retorna false; rota damaged copyAndClear, slot ou infiniteMaterials; rota normal addResource/setCount e iteração enquanto count diminui; sucesso por redução, não necessariamente liquidação integral |
| Player.drop(stack,Z) `619f6f882d28cf9286aaea3daee699b8bdc8d1ce0aba366db2005dbea9b93895` | CommonHooks.onPlayerTossEvent @3, ainda sem corpo selecionado neste report |

ServerGamePacketListenerImpl$1.onInteraction(Hand) Code `63d2b7de5e723d39d481d0defc74590167579be758784e3fa15bc9eba87e3463` bootstrap @2 aponta Player.interactOn, performInteraction @7.

A seleção inicial de EventHooks não retornou corpos para os nomes de interação: o proprietário observado nas referências é CommonHooks. Isso é lacuna do seletor, não ausência da API. A extensão exige os quatro corpos CommonHooks observados e seleciona ShapedRecipe$Serializer.<clinit> para esclarecer o codec dos resultados shaped. Sem promover o selo até replay da extensão.

A captura do Holocoder continua com shrink antes de addItem e fallback drop apenas se addItem retorna false; não equiparar retorno true a transação atômica. A guarda criativa do caminho normal Player.interactOn não é prova de restituição de efeito ocorrido dentro de callback cancelável. Bloco projetor tem outra guarda criativa, sem exigir isBound na rota de uso. Não inferir bypass de permissões, perda/duplicação ou sucesso real.

## Replay da extensão CommonHooks e serializer — evidência observada

[Run 45536075237, job 138942867299](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45536075237/job/138942867299), HEAD `d8fdb6465ac59a026c634b083e2824a03bb79230`: duas saídas idênticas, 604.033 bytes, SHA-256 `f48ec709019002367ace6079f5a7ff2db70d1c88aa207d119548df2f5361567d`, artifact 14987780670. Deduplicação das linhas SEMANTIC por owner/nome/descritor nos dois replays: 74 declarações, 69 executáveis, 23 owners com métodos. Cinco checks de escopo. O workflow atualizado exige também tamanho e digest; replay da HEAD consolidada pendente.

| Corpo / Code SHA-256 | Fronteira observada |
|---|---|
| CommonHooks.onInteractEntity / `eb228b80adeedf04f04a2c5e9c8d1eccb1580c3e54bcbea68a2e799419a87edf` | Cria EntityInteract @7, posta @15, testa isCanceled @22; retorna cancellationResult @29 se cancelado, null caso contrário. |
| CommonHooks.onInteractEntityAt(Vec3) / `c2fa6b4cef18c91b0e887d0ba2efbd5de3af3c0ca002bdb2b0c245dbe2324095` | Cria EntityInteractSpecific @8, post @18, isCanceled @26; retorna cancellationResult ou null. Overload HitResult subtrai Entity.position de getLocation @8 e delega @18. |
| CommonHooks.onRightClickBlock / `afb3715dab3eac8b50e77b6c94d43d47371fd92cbc1c0e6a7976665d7dd97218` | Cria RightClickBlock @8, post @18, devolve evento; decisão de cancelamento fica no caller. |
| CommonHooks.onPlayerTossEvent / `cb37da310474680501209ec41b5f36e812b6eb9e5a8bbafa7f8eb8d69042f05c` | captureDrops @4, drop(stack,false,Z) @12, captureDrops(null) @18. Retorna null se entidade ausente ou evento cancelado. Fora do cliente solicita addFreshEntity @79 e descarta booleano; retorna entidade do evento @85. |
| ShapedRecipe.Serializer.<clinit> / `c67826b3e4c83d30b19087cd1237aca8b8c0bd27b15c608149facffa4e0fcca2` | Inicializa CODEC por RecordCodecBuilder.mapCodec @5, bootstrap aponta lambda$static$5; STREAM_CODEC via toNetwork/fromNetwork @21. A inicialização não prova corpo do codec de resultado, crafting ou settlement. |

O evento de toss pode retornar null e a rota de inserção pode retornar false mesmo quando o objeto retornado é não nulo. Nenhum rollback da captura original foi demonstrado por estes corpos. Cancelamento de interação não comprova compensação de mutações feitas por listeners antes da decisão. Para perks, são fronteiras reais de observação, não autorização de Black Arcana para mutar ou repetir o fluxo. Não inferir perda, duplicação, listener efetivo, ordem entre listeners, configuração ou QA física. Mantém NOT_CERTIFIED / NO_MUTATION / NOT_TESTED.
