# Nuke — `alexscaves:nuke` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Política:** `NO_MUTATION`. O certificado delimita esta classificação de dano e os consumidores descritos; não homologa runtime, cleanup físico ou o universo integral do provider.

## 1. Identidade e diferença entre variantes

- **Provider / mod ID:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1. Artefato `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/damage_type/nuke.json`, SHA-256 `c44737192a4999c35799e24bb3df4cd9ca77e8f58d5fce1c74a53a71f0170d92`.
- **Consumidor:** `com/github/alexmodguy/alexscaves/server/entity/item/NuclearExplosionEntity.class`, SHA-256 `d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912`.
- **Factory desta variante:** `ACDamageTypes.causeNukeDamage(RegistryAccess)`, descritor `(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;`. O inteiro `4` do construtor de mensagem é quantidade de alternativas de mensagem, não hits ou multiplicador de dano.
- **Prova comum:** [manifesto](../EXACT-NUCLEAR-CONTRACTS-1.0.10.json) e [escopo/reprodução](../EXACT-NUCLEAR-CONTRACTS-1.0.10.md).

| Campo | Valor literal do recurso | Interpretação |
|---|---|---|
| `message_id` | `nuke` | Mensagem de morte, não escola de magia |
| `scaling` | `never` | Metadado do DamageType, não dano líquido constante |
| `exhaustion` | `0.1` | Exaustão do tipo de dano, não mana/stamina/custo de cast |

A flag `INTENTIONAL_GAME_DESIGN=false` seleciona este ID no ponto de hurt. Bomba, Nucleeper e o ramo de fornalha crítico são origens nativas delimitadas; não se presume que toda origem ou mutação externa preserve o default. A [variante Intentional Game Design](intentional-game-design.md) compartilha o consumidor, sem gerar um segundo hit pela bifurcação.

Entradas diretas nos seis JSONs nativos de tags de dano:

- `minecraft:bypasses_cooldown`
- `minecraft:is_explosion`
- `minecraft:is_fire`

`bypasses_cooldown` classifica dano no Minecraft; não é bypass de cooldown de lançamento. As três memberships não constituem a composição final de dados, permissões ou prova de resultado físico.

## 2. Consumidor, emissores e autoria

`NuclearExplosionEntity` estende `Entity`, sem um owner de projétil declarado no próprio consumidor. O construtor cria uma `Stack<BlockPos>` vazia, inicia `spawnedParticle=false` e `loadingChunks=false`. O registro nativo declara categoria `MISC`, dimensões `0.99F × 0.99F`, duas chamadas de atualização — `setUpdateInterval(1)` e depois `updateInterval(10)` —, velocity updates `true` e tracking `20`. As duas APIs do builder são registradas como chamadas distintas; sua existência não autoriza supor que ambos os números tenham a mesma unidade ou sejam a frequência física efetiva do ataque.

| Produtor nativo | Parâmetros e ativação delimitados | Custos e fronteira |
|---|---|---|
| `SackOfSatingItem.acInventoryTick` | Com `Exploding` e servidor, cria o consumidor, posiciona no holder com Y adicional `4`, escreve `SIZE=0.5F` e `INTENTIONAL_GAME_DESIGN=true`, solicita inserção e limpa `Exploding` | Encolhe o próprio sack em uma unidade nesse caminho; a preparação por alimento/estado pertence ao item. Não há owner player passado à factory de dano |
| `NuclearBombEntity.explode` | Cria o mesmo consumidor, copia posição e lê `nukeExplosionSizeModifier` para `setSize`; `tick` tem gate servidor com contador `>300`, e há outro caminho servidor de queda `>20` | São gatilhos da bomba, não cooldown de spell. Origem do bloco/entidade não atribui player ao DamageSource |
| `NucleeperEntity.explode` | `SIZE=1.75F` carregado, senão `1F`; `RULE_MOBGRIEFING=false` leva a `NO_GRIEFING=true`; solicita inserção | Carga, fuse e proximidade são estados do mob. A configuração de fuse declara `300`, mínimo `20`, máximo inteiro; não é custo de mana nem um limite universal da entidade de explosão |
| `NuclearFurnaceBlockEntity.destroyWhileCritical(boolean)` | O ramo `true` solicita o consumidor com `SIZE=0.75F`; o ramo `false` usa nuvem Irradiated, outro consumidor. Há destruição local anterior ao booleano | Eventos de bloco e estado crítico são necessários à origem; não classificar toda remoção da fornalha como explosão nuclear nem o processo inteiro como um cast |

Esses quatro emissores são os caminhos diretos delimitados pelo inventário do JAR. A factory de criação `ACCompat.createEntity(EntityType,Level)` delega a `EntityType.create(Level)`. As solicitações de inserção não asseguram que uma entidade seja aceita; seus retornos não constituem confirmação de hit. O comportamento completo da bomba, do mob, da fornalha ou do sack não recebe uma certificação adicional por esta ficha. Os produtores e os dois DamageSources também não criam novas raízes mágicas independentes.

A classe das factories é `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`. Ambas as factories recebem somente `RegistryAccess`. `DamageSourceRandomMessages(Holder.Reference,int)` delega a `DamageSource(Holder)`, sem argumento `Entity` do produtor ou holder do item. Isso documenta a ausência de um owner nesse caminho, não a política final de kill credit, últimos atacantes, XP, Mastery ou outros eventos do Minecraft. Não atribuir o dano automaticamente ao player mais próximo ou a quem acionou o emissor.

## 3. Estado, geometria, tempo e persistência

| Dado próprio | Default / leitura / escrita | Limite |
|---|---|---|
| `SIZE` | Default `1F`; `getSize` lê `SynchedEntityData`, `setSize(float)` grava diretamente | Sem clamp, validação de finitude ou conversão em alcance de cast nesse setter |
| `NO_GRIEFING` | Default `false`; getter/setter encaminham booleano | Só contorna o ramo próprio de blocos/chunks, não o laço de alvos/dano/movimento/efeito |
| `INTENTIONAL_GAME_DESIGN` | Default `false`; getter/setter encaminham booleano | Seleciona fonte e condiciona radiação em leituras distintas, não um tipo de entidade novo |
| `destroyingChunks` | Stack criada vazia; reabastecida, ordenada e consumida pelo tick | Não é serializada pelos overrides próprios |
| `loadingChunks` | Default `false`; persistido como `WasLoadingChunks` | Marcador local, não inventário de tickets aceitos |
| `spawnedParticle` | Default `false`; impede repetir o pedido inicial de partícula nesse estado | Não é cooldown nem marcador de dano realizado |

`tick()` chama `Entity.tick()` primeiro. Define `c=(int)ceil((double)SIZE)` e `B=15*c`. Para entradas finitas e regulares, `c` é a escala em regiões, e não um raio contínuo proporcional ao valor fracionário de SIZE. A consulta de vivos usa **a caixa corporal atual** inflada por `(1.5B, 0.6B, 1.5B)`. O segundo argumento do cálculo de dano é **`r=1.5B+1`**, em aritmética float nesse trecho. Exemplo apenas derivado do código: tamanhos `0.5`, `0.75` e `1` dão `c=1`, inflação `(22.5,9,22.5)` e `r=23.5`; `1.75` dá `c=2`, inflação `(45,18,45)` e `r=46`. A caixa de consulta não é esfera nem alcance de lançamento.

O pedido inicial `MUSHROOM_CLOUD` usa `SIZE` e a flag como argumentos de apresentação. Antes, busca uma altura pela coluna de blocos usando `isDestroyable` até atingir condição de parada, altura mínima ou o deslocamento `Y−B/2`. Não é um cálculo separado de dano ou uma prova de segurança de mundo.

A duração não é fixa em 40 ticks. Se `tickCount>40` **e** a Stack está vazia, chama `remove(DISCARDED)` e salta o restante do tick, inclusive o laço de alvos. Caso contrário, no servidor e com `NO_GRIEFING=false`, uma Stack vazia é preenchida com origens `blockPosition + 16*(x,y,z)` para `x,y,z` de `−c` a `+c`, e ordenada pelo comparador de distância Manhattan. Essa chamada não processa a fila recém-criada no mesmo ramo. Com Stack não vazia, o outro ramo invoca `removeChunk(B)` até `min(3, tamanhoAtual)` vezes. Até passar a condição de remoção, uma fila vazia pode ser reposta novamente. O número `(2c+1)^3` descreve a geração regular da fila, não um budget certificado do servidor; Stack.pop prioriza as entradas próximas após a ordenação inversa.

`getAddEntityPacket(ServerEntity)` delega ao helper nativo de spawn packet. Os overrides `addAdditionalSaveData` e `readAdditionalSaveData` escrevem/leem somente **`WasLoadingChunks`**; seus corpos não chamam superclass save/read e não persistem diretamente SIZE, flags, fila ou partícula. Sincronização de accessors não demonstra restauração desses estados após save/reload. A infraestrutura de entidades e tickets pode conservar outros dados por mecanismos próprios; isso permanece distinto de provar recuperação completa ou cleanup físico.

## 4. Targeting, geometria e dano solicitado

O laço enumera `LivingEntity` dentro da AABB indicada. No corpo próprio não há teste separado de LOS, aliança, owner, direito de PvP/claim, lista de vítimas já processadas ou guard `isClientSide` abrangendo esse laço. A seleção herdada da consulta, agendamento da entidade e intervenções de outros mods continuam externos. O mesmo vivo pode ser considerado em chamadas posteriores; não prometer um único hit por emissão.

Seja `d=target.distanceTo(this)`, `s=getSize()` e `r` o valor acima. `calculateDamage(float,float)` solicita:

```text
M(s) = 100F                       se s <= 1.5F
       100F + (s−1.5F)*400F      se s > 1.5F
D = ((r−d)/r) * M(s)
```

São operações float e leituras próprias de SIZE, sem clamp neste helper. Valores externos zero, negativos, não finitos ou excessivos não recebem uma normalização segura por essa fórmula. O limite JSON/config não transforma todo setter e todo campo em um domínio validado; divisão por zero, casts e overflow não são reinterpretados como caps úteis para perks.

| Etapa no tick | Condição / valor | Consequência delimitada |
|---|---|---|
| Vetor básico | `v=normalize(target.position−this.position+(0,0.3D,0))` | Direção própria, sem chamada ao mecanismo `LivingEntity.knockback` nesse trecho |
| Coeficiente inicial de movimento | `k=s*0.33F`; para `Player`, `k` é multiplicado por `0.5F` | Não é deslocamento final nem resistência a knockback |
| Raycat | Dentro do ramo em que D inicialmente é positivo, escreve `D=0F` | A execução ainda segue às operações posteriores; não confundir com imunidade a toda a entidade |
| `RESISTS_RADIATION` | Nesse mesmo ramo, reduz `D` para `D*0.25F` e `k` para `k*0.1F` | Tag final é resolvida pelo pack; o nome não garante proteção universal |
| Tremorzilla | Somente dentro do ramo de resistência, escreve `D=0F` e `k=0F` | Não inverter a precedência desses testes |
| Dano | Apenas se D ainda for positivo, lê a flag e escolhe uma factory, depois chama `LivingEntity.hurt(source,D)` | As duas alternativas convergem em **uma** solicitação; o retorno é descartado |
| Movimento posterior | Sempre alcançado após os guards de dano: `setDeltaMovement(v.scale((double)(D*0.1F*k)))` | **Substitui** o vetor da vítima, sem somar ao anterior; pode executar quando hurt foi pulado ou recusado |
| Radiação posterior | Relê `isIntentionalGameDesign`; quando falso, pede Irradiated | Não depende de `hurt=true` nem mesmo de ter ocorrido uma chamada de hurt |

O código pode calcular `D<0` para candidatos da caixa fora de `r`. O guard impede hurt nesse ramo, mas não impede automaticamente o pedido de movimento com aquele valor negativo. Isso é uma relação estática entre fórmula e caller, não um efeito físico ou defeito reproduzido. Em `D=0`, a escrita própria de movimento ainda pode substituir o vetor por zero.

A flag é lida antes da factory (`@592`, branch `@595`) e novamente depois de hurt (`@647`, branch `@650`). O valor não é congelado por emissão ou vítima: uma alteração durante callbacks pode separar a classificação usada no dano da decisão posterior sobre radiação. O ramo de fonte Intentional chama `causeIntentionalGameDesign` em `@605`; o outro chama `causeNukeDamage` em `@618`; ambos convergem em `hurt @623`, cujo resultado é descartado em `@626`.

No ramo pós-dano não intentional, o pedido é `MobEffectInstance(IRRADIATED,48000,amplifier,false,false,true)`, com amplificador **1** para `SIZE<=1.5F` ou **2** no outro ramo. São amplificadores do efeito, não nível de magia; os 48.000 são ticks declarados de duração do efeito, não duração da explosão. A implementação do [efeito Irradiated](../effects/irradiated.md) e do [tipo Radiation](radiation.md) tem seus próprios consumidores; imunidade/aceitação/tempo efetivo não são garantidos pelo pedido de `addEffect`, cujo retorno também é descartado.

## 5. Blocos, configuração e custos

O ramo de blocos e aquisição de tickets exige servidor e `NO_GRIEFING=false`; esses guards não envolvem automaticamente o laço de entidades da seção anterior. As configurações comuns declaradas são `nukeExplosionSizeModifier=3D` com limites `[0,Double.MAX_VALUE]`, `nukeMaxBlockExplosionResistance=1000` com `[0,Integer.MAX_VALUE]` e `nukesSpawnItemDrops=true`. O valor de size da bomba é convertido de double para float. Declaração de defaults/limites não comprova o valor carregado, um limite operacional seguro ou finitude após conversão. O modificador de tamanho é lido pelo produtor da bomba; a resistência e os drops são lidos pelos consumidores de blocos.

`removeChunk(B)` primeiro faz Stack.pop. Se a resistência configurada é `<=0`, retorna depois desse pop. Nos demais casos, percorre X/Z de `0..15` e Y de `15..0`, até `4096` candidatos por entrada antes dos filtros. As coordenadas Y são clampadas entre as alturas mínima/máxima pedidas ao Level; a rotina não constitui uma simulação física de ray tracing da explosão.

O teste espacial usa `ACMath.sampleNoise3D`, uma deformação vertical calculada por `ACMath.smin` e distância ao canto inferior: não há raio esférico constante de destruição. Em termos dos operandos próprios, `n=(noise(x,y,z,B)−0.5F)*0.45F+0.55F`, `h=smin(0.6F−abs(originBlockY−y)/B,0.6F,0.2F)` e o limiar compara `distToLowCornerSqr(originBlockX,y−1,originBlockZ)` a `h*(B+n*B)*B`. Os helpers, o Level e os estados atuais continuam seus owners.

`isDestroyable` aceita bloco sem `NUKE_PROOF` cuja resistência é **estritamente menor** que o config, **ou** o caso especial `TREMORZILLA_EGG`. A tag nativa `nuke_proof` referencia `#alexscaves:unmovable`, sujeita à composição final do pack. Não apresentar a tag como política universal de proteção: a exceção do ovo existe nesse predicado.

Para candidato elegível e não apenas ar vazio sem fluido, o ovo especial chama `spawnDinosaurs`. Outros casos escolhem `destroyBlock(pos,true)` quando drops estão ativos, o sorteio é menor que `0.025F/min(1F,SIZE)` e o fluido é vazio; senão delegam a `ACCompat.onBlockExploded`. Não há clamp próprio da probabilidade nesse cálculo. A rotina cria uma vez um objeto auxiliar de explosão com força `10F`, fonte nula e `BlockInteraction.DESTROY` para esse callback. O objeto auxiliar não comprova uma segunda aplicação nuclear de dano. Depois de um candidato marcado como afetado, há caminho de fogo condicionado ao sorteio `<0.15D` e suporte abaixo não aéreo. Nem cada candidato nem cada chamada implica destruição/drop/fogo aceitos.

O consumidor da explosão não cobra mana, stamina, souls, durabilidade ou inventário de player. Custos/gatilhos pertencem aos produtores: por exemplo, o sack encolhe seu próprio stack no caminho intentional. Ausência de débito aqui não define custo global zero nem permite uma segunda cobrança por tipo de dano. `exhaustion` é metadado do DamageType, não custo de casting. A `WorldEffectPolicy` do Black Arcana não recebe autoridade automática sobre mutações nativas do provider.

## 6. Chunks, segurança e integração com perks

`loadChunksAround(boolean)` só prossegue para `ServerLevel`. Recalcula a posição de chunk da entidade e `q=max(c, viewDistance/2)`, com divisão inteira do valor de distância de visão. Percorre o quadrado `−q..q` em X/Z e chama `ACPlatform.forceChunk(server,this,x,z,argumento,argumento)`. Para entradas regulares não negativas e término normal, a solicitação cobre `(2q+1)^2` posições; não é um cap certificado por dimensão nem uma medida de memória. A posição, SIZE e view distance usados na remoção são recalculados, sem uma lista própria persistida das solicitações originais.

A aquisição em `tick @210–211` passa **`true,true`** (`add,ticking`). `remove(RemovalReason)` testa servidor e `loadingChunks`, limpa esse campo antes da chamada e solicita `loadChunksAround(false)` (`@23–24`), que encaminha **`false,false`**. Depois delega a `Entity.remove`. O wrapper `ACPlatform.forceChunk` descarta o booleano retornado pelo `TicketController`; atualizar o marcador local não confirma uma remoção aceita no tracker.

**Descompasso preservado:** o [binário exato NeoForge 21.1.248](../EXACT-NEOFORGE-TICKETS-21.1.248.json) distingue as categorias `ENTITY_TICKING` e `ENTITY`, além dos mapas separados do tracker. A aquisição ticking e a tentativa de retirada não ticking não são operações simétricas. O achado continua **`CONFIRMED_SELECTED_STATIC_BRANCHES_NOT_LIVE_RUNTIME`**; um vazamento persistente real permanece **`NOT_OBSERVED`**. Esta ficha não declara que o problema foi corrigido, que o provider nunca libera chunks ou que o cleanup é garantido.

O binding estático acrescentado liga `AlexsCaves.<init>` a `registerTicketControllers`: cria o controller `alexscaves:forced_chunks`, instala o adapter e registra o callback `ACWorldData.clearLoadedChunksCallback(ServerLevel,TicketHelper)`. Esse corpo copia as chaves de owners UUID e BlockPos e solicita `removeAllTickets` para elas. Isso documenta ligação e chamadas no provider, sem afirmar que o callback foi entregue no runtime ou que restauração/cleanup físico foram bem-sucedidos. Os limites do snapshot antigo continuam descrevendo aquele recorte; o novo selo não altera seus campos. A persistência de `WasLoadingChunks` não prova recuperação de todos os estados ou resolução dos tickets.

As flags de segurança permanecem explícitas: `native_release_ticket_bucket_mismatch=CONFIRMED_SELECTED_STATIC_BRANCHES_NOT_LIVE_RUNTIME` e `actual_persistent_ticket_leak=NOT_OBSERVED`. Nenhum resultado NT-01…NT-07 ou correção do mismatch é afirmado. O [plano de aceitação NT-01…NT-07](../../../../../docs/qa/alexscaves-1010-nuclear-ticket-physical-acceptance.md) permanece um plano, sem execução física afirmada. O selo estático registra os sete campos e a divergência conhecida; não substitui aceitação física nem liberação de integração mutadora.

| Alteração pretendida por perk | Consumidores que precisam de contrato independente |
|---|---|
| SIZE / raio / intensidade | `getChunksAffected`, M(s), AABB, r, fila cúbica e grade de tickets variam por mecanismos diferentes; não escalar por um único raio presumido |
| Tipo de alvo / área / filtros | Consulta de vivos, guards locais, flags e eventos de damage/effect; não remover filtros herdados ou atribuir permissões de PvP |
| Duração / frequência | Condição `tickCount>40 && filaVazia`, reposição da fila e agendamento; não registrar como cast fixo de 40 ticks ou one-hit |
| Knockback / status | `setDeltaMovement` substitui vetor e o efeito é solicitado independentemente do retorno de hurt; não duplicar settlement ou radiação |
| Owner / kills / Mastery | Factories sem argumento Entity, sem bridge nativa a player neste caminho; resultado final depende dos owners do Minecraft/provider |
| Blocos / chunks | Mismatch de categoria, operações e caps/cleanup não homologados; nenhuma autorização por `WorldEffectPolicy` decorre do catálogo |

**Integração mutadora bloqueada:** `NO_MUTATION`. Hooks `NOT_VERIFIED`; QA física `NOT_TESTED`. Não alterar raio, tempo, dano, chunks, blocos, radiação, custo ou autoria por perks a partir deste certificado documental. Não há autorização de runtime, promoção de Stage ou adapter executável para Black Arcana, Enshrouded ou RPG Skill Tree nesta entrega.

## 7. Validação, localizadores e escopo do selo

O [manifesto consolidado](../EXACT-NUCLEAR-CONTRACTS-1.0.10.json) sela a ficha e membros exatos do JAR, descritores JVM e instruções selecionadas. Foram lidos os **20 membros próprios** de `NuclearExplosionEntity`: construtor, métodos, lambda e inicializador estático. Os probes históricos contabilizavam 19 por excluir `<clinit>`; seus dados e limites continuam preservados, sem reescrever a evidência antiga.

As seis provas anteriores permanecem imutáveis: [envelope](../EXACT-NUCLEAR-ENVELOPE-1.0.10.json), [produtores](../EXACT-NUCLEAR-PRODUCERS-1.0.10.json), [numérico](../EXACT-NUCLEAR-NUMERIC-1.0.10.json), [alvos/mundo](../EXACT-NUCLEAR-TARGET-WORLD-1.0.10.json), [lifecycle de chunks](../EXACT-NUCLEAR-CHUNK-LIFECYCLE-1.0.10.json) e [NeoForge TicketController](../EXACT-NEOFORGE-TICKETS-21.1.248.json). Os recortes de [JSONs/tags](EXACT-RESOURCE-MANIFEST-1.0.10.json), [factories/callers](EXACT-CONSUMERS-1.0.10.json) e [janelas de chamadas](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json) também permanecem como provas históricas parciais. Nenhum snapshot, isoladamente, certifica todo o mundo, toda a infraestrutura NeoForge ou o comportamento de um modpack.

A contraparte externa auditada é `neoforge-21.1.248-universal.jar`, **3.551.268 bytes**, SHA-256 `90a56f70425711b4e1a4b94ff0c2904ae9f6d74ca6478b3b2152ac794a07b8e5`. A CI própria desse recorte continua validando o binário externo; classes NeoForge não são confundidas com classes do provider no perfil nuclear. A fonte pública de Alex's Caves `523308608422ab8e31974befa7111ecdf495dd37` declara versão **1.1.1**, apenas corroboração, sem substituir os parâmetros do JAR instalado.

**Contabilidade:** **+0 raízes mágicas novas**. São dois resource IDs de dano com consumidor compartilhado, não dois processos independentes de magia. O universo do provider permanece aberto. O contrato estático é `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; a QA NT-01…NT-07, multiplayer, hit counts, atribuição causal, composição de tags/config e integração mutadora não foram demonstrados. Preservar `NOT_VERIFIED`, `NOT_TESTED` e `NO_MUTATION`.

### Membros próprios e descritores JVM

| Membro | Descritor |
|---|---|
| `<init>` | `(Lnet/minecraft/world/entity/EntityType;Lnet/minecraft/world/level/Level;)V` |
| `getAddEntityPacket` | `(Lnet/minecraft/server/level/ServerEntity;)Lnet/minecraft/network/protocol/Packet;` |
| `tick` | `()V` |
| `remove` | `(Lnet/minecraft/world/entity/Entity$RemovalReason;)V` |
| `getChunksAffected` | `()I` |
| `loadChunksAround` | `(Z)V` |
| `calculateDamage` | `(FF)F` |
| `removeChunk` | `(I)V` |
| `isDestroyable` | `(Lnet/minecraft/world/level/block/state/BlockState;)Z` |
| `defineSynchedData` | `(Lnet/minecraft/network/syncher/SynchedEntityData$Builder;)V` |
| `getSize` | `()F` |
| `setSize` | `(F)V` |
| `isNoGriefing` | `()Z` |
| `setNoGriefing` | `(Z)V` |
| `isIntentionalGameDesign` | `()Z` |
| `setIntentionalGameDesign` | `(Z)V` |
| `readAdditionalSaveData` | `(Lnet/minecraft/nbt/CompoundTag;)V` |
| `addAdditionalSaveData` | `(Lnet/minecraft/nbt/CompoundTag;)V` |
| `lambda$tick$0` | `(Lnet/minecraft/core/BlockPos;Lnet/minecraft/core/BlockPos;)I` |
| `<clinit>` | `()V` |
