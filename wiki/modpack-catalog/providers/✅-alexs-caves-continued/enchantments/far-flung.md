# Far Flung — impulso inicial do Candy Cane Hook (1.0.10)

**Estado:** ✅ **contrato técnico estático individual certificado no escopo publisher 1.0.10**, com leitura de **27 métodos JVM completos, 1.600 instruções e 182 branches diretos**, bootstrap da seleção de entidades, fórmula do vetor inicial, autoria, dano solicitado, reeling e persistência. **Não equivale a perk executável ou QA física.** `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY` · `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · `NO_MUTATION`.

**Identidade:** `alexscaves:far_flung` modifica o lançamento da entidade `CandyCaneHookEntity` pelo item `alexscaves:candy_cane_hook`. É um modificador de equipamento/mobilidade nativo, **não** uma nova magia Black Arcana, uma raiz de cast adicional ou um novo tipo de dano.

## 1. Proveniência e versão

| Objeto | Evidência da release exata |
|---|---|
| Provider | Alex's Caves Continued / mod ID `alexscaves` |
| Modpack | `alexscaves-1.0.10-neoforge+1.21.1.jar`, [modlist do RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), entrada #019 |
| Runtime | Minecraft 1.21.1; NeoForge; Java 21 |
| Publisher JAR | **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Encantamento | `alexscaves:far_flung` / `data/alexscaves/enchantment/far_flung.json`; SHA-256 `a7f48d6ad8eca7a883b3d930313d6962334b0b43a0d6722cb2e60831e9ed8e8c` |
| Tag de item | `data/alexscaves/tags/item/enchantable/candy_cane_hook.json`; SHA-256 `b1d1990dd02fec11c14976f0f0a893e30b6c25e443efc013428cbdd4ef334310` |
| Item | `com/github/alexmodguy/alexscaves/server/item/CandyCaneHookItem.class`; SHA-256 `d999251e494c45420e58881181e9d67757247b6865dc4a547bf0da8a46cf8e44` |
| Consumidor | `com/github/alexmodguy/alexscaves/server/entity/item/CandyCaneHookEntity.class`; SHA-256 `e590bb67ea2b594861a30b05a5099fbd5eafe2920ff867883aaa6fd7cec478f8` |
| Registry de encantamentos | `ACEnchantmentRegistry.class`; SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |

**Evidência anterior preservada:** [EXACT-FAR-FLUNG-1.0.10.json](../EXACT-FAR-FLUNG-1.0.10.json), produzida por [sonda SHA-exata](../../../../../docs/qa/alexscaves_1010_far_flung_probe.py), [testes negativos](../../../../../docs/qa/alexscaves_1010_far_flung_probe_test.py) e [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-far-flung.yml). A sonda anterior verifica SHA-1/SHA-256/tamanho do JAR e guarda recursos, classes, digests de métodos completos e janelas localizadas de `javap -c -p -s`. A [auditoria ampliada](../../../../../docs/qa/alexscaves_1010_far_flung_causal_audit.py), os [testes negativos](../../../../../docs/qa/alexscaves_1010_far_flung_causal_cards_test.py), o [selo individual](../EXACT-FAR-FLUNG-CAUSAL-1.0.10.json) e a [CI dedicada](../../../../../.github/workflows/alexscaves-1010-far-flung-causal.yml) conferem **17 métodos com hash de corpo preexistente e 10 consumidores adjacentes por classfile SHA-exato**, 1.600 instruções, 182 branches e o bootstrap `Entity.isAlive`. A auditoria é estática/read-only, não decompilação ou QA em modpack. O código público de 1.1.1 permanece apenas corroboração, sem alegação de paridade.

A fonte pública [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara versão **1.1.1**. Seus arquivos **não** substituem os bytes publisher 1.0.10; os números abaixo derivam do manifesto extraído do artefato exato. O JAR não foi incorporado ao repositório.

## 2. JSON do encantamento — exato 1.0.10

| Campo embarcado | Valor verificado |
|---|---|
| `description.translate` | `enchantment.alexscaves.far_flung` |
| `supported_items` | `#alexscaves:enchantable/candy_cane_hook` |
| `weight` | **10** — peso de encantamento, não probabilidade de acerto ou puxão |
| `max_level` | **3** |
| `min_cost` | `base=1`, `per_level_above_first=6` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | **1** |
| `slots` | `["mainhand"]` |
| `exclusive_set` | Não declarado neste JSON |

A tag física contém `values=["alexscaves:candy_cane_hook"]`. A sonda também comprovou os símbolos compilados `FAR_FLUNG` e `far_flung` na classe registry. `slots=mainhand` é metadado da definição do encantamento; não demonstra que a consulta de nível de um item alterado externamente na mão secundária é automaticamente bloqueada. Os custos de encantamento não são cobrança de mana, durabilidade por tick ou custo por puxão. Datapacks efetivos e combinações artificiais não foram testados.

## 3. Consumer exato — escalar inicial do lançamento

Classe: `CandyCaneHookEntity`. Construtor com descritor JVM:

`(Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/item/ItemStack;Z)V`

O construtor possui **231 instruções** no parse selecionado. A região certificada contém:

1. `@255`: constante `0.5D`;
2. `@259`: `getstatic ACEnchantmentRegistry.FAR_FLUNG`;
3. `@262`: `ACCompat.enchantLevel(ItemStack,ResourceKey)I`;
4. `@265–270`: conversão para `double`, multiplicação por `0.2D` e soma de `0.5D`;
5. `@271`: armazenamento do escalar calculado; no mesmo construtor, `setDeltaMovement(Vec3) @352`.

A expressão numérica local observada é:

`escalar_de_lançamento = 0,5 + 0,2 × nível(FAR_FLUNG)`

| Nível lido | Escalar calculado |
|---:|---:|
| 0 | 0,5 |
| I | 0,7 |
| II | 0,9 |
| III | 1,1 |

**Fórmula física do vetor inicial reconstruída da versão instalada:** o construtor cria o vetor-base \(\mathbf{v}_0=(-f_3,\operatorname{clamp}(-f_5/f_4,-5,5),-f_2)\) (`@217–246`), calcula \(d=\|\mathbf{v}_0\|\) (`@248–253`) e, para cada componente \(i\in\{x,y,z\}\), passa ao movimento:

\[
v_{\mathrm{inicial},i}=v_{0,i}\left(\frac{0,5+0,2L}{d}+0,5+0,0045\,G_i\right).
\]

\(G_i\) é o retorno de **uma chamada de `RandomSource.nextGaussian()` por componente**. Provas: divisões `ddiv @279/@302/@325`, chamadas gaussianas `@288/@311/@334`, `Vec3.multiply(DDD) @344`, `setDeltaMovement @352`. O parâmetro \(S(L)=0,5+0,2L\) fornece 0,5/0,7/0,9/1,1 nos níveis 0/I/II/III, mas **não é uma velocidade final fixa ou alcance em blocos**. O vetor final também depende da direção-base, de seu comprimento e do ruído gaussiano.

A região local não verifica `d>0` antes das três divisões; não se demonstrou que \(d=0\) seja alcançável em gameplay normal. Níveis artificiais não possuem clamp comprovado no construtor. Duração do tether, hitbox, alcance prático, tempo de voo e velocidade residual dependem da física e de consumidores distintos. A certificação não autoriza alterar esses valores por hook externo.

**Outros encantamentos, separados:** `SHARP_CANE @423` consulta nível `@426`, multiplica por `3.0F @430–432` e solicita `setDamage(F) @433`; `STRAIGHT_HOOK @437` consulta nível `@440` e, quando positivo, escreve `RESISTS_GRAVITY=true @446–457`. Nenhuma dessas operações é um multiplicador próprio de Far Flung. `setDamage` armazena um parâmetro, não prova dano aceito. `RESISTS_GRAVITY` é uma flag da entidade, não imunidade genérica a forças do mundo.

## 4. Emissor — item, ownership e custos

Em `CandyCaneHookItem.use(Level,Player,InteractionHand)InteractionResultHolder`, **188 instruções** próprias foram inspecionadas. A região selecionada identifica `canLaunchHook @42`, criação de `new CandyCaneHookEntity @125`, invocação do construtor `(Player,Level,ItemStack,Z) @145`, `setOwner @153` e `setReeling(false) @159`. Só solicita `Level.addFreshEntity @172` se o nível **não** é client-side (`@163–166`); o resultado booleano do spawn é descartado `@175`. Em seguida registra `LastLaunchedHookUUID @183` e `Reeling=false @189` no stack. A tentativa de criar uma entidade não comprova spawn nem acerto.

O item possui **duas referências** a `ACCompat.hurtAndBreak` (`use @299/@328`) nos ramos de reeling/recolhimento. Não atribuir a Far Flung um débito de durabilidade por lançamento nem assumir uma única cobrança em todos os cenários de mão dupla: os ramos e as reservas pertencem ao provider. Não há consulta a uma nova mana Black Arcana no trecho do encantamento.

`canLaunchHook(Player,ItemStack,Level,boolean,InteractionHand)Z` tem **54 instruções** e árvore de retornos auditada. Em `ServerLevel` consulta `LastLaunchedHookUUID @21/@31`, `getEntity(UUID) @48`, `isAlive @70`, `getOwner @78/@86` e `Entity.is(player) @90`; quando existe gancho vivo do mesmo usuário, a opção `checkHands` e a mão de lançamento afetam a recusa `@96–115`. `isOwnerHoldingHook(Z)Z` (39 instruções) testa `CandyCaneHookItem` na mão correta, UUID do stack igual ao UUID da entidade e a condição de reeling; `postReel()` (22) solicita limpar o UUID do stack. Não há prova de antirreplay de pacotes externos, atomicidade entre spawn/UUID, autenticação em multiplayer ou resistência a tags adulteradas.

## 5. Movimento, colisão, targeting e persistência

| Corpo SHA-exato | Localizadores e limites |
|---|---|
| `CandyCaneHookEntity.tick()V` | **546 instruções**; `getOwner @5`, `getHookedEntity @10`, `setReeling @111/@128`, `discard @201/@214`, `getEntities @380` e múltiplas escritas `setDeltaMovement`. Esse tick trata movimento, seleção e recolhimento; a ficha não deriva daí um alcance máximo universal. |
| `fling()V` | **73 instruções**, `getHookedPosition @1`, `setDeltaMovement @79/@147`. Impulso do owner ou da entidade hooked segue condições nativas; não representa novo cast. |
| `onHitEntity(EntityHitResult)V` | **24 instruções**, `setHookedPosition @12` e `setHookedEntityUUID @42`. A presença de hit não prova um dano específico de Far Flung. |
| `onHitBlock(BlockHitResult)V` | **25 instruções**, `onProjectileHit @20`, `setHookedPosition @45`. O comportamento do bloco e suas proteções têm autoridade própria. |
| `acInventoryTick(ItemStack,Level,Entity,boolean)V` | **39 instruções**; `isClientSide @14`, `setReelingIn @60`, limpeza possível via `setLastLaunchedHookUUID @79` após checagens de mãos/estado. |
| `setLastLaunchedHookUUID` e `setReelingIn` | Escrevem o estado do stack por `ACCompat.setTag`; não constituem hook autorizado de cliente para alterar o mundo. |

Os overrides `readAdditionalSaveData(CompoundTag)V` e `addAdditionalSaveData(CompoundTag)V` chamam a superclasse e leem/gravam diretamente **`Reeling`**, **`HookedEntityUUID`** (condicional) e **`Offhand`** (`@10/@31/@42` na leitura e `@13/@31/@42` na escrita). Não se certifica por isso a restauração integral da velocidade, do owner, do alvo vivo, do stack associado e de todos os estados transitórios após reload/dimensão/morte.

**Targeting nativo (versão SHA-exata):** no ramo **servidor** de `tick` (`Level.isClientSide @23–26`), quando a entidade ainda não está presa/recolhendo, `getBoundingBox().inflate(1D) @355–360` alimenta `Level.getEntities @380` com o predicado `Entity::isAlive`, identificado no bootstrap `InvokeDynamic #0:test`. Segmentos `GumWormSegmentEntity` são convertidos para sua entidade head (`@414–437`). A seleção descarta `null`, outros `CandyCaneHookEntity`, `Projectile` e o owner (se conhecido), compara `Entity.distanceTo(this)` e admite prioridade especial para `GumWormEntity` (`@439–514`). **Não há guarda local demonstrada para aliados, PvP, claims ou LOS**; não inferir permissões de outras camadas. `inflate(1D)` é uma expansão da caixa do projétil, não um raio de alcance concedido por Far Flung.

**Dano e ordem dos efeitos:** a entidade escolhida recebe `HookedEntityUUID @522–528` antes de o método comparar `getDamage()!=0 @531–537`. Havendo dano positivo ou negativo diferente de zero, solicita `DamageSources.thrown(hook,owner) @546` e `Entity.hurt(source,getDamage()) @559`; o retorno é descartado `@562`. `SHARP_CANE` controla separadamente `setDamage(3F×L) @423–433`. Far Flung **não** aumenta dano nem cria proc/XP; alvo preso não implica dano aceito.

**Recolhimento, gravidade, rede e risco de cap:** no servidor `tick` sincroniza `OWNER_ID` e `HOOKED_ENTITY_ID` e processa `setReeling`/`discard`. O movimento do hook usa `move(SELF,getDeltaMovement) @1099`, atenua a velocidade com `0,5D` no chão ou aproximadamente `0,9D` no ar (`@1102–1126`) e zera o vetor quando ancorado (`@1132–1136`). `fling()` usa a distância owner–gancho ou owner–entidade presa multiplicada por `0.20000000298023224D`, soma `+0,2D` vertical e a velocidade anterior (`@27–79/@92–147`). **Quando o delta passa de magnitude 1, o código executa `Vec3.scale(1D)`, que é operação identidade, sem clamp efetivo** (`@45–59/@113–127`). Isso exige atenção especial a perks de força de puxão, velocidade ou alcance.

`getHookedEntity()` resolve UUID no servidor e ID sincronizado no cliente; `getPlayerOwner()` separa resolução de owner entre lados. `isOwnerHoldingHook` exige item e UUID correspondente, mas os buffers de rede/mixins, replay e persistência após troca de dimensão não foram testados. Os overrides próprios de NBT gravam `Reeling`, `HookedEntityUUID` condicional e `Offhand`, sem garantir reconstrução do estado físico completo. A ficha registra **27 métodos com corpos integrais inspecionados** e **182 branches diretos verificados**, mas não certifica a engine Minecraft, os efeitos de outros mods ou o hook mutador.

## 6. Matriz de perks e aceite pendente

| Intenção | Contrato de partida | Estado |
|---|---|---|
| Impulso de lançamento | Construtor `CandyCaneHookEntity(Player,Level,ItemStack,Z)V @255–352` | Escalar numérico **confirmado**, hook mutador seguro, ordem de snapshot, limites e física real **não verificados** |
| Alcance, velocidade, tempo de voo | Vetor do construtor, física herdada, `tick`, colisões e reeling | Não inferir de `0.5+0.2×nível` um alcance fixo em blocos |
| Tipo de alvo, raio e hitbox | `tick`, `onHitEntity`, `onHitBlock`, posição hooked e filtros | Owner/PvP/claims/LOS e regras de mundo ainda condicionados |
| Dano e Mastery | Sharp Cane → `setDamage` e settlement do hook separados | Não contabilizar duas vezes impacto, puxão e XP; hit aceito não certificado |
| Gravidade | Straight Hook → `RESISTS_GRAVITY` | Não confundir flag de gravidade com Far Flung |
| Custos | `CandyCaneHookItem.use`, `hurtAndBreak`, recuo e duas mãos | Não criar segunda cobrança ou segundo casting |
| NBT / rede | `LastLaunchedHookUUID`, `HookedEntityUUID`, `Reeling`, `Offhand` | Multiplayer, recarga, slot swap, forged payload, replay e cleanup pendentes |
| Black Arcana / RPG Skill Tree / Enshrouded | Runtime do gancho pertence ao provider; progressão externa exige contrato explícito | **Fail-closed**: nenhum adapter ou hook mutador homologado |

Black Arcana conserva autoridade sobre **seu próprio** casting, hazards, world safety, Corruption, Strain e Arcane Danger. O Candy Cane Hook continua executado pelo provider; RPG Skill Tree só fornece progressão, perks, Mastery, atributos e gates se existir boundary comprovada. Não cadastrar Far Flung como spell autônoma do Black Arcana.

**QA necessária:** comparação sem encantamento / níveis I–III, mão principal e secundária, colisão vertical/horizontal, Gum Worm, hook em bloco/entidade, reeling e força de puxão, durabilidade, troca de slot, PvP/proteções, servidor dedicado/multiplayer, dimension change, reload, cliente com estados atrasados, níveis incompatíveis por datapack e possíveis cancelamentos. **CI do probe ≠ QA física**.

**Resultado da certificação estática individual:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. Artefato físico 1.0.10, 2 owners de `FAR_FLUNG`, 27 métodos/1.600 instruções/182 branches diretos, cálculo vetorial e RNG por eixo, targeting/owner, dano solicitado, reeling, cleanup, estado sincronizado e NBT sustentam a ficha. **Contabilidade proposta após CI verde:** +1 contrato estático, −1 parcial, +0 novas raízes, +0 hooks, +0 QA física, +0 providers encerrados, +0 Stage. `NO_MUTATION`. **Próximo recurso alfabético:** `alexscaves:ferrous_haste`.
