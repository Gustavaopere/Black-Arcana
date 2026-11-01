# Shot Gum — equipamento, carregador e emissão de Gumball (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Política desta entrega:** `NO_MUTATION`. O contrato cobre o equipamento e os consumidores delimitados; o universo integral de Alex's Caves Continued permanece aberto.

## 1. Identidade, propriedades e aquisição

Item **`alexscaves:shot_gum`**, classe `com.github.alexmodguy.alexscaves.server.item.ShotGumItem`, subclasse de `Item`. Implementa `ACTickingItem`, `UpdatesStackTags`, `AlwaysCombinableOnAnvil`, `ACClientExtensionItem` e `ACEnchantableItem`. Sua ação prepara projéteis Gumball a partir de um carregador por stack. A [ficha de projétil e dano](../damage-types/gumball.md) documenta impacto, ricochete, divisão e explosão; a arma e o tipo de dano são dois contratos, sem acrescentar uma raiz mágica ao inventário histórico.

Autoridade: `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Classe SHA-256 `08aa8b9aa1781f2ead7d899e4fde758ea44bc527a2ee5968997e5b3ffdd32238`. A [prova comum](../EXACT-GUMBALL-CONTRACTS-1.0.10.md) e o [manifesto](../EXACT-GUMBALL-CONTRACTS-1.0.10.json) selam as duas fichas e os membros exatos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e fornece somente corroboração adjacente, não os parâmetros da versão instalada.

O construtor próprio passa `Properties.stacksTo(1)` a `Item` (`@0–15`). Não declara durabilidade, atributos de melee ou custo de magia. `getEnchantmentValue()` retorna **1**; `isEnchantable(ItemStack)` exige `stack.getCount()==1`. Os markers de interface não certificam por si só toda a bigorna, renderização ou integração com mods de combate.

A receita empacotada `data/alexscaves/recipe/shot_gum.json` é `minecraft:crafting_shaped`, padrão **`SPP` / `III` / `IN `**: um `alexscaves:sugar_glass`, dois `alexscaves:gumball_pile`, quatro ingredientes de `#alexscaves:ingots/iron` e um de `#alexscaves:nuggets/iron`, para **um Shot Gum**. Tags/receitas efetivas podem ser alteradas no pack.

A munição reconhecida é o item `ACItemRegistry.GUMBALL_PILE.asItem()`, por identidade no predicado `AMMO`. A lambda `lambda$static$0(ItemStack)Z @0–26` e o bootstrap de `AMMO` em `<clinit>()V @0–8` não aceitam genericamente todo item doce ou todo projétil. A pilha também aparece no loot nativo do Gumbeeper: um roll com contagem base `0..2` e `enchanted_count_increase` de Looting `0..1`; no pool normal de Licowitch Tower, peso **10**, contagem `1..3`, dentro de `3..8` rolls. Peso e intervalos não equivalem a probabilidade final ou obtenção garantida.

## 2. Uso e estado por stack

`use(Level,Player,InteractionHand)` obtém o stack da mão recebida. Com `getGumballsLeft(stack)>0`, arma `Shooting=true` somente quando `ShootTime==0` e `Shooting` ainda é falso; retorna **`ACCompat.usePass(stack)`** nesse ramo, inclusive quando apenas aguardou o estado anterior (`@7–42`). O corpo não chama `startUsingItem`, não seleciona vítima e não registra um cooldown em `ItemCooldowns`. `getUseDuration` declara **72000**, mas esse valor isolado não cria uma canalização nem um cooldown de 72.000 ticks.

Sem cargas positivas, tenta recarregar pelo caminho descrito na seção de custos e retorna **`ACCompat.useConsume(stack)`**, tanto após recarga quanto após o som de arma vazia (`@43–172`). `use` não contém guarda própria `isClientSide`; a resolução das chamadas cliente/servidor pertence ao fluxo de interação nativo.

| Dado em `CUSTOM_DATA` | Leitura própria | Escrita / limite |
|---|---|---|
| `ShootTime` | `getShootTime`: zero se não há tag; caso contrário `ACCompat.getInt` | `setShootTime` grava o inteiro fornecido, sem clamp |
| `CrankAngle` | `getCrankAngle`: zero se não há tag; caso contrário `ACCompat.getFloat` | `setCrankAngle` grava o float fornecido, sem wrap de ângulo próprio |
| `Gumballs` | `getGumballsLeft`: **4** se não há tag ou falta essa chave; senão lê seu inteiro | `setGumballsLeft` grava diretamente, sem impor máximo quatro |
| `Shooting` | `isShooting`: falso se não há tag; senão lê booleano | `setShooting` grava o booleano fornecido |
| `PrevShootTime`, `PrevCrankAngle` | Usados pelos dois getters interpolados e pelo tick | São valores anteriores para apresentação, não reservas de recurso nem timers adicionais de dano |

`ACCompat.getTag` consulta `CUSTOM_DATA` e delega a `CustomData.copyTag` quando o componente existe; sem ele, retorna `null`. `getOrCreateTag` consulta o mesmo componente diretamente e delega a `copyTag` ou cria um `CompoundTag` novo, sem anexá-lo sozinho ao stack. Os setters chamam `ACCompat.setTag` após modificar a tag. Uma alteração apenas no retorno de `getOrCreateTag` não comprova escrita do componente; os detalhes internos de cópia/alias de `CustomData` pertencem ao Minecraft. `setTag` escreve um componente `CustomData` no `ItemStack`; persistência e sincronização efetivas do inventário dependem dos consumidores nativos.

## 3. Ciclo de disparo, quantidade e parâmetros

O método `acInventoryTick(ItemStack,Level,Entity,boolean)` captura na entrada **`S=isShooting(stack)`** e **`T=getShootTime(stack)`**, antes de qualquer mutação (`@0–10`). Atualiza as chaves `Prev*` quando diferem do estado corrente e grava a tag (`@12–78`). O booleano `selected` recebido no quarto argumento **não é lido** nesse corpo.

Somente **`T==5 && S`** entra no ramo de disparo (`@81–89`): solicita som e chama `setShooting(stack,false)` antes de preparar as entidades. Não reconsulta `hasAmmo` nem exige continuar segurando o stack. As comparações por referência com mainhand/offhand escolhem o lado da origem; não são um guard que impeça um stack já armado de emitir depois de sair da mão.

| Parâmetro de produção | Valor / consumidor próprio |
|---|---|
| Flags dos encantamentos | `TARGETED_RICOCHET`, `TRIPLE_SPLIT`, `EXPLOSIVE_FLAVOR`: cada nível `>0` vira um booleano, consultado uma vez antes do laço |
| Máximo de ricochetes | **`4 + 2 × level(BOUNCY_BALL)`**, guardado antes do laço e aplicado em `setMaximumBounces` |
| Quantidade | **Uma tentativa quando explosivo; duas quando não explosivo** (`@291–306`), se o holder for `LivingEntity` |
| Autoria primária | Construtor `GumballEntity(Level,LivingEntity)` com o holder corrente; seu consumidor atribui owner na origem primária |
| Origem | Posição do holder + altura `bbHeight×0.8F` + offset rotacionado de `(lateral,0,0.75D)` |
| Offset lateral | Base `+0.35F` no lado esquerdo, `−0.35F` no direito; não explosivo acrescenta `+0.15F` na primeira tentativa e `−0.15F` na segunda; explosivo acrescenta zero |
| Rotação do offset | `xRot(−getXRot()×0.017453292F)` seguido de `yRot(−getYHeadRot()×0.017453292F)` |
| Pedido de lançamento | `shootFromRotation(holder,getXRot(),getYRot(),0F,velocidade,5F)`; velocidade **0.5F explosivo** ou **1.5F normal**, argumento de dispersão **5F** |
| Dano inicial do projétil | `setDamage(4F)`; não é dano líquido garantido nem atributo de melee da arma |
| Inserção | `Level.addFreshEntity` somente quando `!isClientSide`; seu retorno é descartado. Construção/setters anteriores não têm esse guard próprio |

Lado esquerdo significa `(stack é a referência da mainhand && mainArm==LEFT) || (stack é a referência da offhand && mainArm==RIGHT)`. Na ausência dessas condições, a base lateral é a do lado direito. Flags e máximo são calculados uma vez para o disparo; posição e ângulos são consultados dentro de cada iteração. A rotação da origem usa `getYHeadRot`, enquanto o lançamento usa `getYRot`: não fundir os dois argumentos em um único ângulo de targeting.

Após as tentativas, debita uma carga segundo a seção de custos. O final do método continua usando **S e T capturados na entrada**, mesmo após escrever `Shooting=false`: se `S && T<5`, grava `T+1`; se `!S && T>0`, grava `T−1`; se `S`, acrescenta **45F** a `CrankAngle`. Por isso, o callback do disparo deixa o contador em `5` e ainda avança a manivela; a redução começa em chamadas posteriores que já leem `S=false`. Partindo de `S=true,T=0` e com uma chamada por passo, cinco chamadas levam a `T=5` e a próxima entra no disparo. Isso não é cadência física garantida, nem prova de repetição automática enquanto o botão é mantido. A API própria não normaliza tempos externos acima de cinco nem ângulos acumulados.

## 4. Targeting, projéteis e encantamentos

O equipamento não faz busca de vítima, LOS, filtro de aliado, consulta de raio ou aplicação de `DamageSource`. Ele prepara o projétil e solicita lançamento; aquisição durante o ricochete, impacto, divisão, explosão, deduplicação e uso do owner pertencem à [entidade Gumball](../damage-types/gumball.md). A autoria dos projéteis derivados não é garantida pelo construtor primário da arma. Uma perk de dano/kill deve distinguir o projétil primário, o filho e a fonte efetivamente usada pelo consumidor.

| Recurso `data/alexscaves/enchantment/` | Máximo / peso | Custo mínimo | Custo máximo | Bigorna / slot | Efeito lido no item |
|---|---|---|---|---|---|
| `targeted_ricochet.json` | 1 / 2 | `1+16×(L−1)` | `41+10×(L−1)` | 4 / mainhand | Presença de nível positivo ativa targeting no ricochete |
| `triple_split.json` | 1 / 2 | `1+12×(L−1)` | `41+10×(L−1)` | 4 / mainhand | Presença de nível positivo ativa o ramo de divisão |
| `explosive_flavor.json` | 1 / 1 | `1+16×(L−1)` | `41+10×(L−1)` | 8 / mainhand | Presença de nível positivo ativa explosivo e muda quantidade/velocidade iniciais |
| `bouncy_ball.json` | 3 / 10 | `1+7×(L−1)` | `41+10×(L−1)` | 1 / mainhand | Níveis 0/1/2/3 produzem máximo **4/6/8/10** |

Os quatro referenciam `#alexscaves:enchantable/shot_gum`, que contém diretamente o item. **Targeted Ricochet** declara `exclusive_set=[alexscaves:triple_split]`; Triple Split não repete um `exclusive_set` próprio. A aplicação efetiva dessa regra pertence aos dados/sistema de encantamentos. O item lê os quatro níveis independentemente, sem checar exclusividade nem aplicar novo clamp pelos máximos JSON. Os três flags usam somente a presença positiva; não escalam seu comportamento pelo valor do nível. `BOUNCY_BALL` usa o inteiro retornado na fórmula, inclusive quando fornecido por mecanismos externos aos níveis usuais. O campo JSON `slots=mainhand` não introduz um novo guard de mão na leitura manual de encantamentos desse tick. Os quatro IDs aparecem diretamente nos tags empacotados `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable`; isso não garante uma rolagem, negociação ou composição final dos dados do pack.

## 5. Custos, recarga e apresentação

`findAmmo(Player)` retorna `ItemStack.EMPTY` imediatamente para criativo. Para os demais jogadores, percorre os slots de `player.getInventory()` de zero até `getContainerSize()−1` e retorna a primeira referência cujo item satisfaz `AMMO`. Não faz busca apenas nas mãos e não reserva uma cópia da munição. Sem match retorna `EMPTY`.

No ramo sem cargas de `use`, `isCreative()` inicia o booleano de recarga permitida. Se o stack de munição encontrado não é vazio, chama **`shrink(1)` antes de repor quatro cargas** e habilita a recarga. Criativo já retornou `EMPTY` no finder, então esse caminho não encolhe munição criativa; pode repor quatro sem munição. Sem permissão de recarga, solicita o som de vazio. O corpo não implementa uma transação Black Arcana que desfaça consumo após falha externa.

No disparo do tick, um `Player` criativo preserva suas cargas; todos os outros casos escrevem **`max(getGumballsLeft(stack)−1,0)`**. Esse débito ocorre uma vez depois de todo o laço, tanto para uma tentativa explosiva quanto para duas normais, e independe do booleano de `addFreshEntity`. Se o `Entity` recebido não é `LivingEntity`, o laço é pulado, mas o ramo de débito ainda pode executar. Esses são caminhos do corpo próprio, não prova de que cada tipo de holder seja usado pelo scheduler no modpack.

Os corpos próprios não debitam mana, souls, stamina, durabilidade ou recurso do RPG Skill Tree. Ausência desses débitos não permite prometer custo global zero ou duplicar recursos cobrados por outra camada. Carga do carregador, unidade de Gumball Pile e número de projéteis são unidades diferentes. O campo `MAX_AMMO` é `public static final` com `ConstantValue=4`; os métodos usam literais compilados de quatro no default, na recarga e na barra, em vez de consultar esse campo em cada operação. Uma futura capacidade variável precisa coordenar esses consumidores, não presumir que trocar um único campo altere toda a arma.

Os métodos de apresentação conservam outros limites: `getLerpedShootTime` e `getLerpedCrankAngle` calculam `prev+(current−prev)×partial`, sem clamp próprio de partial; `isBarVisible` testa `Gumballs!=4`; `getBarWidth` retorna `round(Gumballs×13F/4F)` sem clamp a `0..13`; `getBarColor` retorna **16752639**. `shouldBeHeldUpright` retorna `hasAmmo`. `shouldCauseReequipAnimation` retorna falso quando ambos os stacks são Shot Gum, ignorando seu booleano de troca de slot e sem exigir igualdade das tags. `initializeClient` encaminha as propriedades de renderer da proxy a `IClientItemExtensions`; isso não transforma uma escala visual em tamanho de colisão ou range.

## 6. Ativação, estado e integração com perks

`ItemStackTickMixin` é listado em `alexscaves.mixins.json` e injeta no **HEAD** de `ItemStack.inventoryTick(Level,Entity,int,boolean)`, sem declarar `cancellable=true`. Se o item implementa `ACTickingItem`, passa `stack`, `level`, `entity` e `selected` ao método da interface; o inteiro do slot não é repassado. Essa cadeia explica a ativação da rotina própria, em vez de tomar a existência de um nome de método como prova de execução. O callback ainda depende do inventário nativo e de transformações do pack; não é um hook seguro de perks.

`UpdatesStackTags` oferece um receptor genérico que encaminha a tag a `ACCompat.setTag`; seu argumento de entidade não é usado nesse default. Nos **26 métodos próprios de ShotGumItem não há referência a emissão de `UpdateItemTagMessage`, `sendMSGToServer` ou `sendMSGToAll`**. Implementar a interface demonstra capacidade de receber aquele caminho, não que a arma envie essa mensagem em seu ciclo normal nem que seus campos sejam sincronizados por esse payload.

O handler genérico da mensagem e o envelope `playBidirectional` preservam uma fronteira de autoridade separada: resolvem entidade por ID no nível de contexto e escolhem uma mão por comparação de tipo de item antes de aplicar a tag. Esses corpos não constituem validação homologada de owner, slot, conteúdo NBT ou permissão de mutação para o Black Arcana. O catálogo não declara exploração reproduzida, autorização do payload ou convergência cliente/servidor comprovadas.

| Mudança pretendida | Contratos que precisam ser preservados |
|---|---|
| Quantidade / munição | Uma unidade recarrega quatro cargas; o disparo debita uma carga após uma ou duas tentativas. Evitar cobrar por entidade inserida e novamente pelo ataque |
| Dano / escola | O item fixa `4F` no projétil; factory, filtros e `hurt` ficam no impacto. Melee, explosão e dano Gumball são consumidores distintos |
| Tempo / frequência | `Shooting`, `ShootTime`, momento exato `T==5`, snapshots na entrada e dispatcher de inventário. Não reinterpretar `72000` ou animação como cooldown |
| Target / área / alcance | O item não resolve vítima. Ricochete, filhos, explosão e alcance dependem da entidade e de seus próprios filtros |
| Tamanho / velocidade | Origem, `shootFromRotation` e metadados de entidade são separados do renderer e de `CrankAngle` |
| Player / ownership | Construtor primário recebe o holder corrente; esse vínculo não é herdado automaticamente por toda emissão do mod ou por filhos |

Nenhuma integração executável com Black Arcana, Enshrouded, RPG Skill Tree, Epic Fight ou outro sistema de combate é homologada por este catálogo. Owners nativos conservam emissão, custos, estado, filtro e settlement. Hooks mutadores `NOT_VERIFIED`; política `NO_MUTATION`.

## 7. Validação e localizadores JVM

A inspeção cobre os **26 métodos próprios** de `ShotGumItem`, o bootstrap de `AMMO` e os consumidores de apoio delimitados. O manifesto fixa hashes de ficha, classes e recursos e os descritores/instruções do mesmo JAR. As provas históricas de [impacto](../EXACT-GUMBALL-IMPACT-1.0.10.json), [produtores](../EXACT-GUMBALL-PRODUCERS-1.0.10.json), [estado](../EXACT-GUMBALL-STATE-1.0.10.json) e [divisão/encantamentos](../EXACT-GUMBALL-SPLIT-ENCHANT-1.0.10.json) permanecem separadas e imutáveis; não são convertidas em prova de runtime.

| Método próprio | Descritor JVM |
|---|---|
| `<init>` | `()V` |
| `initializeClient` | `(Ljava/util/function/Consumer;)V` |
| `getEnchantmentValue` | `()I` |
| `isEnchantable` | `(Lnet/minecraft/world/item/ItemStack;)Z` |
| `shouldCauseReequipAnimation` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;Z)Z` |
| `getLerpedShootTime` | `(Lnet/minecraft/world/item/ItemStack;F)F` |
| `getLerpedCrankAngle` | `(Lnet/minecraft/world/item/ItemStack;F)F` |
| `getShootTime` | `(Lnet/minecraft/world/item/ItemStack;)I` |
| `setShootTime` | `(Lnet/minecraft/world/item/ItemStack;I)V` |
| `getCrankAngle` | `(Lnet/minecraft/world/item/ItemStack;)F` |
| `setCrankAngle` | `(Lnet/minecraft/world/item/ItemStack;F)V` |
| `getGumballsLeft` | `(Lnet/minecraft/world/item/ItemStack;)I` |
| `setGumballsLeft` | `(Lnet/minecraft/world/item/ItemStack;I)V` |
| `isShooting` | `(Lnet/minecraft/world/item/ItemStack;)Z` |
| `setShooting` | `(Lnet/minecraft/world/item/ItemStack;Z)V` |
| `hasAmmo` | `(Lnet/minecraft/world/item/ItemStack;)Z` |
| `use` | `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` |
| `getUseDuration` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)I` |
| `acInventoryTick` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V` |
| `shouldBeHeldUpright` | `(Lnet/minecraft/world/item/ItemStack;)Z` |
| `findAmmo` | `(Lnet/minecraft/world/entity/player/Player;)Lnet/minecraft/world/item/ItemStack;` |
| `isBarVisible` | `(Lnet/minecraft/world/item/ItemStack;)Z` |
| `getBarWidth` | `(Lnet/minecraft/world/item/ItemStack;)I` |
| `getBarColor` | `(Lnet/minecraft/world/item/ItemStack;)I` |
| `lambda$static$0` | `(Lnet/minecraft/world/item/ItemStack;)Z` |
| `<clinit>` | `()V` |

**Contabilidade:** **+0 raízes mágicas novas**. Este é um contrato adicional de equipamento, complementar ao objeto de dano/projétil; não encerra todos os itens, encantamentos, mobs ou sistemas do provider. `STATIC_TECHNICAL_CATALOG_ONLY`, `NOT_VERIFIED`, `NOT_TESTED` e `NO_MUTATION` permanecem estados separados.

QA física pendente: input de uso, seleção e troca de mão durante a pendência, múltiplos stacks, ativação em inventário, criativo/sobrevivência, inserção recusada, consumo concorrente, dados externos fora dos limites usuais, save/reload, client/server, autoridade de mensagens, ricochetes/filhos e integração de combate. Nenhum número de hits, permissão de PvP/claim ou compatibilidade executável foi demonstrado em jogo por esta ficha.
