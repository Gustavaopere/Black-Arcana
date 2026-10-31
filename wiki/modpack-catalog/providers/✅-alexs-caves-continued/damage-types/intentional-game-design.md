# Intentional Game Design — tipo de dano `alexscaves:intentional_game_design` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED` (recurso SHA-exato). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:intentional_game_design`.
- **Caminho ZIP:** `data/alexscaves/damage_type/intentional_game_design.json`.
- **SHA-256 do JSON:** `4146b42cc4a880583fd8e94600ec2bb34f70ac5d4249289932c627e3cac82a09`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `intentional_game_design` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
| `scaling` | `never` | Campo `scaling` do tipo de dano; não fixa dano causado nem curva de perks |
| `exhaustion` | `0.3` | Valor do campo `exhaustion`; **não** é mana, stamina, custo do feitiço ou dano |

## Tags de tipo de dano declaradas diretamente

- Nenhuma entrada direta para este ID nos seis arquivos `tags/damage_type/*.json` encontrados no artefato.

Essas são **entradas textuais diretas** dos seis arquivos `data/*/tags/damage_type/*.json` encontrados no JAR. Elas não comprovam as tags finais resolvidas depois de datapacks, outras dependências ou overrides. Uma referência a tag não prova que o ataque usado no jogo produza este `DamageSource`.

## Superfícies necessárias para perks — ainda não auditadas

| Capacidade pretendida | Situação |
|---|---|
| Factory de `DamageSource` / chamadas JVM | ✅ localizadas estaticamente; comportamento e caminhos efetivos `NÃO VERIFICADO` |
| Origem, atacante, owner, attribution e condições de PvP | `NÃO VERIFICADO` |
| Fórmula de dano, mitigação, críticos e resistências | `NÃO VERIFICADO` |
| Alvos elegíveis, tipo target/área, alcance, raio e filtros | `NÃO VERIFICADO` |
| Entidades/projéteis, tamanho, velocidade, colisão e homing | `NÃO VERIFICADO` |
| Duração, intervalo de hits, custo de ação e cooldown de casting | `NÃO VERIFICADO` |
| Persistência, ordenação de eventos, server authority e deduplicação | `NÃO VERIFICADO` |
| Hook de mutação seguro na versão instalada | `NOT_VERIFIED` |
| QA real em modpack/multiplayer | `NOT_TESTED` |

## Boundary / decisão provisória

O *provider* mantém autoridade sobre a criação, classificação e aplicação de dano. Black Arcana não altera `DamageSource`, escola, dano, tags ou projéteis sem evidência dos consumidores Java e hooks seguros. O RPG Skill Tree fornece perks/atributos somente através de boundary verificada, sem double-processing. **Fail-closed:** `NO_MUTATION` até a auditoria dos consumidores e a validação específica.

**Contabilidade:** 1/11 recursos de tipo de dano documentados; **+0 raízes mágicas novas**. Este objeto não recebe status `COMPLETE_PERK_READY` apenas por existir como JSON.

## Evidência compilada 1.0.10 — factory e consumidores diretos

**Escopo:** `SHA_EXACT_STATIC_FACTORY_AND_DIRECT_CALLSITE_ONLY`. [Manifesto dos consumidores](EXACT-CONSUMERS-1.0.10.json) · [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40993193816).

- **Classe de fábrica:** `com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes.class`, SHA-256 `389fb88f8d6e1515e3dfe7f401a728bb33629666bd2319ae7e25668f710e4ef6`.
- **Método:** `ACDamageTypes.causeIntentionalGameDesign`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `INTENTIONAL_GAME_DESIGN` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;I)V`.
- **Parâmetros da factory:** apenas `RegistryAccess` — nenhum argumento `Entity` na assinatura da factory.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/entity/item/NuclearExplosionEntity.class` | `public void tick()` | `()V` | 605 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Aprofundamento de fluxo — 1.0.10 (instruções compiladas)

**Evidência estática delimitada:** [manifesto de janelas e branch opcodes](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json), auditado no JAR SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Classe `com/github/alexmodguy/alexscaves/server/entity/item/NuclearExplosionEntity.class` (SHA-256 `d9c827a9acb2d0f9e7050252ed57e6a3d0a8ad49053e54f19a8eaeb6b84da912`). Método `public void tick()`, descritor JVM `()V`; 348 instruções extraídas e 39 anchors de branch registrados. Resumo de chamadas diretas: `causeIntentionalGameDesign` @ `605`, `causeNukeDamage` @ `618`.

- O método `NuclearExplosionEntity.tick()` possui condição `isIntentionalGameDesign()` em `592`, seguida de `ifeq 611` em `595`.
- A factory `causeIntentionalGameDesign()` aparece em `605`; `goto 621` em `608` pula a alternativa `causeNukeDamage()` do offset `618`. A chamada subsequente observada é `LivingEntity.hurt()` em `623`.
- Este recorte comprova **seleção condicional de DamageSource**, mas não autoriza derivar percentuais de dano, proteção contra explosões, extensão de área ou novos hooks.

**Limite metodológico:** offsets, referências de método, testes e desvios são provas do *bytecode*; a análise não reconstruiu exceções, switch dispatch, todos os caminhos de CFG ou condições de runtime. `NOT_CERTIFIED` para comportamento integral; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Black Arcana não deve substituir settlement, autorizações de servidor, segurança do mundo ou rotinas próprias do provider.


## Envelope nativo da explosão nuclear — auditoria SHA-exata 1.0.10

**Prova adicional:** [EXACT-NUCLEAR-ENVELOPE-1.0.10.json](../EXACT-NUCLEAR-ENVELOPE-1.0.10.json), confrontado com o JAR publisher instalado pelo [workflow do envelope](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-nuclear-envelope.yml). O manifesto sela **19 métodos declarados**, **sete métodos próprios selecionados** de `NuclearExplosionEntity`, suas contagens/hashes de instruções, o hash de classe e **29 offsets críticos** de `tick()`. A prova usa somente bytecode delimitado e não executa o gameplay.

### Estado, duração e persistência do objeto consumidor

| Superfície | Evidência da versão instalada | Limite para perks |
|---|---|---|
| Identidade do dano | `NuclearExplosionEntity.tick()` consulta `isIntentionalGameDesign()` (592); `ifeq 611` (595) separa `causeIntentionalGameDesign` (605) de `causeNukeDamage` (618), com convergência em `LivingEntity.hurt(DamageSource,float)` (623). | São duas classificações de `DamageSource` para o **mesmo tipo de entidade consumidora**, não dois feitiços independentes. Uma perk não pode duplicar a aplicação de dano pela bifurcação. |
| Dados sincronizados | `defineSynchedData` define `SIZE` com default `1.0f` (offsets 1/4), `NO_GRIEFING` com `false` (13/16) e `INTENTIONAL_GAME_DESIGN` com `false` (25/28). | Estados iniciais da entidade. Não inferir que esses defaults sejam os parâmetros efetivos de todos os emissores. |
| Escala de dano | `tick()` usa `LivingEntity.distanceTo` (456), `calculateDamage(float,float)` (466) e insere o resultado em `fstore 9` (469). O helper `calculateDamage` tem 26 instruções e inclui as constantes `1.5f`, `100.0f` e `400.0f`. | O valor de dano pode variar com distância e tamanho; as constantes **não autorizam publicar fórmula numérica completa** sem reconstruir e validar a pilha/branches de cálculo. Dano final também depende das regras de `hurt`. |
| Filtro especial de alvo | Em `tick()`, a verificação de `TremorzillaEntity` (570–573) pode zerar parâmetros (576–580); o `ifle 627` (586) avalia o valor antes de emitir `DamageSource`. | Os literais `0` na janela pertencem a um **ramo condicionado**, não provam que todos os ataques causam zero dano. |
| Cálculo de alvos | O consumidor consulta `Level.getEntitiesOfClass(Class,AABB)` (421) e ajusta movimento com `Vec3.scale` (640) e `LivingEntity.setDeltaMovement` (643). | A caixa e os filtros completos, repetição de hits, LOS, raio de dano e PvP ainda não estão validados. Não interpretar a AABB como alcance de cast. |
| Efeito pós-dano | Após `hurt`, a verificação `isIntentionalGameDesign` (647) leva a `ifne 702` (650); o outro ramo referencia `ACEffectRegistry.IRRADIATED` (659). | Evidência de diferenciação de efeitos; não inferir duração, incidência, persistência ou o efeito em todos os alvos sem seguir o ramo completo. |
| Manipulação de blocos | `tick()` chama `Level.getBlockState` (80) e `isDestroyable` (83), e mantém superfície de remoção `Entity.remove` (167). | **World mutation de risco elevado**: não se autoriza reproduzir destruição fora do `WorldEffectPolicy` do Black Arcana. O literal `NO_GRIEFING=false` não prova política efetiva do servidor. |
| Estado persistido diretamente | `addAdditionalSaveData(CompoundTag)` guarda `WasLoadingChunks` com `putBoolean`; `readAdditionalSaveData` usa `ACCompat.getBoolean` para a mesma chave e reatribui `loadingChunks`. | Esses métodos **não apresentam escrita direta** de `SIZE`, `NO_GRIEFING` ou `INTENTIONAL_GAME_DESIGN`. A restauração desses estados, superclass e eventuais mixins exigem auditoria separada. |
| Autor/attribution | `causeIntentionalGameDesign(RegistryAccess)` não recebe `Entity`, `LivingEntity` nem `Player` no descritor JVM da factory; `tick()` passa apenas `Level.registryAccess` (599–605). | Ausência de argumento de atacante **não certifica identidade causal** para perks de kill/XP, nem comprova ausência de atribuição por outras rotas. Atribuição fica `NOT_VERIFIED`. |

**Condicionamento importante:** o `DamageSource` selecionado e o valor de dano são operações distintas. O mesmo `float` do consumidor é passado a `LivingEntity.hurt` (621–623), qualquer que seja a factory selecionada; isso comprova compartilhamento do valor compilado no ponto de chamada, sem validar a fórmula nem o resultado após mitigação. O boolean retornado por `hurt` é descartado (`pop` em 626), portanto não deve servir como prova de hit aceito/trigger de perk.

### Limites de autorização e próximo fechamento

Esta é uma **auditoria de superfícies estáticas**. Faltam rastrear produtores da `NuclearExplosionEntity`, parâmetros de spawn/tamanho, filtros exatos da AABB, comportamento por tick, cálculo integral de dano, raio de destruição, persistência de `INTENTIONAL_GAME_DESIGN` e eventuais interações com outros mods no mundo real. A checagem de mundo e a atribuição de autoria não foram homologadas.

**Status mantido:** ⚠️ `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`. Este checkpoint não adiciona raiz mágica, não certifica `Nuke` por associação, não altera contadores globais e não promove Stage.


## Emissores e configuração de `NuclearExplosionEntity` — JAR exato 1.0.10

**Inventário SHA-exato de referências:** [EXACT-NUCLEAR-PRODUCERS-1.0.10.json](../EXACT-NUCLEAR-PRODUCERS-1.0.10.json), auditado pelo [workflow de producers](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-nuclear-producers.yml). O escopo pesquisou tokens de constant pool `NuclearExplosionEntity`/`NUCLEAR_EXPLOSION` nas classes do provider. **Nove classes candidatas** surgiram; **seis contêm referências em métodos examinados pelo parser**, das quais **quatro são caminhos server-side de emissão/configuração**: `NuclearFurnaceBlockEntity.destroyWhileCritical(boolean)`, `NuclearBombEntity.explode()`, `NucleeperEntity.explode()` e `SackOfSatingItem.acInventoryTick(ItemStack,Level,Entity,boolean)`. `ClientProxy.clientInit` é referência do cliente, **não produtor de dano**; `NuclearExplosionEntity.tick` referencia a própria classe em `invokedynamic` e não constitui produtor adicional. `ACEntityRegistry` e outras candidatas sem método selecionado não provam ausência de inicialização estática, pois o parser exclui `<clinit>`.

| Produtor nativo | Instruções compiladas selecionadas | Limite de inferência |
|---|---|---|
| `SackOfSatingItem.acInventoryTick` | Guardas `isExploding(ItemStack)` @275/278 e `Level.isClientSide()` @282/285; registry `NUCLEAR_EXPLOSION` @288, `ACCompat.createEntity` @300, `setPos` @322, `setSize(0.5f)` @327/330, `setIntentionalGameDesign(true)` @335/336, `Level.addFreshEntity` @342, `setExploding(false)` @348. | Único emissor **identificado neste recorte** que escreve explicitamente `INTENTIONAL_GAME_DESIGN=true`. `Level.addFreshEntity` é solicitação de spawn, não garantia de aceitação ou hit. O literal `4.0d` no posicionamento @315 não deve ser confundido com alcance/custo/cooldown. |
| `NuclearFurnaceBlockEntity.destroyWhileCritical` | `NUCLEAR_EXPLOSION` @260 após um desvio `ifeq 318` @257; `ACCompat.createEntity` @275; `setPos` @294; `setSize(0.75f)` @299/302; `Level.addFreshEntity` @311. | A origem é um evento condicionado de destruição crítica da fornalha. Sem prova de autor/player/custo de ação; não classificar automaticamente como variante `intentional_game_design`. |
| `NuclearBombEntity.explode` | `NUCLEAR_EXPLOSION` @0; `ACCompat.createEntity` @15; `copyPosition` @24; `setSize` @43 a partir de um `ModConfigSpec.DoubleValue.get` do config comum; `Level.addFreshEntity` @51. | Valor efetivo de size depende da configuração do servidor (não auditada); não publicar literal imaginário ou assumir a flag intentional. |
| `NucleeperEntity.explode` | `NUCLEAR_EXPLOSION` @0; `ACCompat.createEntity` @15; `copyPosition` @24; `setSize` @42; `ACCompat.gameRule(Level, RULE_MOBGRIEFING, true)` @53, com `ifne 64` @56; se o ramo permitir, `setNoGriefing(true)` @61; `Level.addFreshEntity` @69. | O efeito destrutivo depende de regras nativas e do estado da entidade, além dos gates de mundo de qualquer integração externa. A fórmula de size não foi fechada por este recorte. |

**Causalidade:** todas as quatro rotas selecionadas chamam `ACCompat.createEntity(EntityType,Level)`, cuja implementação SHA-exata auditada anteriormente delega a `EntityType.create(Level)`; não há prova de propagação de owner para estes quatro objetos. O `DamageSource` `intentional_game_design` tem factory `(RegistryAccess)->DamageSource`, sem argumento de atacante; não anexar Mastery, procs, PvP ou XP a um player com base apenas em proximidade, item ou posição.

**Fronteira:** a classificação de dano depende da flag sincronizada **no consumidor**, não do nome ou visual da explosão. O mesmo consumidor também pode usar `alexscaves:nuke`; o `SackOfSatingItem` fornece evidência explícita da variante intentional no caminho selecionado, **sem provar que essa seja a única origem possível** (reflexão, mixins, indireção e mudanças de configuração permanecem fora do inventário). Não duplicar raízes mágicas ou o pipeline de `hurt`.

**Status:** ⚠️ evidência de emitters adicionada, contrato integral `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; contadores e Stage sem promoção.


## Expressão de dano compartilhada com Nuke — SHA-exata 1.0.10

**Evidência selecionada:** [EXACT-NUCLEAR-NUMERIC-1.0.10.json](../EXACT-NUCLEAR-NUMERIC-1.0.10.json), [verificador da CI](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-nuclear-numeric.yml) e [análise ampliada da ficha Nuke](nuke.md#cálculo-numérico-e-tamanho-de-emissão--método-sha-exato-1010). `NuclearExplosionEntity.calculateDamage(float,float)` é o **mesmo helper nativo** utilizado na execução que seleciona `causeIntentionalGameDesign` ou `causeNukeDamage`. A escolha do `DamageSource` acontece depois de o consumidor armazenar o valor bruto. Não registrar duas fórmulas ou dois hits para um único evento.

Do método compilado (26 instruções), com `d` = primeiro `float`, `r` = segundo `float` e `s` = `getSize()`:

\[
D_{\mathrm{raw}}=\frac{r-d}{r}\times
\begin{cases}
100,&s\leq1.5\\
100+400(s-1.5),&s>1.5.
\end{cases}
\]

A multiplicação se baseia nos offsets `0–4`, `7–14`, `17–38` e `41–45`. O valor bruto pode ser descartado por guards do `tick`, sofrer mitigação, ou não resultar em hit válido; não inferir a partir deste cálculo que houve dano real.

**Atribuição da variante:** `SackOfSatingItem.acInventoryTick` usa `setSize(0.5f)` e `setIntentionalGameDesign(true)` antes de solicitar spawn, conforme manifesto anterior. A expressão desta seção descreve o helper compartilhado; não significa que as explosões de `NucleeperEntity` (tamanho `1.0f` ou `1.75f` dependendo de `isCharged`) ou `NuclearBombEntity` (size por `ACServerConfig.nukeExplosionSizeModifier`) usem automaticamente a classificação `intentional_game_design`. Consultar a flag real do consumidor. O inventário de produtores permanece parcial quanto a indireções e mods externos.

**Limites:** contrato `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Sem claims de player-owner, Mastery, custo, PvP, proteção do mundo ou fechamento do provider.


## Filtros, geometria e efeitos destrutivos compartilhados — SHA 1.0.10

**Referência auditável:** [EXACT-NUCLEAR-TARGET-WORLD-1.0.10.json](../EXACT-NUCLEAR-TARGET-WORLD-1.0.10.json) e a seção de [alvos/mundo em Nuke](nuke.md#alvos-geometria-e-mutação-do-mundo--seleção-jvm-1010). Ambas as damage types reutilizam o mesmo `NuclearExplosionEntity.tick` (348 instruções). A distinção é a flag `INTENTIONAL_GAME_DESIGN` no consumidor, usada para selecionar apenas uma das duas factories de `DamageSource` @592–623. **Não duplicar** consultas, dano, movimento ou callbacks de perks por existirem duas damage types.

- A fórmula bruta `((r-d)/r)*M(getSize())` usa `r=1.5*(15*ceil(getSize()))+1` na entidade; o conjunto de alvos vem de `getBoundingBox().inflate(1.5B,0.6B,1.5B)`, `B=15*ceil(getSize())`, e `getEntitiesOfClass(LivingEntity,AABB)` @421. Não é contrato de alcance do item `SackOfSatingItem`, de targeting de spells, nem área de destruição.
- Os branches de `RaycatEntity`, da tag `RESISTS_RADIATION` e de `TremorzillaEntity` podem suprimir/reduzir dano e deslocamento; `LivingEntity.hurt` é condicional, enquanto `setDeltaMovement` fica numa rota posterior que também pode ser atingida com dano local zero. O valor de `hurt` é descartado.
- **Diferença de effect:** em `tick` @647–702, `isIntentionalGameDesign()=true` pula a criação/aplicação da effect `IRRADIATED`, que no outro ramo usa duração literal de 48000 ticks e amplificador 1 ou 2 conforme `getSize()>1.5f`. Isso é uma bifurcação nativa da **effect**, não prova de efeito realmente aceito em jogo.
- `setIntentionalGameDesign(true)` no emissor `SackOfSatingItem` **não** implica `NO_GRIEFING=true`. O ramo de destruição depende de `Level.isClientSide` e `isNoGriefing` @174–187, consulta `isDestroyable` com tag `NUKE_PROOF` e configuração de resistência, e pode alcançar `Level.destroyBlock`/`ACCompat.onBlockExploded`/`setBlockAndUpdate` via `removeChunk`. Também existe `ACPlatform.forceChunk` no helper. Não pressupor segurança de regiões, rollback ou cleanup.
- Sob a origem conhecida `SackOfSatingItem`, `SIZE=0.5f` produz `ceil(SIZE)=1`, com inflação geométrica de `(22.5,9,22.5)` blocos adicionados à AABB-base e segundo argumento do dano bruto `r=23.5`. Esses são parâmetros internos compilados do consumidor, não raio de casting, alcance de clique ou hit confirmado.

**Permissão:** não ativar perks de range/AoE, griefing, tamanho, efeito, owner, Mastery, PvP ou multiplicação de procs com base nesta evidência. É necessário contrato mutador nativo realmente comprovado, política de mundo no Black Arcana, bounds e QA físico. **⚠️ `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`.** Catálogo e Stage inalterados.


## Cleanup de tickets de chunk compartilhado — auditoria SHA-exata 1.0.10

**Fonte:** [EXACT-NUCLEAR-CHUNK-LIFECYCLE-1.0.10.json](../EXACT-NUCLEAR-CHUNK-LIFECYCLE-1.0.10.json) · [ficha Nuke — tickets e lifecycle](nuke.md#tickets-de-chunks-aquisição-tentativa-de-liberação-e-restauração--jar-1010) · [CI dedicada](https://github.com/Gustavaopere/Black-Arcana/actions/workflows/alexscaves-1010-nuclear-chunk-lifecycle.yml).

A flag `INTENTIONAL_GAME_DESIGN` seleciona o tipo de `DamageSource`, mas **não cria outro sistema de gerenciamento de chunks**. O consumidor compartilhado `NuclearExplosionEntity.tick()` define `loadingChunks=true` e solicita `loadChunksAround(true)` no ramo de destruição do servidor; seu `remove(RemovalReason)` sobrescrito testa `loadingChunks`, grava `false` e chama `loadChunksAround(false)` antes de `Entity.remove`. A rotina encaminha os dois booleanos para `ACPlatform.forceChunk`, que delega a `TicketController.forceChunk` NeoForge e descarta o resultado booleano. É evidência de **tentativa de release**, não prova de êxito integral ou persistência de tickets.

O `SackOfSatingItem` registra `SIZE=0.5f` e `setIntentionalGameDesign(true)` no caminho previamente selecionado, mas **não** demonstrou alteração explícita de `NO_GRIEFING`. Se o caminho de destruição for ativado, o raio da grade de tickets depende de `q=max(ceil(SIZE), floor(viewDistance/2))`, não apenas do tamanho visual/raio de dano. O estado `WasLoadingChunks` persistido na entidade é um booleano, sem lista de tickets ou confirmação de cleanup após restart. Não promover claims de proteção do mundo, economia de chunks, owner ou segurança por associação à variante intentional.

**Estado permanece:** ⚠️ `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`, sem incremento de ficha ou promoção de Stage.


## Atenção: descompasso nos tickets de chunks também afeta a variante intentional

**Prova SHA-exata:** [EXACT-NEOFORGE-TICKETS-21.1.248.json](../EXACT-NEOFORGE-TICKETS-21.1.248.json) · [análise detalhada em Nuke](nuke.md#bloqueio-de-integração-tickets-ticking-não-correspondem-à-liberação--binários-exatos-1010--neoforge-211248).

A seleção de `causeIntentionalGameDesign` não substitui o `NuclearExplosionEntity` nem sua rotina de forçamento de chunks. O caminho de emissão anteriormente observado de `SackOfSatingItem` define `SIZE=0.5f` e `INTENTIONAL_GAME_DESIGN=true`, sem comprovação de `NO_GRIEFING=true`. Portanto, quando a entidade ingressa no ramo de destruição, mantém o mesmo descompasso observado entre `loadChunksAround(true)` (força tickets `ENTITY_TICKING`, usando `tickingChunks` no NeoForge) e `loadChunksAround(false)` (tenta remover tickets `ENTITY`, consultando o mapa separado `chunks`). A ida/volta repassa o mesmo booleano aos parâmetros `add` e `ticking`, conforme offsets `86–88` da versão compilada 1.0.10.

O adaptador `ACPlatform` ignora o retorno booleano do `TicketController`. Reinicialização e recuperação dos tickets são geridas pelo NeoForge com `ForcedChunksSavedData` e `LoadingValidationCallback` opcionais, mas o callback registrado pelo Alex’s Caves e o estado efetivo pós-restart não foram fechados nesta auditoria. **Não certificar cleanup, ausência de vazamento, WorldEffectPolicy ou integração de propriedades mutadoras.** A evidência registra descompasso estático, não observação de vazamento em servidor real.

**Estado:** ⛔ integração mutadora bloqueada; ficha ⚠️ `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`. O universo do provider, Stage e índices permanecem inalterados.
