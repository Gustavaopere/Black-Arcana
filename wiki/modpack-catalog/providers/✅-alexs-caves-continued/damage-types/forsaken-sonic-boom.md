# Forsaken Sonic Boom — tipo de dano `alexscaves:forsaken_sonic_boom` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED` (recurso SHA-exato). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:forsaken_sonic_boom`.
- **Caminho ZIP:** `data/alexscaves/damage_type/forsaken_sonic_boom.json`.
- **SHA-256 do JSON:** `1a8c19b6e54d9030fb706055906dc1598ac20dd9e2fbc5813858855310bbbf30`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `forsaken_sonic_boom` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
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
- **Método:** `ACDamageTypes.causeForsakenSonicBoomDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `FORSAKEN_SONIC_BOOM` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
- **Parâmetros da factory:** `RegistryAccess` e `Entity` — não comprova autoria final.
- **Referências `invokestatic` encontradas:** 2 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/entity/ai/ForsakenAttackGoal.class` | `public void tick()` | `()V` | 108 | `invokestatic` |
| `com/github/alexmodguy/alexscaves/server/entity/ai/ForsakenAttackGoal.class` | `public void tick()` | `()V` | 576 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.

## Aprofundamento de fluxo — 1.0.10 (instruções compiladas)

**Evidência estática delimitada:** [manifesto de janelas e branch opcodes](EXACT-DAMAGE-PATH-ANCHORS-1.0.10.json), auditado no JAR SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Classe `com/github/alexmodguy/alexscaves/server/entity/ai/ForsakenAttackGoal.class` (SHA-256 `48cfdd6c370f68550d0d7af768466f99f330e8fd4f825a520411a1bc5d70fb55`). Método `public void tick()`, descritor JVM `()V`; 826 instruções extraídas e 98 anchors de branch registrados. Resumo de chamadas diretas: `causeForsakenSonicBoomDamage` @ `108`, `causeForsakenSonicBoomDamage` @ `576`.

- Em `tick()`, o offset `87` referencia `ForsakenEntity.hasLineOfSight()` antes da factory de offset `108`; a rota também referencia `getSonicDamageAgainst()` em `116` e `LivingEntity.hurt()` em `119`.
- Na segunda factory (`576`), são visíveis `ACTagRegistry.FORSAKEN_IGNORES` em `551`, o desvio `ifne` em `557`, `getSonicDamageAgainst()` em `584`, a constante `0.65f` em `587`, `fmul` em `590`, `Math.ceil()` em `592` e `LivingEntity.hurt()` em `596`.
- Essas duas referências pertencem ao mesmo método `tick()`, mas **não comprovam dois hits** por ciclo nem a quantidade final de vítimas.

**Limite metodológico:** offsets, referências de método, testes e desvios são provas do *bytecode*; a análise não reconstruiu exceções, switch dispatch, todos os caminhos de CFG ou condições de runtime. `NOT_CERTIFIED` para comportamento integral; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Black Arcana não deve substituir settlement, autorizações de servidor, segurança do mundo ou rotinas próprias do provider.

## Helper de dano confirmado no JAR 1.0.10 — `getSonicDamageAgainst`

**Grau da prova:** `SHA_EXACT_HELPER_ABI_AND_BYTECODE`. [Manifesto fixado](EXACT-DAMAGE-HELPERS-1.0.10.json) e [CI da auditoria](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40997154302). Classe `com/github/alexmodguy/alexscaves/server/entity/living/ForsakenEntity.class` (SHA-256 `72981b25b3af251b3ee66b6ef16b650997359ff94673ad500256b2d1cee0cde1`). Método `public float getSonicDamageAgainst(net.minecraft.world.entity.LivingEntity)`, descritor `(Lnet/minecraft/world/entity/LivingEntity;)F` e SHA-256 do método parseado `db47e82eebdb86724b6a71164ca563d0a75910bb143c16b944a5beb63f537d88`.

- O bytecode de `getSonicDamageAgainst(LivingEntity)` usa `LivingEntity.getType()`, `EntityType.builtInRegistryHolder()`, `Holder.Reference.is(TagKey)` e a chave `ACTagRegistry.WEAK_TO_FORSAKEN_SONIC_ATTACK`.
- Ramo verdadeiro da consulta à tag: constante `45.0f` no offset 16; ramo alternativo: `4.0f` no offset 22. Os dois caminhos convergem no retorno `freturn` offset 25.
- **Parâmetro bruto para a entidade passada ao helper:** `45.0f` ou `4.0f` segundo aquela tag, **antes** de processamentos do caller, da `LivingEntity.hurt`, resistências ou outros modificadores.
- A auditoria anterior de `ForsakenAttackGoal.tick()` mostrou dois usos. O segundo caminho possui `0.65f`, `Math.ceil()` e `LivingEntity.hurt()`: a operação local sobre esses retornos resulta, aritmeticamente, em `ceil(45×0.65)=30` ou `ceil(4×0.65)=3` como **argumento bruto daquele trecho**, quando executado. O primeiro caminho não deve herdar esse multiplicador.

**Limites obrigatórios:** a tag de entidade pode ser modificada por datapacks; a condição de ativação do ataque, o número de alvos, o resultado de `LivingEntity.hurt`, as proteções e a frequência de aplicação dependem de outros caminhos. A inspeção **não** homologou hook mutador nem dano efetivo. `NOT_CERTIFIED` / `NOT_VERIFIED` / `NOT_TESTED` / `NO_MUTATION`.


## Contratos estáticos adicionais — fluxo Forsaken Sonic (JAR 1.0.10)

**Fonte:** [manifesto exato dos métodos de ataque](EXACT-FORSAKEN-SONIC-1.0.10.json), extraído do JAR 1.0.10 com SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` / SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O manifesto registra `ForsakenAttackGoal` (SHA de classe `48cfdd6c370f68550d0d7af768466f99f330e8fd4f825a520411a1bc5d70fb55`) e `ForsakenEntity` (`72981b25b3af251b3ee66b6ef16b650997359ff94673ad500256b2d1cee0cde1`), com descritores, hashes de métodos e instruções simbólicas delimitadas. A fonte 1.1.1 não é utilizada como autoridade para esta build.

### Dois caminhos observados — não presumir dois hits

| Condição e execução | Instruções verificadas | Limitação |
|---|---|---|
| Habilitação do goal | `canUse()` consulta `ForsakenEntity.getTarget()`; exige referência não nula e `LivingEntity.isAlive()` | Não constitui condição integral de combate: goals concorrentes podem impedir execução |
| Inicialização | `start()` zera `navigationCheckCooldown`, `jumpEnqueued` e `attemptSonicDamageIn`; `getRandom().nextBoolean()` alimenta `sonicEnqueued` | Não traduzir o booleano aleatório em chance efetiva de ataque/hit |
| **Sonic direcionado** | `tick()`: obtém alvo principal via `ForsakenEntity.getTarget()` em offset 4 e `astore_1` em 7; sob `attemptSonicDamageIn == 0` (branch 79) e `hasLineOfSight(alvoPrincipal)` em 87 (branch 90), cria fonte `causeForsakenSonicBoomDamage` em 108 e chama `getSonicDamageAgainst(alvoPrincipal)` em 116; solicita `LivingEntity.hurt` em 119, com posterior `knockBackAngle` em 127 | O retorno de `hurt` é descartado (`pop` em 122). Não presumir dano aplicado/knockback condicionado ao hit aceito |
| **Sonic Blast em área** | `sonicEnqueued` e LOS (branches 134/145) e `ANIMATION_SONIC_BLAST` controlam caminho; na janela da animação, `AABB.inflate(16,8,16)` precede `Level.getEntitiesOfClass(LivingEntity,...)` em 459 e iteração da lista | `16,8,16` são expansões de caixa da consulta, não raio esférico de dano nem alcance garantido |
| Filtro por vítima na varredura de área | `isAlliedTo` do Forsaken (510) e da vítima (522), checagem de distância `distanceTo` com valor `14.0f` (534/537/540) e `ACTagRegistry.FORSAKEN_IGNORES` (551/554/557); desvios pulam a solicitação de dano | Os valores de tags são resolvidos no ambiente, inclusive datapacks; execução do laço, alvos e compatibilidade multiplayer não foram medidos |
| Aplicação solicitada na varredura | `aload 9` em 560 carrega a **vítima iterada**; `causeForsakenSonicBoomDamage` em 576; `getSonicDamageAgainst` em 584, multiplicação por `0.65f` em 587/590, `Math.ceil` em 592 e `LivingEntity.hurt` em 596 | O caminho é condicional; não são garantidos hits, número de vítimas, settlement ou permissões |

### Distinção causal essencial: alvo principal ≠ vítima iterada

Em `tick()`, **`astore_1` no offset 7 armazena o alvo principal** consultado via `getTarget()`. Já o caminho de varredura mantém uma entidade candidata em um slot local distinto, **`aload 9` no offset 560**, que é o destinatário de `LivingEntity.hurt`. Porém, no offset **583 ocorre `aload_1`**, imediatamente antes de `getSonicDamageAgainst(LivingEntity)` no **584**. Portanto, no caminho de Sonic Blast documentado, **a classificação de dano-base é consultada para o alvo principal**, e não recalculada contra cada vítima da área.

O helper `ForsakenEntity.getSonicDamageAgainst(LivingEntity)`, SHA-256 de método parseado `db47e82eebdb86724b6a71164ca563d0a75910bb143c16b944a5beb63f537d88`, consulta `WEAK_TO_FORSAKEN_SONIC_ATTACK`: retorna `45.0f` se a entidade **passada ao helper** pertence à tag, senão `4.0f`. No caminho direto (offset 116), ela é o alvo atingido. Na varredura (offset 584), ela é o **alvo principal** e o valor fica **`ceil(45×0.65)=30`** ou **`ceil(4×0.65)=3`** como parâmetro bruto solicitado a `hurt` para a vítima iterada, se todos os filtros e o ramo de execução forem satisfeitos.

Essa distinção invalida assumir que uma perk de dano em área pode obter a categoria de cada vítima só observando `getSonicDamageAgainst` no ponto 584. Qualquer proposta de escalonamento específico por vítima precisaria de contrato de hook independente, preservação de filtros, ausência de dupla aplicação e respeito à autoridade do provider.

### Movimento, animação, custos e limites

`ForsakenAttackGoal.start()` escolhe o estado `sonicEnqueued` e a animação consulta `ANIMATION_SONIC_ATTACK` / `ANIMATION_SONIC_BLAST`; `stop()` limpa flags e `setRunning(false)`. `knockBackAngle(LivingEntity,double,float)` delega a `ACCompat.knockback` com componentes construídos a partir de `yBodyRot`, `Mth.sin` e `Mth.cos`. Os valores de força aplicados e efeitos de colisão em mundo real não foram homologados. O goal não constitui um cast do Black Arcana: custos de mana, cooldown de feitiço, mana pool e progressão permanecem **não aplicáveis como contratos nativos provados**, em vez de assumir valores zero.

**Pendências:** sem certificado estático integral desta ficha, sem hook mutador certificado, sem QA física, sem prova de direito de interceptação, owner/PvP/protection, número de hits, noção exata de período, alcance de LOS ou semântica integral dos helpers herdados. Registro: `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Não elevar o contador de fichas certificadas por esta auditoria parcial.


## Animações, leitura de estado e knockback — helpers exatos 1.0.10

**Fonte:** [manifesto SHA-exato de 10 métodos](EXACT-FORSAKEN-HELPERS-1.0.10.json) e [CI da inspeção](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41087017470); publisher JAR `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Foram verificados os SHA-256 das classes `ForsakenAttackGoal` (`48cfdd6c370f68550d0d7af768466f99f330e8fd4f825a520411a1bc5d70fb55`), `ForsakenEntity` (`72981b25b3af251b3ee66b6ef16b650997359ff94673ad500256b2d1cee0cde1`) e `ACCompat` (`333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`). A inspeção cobre **somente métodos selecionados**, e não a IA herdada ou a execução completa em jogo.

### Gating de animações e movimento

- `ForsakenAttackGoal.tryAnimation(Animation)` verifica `ForsakenEntity.getAnimation()` (offset 4) contra `IAnimatedEntity.NO_ANIMATION` (7) e o branch `if_acmpne 23` (10). Quando a animação atual é `NO_ANIMATION`, chama `ForsakenEntity.setAnimation(Animation)` no offset 18 e retorna `true` (21–22); caso contrário retorna `false` (23–24). **Não significa que o novo ataque já atingiu o alvo.**
- `ForsakenAttackGoal.isMovementFrozen()` compara o estado de animação com `ANIMATION_LEFT_PICKUP` (offset 7) e `ANIMATION_RIGHT_PICKUP` (20), retornando booleano de pertencimento a essas duas animações. Não considerar **toda** animação uma imobilização.
- `ForsakenEntity.getAnimation()` lê o campo `currentAnimation`; `setAnimation(Animation)` escreve nesse mesmo campo. A existência dessa superfície **não prova** sincronização de rede por si só nem validação de servidor externo.
- `ForsakenEntity.hasSonicCharge()` obtém o booleano do accessor sincronizado `SONIC_CHARGE` via `SynchedEntityData.get`; `setSonicCharge(boolean)` encaminha o argumento a `SynchedEntityData.set`. São métodos de leitura/escrita **nativos**, não hooks de perks certificados.
- `ForsakenEntity.getSonarTarget()` lê `SONAR_ID`; devolve `null` quando o ID vale `-1`, ou chama `Level.getEntity(int)` nos demais casos. **SONAR_ID não equivale automaticamente a `Mob.getTarget()`**, usado no cálculo-base do Sonic Blast. Não confundir os dois caminhos para targeting.

### Dano corpo a corpo versus dano Sonic

`ForsakenAttackGoal.checkAndDealDamage(LivingEntity,double,float)` é uma superfície distinta dos dois callsites Sonic em `tick()`: consulta `hasLineOfSight` (5), distância e larguras das caixas; monta `DamageSources.mobAttack(ForsakenEntity)` (47), lê `Attributes.ATTACK_DAMAGE` e `AttributeInstance.getValue` (55–61), e chama `ACCompat.hurt(Entity,DamageSource,float)` (66). O fluxo do helper também consulta `RandomSource.nextInt(2)` e `nextInt(5)`, modifica `sonicEnqueued` em caminho condicionado e retorna um booleano. Estes símbolos **não** permitem transportar os valores `45.0f/4.0f` do Sonic Boom para a fórmula corpo a corpo, nem afirmar chance global de ataque só pelas constantes de randomização.

`ForsakenAttackGoal.knockBackAngle(LivingEntity,double,float)` usa `yBodyRot`, `Mth.sin`, `Mth.cos` e a constante angular `0.017453292f`, delegando a `ACCompat.knockback(LivingEntity,double,double,double)` (offset 35). O corpo desse wrapper contém a única invocação `LivingEntity.knockback(double,double,double)` (offset 5), sem branches ou modificadores próprios. Isso confirma a **delegação**, mas não os deslocamentos efetivos quando as resistências, colisões e outros sistemas do Minecraft intervêm.

### Índice exato de métodos

| Método compilado | Descritor JVM | SHA-256 do método parseado |
|---|---|---|
| `isMovementFrozen` | `()Z` | `d6066616df310a8d53b81481d1dde352801433f246df9767437050be2d3d0e54` |
| `tryAnimation` | `(Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;)Z` | `83c4dd2d1f87f654d3eeef7f4f6914b9360a52243cda2c9796a95d9581d4450b` |
| `checkAndDealDamage` | `(Lnet/minecraft/world/entity/LivingEntity;DF)Z` | `e730ecfd665bf10060e4592ff81c16c91ce472541de43c2418c947da80eb4825` |
| `knockBackAngle` | `(Lnet/minecraft/world/entity/LivingEntity;DF)V` | `8ef9a3e156ca8311e23507cde598367388a0ceffd92e5bf7fd33f09f003003fa` |
| `hasSonicCharge` | `()Z` | `22a775652346057551780b9ee73aa9be765fc324bfce53d6424bf2159d51a111` |
| `setSonicCharge` | `(Z)V` | `4af4bb0f7993dd0eebd895bd7c0f3a564eaa0ceb47bd33374ba6d2d27fe984cb` |
| `getSonarTarget` | `()Lnet/minecraft/world/entity/Entity;` | `0508d61342066d9992ae16df6934341f8555d96b2d2e49675644bf2f072c5188` |
| `getAnimation` | `()Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;` | `b377f6d233817c6c962ee3cce1af4f71ff4455d1dd019be76c8ec73addab4fbf` |
| `setAnimation` | `(Lcom/github/alexmodguy/alexscaves/citadel/animation/Animation;)V` | `6929fc02dcd16b3ac008164d88f69c74ec7f7f5213dc84d807526dfb305bbd85` |
| `knockback` | `(Lnet/minecraft/world/entity/LivingEntity;DDD)V` | `b5340a2a4a3dfaecf0a4f39700ee15b8c0134015b594734d0f22c5e0548095f7` |

### Consequências para perks e validação

O player poderá ter interesse em perks de seleção de alvo, knockback, estados de animação ou dano, mas **nenhum desses métodos configura, por si, contrato estável de mutação**. A responsabilidade pela IA, pelo `LivingEntity.knockback`, pelo estado sincronizado e pelo `LivingEntity.hurt` continua nos owners nativos. Não duplicar settlement, atribuição de dano ou cálculos de seleção de alvos. Pendente comprovar conflitos de IA, permissões, PvP, resistência a knockback, frequência e resultados de hit em QA real. **Contrato do Forsaken permanece ⚠️ parcial:** `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Nenhum contador é incrementado neste lote.


## Auditoria adicional — registro de IA e ciclo de vida (JAR 1.0.10)

**Evidência primária:** [manifesto SHA-exato do lifecycle](EXACT-FORSAKEN-LIFECYCLE-1.0.10.json) e [CI da coleta](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41093385042). O artefato publisher foi validado por SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, tamanho `75279314` bytes. As classes de `ForsakenAttackGoal` e `ForsakenEntity` são as mesmas já verificadas na auditoria da PR #964.

### Registro de goals e seleção de alvos

`ForsakenEntity.registerGoals()` faz **seis** chamadas diretas a `goalSelector.addGoal` (offsets 13, 29, 45, 64, 84, 100), incluindo `ForsakenAttackGoal` no construtor do offset **26** e seu registro no **29**, além de goals de flutuação, salto aleatório, passeio e observação. A mesma rotina registra **três** entradas em `targetSelector.addGoal` (125, 145 e 173). Os construtores compilados incluem `HurtByTargetGoal` (122) e duas variantes de `NearestAttackableTargetGoal` (142 e 170), sendo a última acompanhada da referência a `TARGETING` (164) e `ACCompat.targetSelector(Predicate)` (167).

As prioridades inteiras aparecem no JAR, mas **a ordenação de execução efetiva, a possibilidade de targets concomitantes, as condições de compatibilidade entre goals e o resultado da seleção em mundo não foram simulados**. Não confundir predicados de `targetSelector` com permissões de PvP/claim ou com o estado de sonar.

### Alcance de navegação e salto

- `ForsakenAttackGoal.canReach(LivingEntity)` invoca `PathNavigation.createPath(Entity,int)` no **9**, consulta `Path.getEndNode()` no **20** e trata referências nulas em branches **14/25**. O caminho final inclui a constante `3.0d` no offset **81** e um teste no **85**. Esse número não deve ser rotulado como alcance universal da habilidade Sonic.
- `startCleanJump()` escreve `jumpTarget` (offset **2**) e define `jumpEnqueued` no **7**, com `iconst_1` no **6**. O significado de “salto limpo” depende dos demais controles da IA; não equivale a um cast, teleport ou dash autorizado pelo Black Arcana.
- `findJumpTarget(LivingEntity,boolean)` avalia posição candidata com `ACCompat.isSolidRender` (offset **205**), `ACCompat.pathTypeStatic` (231), `ForsakenEntity.getPathfindingMalus` (234) e `Level.isUnobstructed` (258). O retorno tem caminho de posição candidata (266) ou `null` (268). Seleção espacial e sucesso de movimento permanecem condicionais, sem promessa de distância ou coordenada fixa.

### Sonic, efeitos visuais e estado da entidade

`ForsakenEntity.tick()` (817 instruções parseadas) referencia `ANIMATION_SONIC_ATTACK` (**806**) e `ANIMATION_SONIC_BLAST` (**898**) e consulta `getAnimationTick()` nas janelas de ambas. Também referencia as partículas `FORSAKEN_SONAR` (**843**) e `FORSAKEN_SONAR_LARGE` (**935**) e invoca `AnimationHandler.updateAnimations(Entity)` em **1679**. **Essas referências não convertem partículas, sons ou atualização de animação em dano adicional**: os dois callsites `LivingEntity.hurt` do Sonic continuam no `ForsakenAttackGoal.tick()` (manifesto anterior).

`ForsakenEntity.setAnimationTick(int)` grava o campo `animationTick` (offset **2**). `setSonarId(int)` escreve o accessor sincronizado `SONAR_ID` via `SynchedEntityData.set`; `setLeaping(boolean)` escreve `LEAPING` da mesma forma. São pontos nativos de estado, **não hooks públicos mutadores certificados para perks**.

### World safety — caminho de destruição separado do Sonic

`ForsakenEntity.customServerAiStep()` contém uma rotina distinta que verifica `ACPlatform.canEntityGrief(Level,Entity)` (**40**), `ACCompat.canEntityDestroy` (**153**), `EventHooks.onEntityDestroyBlock` (**175**) e solicita `Level.destroyBlock` (**189**), com branches de interrupção. Essa presença prova um **caminho condicionado de destruição de blocos pela IA** e é relevante ao planejamento de proteção de mundo. **Não** comprova que Sonic Blast destrói blocos; o método não é um hook do runtime Black Arcana, e a política `WorldEffectPolicy` do Black Arcana não assume automaticamente autoridade sobre efeitos nativos de terceiros.

### Métodos e identidades verificadas

| Método | Descriptor JVM | SHA-256 das instruções parseadas |
|---|---|---|
| `canReach` | `(Lnet/minecraft/world/entity/LivingEntity;)Z` | `2dd5166c68f7f909aadd4288303b7ad7aaca0e15823d38a3c79d9fc0633ef8f0` |
| `startCleanJump` | `()V` | `da3033d7ee48849e4035731c14dda7c23914271a97b44325197d10327eb68466` |
| `findJumpTarget` | `(Lnet/minecraft/world/entity/LivingEntity;Z)Lnet/minecraft/core/BlockPos;` | `198642c7720d30d8a93062cf893a7d2e4d3147e41817dc211279c19e8a4f43a8` |
| `registerGoals` | `()V` | `c9f73f7eda5fa9b0368ccccb497b35be1395580889fb3bca9106cdf62578365e` |
| `tick` | `()V` | `733efd62558f45ce4d8390e43fb09baff389490f8d96f9be709952a6a284341f` |
| `customServerAiStep` | `()V` | `abdd554815865a9cda9fc13f68df7a4a274d450fda04d5f3aa06027478ae79fb` |
| `setSonarId` | `(I)V` | `85d993ec2e0a26d21e726f705645dfbf86b97a18808994ceb6c1e62d7e073f30` |
| `setAnimationTick` | `(I)V` | `4a9aafe463d849f469ef90d0d5e4fe54b08b521d9424e16b3b71661740d71d2a` |
| `setLeaping` | `(Z)V` | `9ce582d416a6b73fa739ad2d2ddad336628bb805798ba831920149baf4d68dd6` |

**Limites persistentes:** o estudo registra referências simbólicas e branches de nove métodos, sem reconstrução de CFG completo, sem execução de goals no mundo, sem medir quantidade de hits, sem verificar permissões, sem QA física e sem hook seguro para alterar targeting, alcance, animações ou dano. `NOT_CERTIFIED` / `mutating_hook=NOT_VERIFIED` / `physical_qa=NOT_TESTED` / `NO_MUTATION`. Não promover o contrato estático integral da ficha, nem acrescentar nova magia ao catálogo por esta auditoria.


## Temporização do Sonic e estados próprios — auditoria 1.0.10

**Evidência:** [manifesto de ticks e declarações NBT](EXACT-FORSAKEN-TIMING-1.0.10.json) extraído do [workflow CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41096171833) contra o JAR instalado (SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`). Os dois métodos `tick()` preservam seus hashes compilados anteriores: `ForsakenAttackGoal.tick` = `1fb8ecdd23c6c76d836ee25a4176f788163ef1226220a142a40e5f48d4df8abe` e `ForsakenEntity.tick` = `733efd62558f45ce4d8390e43fb09baff389490f8d96f9be709952a6a284341f`.

### Gating temporal, dano e duração

- O contador interno `attemptSonicDamageIn` é lido em **59**; se positivo, passa pelo decremento `getfield 67`, `iconst_1 70`, `isub 71`, `putfield 72`. Na transição para zero, o caminho de disparo direto também verifica linha de visão. Uma passagem de `Goal.tick()` não garante um tick efetivo em toda atualização de mundo: o escalonador nativo ainda é autoridade.
- Para `ANIMATION_SONIC_ATTACK`, `getAnimationTick` é comparado com **10** (`bipush 325`, branch 327) e **30** (337, branch 339). Quando `attemptSonicDamageIn` não é positivo (branch 346), um caminho escreve o resultado de um cálculo que contém literal double `0.20000000298023224d` e `Math.ceil` nos offsets **351/355/359**. A origem e os limites do operando local não foram formalmente certificados: **não** chamar essa expressão de cooldown global.
- O flag `sonicEnqueued` pode ser limpo após `getAnimationTick > 30` na animação direcionada (`getAnimationTick 366`, branch 371, `putfield 376`) ou após tick **40** no caminho do Sonic Blast (`getAnimationTick 607`, branch 612, `putfield 617`). Essas são transições locais de estado, não garantias de duração efetiva da animação.
- A varredura Sonic Blast depende de `ANIMATION_SONIC_BLAST` e do tick de animação entre **10 e 30, inclusive** (`getAnimationTick` em 399/411 e branches 404/416). Exige ainda `animationTick % 5 == 0` (`getAnimationTick 423`, `iconst_5 426`, `irem 427`, `ifne 428`). Isso define **momentos potenciais para processamento de área**, não número fixo de hits; filtros de aliados, tags, distância, aceitação do `LivingEntity.hurt` e agendamento do goal continuam aplicáveis.
- Quando `hasSonicCharge()` é verdadeiro (consulta em 1097) e `sonicEnqueued` está falso (1104/1107), há ramo que define `sonicEnqueued=true` (**1112**) e chama `setSonicCharge(false)` (**1120**). A carga é estado do provider, sem equivalência automática a mana, custos de cast ou perk.

### Estado sincronizado não equivale a NBT persistido

O método `ForsakenEntity.defineSynchedData(SynchedEntityData.Builder)` (SHA-256 parseado `a0a8ea7ca18a20a07a12bc39710ea22447264a4f359767c809c7044fb1cacde2`) chama o método de `Monster` e inicializa `LEAPING = false` (offsets 18/21/25), `SONIC_CHARGE = false` (30/33/37) e `SONAR_ID = -1` (54/57/61). Esses valores são **defaults no nascimento da entidade**. O getter próprio `getAnimationTick()` (SHA `d2f19727526eec9cd6ae71b7d2ce80ee9d587192c88551b7e92564bf446149ae`) lê o campo local `animationTick`.

A classe `ForsakenEntity` da build 1.0.10 **não declara** métodos próprios com as assinaturas exatas `addAdditionalSaveData(CompoundTag):void` e `readAdditionalSaveData(CompoundTag):void`. **Isso não prova ausência de persistência em disco:** superclasses, outros mixins e mecanismos de saves/entidades não foram auditados. Tampouco comprova recuperação dos flags sincronizados após troca de dimensão, reinício ou unload.

**Limites:** análise estática de métodos selecionados, sem reconstruir CFG inteiro, sem medir tempo real/hitcount, sem teste multiplayer ou física do modpack, nem hook mutador certificado. `NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION`. Nenhuma nova ficha ou certificação global é criada.


## Seleção por tag e entrada/saída do goal — contrato delimitado 1.0.10

**Evidência:** [snapshot reproduzível dos cinco métodos](EXACT-FORSAKEN-TARGETING-1.0.10.json), validado pela [auditoria de targeting](../../../../../.github/workflows/alexscaves-1010-forsaken-target.yml). JAR publisher de 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O snapshot sela **52 instruções em cinco métodos**, com descritores, hashes, branches e janelas simbólicas; a fonte 1.1.1 não fornece os parâmetros desta build.

### Elegibilidade do predicado e adapter

- `ForsakenEntity.lambda$static$0(LivingEntity)` consulta `getType()` no offset **1**, `builtInRegistryHolder()` em **4** e a tag `FORSAKEN_IGNORES` em **7**, seguida de `Holder.Reference.is(TagKey)` em **10**. O branch `ifne 20` (**13**) retorna falso para uma entidade cujo tipo pertence à tag; o outro ramo retorna verdadeiro (**16–21**). Esta seleção não sela a ligação de bootstrap entre a lambda e o campo `TARGETING`; o registro de goals lê esse campo, como documentado acima. A própria lambda não contém verificação de vida, distância, linha de visão ou permissões de PvP/claims.
- `ACCompat.targetSelector(Predicate)` contém somente `aload_0` (**0**) e `areturn` (**1**): **devolve a mesma referência recebida**, sem adicionar filtros ou wrapper próprio. Essa identidade não estabelece a política final de `NearestAttackableTargetGoal`, de seu construtor ou de outras camadas nativas.
- A tag de exclusão pode receber alterações de datapacks. O predicado de aquisição não substitui a filtragem por vítima no Sonic Blast: o caminho de dano continua com suas verificações de aliança, distância e tag, documentadas anteriormente. Uma perk que pretenda trocar o tipo de alvo precisaria preservar essas duas etapas e o escalonamento da IA; nenhum hook seguro foi homologado.

### Ativação, inicialização e encerramento

| Método próprio | Fluxo confirmado pelas instruções | Limite para integração |
|---|---|---|
| `canUse()` | `getTarget()` em **4**, branch nulo em **9**, `isAlive()` em **13** e branch falso em **16**; retorna verdadeiro somente para referência não nula e viva nesse método | Não verifica diretamente LOS, alcance, tag ou cooldown; guards herdados, prioridades, concorrência e seleção final não foram executados |
| `start()` | Zera `navigationCheckCooldown` (**1–2**), `jumpEnqueued` (**6–7**) e `attemptSonicDamageIn` (**27–28**); grava em `sonicEnqueued` (**23**) o retorno de `RandomSource.nextBoolean()` (**18**) | O booleano inicial não equivale à chance efetiva de um Sonic acertar nem permite inferir custo de mana ou período global |
| `stop()` | Zera `jumpEnqueued` (**1–2**) e `sonicEnqueued` (**6–7**); chama `setRunning(false)` (**14–15**) | O corpo próprio não zera `attemptSonicDamageIn`, não limpa o alvo e não redefine animação; isso não demonstra persistência após nova inicialização nem define quando o escalonador cancela o goal |

### Identidades seladas e fronteira de execução

Classes auditadas: `ForsakenEntity.class` SHA-256 `72981b25b3af251b3ee66b6ef16b650997359ff94673ad500256b2d1cee0cde1`; `ACCompat.class` `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b`; `ForsakenAttackGoal.class` `48cfdd6c370f68550d0d7af768466f99f330e8fd4f825a520411a1bc5d70fb55`.

| Método | Descritor JVM | SHA-256 das instruções parseadas |
|---|---|---|
| `ForsakenEntity.lambda$static$0` | `(Lnet/minecraft/world/entity/LivingEntity;)Z` | `cfa4a5d278a63d29041f8af87ec32c148db680704cadaca1df546de4d46ea865` |
| `ACCompat.targetSelector` | `(Ljava/util/function/Predicate;)Ljava/util/function/Predicate;` | `b10a5989478262171604d8f1692ba5ad5da3f4d13f96e2ab39f78e9c57e61ca1` |
| `ForsakenAttackGoal.canUse` | `()Z` | `6309c2f6f04ccaa8100eb422ad81cdd6f5ba1b05ff0a973157b378a546803661` |
| `ForsakenAttackGoal.start` | `()V` | `8e2fdcc7854b68ac0ad8d5b4c04b16b82aa8183c47016eb03d549cb42a816797` |
| `ForsakenAttackGoal.stop` | `()V` | `eca88a14990b3181b0622017a017334a9c1b23339bd8cdc51440e318258198b7` |

**Estado mantido:** `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. A prova delimita o corpo dos cinco métodos próprios; não reconstrói a seleção herdada, o agendamento de goals, os valores finais de tags, resultados multiplayer ou permissões. Não prova frequência de ataques, número de hits, dano líquido nem segurança para mutar range, alvo ou animação. Nenhuma nova ficha, raiz mágica ou certificação é contabilizada nesta etapa.
