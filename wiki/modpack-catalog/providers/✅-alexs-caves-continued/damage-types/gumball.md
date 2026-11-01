# Gumball — `alexscaves:gumball` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Política de integração:** `NO_MUTATION`. O certificado cobre o projétil, seu tipo de dano e os consumidores delimitados nesta ficha; o universo integral do provider continua aberto.

## 1. Identidade e proveniência

- **Provider / mod ID:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; artefato `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID:** `alexscaves:gumball`; membro `data/alexscaves/damage_type/gumball.json`; SHA-256 `70b62fe5851e5cbbb630f8dfb0202018fe7184f99c4b8bb19a98e68c4ed83687`.
- **Classe consumidora:** `com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.class`, SHA-256 `343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535`; estende `ThrowableProjectile` e declara **29 métodos próprios**, incluindo dois construtores e o inicializador estático.
- **Emissores:** [Shot Gum — equipamento e custos](../equipment/shot-gum.md), disparo de Gumbeeper e sua emissão radial condicionada. Filhos do split são outro caminho de criação.
- **Prova:** [manifesto consolidado](../EXACT-GUMBALL-CONTRACTS-1.0.10.json) e [limites/reprodução](../EXACT-GUMBALL-CONTRACTS-1.0.10.md). Fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`, versão declarada **1.1.1**, é somente corroboração adjacente; não fornece parâmetros certificados da build 1.0.10.

| Campo | Valor literal do recurso | Interpretação delimitada |
|---|---|---|
| `message_id` | `gumball` | Chave de mensagem de morte; não escola RPG ou fórmula |
| `scaling` | `never` | Metadado do tipo de dano; não dano líquido invariável |
| `exhaustion` | `0.3` | Exaustão do DamageType; não mana, stamina ou custo de cast |

Nenhum dos seis arquivos nativos `tags/damage_type/*.json` inclui diretamente `alexscaves:gumball`. Isso não resolve memberships herdadas/recursivas nem tags finais após datapacks e outros mods. O tipo Gumball do impacto direto e o mecanismo de explosão abaixo são caminhos distintos.

## 2. Comportamento, construção e autoria

O construtor `(EntityType,Level)` chama o construtor de `ThrowableProjectile`, cria uma **lista vazia `hitEntityIds`**, zera `bounceSoundCooldown` e sorteia `setColor(level.random.nextInt(12))`, portanto cor inicial entre `0..11`. Não recebe nem atribui owner próprio. O construtor `(Level,LivingEntity)` usa o tipo `ACEntityRegistry.GUMBALL`, chama o primeiro e então `setOwner(emissor)` em **18**. Esse é o caminho de autoria explicitamente usado pelos emissores primários auditados.

| Origem nativa | Estado/valor fornecido ao projétil | Limite de contagem e autoria |
|---|---|---|
| `ShotGumItem.acInventoryTick` | Construtor `(Level,LivingEntity)`, `DAMAGE=4F`, flags por nível positivo de `TARGETED_RICOCHET`, `TRIPLE_SPLIT`, `EXPLOSIVE_FLAVOR`; máximo `4+2×BOUNCY_BALL` | Custos, cadência e guards são do [equipamento](../equipment/shot-gum.md); chamadas de inserção não garantem entidades aceitas |
| `GumbeeperEntity.shootGumball` | Construtor `(Level,this)`; uma tentativa normal ou três quando carregado; dano `(float)ATTACK_DAMAGE`, somando `2F` quando carregado; carregado usa máximo `10` | O retorno de `addFreshEntity` é descartado e a chamada precede esses setters; não transferir a fórmula da arma para o mob |
| Emissão radial em `GumbeeperEntity.tick` | Construtor `(Level,this)`; mesmos ramos de dano/máximo, direção aleatória | Guard `isExploding`, progresso `>=20`, servidor e `!hasExploded`; a base é capturada antes do laço: `15` normal ou `30` carregado. A condição reavalia `base+nextInt(5)` a cada comparação. Sem interrupção externa, são `base..base+4` tentativas; o sorteio não é fixado antes do laço, e inserções/hits não são garantidos |
| Filhos de `GumballEntity.onHitEntity` | `ACCompat.createEntity(GUMBALL,level)`; copia valores correntes de dano, targeting, explosivo e máximo; desativa split | Essa chamada não fornece o owner do pai; não herdar automaticamente crédito de dano/kill/Mastery |

O disparo do Gumbeeper usa `shoot(dx,dy+sqrt(dx²+dz²)×0.20000000298023224,dz,1.2F,(float)(14−4×difficultyId))`; seus gates, munição e carga pertencem ao mob. Seu burst radial não é a chamada `Level.explode` do projétil. A ficha não certifica toda a IA do Gumbeeper, suas transformações ou todos os caminhos de possessão.

### Gates e custos do emissor Gumbeeper

O `AttackGoal` nativo habilita-se com alvo não nulo e vivo. Com munição e LOS pelo buraco de Gumball, aumenta `ATTACK_CHARGE` até `1F`, em passos solicitados de `0.1F` normal ou `0.3F` carregado. `canShootGumball()` exige **`GUMBALLS_LEFT>0`, `dialRot>=450F` e `ATTACK_CHARGE==1F`**. No tick da entidade, o dial aproxima-se de `450F×charge` em passos de `10F` quando a carga não é zero. A comparação de distância `<16` no goal controla navegação/strafe; não é um limite universal próprio de disparo.

`shootGumball` captura a quantidade normal/carregada antes do laço, mas relê o estado carregado depois de solicitar cada inserção para escolher dano e máximo. Ao final, debita uma munição no estado normal; no carregado, só quando um novo `nextFloat()<0.33F`. O retorno de inserção não condiciona esse débito próprio. Em seguida zera attack charge, ativa `SHOOTING` e escreve `postShootTime=5`; esse contador também serve à apresentação, sem equivalência automática a cooldown de casting. Mutações externas durante callbacks não constituem um snapshot imutável desses campos.

Os defaults próprios são `GUMBALLS_LEFT=6`, `CHARGED=false`, `ATTACK_CHARGE=0F`, `EXPLODING=false`, `SHOOTING=false` e possessor ID `−1`. Os overrides NBT persistem diretamente `Charged` e `Gumballs`, além de chamar a superclasse; não demonstram restauração de toda a carga transitória ou dos projéteis. Sem munição, o goal pode armar explosão em distância `<larguraDoAlvo+1.5F`; isso habilita o burst radial já descrito, não transforma esse corpo em `Level.explode`. Esses estados são do mob, separados do carregador de quatro cargas da arma; o contrato não encerra a IA inteira.

**Factory de dano:** `ACDamageTypes.causeGumballDamage` tem descritor `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`. Classe `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`. Resolve o holder `GUMBALL` e constrói `DamageSourceRandomMessages(holder,callerEntity,1)`; o construtor delega a `DamageSource(Holder,Entity)`. O inteiro `1` regula mensagens de morte, não quantidade de hits. Neste impacto, o argumento é o owner lido da instância, sem um segundo parâmetro separado para projétil/dono; classificação e fonte solicitadas não garantem atribuição final ou permissões.

## 3. Parâmetros, movimento, estado e persistência

`defineSynchedData(SynchedEntityData.Builder)` define sete accessors. Seus getters leem o valor sincronizado e os setters o escrevem diretamente, sem clamp próprio de nível, limite, dano, cor ou flags.

| Accessor | Default sincronizado | Getter / setter próprio |
|---|---|---|
| `MAXIMUM_BOUNCES` | `5` | `getMaximumBounces()` / `setMaximumBounces(int)` |
| `BOUNCES` | `0` | `getBounces()` / `setBounces(int)` |
| `DAMAGE` | `2F` | `getDamage()` / `setDamage(float)` |
| `COLOR` | `0`, depois sobrescrito pelo sorteio do construtor | `getColor()` / `setColor(int)` |
| `TARGETS_ON_BOUNCE` | `false` | `targetsOnBounce()` / `setTargetsOnBounce(boolean)` |
| `SPLITS_ON_HIT` | `false` | `splitsOnHit()` / `setSplitsOnHit(boolean)` |
| `EXPLOSIVE` | `false` | `isExplosive()` / `setExplosive(boolean)` |

O registro `GUMBALL` declara categoria `MISC`, dimensões **`0.25F × 0.25F`**, velocity updates `true` e update interval **`1`**. Não declara `clientTrackingRange` próprio nesse builder. A ligação do supplier ao construtor `(EntityType,Level)` está no bootstrap selado da classe de registro. Dimensões corporais, tracking herdado e escala/cor do renderer são parâmetros diferentes de dano, alcance e busca.

`getDefaultGravity()D` retorna **`0.07999999821186066D`** (float `0.08` alargado). A classe não implementa um alcance balístico universal ou velocidade inicial única; os emissores, ricochete e split escrevem movimento. A execução herdada de `ThrowableProjectile.tick()` continua responsável por sua física/colisão nativa, sujeita ao motor e outros mods. O método próprio não define um limite de vida por `tickCount`.

`tick()` chama a superclasse primeiro, copia `explodeProgress` para `prevExplodeProgress`, depois trata apresentação/interpolação e explosão. No cliente, `lerpTo(DDDFFI)V` guarda posição/ângulos/passos e reaplica a velocidade guardada por `lerpMotion(DDD)V`; o tick interpola posição e pitch quando `lSteps>0`, usa `wrapDegrees(lyr)` para yaw e decrementa os passos. Sem passos, reaplica posição. No servidor, também reaplica posição/rotação nesse caminho próprio. São consumidores de apresentação; não acrescentam dano por interpolação.

`getAddEntityPacket(ServerEntity)` delega a `ACPlatform.getEntitySpawningPacket(Entity,ServerEntity)`, que constrói `ClientboundAddEntityPacket(entity,serverEntity)`. Isso demonstra o pedido nativo de spawn sync, não restauração durável de todos os campos. `addAdditionalSaveData(CompoundTag)` e `readAdditionalSaveData(CompoundTag)` chamam a superclasse e salvam/leem diretamente apenas **`Color`**; a leitura usa `ACCompat.getInt(CompoundTag,String)`. Não há gravação própria desses seis outros accessors, lista de vítimas, contadores de som/progresso ou interpolação. A persistência herdada de owner e a composição final de saves/mixins não são inferidas dessas duas chamadas ao pai.

## 4. Targeting, impacto e dano solicitado

### Ordem de colisão e filtros

`onHit(HitResult)` chama **`super.onHit` antes dos seus filtros locais**. Em hit de bloco, busca seu collision shape e só solicita `bounceFromDirection(face)` quando não está vazio. Em hit de entidade, o trecho posterior exige `!ownedBy(vítima)` e que a vítima não seja outra `GumballEntity`; então adiciona seu ID à lista e, se `!splitsOnHit()`, calcula a direção horizontal da vítima e solicita ricochete. Esses filtros posteriores não são um novo guard anterior à chamada da superclasse.

**A lista `hitEntityIds` não deduplica o dano próprio.** `onHit` faz `List.add` sem `contains`, e `onHitEntity` não consulta a lista. Ela exclui entidades da aquisição de homing em `bounceFromDirection`; não comprova que contatos posteriores contra o mesmo alvo sejam incapazes de solicitar dano. A enumeração de colisões, a dispatch herdada e imunidades temporárias permanecem com o motor.

`onHitEntity(EntityHitResult)` lê uma vez a vítima, o owner (`@6`) e o dano corrente (`@11`). Se o owner é Gumbeeper possuído, resolve a Licowitch e retorna antes dos demais efeitos quando a vítima é do tipo `LivingEntity` e ela a classifica como friendly fire. Fora dessa saída especial:

A resolução da possessora usa o ID numérico na Level atual: `-1`, entidade ausente ou entidade de outro tipo retornam `null`; não há busca por UUID. Em `LicowitchEntity.isFriendlyFire(LivingEntity)`, uma vítima que implementa `PossessedByLicowitch` é classificada pela igualdade do seu possessor ID com o ID dessa Licowitch. Só no ramo alternativo o método testa `Witch` ou `vítima.is(estaLicowitch)`; não são três testes somados indiscriminadamente. Isso descreve o predicado nativo, não permissões gerais de PvP/claim.

1. Cria a fonte Gumball com `registryAccess` da Level da vítima e o owner capturado (`@86`).
2. Se owner não é nulo, impede a solicitação de dano quando `vítima.is(owner)`, `vítima.isAlliedTo(owner)` **ou** `owner.isAlliedTo(vítima)`. Com owner nulo, essa sequência de comparação é pulada.
3. Se elegível nesse trecho, solicita som e `Entity.hurt(source,danoCapturado)` em **139**. Seu booleano é descartado em **142**; esse corpo não adiciona teste de vida, LOS, raio ou aceitação para prosseguir ao split.
4. Consulta `splitsOnHit()` em **144**. O ramo é alcançável inclusive quando o passo de dano foi pulado por owner/aliança; apenas a saída friendly-fire anterior retorna antes. Não equiparar divisão a um hit aceito.

### Ricochete, busca e limite

Defina `B=getBounces()` e `M=getMaximumBounces()`. A ordem de `bounceFromDirection(Direction)` é:

- Se **`B>M−1 && isExplosive()`**, fixa movimento `Vec3.ZERO`, escreve `BOUNCES=M` e retorna imediatamente, sem o processamento posterior de som ou incremento. É o caminho de parada para progressão explosiva; os setters não impõem um domínio externo seguro a esses inteiros.
- Com `TARGETS_ON_BOUNCE`, busca `LivingEntity` em **AABB entre `eyePosition+(−10,−10,−10)` e `eyePosition+(10,10,10)`**. Não é um raio esférico. Quando há owner, exclui `candidato.is(owner)` e `candidato.isAlliedTo(owner)`; aqui não testa aliança inversa. Exclui IDs já na lista e escolhe a menor `distanceTo(this)` estrita entre os candidatos restantes, preservando o primeiro em empate. Não há teste próprio de LOS ou `isAlive` nesse laço; filtros herdados da consulta continuam externos.
- Ao escolher candidato, marca o ramo como tratado; somente no servidor incrementa `B`. Se o contador lido fica **`>M`**, solicita descarte; caso contrário fixa movimento `normalize(candidato.eyePosition−position)×0.800000011920929`. Não guarda alvo persistente: uma nova chamada pode escolher outra entidade. O descarte não é retorno imediato, mas esse ramo tratado não executa a reflexão comum.
- Se nenhum candidato foi escolhido, reflete somente o componente do eixo da face: X/Z tornam-se `−componente×0.800000011920929`; Y torna-se `−componente×0.5`; demais componentes são preservados. Depois incrementa `B` somente no servidor e descarta quando **`B>M`**, senão escreve o movimento refletido. O mapa de switch de `GumballEntity$1` liga explicitamente os casos aos eixos X/Y/Z.

Os guards de servidor acima cobrem o incremento; busca, direção, parada explosiva, som e comparações não têm automaticamente o mesmo guard próprio. `bounceSoundCooldown==0` permite solicitar som e repõe **5**; o tick o decrementa quando positivo. Esse contador é de som, não cooldown da arma ou intervalo de dano. Limite `>M` para descarte e limiar `>=M` da explosão são condições diferentes.

### Split e autoria dos descendentes

O laço tenta criar três filhos (`i=0,1,2`), usando `ACCompat.createEntity(EntityType,Level)`. O wrapper contém somente a delegação `EntityType.create(Level)` e retorno; o tipo registrado é o construtor `(EntityType,Level)`. Esse caminho nativo não fornece o owner do pai e **não chama `setOwner`** nessa rotina. Não é prova de owner nulo sob todos os mecanismos externos, nem defeito reproduzido, mas impede atribuir automaticamente suas kills/procs ao jogador por identidade da arma.

Cada filho recebe:

- Direção horizontal derivada do movimento normalizado do pai, com ângulos relativos `+30`, `0`, `−30` graus; vetor de base `(0,0,s)`, onde **`s=0.699999988079071`** se o pai é explosivo e **`s=1.5`** no outro caso. O vetor é rotacionado por `yRot(−radians(heading+30−30×i))`.
- Posição `vítima.eyePosition + vetor` e deltaMovement igual a esse vetor, sem componente vertical de lançamento nessa construção.
- `SPLITS_ON_HIT=false`; valores **correntes** do pai para `DAMAGE`, `TARGETS_ON_BOUNCE`, `EXPLOSIVE` e `MAXIMUM_BOUNCES`. O dano do impacto foi capturado antes de `hurt`, mas estes getters são lidos depois; não constituem um snapshot imutável quando eventos externos alteram o pai.

Não copia explicitamente owner, `COLOR`, `BOUNCES`, lista de vítimas ou progresso da explosão. O construtor próprio inicializa lista vazia/cor aleatória e os defaults sincronizados continuam sujeitos aos setters apresentados. O máximo copiado é o total `M`, não `M−B`; split falso impede nova divisão **nesse estado nativo**, sem prometer imunidade a alterações externas. Não há guard de lado, checagem de null da fábrica ou teste do retorno de `addFreshEntity` nesse laço. Depois das três tentativas, descarta o pai; exceções/recusa de inserção não foram simuladas no jogo.

## 5. Explosão, tempo e custos

O trecho explosivo de `tick` só progride quando **`isExplosive() && B>=M`**. Se `explodeProgress<=20F`, incrementa em `1F`; quando já é **`>20F`**, no servidor solicita:

```text
level.explode(getOwner(), x, y+0.5, z, 2F, false, ExplosionInteraction.NONE)
discard()
```

Partindo de progresso zero, são 21 incrementos elegíveis até `21`, com a solicitação na passagem elegível seguinte; não são “20 ticks de vida” para toda Gumball. O próprio trecho incrementa dos dois lados, e só chamada de explosão/descarte possui esse guard de servidor. Se flags/contadores deixam de satisfazer o gate, o progresso não é incrementado nem zerado por esse ramo. As partículas SMOKE são solicitadas após esse processamento, inclusive na passagem que pediu descarte.

O argumento de origem da explosão é `getOwner()` naquele momento, não um `DamageSource` Gumball explícito nem o projétil como argumento separado. O `Level.explode` usado não recebe `causeGumballDamage`; a resolução nativa de dano, exposição, eventos e bloco é externa. `false` é o argumento de fogo e `NONE` o modo solicitado de interação: não é autorização para burlar proteção de mundo, nem prova de ausência de toda alteração externa. `WorldEffectPolicy` do Black Arcana não assume autoridade automática sobre essa explosão nativa.

`getExplodeProgress(partial)` interpola `prev+(atual−prev)×partial`, divide por **20F** e retorna sem clamp próprio; esse valor de apresentação pode passar de `1` e não é uma unidade de dano. O tick não implementa age timeout próprio, cooldown global ou custo de mana/stamina/almas/inventário/durabilidade. Carga da arma e débito de munição são do [Shot Gum](../equipment/shot-gum.md); munição/charge do mob são outros estados. Ausência de débito neste consumidor não define custo global zero para uma integração.

## 6. Integração com perks e sistemas

| Mutação pretendida | Contrato nativo que precisaria preservar | Estado |
|---|---|---|
| Dano e Mastery por kill | Owner primário versus descendentes, fonte do impacto versus explosão, dano capturado e aceitação de `hurt` | `NOT_VERIFIED`; não atribuir procs por nome do item nem multiplicar settlement |
| Mais ricochetes | Máximo produzido pelo emissor, contador atual, descarte `>M`, parada/progresso explosivo e listas por instância | Preservar diferenças entre limite de dano, som e explosão |
| Targeting/homing/área | Consulta cúbica em torno dos olhos, filtros de owner/aliados/IDs, seleção por distância e física herdada | Uma caixa maior não se transforma em LOS, projétil autorizado ou filtro de PvP |
| Mais filhos ou flags | Três tentativas, estado dos filhos, autoria não propagada explicitamente e split independente de dano aceito | Não duplicar criação, débito de munição ou callbacks de dano |
| Tamanho, velocidade ou tempo | Registro/hitbox, gravidade, vetores escritos pelos emissores/ricochete/split e progresso de explosão são owners diferentes | Não usar cor, smoke ou escala visual como tamanho de colisão |
| Black Arcana / Enshrouded / RPG Skill Tree | Cast/owner de jogador e autoridade de servidor próprios, filtros nativos, deduplicação e canal de efeitos | Nenhum adapter executável ou hook seguro homologado por este catálogo |

As flags por encantamento e seus limites de nível/slots/compatibilidade estão no [contrato do equipamento](../equipment/shot-gum.md). Alterar atributo melee ou uma descrição de encantamento não muda automaticamente o `DAMAGE` armazenado ou a explosão. A lista de IDs e as condições de split não fornecem sozinhas um token de cast para evitar múltiplos procs.

## 7. Validação e evidência preservada

O manifesto consolidado sela esta ficha, todos os **29 métodos próprios** do projétil e os consumidores delimitados. O [contrato do equipamento](../equipment/shot-gum.md) cobre os custos e a ativação de outro objeto; o suporte do Gumbeeper cobre suas emissões sem certificar toda a IA/possessão/explosão do mob. Helpers e registries mantêm os seus owners. Não se certificam toda a física de ThrowableProjectile/Explosion, todas as políticas de alvo, o sistema de pacotes inteiro ou o universo do provider.

Os quatro snapshots anteriores permanecem imutáveis, com seus limites históricos: [impacto](../EXACT-GUMBALL-IMPACT-1.0.10.json), [produtores](../EXACT-GUMBALL-PRODUCERS-1.0.10.json), [estado/munição](../EXACT-GUMBALL-STATE-1.0.10.json) e [split/encantamentos](../EXACT-GUMBALL-SPLIT-ENCHANT-1.0.10.json). Também são preservadas as provas de [recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [factories/consumidores](EXACT-CONSUMERS-1.0.10.json). Esses snapshots parciais isolados não substituem o contrato consolidado nem promovem hooks/QA.

**Contabilidade:** esta é a ficha já existente do tipo de dano, com **+0 raízes mágicas novas**; o provider mantém oito raízes históricas. `STATIC_TECHNICAL_CATALOG_ONLY` não promove integração executável. Permanecem `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION` e universo integral aberto. QA física pendente: impactos aceitos/recusados e repetidos, alterações de owner/flags por evento, spawn recusado, split e autoria real, colisões, explosão/proteção de mundo, reload/persistência, latência, multiplayer e composições de combate.
