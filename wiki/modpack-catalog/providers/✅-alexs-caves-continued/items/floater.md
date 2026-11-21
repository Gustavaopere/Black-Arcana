# Floater — Flutuador

**Catálogo** ✅ Contrato técnico estático de `alexscaves:floater` em Alex's Caves Continued 1.0.10. Utilidade de mobilidade aquática com **zero novas raízes mágicas**. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`, perk executável `NOT_CERTIFIED` e `NO_MUTATION`. [Disposição de ações](../ITEM-ACTION-DISPOSITION-1.0.10.md)

## 1. Identidade

O JAR publisher 8856293 tem SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. `server.item.FloaterItem` estende `Item`, usa `Item.Properties` padrão e declara dois corpos, o construtor e `use`. Seu SHA-256 é `30d98e6b5db3fc977c8e8e66adb82576c934d5a7cdc423bbd258f1e7a3224a05`. `ACItemRegistry.<clinit> @1953–1967` registra o item em `FLOATER`, e `lambda$static$103 @0–7` fornece a classe concreta. No censo tipado de 1.555 classes do JAR, `ACItemRegistry` é a única classe externa que referencia `FloaterItem`. [Registro de itens](../systems/item-registry.md) · [Prova e reprodução](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

O registro de entidade usa o mesmo identificador em `ACEntityRegistry.<clinit> @891–905`. `lambda$static$51` fornece `server.entity.item.FloaterEntity`, categoria `MISC`, largura e altura `0.98F`, atualização de velocidade habilitada e argumento **20** de rastreamento do cliente. A fábrica chama `setUpdateInterval(1)` e depois `updateInterval(10)`. Na referência NeoForge 21.1.250, a primeira chamada fixa o fornecedor consultado pelo getter, e a segunda grava o campo que o fornecedor padrão leria. O valor retornado por esse getter na referência é **1**. A frequência física de pacotes depende do sistema de rastreamento. `FloaterEntity` declara 14 corpos e o campo `timeOutOfWater`. Seu SHA-256 é `b675ebd726fc8045610a48fbd310abbd5f6762fe68e1158badd8026e47ac2c30`. [Prova do registro de entidade](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

O Code SHA-256 de `use` é `4a1d004b4ebb4270900189a914b01ee0a8ad927ec18a4848d6129668baecef46`. O de `FloaterEntity.tick` é `4189b44505454cce8089021252d762b641ad024925a2b07a3aebe1db4dc38beb`.

## 2. Uso e seleção

| Etapa | Regra própria do item |
|---|---|
| Entrada | `use @0–18` lê a stack da mão e exige que o jogador esteja na água ou em coluna de bolhas e mantenha a tecla de agachar solta. Sem elegibilidade, retorna `PASS` com a mesma stack em `@94–99`. |
| Criação | `@21–44` cria a entidade via registro para o nível recebido e copia a posição e rotação do jogador pela chamada `copyPosition`. O corpo dereferencia a entidade sem guarda de nulidade. Na referência Mojang, `EntityType.create` retorna `null` quando os recursos exigidos pelo tipo estão desabilitados. |
| Inserção e montagem | Solicita `Level.addFreshEntity` somente no servidor (`@47–60`). Em ambos os lados, o item chama `startRiding` no **veículo raiz** do jogador com o Flutuador como destino (`@61–70`). Sem montaria anterior, `getRootVehicle` devolve o próprio jogador. Os dois resultados booleanos são descartados. |
| Saída | O corpo pede a redução de uma unidade fora do criativo (`@71–81`) e devolve a mesma stack por `useSidedSuccess` (`@84–93`). A referência Mojang traduz esse retorno para `SUCCESS` no cliente e `CONSUME` no servidor. |

O item usa o jogador, a stack e o veículo raiz. Alcance próprio, seleção de bloco, dano direto e busca de outros alvos são inaplicáveis. A guarda de água do item vem de `Entity.isInWaterOrBubble`. O movimento posterior consulta a condição de água nos olhos da entidade do Flutuador. [Prova da seleção](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

## 3. Montagem e posicionamento

A montagem por item usa a sobrecarga comum de `Entity.startRiding` com `force=false` na referência Mojang. O engine verifica a cadeia de veículos, a aceitação de passageiro e os métodos `canRide` e `canAddPassenger`. A referência NeoForge acrescenta `EventHooks.canMountEntity` com `EntityMountEvent` cancelável. Negar a montagem retorna falso nesse caminho e o item segue para a redução da stack quando a guarda de criativo permite. A interação com a entidade já existente tem outra entrada. `FloaterEntity.interact @0–31` solicita que o **próprio jogador** monte no servidor, retornando `CONSUME` se aceito e `PASS` se recusado. No cliente, retorna `SUCCESS`. [Referências de montagem](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

`positionRider @0–74` usa o posicionamento próprio quando o passageiro é uma `LivingEntity`, compartilha o veículo raiz e o Flutuador não toca chunk descarregado segundo `touchingUnloadedChunk`. Usa X e Z do Flutuador e calcula Y como `FloaterY + 0.699999988079071D − getVehicleAttachmentPoint(floater).y`. Em seguida zera `fallDistance` do passageiro. Os demais casos delegam a `Entity.positionRider`. O teste de chunks delimita esse ramo do posicionamento. [Prova do posicionamento](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

## 4. Movimento e ciclo de vida

| Localizador em `FloaterEntity.tick` | Efeito solicitado |
|---|---|
| `@0–27` | Chama `Entity.tick` e aplica **−0.04D** à componente Y da velocidade se a gravidade estiver habilitada. |
| `@27–90` | Quando `wasEyeInWater` está ativo, acrescenta **+0.2D** à componente Y. No cliente, pede uma partícula `CURRENT_DOWN` na posição atual com velocidade inicial zero. |
| `@93–128` | Com os olhos fora da água, incrementa `timeOutOfWater` no servidor. Ao ultrapassar **5**, transmite o evento de entidade **3** e chama `discard`. A contagem é cumulativa porque o ramo molhado preserva seu valor. |
| `@131–156` | Pede movimento `MoverType.SELF` com a velocidade resultante e multiplica a velocidade lida após `move` por **0.9D**. Essa sequência está também no caminho do tick que pede descarte. O engine resolve colisões e deslocamento. |

No evento de byte **3**, `handleEntityEvent @0–129` pede partículas `ITEM` com a aparência do Flutuador, usando `10 + nextInt(4)` como limite reavaliado a cada iteração. Os outros eventos delegam à superclasse. `isPickable` e `shouldBeSaved` devolvem verdadeiro enquanto a entidade não está removida. `getPickResult` devolve uma nova stack do item para seleção pelo engine. `isAttackable` e `causeFallDamage` da própria entidade devolvem falso. [Prova do ciclo de vida](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

## 5. Aquisição e custos

`data/alexscaves/recipe/floater.json` (SHA-256 `379259801117cfd1aba2045bec78b19d55c913f47d33b1e925b4e241f0c0ce51`) declara `minecraft:crafting_shaped`, padrão `·B· / BBB / PPP`, com quatro `alexscaves:bioluminesscence` e três `alexscaves:ping_pong_sponge`. O símbolo `·` representa uma posição vazia. O resultado usa a contagem padrão de uma unidade. O avanço `alexscaves:alexscaves/floater` usa `inventory_changed` com o item como condição e tem como pai `alexscaves:alexscaves/bioluminesscence`. A aba Abyssal Chasm inclui a stack via `ACCreativeTabRegistry.lambda$static$14 @405–417`. O livro do bioma mostra a receita na página 3 de `abyssal_chasm/utilities.json`. [Recursos publisher](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

O pedido `shrink(1)` no uso vem depois das tentativas de inserção e montagem. O teste é `Player.isCreative()` e o débito próprio não tem guarda de lado. A interação com um Flutuador já existente e seu descarte carecem de cobrança própria e o descarte pede apresentação por partículas. O consumo final da mão, a reconciliação cliente-servidor e eventuais alterações pelo modpack continuam pendentes de QA. Mana, durabilidade, XP e cooldown próprios são inaplicáveis. [Prova de custos](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

## 6. Dados e apresentação

O construtor inicializa `timeOutOfWater` em zero. Os corpos próprios de `defineSynchedData`, `readAdditionalSaveData` e `addAdditionalSaveData` retornam imediatamente. O contador fica sem campo sincronizado ou gravação própria. O engine mantém responsabilidade pelos demais dados e pelo ciclo de salvar e carregar. `getAddEntityPacket` delega a `ACPlatform.getEntitySpawningPacket`, que constrói `ClientboundAddEntityPacket`. Isso delimita o pedido nativo de sincronização da entidade. [Prova de dados e rede](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

O modelo de inventário usa `minecraft:item/generated` com a textura `alexscaves:item/floater`. `ClientProxy.clientInit` registra `FloaterRenderer` para o tipo de entidade. O renderer usa `alexscaves:textures/entity/floater.png` com `ACRenderTypes.getGhostly`, desloca a pose em **+1.5** no eixo Y e gira **180°** em X. `FloaterModel.setupAnim` restaura a pose padrão e soma `0.5F × (tickCount + partialTick)` à rotação em Y da hélice. A transformação do modelo é visual. [Prova de apresentação](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)

## 7. Integração e validação

A [descoberta inicial](../EXACT-FLOATER-FROSTMINT-1.0.10.md) e o [manifesto histórico](../EXACT-FLOATER-FROSTMINT-DISCOVERY-1.0.10.json) mantêm a captura parcial original. O [selo atual](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.json) sustenta os campos desta ficha.

O contrato cobre os dois corpos do item, os 14 da entidade associada, os bindings, as rotas auxiliares e os dados do publisher. A inspeção submete a aceitação de criação, montagem, movimento, descarte, persistência e consumo aos respectivos mecanismos do ambiente. A QA física ainda precisa verificar uso livre e com montaria, recusa de inserção ou de montagem, travessia da superfície, retorno à água e sincronização da stack. A ficha certifica o comportamento estático da utilidade e mantém a autoridade de magia e de progressão nas camadas existentes. [Prova do publisher e referências do engine](../EXACT-FLOATER-FROSTMINT-CATALOG-1.0.10.md)
