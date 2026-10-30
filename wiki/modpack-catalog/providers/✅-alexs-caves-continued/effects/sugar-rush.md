# Sugar Rush — velocidade e modificação local de ticks

Provider **Alex's Caves Continued**; ID `alexscaves:sugar_rush`; campo `ACEffectRegistry.SUGAR_RUSH`; implementação `server.potion.SugarRushEffect`, subclasse de `ACMobEffect`. Categoria `BENEFICIAL`, cor decimal `16753899`. É um estado produzido por comida/poção; registrar seus consumidores não cria um novo spell nem duplica cada alimento como magia.

Autoridade: JAR **1.0.10**, arquivo publisher `8856293`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A [prova comum dos efeitos](../EXACT-EFFECT-CONTRACTS-1.0.10.md) e seu manifesto selam os bytes. O source público `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, sem paridade comprovada com este binário. Contrato estático `VERIFIED_EXACT_BINARY`; hook mutador `NOT_VERIFIED`; QA física `NOT_TESTED`; configuração efetiva `NOT_VERIFIED`.

## Identidade, atributo e tick

`ACEffectRegistry.<clinit>()V @138–151` registra `sugar_rush`. O construtor `SugarRushEffect.<init>()V @9–29` declara um modifier em `Attributes.MOVEMENT_SPEED`, ID **`alexscaves:effect.sugar_rush`**, amount double **`0.699999988079071D`** (aproximadamente `0.7`) e operação **`ADD_MULTIPLIED_TOTAL`**. Esse é o valor base registrado; a aplicação de níveis, limites e composição com outros modifiers pertence ao pipeline de atributos de Minecraft. Não é `+0.7` blocos/tick, nem garante multiplicador final de movimento `1.7` em qualquer modpack.

`shouldTick(duration,amplifier)` retorna `duration>0`. `ACMobEffect.applyEffectTick(LivingEntity,int)Z` delega a `tick` e retorna true; o tick de Sugar Rush só solicita, **no cliente**, `PROXY.playWorldSound(entity,(byte)18)`. O estado temporal servidor é iniciado por evento de aplicação, não recriado em todo tick do efeito. O amplifier não entra na fórmula do campo temporal nem nos dois overrides de velocidade do jogador examinados abaixo. Duração infinita requer QA própria: não há conversão especial de duração não positiva neste `shouldTick`.

## Produtores, duração e custos

| Produtor | Parâmetros estáticos de 1.0.10 |
|---|---|
| Poção `alexscaves:sugar_rush` | Instância com **1800 ticks**, construtor de efeito sem amplifier explícito. |
| Poção `alexscaves:long_sugar_rush` | Instância com **3600 ticks**, mesmo efeito; não é uma nova habilidade. |
| Brewing | `STRONG_SWIFTNESS` vanilla + `ACItemRegistry.SWEET_TOOTH` → poção Sugar Rush; Sugar Rush + `REDSTONE` → longa. `registerBrewing` entrega `ProperBrewingRecipe` ao consumer. Disponibilidade da receita no pack/overrides não é inferida do registro. |
| Comida | **33 campos** de `ACFoods` constroem o estado, normalmente por **200 ticks**; Sundae usa **400 ticks**. Os suppliers usam construtor de `MobEffectInstance` sem amplifier explícito. A tabela abaixo registra as probabilidades declaradas, não chances medidas em jogo. |

`ACFoodBuilder.effect` guarda supplier/probabilidade; `resolve()FoodProperties @61–110` resolve cada instância e passa a probabilidade para `FoodProperties.Builder.effect`. Os 33 suppliers foram ligados aos campos do `<clinit>` pelo `BootstrapMethods` do próprio JAR; os valores não foram copiados da versão-fonte 1.1.1.

| Chance declarada | Campos de comida | Duração |
|---|---|---|
| `0.01F` | `BLOCK_OF_CHOCOLATE`, `COOKIE`, `COOKIE_HALF`, `DOUGH`, `SMALL_PEPPERMINT`, `LARGE_PEPPERMINT`, `SPRINKLES`, `CANDY_CANE`, `CANDY_CANE_POLE`, `LOLLIPOP_BUNCH`, `FROSTMINT`, `SUGAR_GLASS`, `GUMMY_RING`, `ROCK_CANDY`, `GINGERBREAD`, `GINGERBREAD_HALF`, `GINGERBREAD_CRUMBS`, `PURPLE_SODA_BOTTLE`, `SWEETISH_FISH`, `GELATIN`, `PEPPERMINT_POWDER`, `GUMBALL_PILE` | 200 ticks |
| `0.02F` | `BLOCK_OF_FROSTING`, `SWEET_PUFF`, `CAKE_LAYER`, `HOT_CHOCOLATE_BOTTLE`, `CARAMEL_APPLE` | 200 ticks |
| `0.03F` | `VANILLA_ICE_CREAM`, `CHOCOLATE_ICE_CREAM`, `SWEETBERRY_ICE_CREAM` | 200 ticks |
| `0.04F` | `CARAMEL` | 200 ticks |
| `0.05F` | `SUNDROP` | 200 ticks |
| `0.2F` | `SUNDAE` | 400 ticks |

A classe do efeito não cobra mana, durabilidade, fome, carga ou cooldown. Consumir comida/poção é custo do produtor e do pipeline vanilla, não uma cobrança por tick que Black Arcana deva reproduzir. A existência de nomes traduzidos de splash/lingering/arrow no lang não demonstra, sozinha, uma receita ou uma duração física desses deliverys. Regras de merge/atualização de instâncias também não equivalem a somar automaticamente todas as durações de comida.

## Consumidor temporal servidor e geometria

`ACServerConfig.<init> @761–782` declara **`sugar_rush_slows_time = true`**. O valor efetivo do servidor não foi lido. `CommonEvents.livingAddEffect` exige portador `Player`, `ACCompat.isAddedToWorld(player)` e essa config; chama `enterSlowMotion(player,level,ceil(duration*2F),2F)`. Não impõe nível mínimo de amplifier, PvP, owner ou aliança nesse bloco.

| Camada | Contrato exato |
|---|---|
| Entrada `enterSlowMotion` | Só modifica tracker em `!level.isClientSide()` e `ServerLevel`. Busca `LocalEntityTickRateModifier` de mesmo **ID inteiro** do jogador. Se existe, faz `setMaxDuration(newDuration)` e retorna; não reinicia `duration`, não atualiza multiplier/range/tipo/dimensão nesse ramo e não chama `addTickRateModifier`/sync ali. |
| Criação | Cria modifier da classe **embutida** `alexscaves.citadel...LocalEntityTickRateModifier`: ID do jogador, seu `EntityType`, range **10D**, `level.dimension()`, duração calculada e multiplier **2F**. `ServerTickRateTracker.addTickRateModifier` adiciona à lista e chama `sync`. |
| Centro / elegibilidade do owner | `getCenter(level)` resolve o ID em `level`; aceita entidade presente, adicionada ao mundo, tipo esperado e viva. Para owner implementando `IModifiesTime`, exige `isTimeModificationValid(modifier)`; o `PlayerMixin` retorna false para um modifier local de entidade quando o jogador não tem Sugar Rush. |
| Área | `LocalTickRateModifier.appliesTo(Level,x,y,z)` testa **distanceToSqr(center)<range²**: esfera aberta de raio10, não AABB nem alcance de ataque. O override LocalEntity acrescenta a validação do owner. Não há seleção por Mob, ally, PvP ou LOS nesse teste. |
| Dimensão | A dimensão é armazenada/serializada, mas não há comparação própria com ela nos dois corpos `appliesTo` examinados nem em `getEntityTickLengthModifier`. O ID é resolvido no Level recebido. Não presumir isolamento entre dimensões a partir da assinatura do construtor; o comportamento de execução exige QA. |
| Composição | `TickRateTracker.getEntityTickLengthModifier(entity)` inicia em1 e **multiplica** os multipliers dos modifiers locais cujo `appliesTo` passa. Sobreposição não é deduplicada por owner nesse consumidor. |
| Vida do modifier | `TickRateModifier.masterTick` incrementa `duration` em1; `doRemove()` compara `duration >= maxDuration*(1/multiplier)` para multiplier nãozero e tipo não Celestial. O par de entrada `ceil(effectDuration*2),2` não deve ser apresentado como extensão garantida de duas vezes o tempo real. |
| Saída explícita | `leaveSlowMotion` só executa no servidor/ServerLevel e remove **o último** modifier local da lista que corresponde ao ID; não faz remoção de todos e não chama `sync()` nesse corpo. |

A alteração observada é um **modifier de duração de tick**, não mudança global do TPS do servidor. Esta ficha certifica o contrato de criação, seleção, composição e remoção chamado pelo efeito. O agendamento efetivo de entidades, interação com modificadores concorrentes, transporte dos trackers e ordem de eventos continuam parte do sistema temporal e da QA física; não declarar todos os mobs próximos exatamente à metade da velocidade com base apenas em `2F`.

## Overrides do jogador, equipamento e cleanup

| Consumidor | Regra estática |
|---|---|
| `PlayerMixin.ac_getSpeed` | Config ligada + estado presente + `PROXY.isTickRateModificationActive(level)` → substitui retorno por **retorno anterior ×3F**. Não aplica esse3 somente por a config estar habilitada. |
| `PlayerMixin.ac_getFlyingSpeed` | Mesmos gates → retorna **getSpeed()*0.5F**, em vez de multiplicar o antigo retorno de flying speed. Não é o `Abilities.setFlyingSpeed` do Darkness Incarnate. |
| `RainbounceBootsItem.onEntityLand` | Dentro do ramo de quique elegível, usa multiplicador horizontal **1.2F** com Sugar Rush, **1.9F** sem; não cria Sugar Rush. As condições e o impulso vertical são do equipamento, não alcance do efeito. |
| Expiração | `CommonEvents.livingExpireEffect` chama `leaveSlowMotion` para Player, efeito SugarRush e config ligada. |
| Remoção direta | `CommonEvents.livingRemoveEffect` tem ramo SugarRush que toca som de saída; **não chama `leaveSlowMotion` nesse ramo**. `ACMobEffect.onEffectEnd` herdado é vazio para Sugar Rush. A validação do owner sem o estado pode fazer um modifier deixar de se aplicar, sem provar remoção imediata da lista. |
| Dimensão / parada | `travelToDimension` pede `leaveSlowMotion` se Player ainda possui o estado; `onServerStopping` limpa a lista inteira do tracker quando config ligada. Isso não demonstra cleanup equivalente em logout, morte ou reload. |

Não confundir atributo, velocidade retornada pelo mixin, movimento das botas e scheduler temporal: são quatro pontos de cálculo e podem compor-se de forma diferente entre cliente e servidor. Mudanças por perks precisam escolher o owner correto, arbitrar modificadores sobrepostos e respeitar criação/refresh/remoção sem liquidar duas vezes.

## Apresentação cliente

`ClientEvents.renderStage` consulta a câmera e `sugarRushSaturationEffect` para carregar/remover `SUGAR_RUSH_SHADER`, respeitando ramos anteriores de outros shaders. `ACPotionEffectLayer.render` aplica textura de Sugar Rush a modelo humanoide. `ClientEvents.onPoseHand` altera pose/animação, com ajuste quando o sistema temporal está ativo. `SugarRushSound.tick` acompanha posição do portador, sobe volume enquanto vivo/com efeito e esvazia/para sem essas condições. Esses caminhos não são dano, crowd control ou prova de autoridade servidor. O loop de som solicitado por `tick` não constitui novo efeito.

## Integração e validação

Sete campos estáticos: identidade do registro; lifecycle por classe/evento; amount/operation, durações, probabilidades e fórmulas; portador/owner/área; consumo no produtor; fronteiras entre atributo, mixin, tracker e apresentação; e reprodução no JAR selado. `range=10` pertence ao campo temporal criado; a chance pertence à comida; o amplifier pertence à instância; `ADD_MULTIPLIED_TOTAL` pertence ao atributo. Não oferecer uma única perk genérica de range/speed que escreva todos esses valores.

Hooks mutadores permanecem `NOT_VERIFIED`. QA física `NOT_TESTED`: aplicação/reaplicação/refresh, comida e poção, níveis normal/alto/infinito, config on/off e mudança durante efeito, centros simultâneos, limite exatamente10, outros jogadores/mobs/projéteis, dimensões/ID reutilizado, remoção versus expiração, logout/morte, sincronização e empilhamento com outros controladores de ticks. Os caminhos estáticos de refresh e remoção listados acima não foram classificados como defeitos reproduzidos.

## Localizadores binários

Prefixo: `com.github.alexmodguy.alexscaves`; descritores JVM, offsets do artefato1.0.10.

| Classe / método | Descritor / offsets |
|---|---|
| `server.potion.SugarRushEffect.<init>` / `shouldTick` | `()V @0–30`; `(II)Z @0–9` |
| `SugarRushEffect.tick` | `(Lnet/minecraft/world/entity/LivingEntity;I)V @0–19` |
| `SugarRushEffect.enterSlowMotion` / `leaveSlowMotion` | `(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/level/Level;IF)V @0–124`; `(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/level/Level;)V @0–105` |
| `server.potion.ACEffectRegistry.lambda$static$18` / `$19` | `()Lnet/minecraft/world/item/alchemy/Potion; @0–40` para ambas; duração @30 |
| `ACEffectRegistry.registerBrewing` | `(Ljava/util/function/Consumer;)V @386–468` |
| `server.item.ACFoods.<clinit>` | `()V @569–1600`: os33 campos/suppliers; `lambda$static$9..15`, `$18..43()Lnet/minecraft/world/effect/MobEffectInstance; @0–24` são os produtores SugarRush |
| `server.item.ACFoodBuilder.resolve` | `()Lnet/minecraft/world/food/FoodProperties; @61–118` |
| `server.event.CommonEvents.livingAddEffect` | `(Lnet/neoforged/neoforge/event/entity/living/MobEffectEvent$Added;)V @122–201` |
| `CommonEvents.livingRemoveEffect` / `livingExpireEffect` | `(Lnet/neoforged/neoforge/event/entity/living/MobEffectEvent$Remove;)V @77–138`; `(Lnet/neoforged/neoforge/event/entity/living/MobEffectEvent$Expired;)V @47–103` |
| `CommonEvents.travelToDimension` / `onServerStopping` | `(Lnet/neoforged/neoforge/event/entity/EntityTravelToDimensionEvent;)V @0–46`; `(Lnet/neoforged/neoforge/event/server/ServerStoppingEvent;)V @0–38` |
| `mixin.PlayerMixin.ac_getSpeed` / `ac_getFlyingSpeed` | `(Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V @0–72` / `@0–66` |
| `PlayerMixin.isTimeModificationValid` | `(Lcom/github/alexmodguy/alexscaves/citadel/server/tick/modifier/TickRateModifier;)Z @0–33` |
| `citadel.server.tick.modifier.LocalEntityTickRateModifier.getCenter` / `isEntityValid` | `(Lnet/minecraft/world/level/Level;)Lnet/minecraft/world/phys/Vec3; @0–29`; `(Lnet/minecraft/world/level/Level;)Z @0–66` |
| `citadel.server.tick.modifier.LocalTickRateModifier.appliesTo` | `(Lnet/minecraft/world/level/Level;DDD)Z @0–35` |
| `citadel.server.tick.modifier.TickRateModifier.doRemove` / `masterTick` | `()Z @0–49`; `()V @0–10` |
| `citadel.server.tick.TickRateTracker.getEntityTickLengthModifier` | `(Lnet/minecraft/world/entity/Entity;)F @0–79` |
| `citadel.server.tick.ServerTickRateTracker.addTickRateModifier` | `(Lcom/github/alexmodguy/alexscaves/citadel/server/tick/modifier/TickRateModifier;)V @0–15` |
| `server.item.RainbounceBootsItem.onEntityLand` | `(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/phys/Vec3;)V @93–150` |

Recursos selados incluem `assets/alexscaves/lang/en_us.json` e `assets/alexscaves/shaders/post/sugar_rush.json`; tradução e shader são evidência de apresentação, sem ampliar o claim servidor.
