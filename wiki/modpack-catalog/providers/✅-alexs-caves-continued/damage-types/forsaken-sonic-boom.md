# Forsaken Sonic Boom — `alexscaves:forsaken_sonic_boom` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Política de integração:** `NO_MUTATION`. A certificação cobre este ataque nativo e os consumidores delimitados; o universo integral do provider continua aberto.

## 1. Identidade e proveniência

- **Provider / mod ID:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1, artefato `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID:** `alexscaves:forsaken_sonic_boom`; membro `data/alexscaves/damage_type/forsaken_sonic_boom.json`, SHA-256 `1a8c19b6e54d9030fb706055906dc1598ac20dd9e2fbc5813858855310bbbf30`.
- **Execução própria:** `ForsakenAttackGoal` e `ForsakenEntity`; **factory:** `ACDamageTypes.causeForsakenSonicBoomDamage`.
- **Prova consolidada:** [manifesto do contrato](../EXACT-FORSAKEN-CONTRACT-1.0.10.json) e [escopo da evidência](../EXACT-FORSAKEN-CONTRACT-1.0.10.md). A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve somente de corroboração; não fornece os parâmetros certificados da build instalada 1.0.10.

| Campo | Valor literal do recurso | Significado delimitado |
|---|---|---|
| `message_id` | `forsaken_sonic_boom` | Chave da mensagem de morte; não uma escola mágica |
| `scaling` | `never` | Campo do DamageType; não fixa dano líquido nem escalonamento de perks |
| `exhaustion` | `0.3` | Exaustão do tipo de dano; não mana, stamina ou custo do ataque |

Não há entrada direta deste ID nos seis JSONs nativos de `tags/damage_type` inventariados. Isso não determina as tags finais após datapacks e outros mods. A factory recebe `(RegistryAccess, Entity)`, resolve `FORSAKEN_SONIC_BOOM` no registry e cria `DamageSourceRandomMessages(holder, entity, 2)`. O inteiro `2` é `messageCount`, utilizado pelo sorteio da mensagem de morte; não é quantidade de hits nem multiplicador de dano. O construtor delega a `DamageSource(holder, entity)`; o caller entrega o próprio Forsaken. Não existe neste caminho um projétil com owner separado nem atribuição nativa ao jogador. Mensagem de morte e fonte solicitada não comprovam kill credit, permissões ou resultado final do motor.

## 2. Comportamento e ciclo de vida nativos

O Forsaken usa duas formas do mesmo tipo de dano: **Sonic direcionado** contra seu alvo principal e **Sonic Blast em área** com vítimas filtradas. O ataque pertence à IA do mob. Não há entidade de projétil Sonic criada pelos dois callsites; partículas e sons são caminhos visuais separados.

O construtor de `ForsakenAttackGoal` define `jumpTarget=null`, flags de salto/Sonic falsas e os dois contadores em zero, guarda a entidade e reserva `Goal.Flag.MOVE` / `LOOK`. `canUse()` retorna verdadeiro somente para `getTarget()` não nulo e vivo. `start()` zera `navigationCheckCooldown`, `jumpEnqueued` e `attemptSonicDamageIn`, e inicializa `sonicEnqueued` com `RandomSource.nextBoolean()`. `stop()` limpa os flags de salto/Sonic e chama `setRunning(false)`; seu corpo não limpa o alvo, `jumpTarget`, animação nem contador pendente. Uma inicialização posterior volta a zerar o contador. Prioridades, continuação e agendamento herdados pertencem ao scheduler do Minecraft; uma chamada de `Goal.tick()` não é prova de um tick físico por atualização do mundo.

Cada `tick()` próprio retorna imediatamente se o alvo principal estiver ausente ou morto. Em seguida calcula a distância `d` por `distanceTo(target)` (float alargado para double), a soma das larguras e a possibilidade local de movimento. A ordem importa:

1. **Processa uma tentativa direcionada pendente:** se `attemptSonicDamageIn>0`, decrementa; na transição para zero, exige LOS para o alvo principal, solicita dano e então knockback de força `1`, ângulo adicional `0`. Esse trecho antecede o gate de `sonicEnqueued`, a distância `200` e a seleção da animação. Uma pendência não é cancelada simplesmente porque o flag Sonic foi limpo ou a janela de animação terminou. O contador não guarda um alvo próprio: ao atingir zero, usa o `getTarget()` corrente no slot `1`, e não o `SONAR_ID` gravado no armamento anterior.
2. **Processa a árvore Sonic:** exige `sonicEnqueued`, LOS para o alvo principal e `d<200`. Olha para seus olhos, grava seu ID em `SONAR_ID` e para a navegação. Se `d>10` ou o sorteio `nextFloat()<0.4`, tenta `ANIMATION_SONIC_ATTACK`; nos demais casos tenta `ANIMATION_SONIC_BLAST`. `tryAnimation` só troca a animação se a atual for `NO_ANIMATION`; seu retorno é descartado pelo caller. Os sons são solicitados mesmo quando essa tentativa de troca não for aceita. Esses sorteios não representam chance global de hit.
3. **Arma/processa segundo a animação corrente:** ATTACK arma o contador na janela inclusiva `10..30` quando ele está `<=0`; BLAST varre a área na mesma janela e somente quando `animationTick%5==0`. ATTACK limpa `sonicEnqueued` após tick `30`; BLAST após `40`. Os ramos que fazem isso ainda dependem do gate do item anterior.
4. **Executa os caminhos adjacentes de salto, perseguição e melee:** estes podem modificar flags para chamadas seguintes, mas não usam a factory Sonic. A ficha separa seus parâmetros abaixo para evitar aplicar a fórmula Sonic ao corpo a corpo.

No final do trecho comum, `((d>20 && nextFloat()<0.01) || hasSonicCharge()) && !sonicEnqueued` arma Sonic e limpa `SONIC_CHARGE`. Se o flag já estiver armado, esse trecho não consome a carga. `checkAndDealDamage` também pode armar Sonic após um sorteio `nextInt(5)==0`; essa tentativa ocorre após solicitar melee e independe de `hurt` ter sido aceito, desde que LOS e distância tenham passado.

**Origem da carga:** `ForsakenEntity.hurt(DamageSource,float)` testa a chave vanilla `DamageTypes.SONIC_BOOM`. Se verdadeira, define `SONIC_CHARGE=true` e retorna `false`, sem chamar `Monster.hurt` nesse ramo. A chave vanilla não é `alexscaves:forsaken_sonic_boom`. No outro ramo, se a entidade fonte obtida por `DamageSource.getEntity()` é `AbstractGolem`, reduz o valor solicitado a metade antes da delegação a `Monster.hurt`; não se trata da fórmula do ataque Sonic emitido pelo mob.

## 3. Parâmetros, duração, estado e movimento

| Parâmetro próprio | Consumidor e valor exato | Limite útil para perks |
|---|---|---|
| Habilitação da árvore Sonic | `sonicEnqueued && LOS(alvo principal) && d<200` | `200` habilita esse ramo; não é raio de área nem garantia de aquisição do alvo |
| Escolha ATTACK / BLAST | ATTACK quando `d>10` ou sorteio `<0.4`; caso contrário BLAST | A animação corrente pode impedir a troca; não inferir frequência de ataques |
| Atraso direcionado | `ceil(d × 0.20000000298023224d)`, convertido para int e gravado quando `attemptSonicDamageIn<=0` na janela `10..30` | Literal compilado exato; não substituir por `ceil(d/5)`: em `d=5`, o produto fica ligeiramente acima de `1`, resultando em `2` |
| Repetição potencial | ATTACK pode rearmar após o contador voltar a `<=0`; BLAST avalia `%5==0` dentro de `10..30` | São oportunidades condicionais, sem limite medido de hits aceitos por cast |
| Duração declarada da animação | `Animation.create(35)` para ATTACK; `Animation.create(45)` para BLAST | Duração do contador nativo, não segundos garantidos nem tempo de canalização de feitiço |
| Geometria corporal do registro | `MONSTER`, `sized(3.0f,3.5f)`, tracking `12`, velocity updates `true`, update interval `1` | Tamanho do mob, não tamanho de projétil; tracking de rede não é alcance de dano |
| Atributos-base registrados | movimento `0.25`, vida `250`, `FOLLOW_RANGE=64`, `ATTACK_DAMAGE=10`, resistência a knockback `0.6` | Defaults de atributos modificáveis; `ATTACK_DAMAGE` alimenta melee, não o helper Sonic `45/4` |
| Aquisição e estado | `SONAR_ID=-1`, `SONIC_CHARGE=false` e `LEAPING=false` nos defaults sincronizados | `SONAR_ID` não substitui `Mob.getTarget()`; sincronização não comprova persistência |

`getSonarTarget()` devolve `null` para `SONAR_ID=-1`, senão resolve ID numérico na `Level` atual. Não oferece fallback por UUID ou dimensão. `ForsakenEntity` não declara overrides próprios com as assinaturas exatas `addAdditionalSaveData(CompoundTag):void` e `readAdditionalSaveData(CompoundTag):void`; isso não prova ausência de persistência nas superclasses, mixins ou outros mecanismos. Os flags/contadores do goal não são certificados como estado recuperado após reload, unload ou troca de dimensão.

### Avanço de animação, eventos e apresentação

`ForsakenEntity.setAnimation` apenas grava `currentAnimation`; não zera o contador. No caminho auditado de `AnimationHandler.updateAnimations(Entity)`, animação nula é trocada por `NO_ANIMATION` e retorna; `NO_ANIMATION` retorna. No contador zero, publica `AnimationEvent.Start`: seu setter pode trocar a animação do evento e o cancelamento impede o envio por `sendAnimationMessage`, **sem retornar nem impedir automaticamente o avanço do contador**. Depois incrementa quando `tick<duration`, publica `AnimationEvent.Tick` e, quando `tick==duration`, zera o contador e aplica `NO_ANIMATION`. As comparações releem o tick e a animação correntes da entidade: não mantêm um snapshot imutável de duração. No servidor, um Start não cancelado passa a animação do evento ao envio, que a aplica na entidade; o cancelamento não aplica essa substituição por esse envio. Mutações durante o evento Tick podem alterar a comparação final. Um valor externo já maior que a duração não é normalizado por esses testes de igualdade.

`sendAnimationMessage(Entity,Animation)` só prossegue no servidor; aplica a animação e solicita uma mensagem com ID da entidade e índice na lista de animações. `getAnimations()` do Forsaken coloca ATTACK no índice `6` e BLAST no `7`. O consumidor cliente resolve o ID e o índice, aplica animação e zera o contador. O registro do payload é `playBidirectional`; este envio partir do servidor não torna todo o canal exclusivamente S2C nem comprova autorização de pacotes. Envelope, permissões e comportamento de outros consumidores permanecem sob os owners nativos, sem hook homologado.

Em `ForsakenEntity.tick()`, as partículas `FORSAKEN_SONAR` / `FORSAKEN_SONAR_LARGE` e screen shake usam uma janela visual **estrita** `10<animationTick<30` e cadência `%4==0`. Esse trecho não solicita dano. A janela inclusiva `10..30` e `%5` do BLAST pertencem ao goal, não às partículas. O método da entidade chama `Monster.tick()` e mais adiante `AnimationHandler.updateAnimations`; a sequência física entre scheduler, eventos, rede e outros mods não foi reproduzida.

### Navegação e melee adjacentes, mantidos separados

`isMovementFrozen()` reconhece somente as animações LEFT/RIGHT_PICKUP. Dentro do gate Sonic, as duas animações Sonic também desabilitam o movimento local; sem passar pelo gate, esse efeito não é universal. Quando pode mover, o goal olha para o alvo e solicita `navigation.moveTo(target,1.0)`. Marca running somente se `d<64`, `d>somaDasLarguras` e o movimento local estiver habilitado. São pedidos de navegação, não velocidade garantida nem alcance Sonic.

`startCleanJump()` limpa `jumpTarget` e arma `jumpEnqueued`. O tick pode solicitá-lo em `d>30` com sorteio `<0.05`, após melee com `nextInt(2)==0` ou após checagem de navegação que falhou. A checagem usa o valor anterior de `navigationCheckCooldown--<0`; se o mob está no chão, repõe `20+nextInt(40)` e chama `canReach`. Esse helper exige path e end node não nulos e distância **quadrática entre coordenadas de blocos** do end node ao alvo `<=3`, não alcance Sonic de três blocos.

`findJumpTarget(target,d>20)` escolhe deslocamento radial `4+nextInt(2)` quando o booleano é verdadeiro ou `15+nextInt(10)` no outro ramo, gira por `2π×nextFloat()` e delega a `LandRandomPos`. Exige suporte sólido, malus de pathfinding igual a zero e caixa candidata desobstruída; pode devolver `null`. No salto, o tick forma deslocamento horizontal ao centro X/Z do bloco; se seu comprimento quadrático excede `1e-7`, combina `deslocamento×0.1550000011920929 + movimentoAnterior×0.2`. Solicita velocidade Y `0.20000000298023224 + comprimento(vetor)×0.30000001192092896`, limpa alvo/flag do salto e deixa colisão/gravidade com o motor. Nenhuma dessas distâncias é parâmetro do Sonic Blast.

O helper `checkAndDealDamage(vítima,multiplicador,extraAlcance)` exige LOS e `distância < larguraForsaken+larguraVítima+extraAlcance`, solicita `mobAttack(Forsaken)` com `(float)(multiplicador×ATTACK_DAMAGE)` via `ACCompat.hurt` e devolve o resultado de `hurt` quando solicitado; retorna `false` diretamente se LOS ou distância falharem. Os sorteios de salto/Sonic vêm depois dessa solicitação, independentemente do booleano. Pickup, slash, ground smash e bite usam esse helper e **não** `causeForsakenSonicBoomDamage`:

| Caminho melee | Janela / parâmetro próprio | Fronteira |
|---|---|---|
| Pickup com ID da entidade segurada igual ao alvo | `animationTick>=30`, multiplicador `1.2000000476837158`, extra alcance `5` | Não aplicar base Sonic `45/4` |
| Slash esquerdo/direito | ticks `15..18`, multiplicador `0.800000011920929`, extra `2`; knockback força `3` quando o helper retorna `true`, ou `0.5` quando retorna `false`, ângulo `±90` | Retorno do helper afeta força, distinto do Sonic direcionado |
| Ground Smash | ticks `10..15`, centro `3.5` à frente, caixa X/Z `±4`, Y `−2/+3`, filtro de distância quadrática `<=16`, self/aliança/tag; multiplicador `0.800000011920929`, extra `3` | Acrescenta Y `0.5` apenas a vítima no chão cujo helper retornou `true`; não é Sonic Blast |
| Bite | ticks `5..8`, multiplicador `1`, extra `1`; knockback `0.5` quando o helper retorna `true`, ou `0` quando retorna `false` | Outro DamageSource e outra fórmula |

## 4. Targeting, geometria e dano solicitado

### Aquisição versus aplicação

`ForsakenEntity.<clinit>` liga o campo `TARGETING` à lambda `lambda$static$0` por bootstrap de `invokedynamic`. A lambda consulta a tag `FORSAKEN_IGNORES`: seu retorno é falso para membros e verdadeiro para os demais, sem impor por si só LOS, distância, vida ou permissões. `ACCompat.targetSelector(Predicate)` devolve a mesma referência (`aload_0; areturn`), sem filtros próprios. `registerGoals()` registra seis goals de ação, incluindo `ForsakenAttackGoal`, e três target goals, incluindo `HurtByTargetGoal` e variantes de `NearestAttackableTargetGoal`. Seus construtores, prioridades e scheduler mantêm a seleção final sob o Minecraft; o predicado não é política de PvP ou claims.

A tag nativa `alexscaves:forsaken_ignores` contém `minecraft:bat`, `alexscaves:vesper`, `alexscaves:corrodent`, `alexscaves:underzealot`, `alexscaves:forsaken` e `alexscaves:watcher`; `alexscaves:weak_to_forsaken_sonic_attack` declara `minecraft:warden`. São entradas do artefato, sujeitas à composição e substituição por datapacks.

O handler global `CommonEvents.acLivingFindTarget` também possui ramos de cancelamento na mudança de alvo: self-target é recusado quando `mobsCanTargetThemselves` é falso; um novo alvo Vallumraptor com `hideFor>0` provoca limpeza do target e cancelamento. O método `livingFindTarget` tem `@SubscribeEvent`, e o construtor de `AlexsCaves` registra `CommonEvents` em `NeoForge.EVENT_BUS`. A opção `mobs_can_target_themselves` tem default nativo `false`; a configuração carregada pode diferir. Esses são consumidores do evento de aquisição quando ele é entregue ao handler, não filtros automaticamente aplicados a cada vítima de BLAST. A presença desse evento não comprova que toda atribuição de alvo ou mod terceiro percorra o mesmo caminho.

### Dois caminhos de dano Sonic

| Contrato | Sonic direcionado | Sonic Blast em área |
|---|---|---|
| Destinatário | Alvo principal lido por `getTarget()` e armazenado no slot local `1` | Cada vítima iterada, armazenada no slot `9` |
| Gate próprio de aplicação | Contador positivo passa a zero e LOS para o alvo principal; o alvo principal está vivo no início do tick | Árvore Sonic habilitada; animação BLAST; ticks inclusivos `10..30` e `%5==0` |
| Geometria | Não há consulta de projétil, caixa de colisão ou novo limite de distância neste callsite | Consulta `LivingEntity` na caixa atual do Forsaken expandida por `(16,8,16)`; depois distância da vítima ao Forsaken `<=14` |
| Filtros locais | Não reaplica aliança/tag/raio de área neste callsite | Exclui próprio Forsaken, aliados nos dois sentidos, distâncias acima de `14` e membros de `FORSAKEN_IGNORES`; não testa LOS separada por vítima |
| Dano solicitado | `getSonicDamageAgainst(alvo principal)`: `45` se pertence a `WEAK_TO_FORSAKEN_SONIC_ATTACK`, senão `4` | `ceil(getSonicDamageAgainst(alvo principal)×0.65f)`: `30` ou `3`, aplicado à vítima iterada |
| Fonte | `causeForsakenSonicBoomDamage(registryAccess,Forsaken)` | A mesma factory com o Forsaken |
| Após `hurt` | Retorno descartado; solicita `knockBackAngle(alvo,1,0)` mesmo quando o dano for rejeitado | Retorno descartado; esse caminho não chama knockback |

**Distinção causal:** na área, `aload 9` no offset **560** identifica a **vítima iterada**, enquanto `aload_1` no **583** alimenta `getSonicDamageAgainst` no **584**. A categoria `45/4` depende do **alvo principal**, não da tag de cada vítima. No caminho direto, helper **116**, `hurt` **119** e knockback **127**; no BLAST, factory **576**, multiplicação **587/590**, `Math.ceil` **592** e `hurt` **596**. Os retornos descartados estão em **122/599**. Dois callsites não significam dois hits por tick.

`knockBackAngle(vítima,força,ângulo)` calcula `a=yBodyRot+ângulo`, passa `sin(a×0.017453292f)` e `−cos(a×0.017453292f)` para `ACCompat.knockback`; o wrapper delega diretamente a `LivingEntity.knockback`. Força não é deslocamento final: resistência, colisão e hooks nativos ainda intervêm. `16/8/16` expande uma caixa corporal dinâmica; não equivale a raio esférico de dano. Dano solicitado, chamadas aceitas, dano líquido, imunidade temporária e efeitos de outros mods são camadas distintas.

## 5. Custos, cadência e autoridade

No caminho próprio auditado não há débito de mana, souls, stamina, inventário, durabilidade ou recurso do RPG Skill Tree. Trata-se de ação da IA, sem contrato nativo de casting do Black Arcana. Ausência de chamadas de recurso nesses métodos não determina custo global zero nem permite cobrar novamente custos de terceiros. `exhaustion=0.3` é metadado do DamageType, e `navigationCheckCooldown` regula checagem de path; nenhum dos dois é cooldown de magia.

Não há guard explícito de `isClientSide` nos dois callsites de dano de `ForsakenAttackGoal.tick()`. A autoridade e a frequência de execução do goal vêm do scheduler nativo; não deslocar esse código para um tick de jogador ou cliente. O contrato descreve os parâmetros e a ordem no corpo próprio, sem executar o scheduler inteiro, inferir duração real de canalização, multiplicidade máxima de alvos ou número de hits aceitos. As oportunidades do BLAST nos valores `10,15,20,25,30` dependem das demais condições e do agendamento; não são cinco impactos garantidos.

## 6. Integração com perks e sistemas

| Mudança pretendida | Owner/valor que precisaria preservar | Situação |
|---|---|---|
| Aumentar alcance | Gate de seleção Sonic `d<200`, aquisição herdada, filtro BLAST `<=14` e consulta de caixa são camadas diferentes | Hook mutador `NOT_VERIFIED` |
| Trocar target por área | Seleção de `Mob.getTarget()`, tags, alianças, LOS do alvo principal, iteração e semântica de classificação do dano | Não converter por setter ou referência ao helper apenas |
| Alterar dano/escola | Helper `45/4`, callsite BLAST `ceil(base×0.65f)`, registry/type e settlement de `LivingEntity.hurt` | `ATTACK_DAMAGE` afeta melee; não presumir atributo mágico equivalente |
| Alterar duração/frequência | Criação das animações `35/45`, eventos, contador do handler, janelas `10..30`, atraso e flag Sonic | Preservar ordem e evitar rearme/dano duplicado |
| Alterar tamanho/velocidade | Dimensões corporais e navegação do mob; não há projétil Sonic nesses callsites | Não reinterpretar partículas/tracking como hitbox/alcance |
| Integrar RPG/Enshrouded/Black Arcana | Contexto do atacante, autoridade de servidor, filtros e canal de efeitos do provider | Sem adapter executável ou homologação física por este catálogo |

A rotina de destruição de blocos em `ForsakenEntity.customServerAiStep` é separada: consulta `canEntityGrief`, `canEntityDestroy`, `EventHooks.onEntityDestroyBlock` e solicita `destroyBlock` em caminho condicionado. Isso não demonstra destruição de blocos pelo Sonic. A `WorldEffectPolicy` do Black Arcana não assume automaticamente autoridade sobre efeitos nativos de terceiros. Nenhuma transformação de dano, target, animação, recursos, ownership ou efeitos de mundo foi habilitada; os owners nativos mantêm seleção, eventos e settlement.

## 7. Validação, evidências e limites

O [manifesto consolidado](../EXACT-FORSAKEN-CONTRACT-1.0.10.json) sela a ficha, classes/recursos, descritores e âncoras relevantes no JAR exato. O recorte lê todos os **12 métodos próprios de `ForsakenAttackGoal`**, incluindo construtor e 11 métodos, mais os consumidores delimitados da entidade, animações, registro, tags, factory e rede. Isso não certifica todo o mob, toda a IA herdada, todos os eventos do Forge, o sistema completo de pacotes ou toda a configuração do modpack. O provider ainda tem famílias de equipamentos, encantamentos e sistemas abertas.

As provas anteriores permanecem imutáveis, com os limites originais de seus recortes: [recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json), [factories e consumidores](EXACT-CONSUMERS-1.0.10.json), [janelas de dano](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json), [helper de dano](EXACT-DAMAGE-HELPERS-1.0.10.json), [fluxo Sonic](EXACT-FORSAKEN-SONIC-1.0.10.json), [helpers](EXACT-FORSAKEN-HELPERS-1.0.10.json), [lifecycle](EXACT-FORSAKEN-LIFECYCLE-1.0.10.json), [temporização/NBT](EXACT-FORSAKEN-TIMING-1.0.10.json) e [targeting](EXACT-FORSAKEN-TARGETING-1.0.10.json). O último preserva **52 instruções em cinco métodos**; o novo fechamento acrescenta a ligação bootstrap e a causalidade completa do ataque. Nenhum desses snapshots parciais, isoladamente, prova o contrato integral.

**Contabilidade:** uma ficha consolidada do tipo de dano; **+0 raízes mágicas novas**. O inventário histórico mantém oito raízes mágicas do provider. `STATIC_TECHNICAL_CATALOG_ONLY` não promove hooks nem QA: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Testes de targeting real, imunidades, alterações de tags/config em execução, eventos concorrentes, persistência, PvP/proteção de mundo e multiplayer permanecem necessários para integração executável.

### Identidades históricas preservadas

Estas identidades vinculam os recortes anteriores ao mesmo JAR. Os SHA-256 de métodos abaixo são os hashes das instruções parseadas nos respectivos snapshots; não são resultados de execução em jogo.

| Classe | SHA-256 |
|---|---|
| `com/github/alexmodguy/alexscaves/server/entity/ai/ForsakenAttackGoal.class` | `48cfdd6c370f68550d0d7af768466f99f330e8fd4f825a520411a1bc5d70fb55` |
| `com/github/alexmodguy/alexscaves/server/entity/living/ForsakenEntity.class` | `72981b25b3af251b3ee66b6ef16b650997359ff94673ad500256b2d1cee0cde1` |
| `com/github/alexmodguy/alexscaves/server/misc/ACCompat.class` | `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b` |
| `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class` | `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6` |

| Classe / método | Descritor JVM | SHA-256 das instruções parseadas |
|---|---|---|
| `defineSynchedData` | `(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V` | `a0a8ea7ca18a20a07a12bc39710ea22447264a4f359767c809c7044fb1cacde2` |
| `getAnimationTick` | `()I` | `d2f19727526eec9cd6ae71b7d2ce80ee9d587192c88551b7e92564bf446149ae` |
| `ForsakenAttackGoal.canReach` | `(Lnet/minecraft/world/entity/LivingEntity;)Z` | `2dd5166c68f7f909aadd4288303b7ad7aaca0e15823d38a3c79d9fc0633ef8f0` |
| `ForsakenAttackGoal.canUse` | `()Z` | `6309c2f6f04ccaa8100eb422ad81cdd6f5ba1b05ff0a973157b378a546803661` |
| `ForsakenAttackGoal.checkAndDealDamage` | `(Lnet/minecraft/world/entity/LivingEntity;DF)Z` | `e730ecfd665bf10060e4592ff81c16c91ce472541de43c2418c947da80eb4825` |
| `ForsakenAttackGoal.findJumpTarget` | `(Lnet/minecraft/world/entity/LivingEntity;Z)Lnet/minecraft/core/BlockPos;` | `198642c7720d30d8a93062cf893a7d2e4d3147e41817dc211279c19e8a4f43a8` |
| `ForsakenAttackGoal.isMovementFrozen` | `()Z` | `d6066616df310a8d53b81481d1dde352801433f246df9767437050be2d3d0e54` |
| `ForsakenAttackGoal.knockBackAngle` | `(Lnet/minecraft/world/entity/LivingEntity;DF)V` | `8ef9a3e156ca8311e23507cde598367388a0ceffd92e5bf7fd33f09f003003fa` |
| `ForsakenAttackGoal.start` | `()V` | `8e2fdcc7854b68ac0ad8d5b4c04b16b82aa8183c47016eb03d549cb42a816797` |
| `ForsakenAttackGoal.startCleanJump` | `()V` | `da3033d7ee48849e4035731c14dda7c23914271a97b44325197d10327eb68466` |
| `ForsakenAttackGoal.stop` | `()V` | `eca88a14990b3181b0622017a017334a9c1b23339bd8cdc51440e318258198b7` |
| `ForsakenAttackGoal.tick` | `()V` | `1fb8ecdd23c6c76d836ee25a4176f788163ef1226220a142a40e5f48d4df8abe` |
| `ForsakenAttackGoal.tryAnimation` | `(Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;)Z` | `83c4dd2d1f87f654d3eeef7f4f6914b9360a52243cda2c9796a95d9581d4450b` |
| `ForsakenEntity.customServerAiStep` | `()V` | `abdd554815865a9cda9fc13f68df7a4a274d450fda04d5f3aa06027478ae79fb` |
| `ForsakenEntity.getAnimation` | `()Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;` | `b377f6d233817c6c962ee3cce1af4f71ff4455d1dd019be76c8ec73addab4fbf` |
| `ForsakenEntity.getAnimationTick` | `()I` | `d2f19727526eec9cd6ae71b7d2ce80ee9d587192c88551b7e92564bf446149ae` |
| `ForsakenEntity.getSonarTarget` | `()Lnet/minecraft/world/entity/Entity;` | `0508d61342066d9992ae16df6934341f8555d96b2d2e49675644bf2f072c5188` |
| `ForsakenEntity.getSonicDamageAgainst` | `(Lnet/minecraft/world/entity/LivingEntity;)F` | `db47e82eebdb86724b6a71164ca563d0a75910bb143c16b944a5beb63f537d88` |
| `ForsakenEntity.hasSonicCharge` | `()Z` | `22a775652346057551780b9ee73aa9be765fc324bfce53d6424bf2159d51a111` |
| `ForsakenEntity.lambda$static$0` | `(Lnet/minecraft/world/entity/LivingEntity;)Z` | `cfa4a5d278a63d29041f8af87ec32c148db680704cadaca1df546de4d46ea865` |
| `ForsakenEntity.registerGoals` | `()V` | `c9f73f7eda5fa9b0368ccccb497b35be1395580889fb3bca9106cdf62578365e` |
| `ForsakenEntity.setAnimation` | `(Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;)V` | `6929fc02dcd16b3ac008164d88f69c74ec7f7f5213dc84d807526dfb305bbd85` |
| `ForsakenEntity.setAnimationTick` | `(I)V` | `4a9aafe463d849f469ef90d0d5e4fe54b08b521d9424e16b3b71661740d71d2a` |
| `ForsakenEntity.setLeaping` | `(Z)V` | `9ce582d416a6b73fa739ad2d2ddad336628bb805798ba831920149baf4d68dd6` |
| `ForsakenEntity.setSonarId` | `(I)V` | `85d993ec2e0a26d21e726f705645dfbf86b97a18808994ceb6c1e62d7e073f30` |
| `ForsakenEntity.setSonicCharge` | `(Z)V` | `4af4bb0f7993dd0eebd895bd7c0f3a564eaa0ceb47bd33374ba6d2d27fe984cb` |
| `ForsakenEntity.tick` | `()V` | `733efd62558f45ce4d8390e43fb09baff389490f8d96f9be709952a6a284341f` |
| `ACCompat.knockback` | `(Lnet/minecraft/world/entity/LivingEntity;DDD)V` | `b5340a2a4a3dfaecf0a4f39700ee15b8c0134015b594734d0f22c5e0548095f7` |
| `ACCompat.targetSelector` | `(Ljava/util/function/Predicate;)Ljava/util/function/Predicate;` | `b10a5989478262171604d8f1692ba5ad5da3f4d13f96e2ab39f78e9c57e61ca1` |

Factory: `ACDamageTypes.causeForsakenSonicBoomDamage`, descritor `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`. A factory é chamada nos offsets **108** e **576** de `ForsakenAttackGoal.tick()`, descritor `()V`. O inner source recebe `(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
