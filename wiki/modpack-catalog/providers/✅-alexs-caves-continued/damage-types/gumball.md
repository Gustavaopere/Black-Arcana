# Gumball — tipo de dano `alexscaves:gumball` (1.0.10)

**Estado de catalogação:** ⚠️ `RESOURCE_JSON_VERIFIED` (recurso SHA-exato). **Contrato técnico estático para perks:** ⚠️ `NOT_CERTIFIED`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`.

## Proveniência e identidade

- **Provider / mod ID:** `Alex's Caves Continued` / `alexscaves`.
- **Versão do artefato:** `alexscaves-1.0.10-neoforge+1.21.1.jar` (Minecraft 1.21.1).
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`.
- **JAR SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Resource ID exato:** `alexscaves:gumball`.
- **Caminho ZIP:** `data/alexscaves/damage_type/gumball.json`.
- **SHA-256 do JSON:** `70b62fe5851e5cbbb630f8dfb0202018fe7184f99c4b8bb19a98e68c4ed83687`.
- **Manifesto verificável:** [snapshot dos recursos](EXACT-RESOURCE-MANIFEST-1.0.10.json) e [auditoria da CI](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).

## Campos JSON confirmados no artefato

| Campo | Valor literal do recurso | Limite de interpretação |
|---|---|---|
| `message_id` | `gumball` | Chave de mensagem; não é sinônimo do registro nem classe de implementação |
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
- **Método:** `ACDamageTypes.causeGumballDamage`.
- **Descritor JVM:** `(Lnet/minecraft/core/RegistryAccess;Lnet/minecraft/world/entity/Entity;)Lnet/minecraft/world/damagesource/DamageSource;`.
- **Campo de DamageType lido:** `GUMBALL` (offset `19`).
- **Construtor de DamageSource referenciado:** `Method com/github/alexmodguy/alexscaves/server/misc/ACDamageTypes$DamageSourceRandomMessages."<init>":(Lnet/minecraft/core/Holder$Reference;Lnet/minecraft/world/entity/Entity;I)V`.
- **Parâmetros da factory:** `RegistryAccess` e `Entity` — não comprova autoria final.
- **Referências `invokestatic` encontradas:** 1 em 1 classes. Isso não representa quantidade de hits por ataque.

| Classe chamadora | Método chamador | Descritor JVM | Offset | Opcode |
|---|---|---|---:|---|
| `com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.class` | `protected void onHitEntity(net.minecraft.world.phys.EntityHitResult)` | `(Lnet/minecraft/world/phys/EntityHitResult;)V` | 86 | `invokestatic` |

**Limites:** as invocações são referências estáticas no bytecode exato; não demonstram execução, alcance, área, cooldown, fórmula de dano, filtros de alvo, persistência, autoridade/attribution, proteção PvP nem segurança de intercepção. Chamadas indiretas, mixins, reflexão, datapacks e comportamento do modpack não estão comprovados. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NOT_CERTIFIED`**. Black Arcana e RPG Skill Tree devem preservar o settlement nativo, evitando processamento duplicado e aplicando `NO_MUTATION` sem contrato seguro.


## Auditoria do impacto e ricochete — JAR físico 1.0.10

**Novo escopo comprovado:** `SHA_EXACT_1010_GUMBALL_SELECTED_BYTECODE_ANCHORS_ONLY`, a partir da execução [Gumball bounded probe](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41216742769), com o mesmo artefato SHA-1/SHA-256 acima. O [manifesto de regressão](../EXACT-GUMBALL-IMPACT-1.0.10.json) fixa **17 métodos selecionados**, seus descritores e hashes da extração `javap`, mais âncoras de offsets selecionados em seis métodos. Não é um manifesto de todos os consumidores nem auditoria de fluxo total.

A classe compilada auditada é `com/github/alexmodguy/alexscaves/server/entity/item/GumballEntity.class`, SHA-256 `343cc816bcb545241205a6dd1f94c34c37990273aa360bfc82c9fb9485f0f535`. O `GumballEntity` é uma entidade de projétil; **não** se deve confundir seu `DamageSource` com o ataque que originou a entidade, nem um evento visual com uma aplicação de dano.

| Campo de interesse para perks | Evidência delimitada no método compilado | Implicação/limite |
|---|---|---|
| Origem e autoria | `onHitEntity(EntityHitResult)` lê `getOwner()` (offset 6); a chamada `causeGumballDamage(RegistryAccess, Entity)` no offset **86** recebe esse owner. | Autoridade e atribuição dependem do owner efetivo da instância. O manifesto não prova restauração de owner nas entidades-filhas. |
| Dano | O método lê `getDamage()` (11), constrói o `DamageSource` (86) e invoca `Entity.hurt(DamageSource,float)` (139). | É uma solicitação de dano; não comprova dano efetivamente aceito, resistência, crítico, morte nem proc resultante. Os valores iniciais do `getDamage()` dependem do produtor, ainda pendente. |
| Filtro de alvo | Antes do dano há um caso especial `GumbeeperEntity`/`LicowitchEntity.isFriendlyFire` (offset 71). O caminho de dano também compara `Entity.is` (97) e `isAlliedTo` (105, 113). `onHit(HitResult)` consulta `ownedBy` (77) e `hitEntityIds` (94). | Alianças, vítima anterior e owner importam. Uma perk não pode remover esses filtros apenas ampliando a seleção de alvo. A elegibilidade global, inclusive PvP e dependências, não está homologada. |
| Ricochete e aquisição de alvo | `onHit` invoca `bounceFromDirection(Direction)` para colisão com bloco (54) e no caminho de impacto de entidade (168). `bounceFromDirection` consulta `targetsOnBounce()` (39), `getOwner()` (46), `getEntitiesOfClass(LivingEntity, AABB)` (101), `hitEntityIds.contains` (167) e duas medidas `distanceTo` (183, 189). A construção da caixa usa componentes **−10 a +10** (offsets 72–92). | A caixa de busca não prova raio esférico de acerto, linha de visão nem alcance efetivo de ataque. O consumidor e o filtro devem ser preservados ao projetar perks de targeting ou homing. |
| Limite de ricochetes e velocidade | O método consulta `getBounces/getMaximumBounces`, incrementa `setBounces`, contém `discard` em caminhos de limite (242 e 445) e escreve `setDeltaMovement` (287 e 458). Há `Vec3.scale(0.800000011920929d)` na rota de perseguição e `bounceSoundCooldown = 5` no offset 298. | `5` é cooldown **de som**, não cooldown de lançamento. `0.8` é literal convertido de float, não multiplicador global de todos os movimentos. |
| Divisão em projéteis | Após `splitsOnHit()` (144), `onHitEntity` contém um laço delimitado pelo literal **3** (155–156). O caminho usa `ACCompat.createEntity` (174), `setDeltaMovement` (284), `setSplitsOnHit(false)` (290), `setDamage` (299), copia flags `targetsOnBounce`/`isExplosive`, atualiza `setMaximumBounces` e solicita `Level.addFreshEntity` (335). | São até três **tentativas de criação** por execução desse ramo, não três impactos confirmados. Não há chamada direta `setOwner` nessa rotina selecionada; investigar o produtor e a propagação real de autoria antes de perks de multiplicação ou bônus por kill. |
| Explosão e tempo | `tick()` contém `getBounces/getMaximumBounces` (183/187), contador `explodeProgress` e comparação com literal **20.0f** (197/200), guard `isClientSide` (207/210), e invoca `Level.explode` (242) com força **2.0f** e `ExplosionInteraction.NONE` (237–239), seguido de `discard` (247). | O literal 20 refere-se ao ramo do progresso da explosão, não ao tempo de vida geral de todo projétil. `NONE` é o modo nativo solicitado; não autoriza bypass do `WorldEffectPolicy` do Black Arcana. |
| Persistência local | `addAdditionalSaveData(CompoundTag)` salva diretamente a chave `Color` via `putInt`; `readAdditionalSaveData` lê `Color` por `ACCompat.getInt`. Ambos chamam os métodos da superclasse. | Esses overrides não demonstram persistência de dano, flags, contagem de ricochetes, lista de vítimas ou autoria em save/reload. Dados sincronizados e restauração devem ser auditados separadamente. |
| Custo, cooldown e emissão | Os métodos selecionados da entidade não demonstram o custo de munição, cooldown do item produtor, quantidade de disparos, velocidade inicial ou balanceamento da arma. | **NÃO VERIFICADO**; requer auditoria dos produtores e registries exatos, sem usar parâmetros da fonte 1.1.1 como autoridade para 1.0.10. |

### Limites para integração

A auditoria identifica métodos e argumentos no binário exato, mas não reconstrução completa do fluxo de controle com exceções, mixins, datapacks, chamadas indiretas ou execução física. Os offsets e literais acima não autorizam inferir segurança de alterar `Entity.hurt`, `getOwner`, `SynchedEntityData`, `onHit` ou `Level.explode`.

**Estado após este checkpoint:** `NOT_CERTIFIED` para o contrato completo da ficha, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Sem nova raiz mágica, sem promoção de Stage e **sem incremento** em 22/29 fichas do Alex’s Caves ou 160/2341 certificações estáticas globais. Próximos requisitos: identificar produtores, parâmetros iniciais e owners; fechar os sete campos do contrato; validar o manifesto e regressões antes de promover esta ficha no índice.


## Produtores nativos do Gumball — evidência exata 1.0.10

A [auditoria SHA-exata dos produtores](../EXACT-GUMBALL-PRODUCERS-1.0.10.json) usa o mesmo JAR publisher 1.0.10 verificado acima. O teste de referências diretas varreu classes de servidor contendo `GumballEntity` ou `GUMBALL` no pool de constantes, encontrou **nove classes candidatas** e preservou **três classes com quatro métodos selecionados**, além de duas classes de registry classificadas somente como suporte. O manifesto sela hashes das classes e dos métodos, mais **17 pontos de referência**; a [execução CI da investigação](https://github.com/Gustavaopere/Black-Arcana/actions/runs/41221362508) passou. Não se trata de enumeração de todos os produtores indiretos, reflexão, mixins ou runtime.

| Fonte nativa e método | Instruções verificadas | Implicação para perks |
|---|---|---|
| `ShotGumItem.acInventoryTick(ItemStack,Level,Entity,boolean)` | Cria `GumballEntity(Level,LivingEntity)` no offset **316**, ajusta `setPos` (427), `setTargetsOnBounce` (434), `setSplitsOnHit` (441), `setExplosive` (448), `shootFromRotation` (480), `setMaximumBounces` (487) e `setDamage` (495). O trecho contém `Level.isClientSide` (499) e `addFreshEntity` (508), e uma comparação com literal `2` no laço observado. | O equipamento é um produtor efetivo de parâmetros de projétil. O literal do laço não prova duas entidades inseridas em toda ativação. Requer auditoria da origem das flags, custo, cadência e valores usados em cada setter. |
| `GumbeeperEntity.shootGumball(LivingEntity)` | Cria `GumballEntity` (80), ajusta posição (88), invoca `shoot(DDDFF)` (265), solicita `Level.addFreshEntity` (274), consulta `isCharged` (279) e nos ramos seguintes usa `setMaximumBounces` (289) e `setDamage` (307, 326). O ramo carregado apresenta o literal inteiro `10` para `setMaximumBounces`; a construção de `shoot` usa `getDifficulty().getId()` e constantes compiladas `14` e `4`. | Distinguir os parâmetros do disparo do mob dos parâmetros da arma do jogador. Os setters de dano usam `Attributes.ATTACK_DAMAGE`, com literal `2f` no ramo carregado; não transferir fórmula ou spawn count sem verificar as instruções intermediárias. |
| `GumbeeperEntity.tick()` | Cria `GumballEntity` (385), atualiza posição/movimento (436/518), solicita `Level.addFreshEntity` (527) e, condicionado a `isCharged` (532), chama `setMaximumBounces(10)` (542) e `setDamage` (560/579). Há uma chamada `RandomSource.nextInt(5)` no caminho de repetição (367). | Uma chamada probabilística com limite `5` não significa cinco disparos garantidos. O caminho de morte/explosão do Gumbeeper não deve ser confundido com `shootGumball`. |
| `ACDamageTypes.causeGumballDamage(RegistryAccess,Entity)` | Lê `GUMBALL` (19); a chamada `GumballEntity.onHitEntity` em offset 86 já está catalogada. | É a fábrica de `DamageSource` compartilhada, não um quarto produtor de projétil e não mais um tipo de dano. |

**Relação de autoria:** os três métodos de emissão observados chamam o construtor `GumballEntity(Level,LivingEntity)`; isso é uma pista de ownership na origem. Os efeitos efetivos desse construtor, a restauração de autoria, a criação dos descendentes após `splitsOnHit` e a identidade de eventos para evitar múltiplas perks ainda requerem validação de consumidores e de ciclo de vida.

**Limites da busca:** `ACEntityRegistry` e `ACItemRegistry` aparecem apenas como registries de suporte, não prova de disparo. As outras candidatas sem chamadas simbólicas selecionadas não são afirmadas como irrelevantes. A ausência de um match não demonstra ausência de emitters indiretos.

**Status:** este checkpoint **não** sela ainda os sete campos do contrato completo de Gumball. Continuam `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`; nenhum aumento dos contadores, nenhuma raiz mágica nova ou promoção de Stage. Próximo fechamento deve ligar guardas completos, formulação dos valores iniciais, herança de owner/atribuição e persistência ao contrato de impacto, validar a versão instalada e só então alterar índices.


## Estado sincronizado, munição e temporização — JAR exato 1.0.10

**Evidência estática adicional:** [EXACT-GUMBALL-STATE-1.0.10.json](../EXACT-GUMBALL-STATE-1.0.10.json) sela hashes de **52 métodos selecionados**, três classes e **105 âncoras de offsets críticos** em 19 recortes, a serem confrontados com o JAR publisher pela CI. Não é certificação de hook/perk, nem reprodução dos métodos completos.

### `GumballEntity`: valores padrão e autoria

| Campo | Valor e prova compilada | Fronteira de integração |
|---|---|---|
| `MAXIMUM_BOUNCES` | `5`, `defineSynchedData` offsets 1/4 | Pode ser sobrescrito pelo emissor |
| `BOUNCES` | `0`, offsets 13/16 | Contador de ricochetes, não cooldown |
| `COLOR` | `0`, offsets 25/28; construtor chama `RandomSource.nextInt(12)` e `setColor` | Cor visual não constitui tipo de dano |
| `DAMAGE` | `2.0f`, offsets 37/40 | Valor inicial; ShotGum usa `setDamage(4.0f)` |
| `TARGETS_ON_BOUNCE` | `false`, offsets 49/52 | Configuração nativa de targeting |
| `SPLITS_ON_HIT` | `false`, offsets 61/64 | Filhos não surgem por padrão |
| `EXPLOSIVE` | `false`, offsets 73/76 | A explosão exige flag do produtor |
| Owner | Construtor `GumballEntity(Level,LivingEntity)` invoca `setOwner(Entity)` no offset 18 | Demonstra atribuição na emissão primária; não prova owner em descendentes |
| Gravidade | `getDefaultGravity()` retorna double `0.07999999821186066` | Constante compilada, não trajetória medida |
| NBT específico | `addAdditionalSaveData` e `readAdditionalSaveData` salvam/leem diretamente `Color`, mais chamadas à superclasse | Não presumir que os outros seis campos sincronizados sobrevivam ao save/reload |

Os sete atributos acima usam `SynchedEntityData` com setters/getters próprios. Esse armazenamento não constitui uma API autorizada para perks. A emissão e a mutação permanecem sob autoridade do provider.

### `ShotGumItem`: custos e tempo próprios

| Superfície | Prova no binário | Limites |
|---|---|---|
| Carregador | `getGumballsLeft` lê a tag `Gumballs`, retornando **4** se não houver tag (offset 27) | Não é o inventário de munição do mob |
| Disparo | `isShooting`, `setShooting`, `getShootTime` e `setShootTime` usam tags `Shooting`/`ShootTime`; `acInventoryTick` compara o contador com literal **5** (83–89) | A comparação não homologa cadência total ou cooldown de casting |
| Uso mantido | `getUseDuration` retorna **72000** | Limite declarado de duração da interação, não cooldown de 72.000 ticks |
| Recarga | `use` invoca `findAmmo(Player)` (45), verifica criativo e stack vazia (51/58), pode chamar `ItemStack.shrink(1)` (67) e `setGumballsLeft(...,4)` (80/81) | Um ramo nativo pode consumir **uma unidade de item para repor quatro cargas**, condicionado aos guards; custo transacional Black Arcana não verificado |
| Emissão | `acInventoryTick` cria `GumballEntity(Level,LivingEntity)` (316), escreve `setTargetsOnBounce` (434), `setSplitsOnHit` (441), `setExplosive` (448), `shootFromRotation` (480), `setMaximumBounces` (487) e `setDamage(4.0f)` (492/495) | Dano solicitado não garante quatro pontos líquidos após mitigação |
| Lado servidor | `Level.isClientSide` (499) guarda a chamada `addFreshEntity` (508) | Não autoriza criar segundo emitter Black Arcana |
| Encantamentos do disparador | `TARGETED_RICOCHET` (138/141), `TRIPLE_SPLIT` (155/158), `EXPLOSIVE_FLAVOR` (172/175), `BOUNCY_BALL` (190/193) são consultados via `ACCompat.enchantLevel` | Variantes/níveis e compatibilidade precisam de contratos de enchantment independentes |
| Persistência de estado | As tags do item incluem `PrevShootTime`, `ShootTime`, `PrevCrankAngle`, `CrankAngle`, `Gumballs` e `Shooting` | ItemStack e NBT de projétil são domínios separados |

A avaliação dos perks deve identificar o valor aplicado ao projétil, a quantidade de emissões e a unidade de munição realmente debitada, sem duplicar hit, charge ou consumo.

### `GumbeeperEntity`: flags, disparo e save

- `defineSynchedData` inicia `GUMBALLS_LEFT=6`, `CHARGED=false` e `POSSESSOR_LICOWITCH_ID=-1`, além de `EXPLODING`, `ATTACK_CHARGE` e `SHOOTING`. Esses valores são do mob.
- `canShootGumball` consulta `getGumballsLeft`, `dialRot` (literal **450.0f**) e `getAttackCharge` (comparação com `1.0f`). Esses gates pertencem ao ciclo de ataque do mob e não à arma do jogador.
- `shootGumball` e `tick` são emissores distintos. A flag `isCharged` modifica seus ramos; aparecem `setMaximumBounces(10)` e `Attributes.ATTACK_DAMAGE`, com literal `2.0f` na variante carregada. A fórmula efetiva depende das instruções intermediárias e do ramo escolhido.
- Os overrides de `addAdditionalSaveData` e `readAdditionalSaveData` persistem diretamente `Charged` (boolean) e `Gumballs` (int), além da superclasse. Não provam persistência de charge intermediária, alvo nem projéteis ativos.
- `canAttack` consulta o possessor Licowitch e `isFriendlyFire`; `hasLineOfSightToGumballHole` usa `Level.clip` com `COLLIDER` e `Fluid.NONE`, contendo literal `128.0d` no cálculo de distância. Esse valor não deve ser anunciado como alcance efetivo de Gumball.

### Fronteiras ainda pendentes

A prova é SHA-exata, porém não reconstrói integralmente CFG/branches, nem confirma aceitação de `Entity.hurt`, execução de todas as variantes de enchantments, persistência real em save/reload ou herança de owner nos descendentes. Explosões nativas em `Level.explode` e novos efeitos Black Arcana exigem contratos de world safety distintos. O RPG Skill Tree continua restrito a progressão/atributos/perks por boundary verificada.

**Estado:** `NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED` e `NO_MUTATION`. Sem certificação integral, o índice permanece em **22/29** para Alex’s Caves e **160/2341** para contratos técnicos estáticos globais. Próximo fechamento: validar fluxo completo dos produtores, propagação de autoria, limites dos encantamentos e os sete campos técnicos individuais, antes de promover Gumball.
