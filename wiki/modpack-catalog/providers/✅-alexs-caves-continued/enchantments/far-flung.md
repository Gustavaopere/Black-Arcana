# Far Flung — impulso inicial do Candy Cane Hook (1.0.10)

**Estado:** ⚠️ ficha individual **parcial/condicionada**. O JSON, a tag e os consumidores JVM selecionados foram inspecionados na release publisher **SHA-exata 1.0.10**, por sonda *read-only*. **Não** existe certificação de hook seguro para perks, CFG completo, alcance físico no jogo ou QA real. Marcadores: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`.

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

**Nova evidência selada:** [EXACT-FAR-FLUNG-1.0.10.json](../EXACT-FAR-FLUNG-1.0.10.json), produzida por [sonda SHA-exata](../../../../../docs/qa/alexscaves_1010_far_flung_probe.py), [testes negativos](../../../../../docs/qa/alexscaves_1010_far_flung_probe_test.py) e [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-far-flung.yml). A sonda verifica SHA-1/SHA-256/tamanho do JAR e salva JSON de recursos, classes e janelas limitadas de instruções `javap -c -p -s`, com digests de métodos. O modo `--seal` exige igualdade integral do manifesto. Isto é auditoria estática, não decompilação, execução do modpack ou certificação de API externa.

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

**Limite de interpretação:** esse escalar participa do cálculo do vetor inicial. Ele **não é** alcance máximo em blocos, duração de tether, tamanho de hitbox, tempo de voo, velocidade final de cada eixo nem distância garantida de captura. O método possui outras operações, inclusive cálculo de vetor e `setDeltaMovement`, cujas relações completas não foram fechadas como CFG. Física herdada, RNG, colisão e obstáculos influenciam o deslocamento. O recurso declara máximo III; não foi certificado clamp adicional para níveis anômalos no conjunto de janelas selecionado.

**Outros encantamentos, separados:** `SHARP_CANE @423` consulta nível `@426`, multiplica por `3.0F @430–432` e solicita `setDamage(F) @433`; `STRAIGHT_HOOK @437` consulta nível `@440` e, quando positivo, escreve `RESISTS_GRAVITY=true @446–457`. Nenhuma dessas operações é um multiplicador próprio de Far Flung. `setDamage` armazena um parâmetro, não prova dano aceito. `RESISTS_GRAVITY` é uma flag da entidade, não imunidade genérica a forças do mundo.

## 4. Emissor — item, ownership e custos

Em `CandyCaneHookItem.use(Level,Player,InteractionHand)InteractionResultHolder`, **188 instruções** próprias foram inspecionadas. A região selecionada identifica `canLaunchHook @42`, criação de `new CandyCaneHookEntity @125`, invocação do construtor `(Player,Level,ItemStack,Z) @145`, `setOwner @153` e `setReeling(false) @159`. Só solicita `Level.addFreshEntity @172` se o nível **não** é client-side (`@163–166`); o resultado booleano do spawn é descartado `@175`. Em seguida registra `LastLaunchedHookUUID @183` e `Reeling=false @189` no stack. A tentativa de criar uma entidade não comprova spawn nem acerto.

O item possui **duas referências** a `ACCompat.hurtAndBreak` (`use @299/@328`) nos ramos de reeling/recolhimento. Não atribuir a Far Flung um débito de durabilidade por lançamento nem assumir uma única cobrança em todos os cenários de mão dupla: os ramos e as reservas pertencem ao provider. Não há consulta a uma nova mana Black Arcana no trecho do encantamento.

`canLaunchHook(Player,ItemStack,Level,boolean,InteractionHand)Z` possui **54 instruções**, incluindo duas consultas nominais a `LastLaunchedHookUUID @21/@31`, `ServerLevel.getEntity(UUID) @48`, `isAlive @70` e `getOwner @78/@86`. São predicados nativos relacionados a reutilização do gancho, identidade e mão. O recorte **não** certifica todos os retornos, antirreplay de mensagens, atomicidade entre gravação e spawn, segurança de componentes NBT adulterados ou impossibilidade de hooks duplicados em mods externos.

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

**Targeting:** `getEntities` no tick é um ponto nativo de busca; os filtros efetivos de aliados, PvP, claims, LOS, tipo de entidade, alcance e permissões **não foram integralmente auditados** nesta sonda de janelas locais. Uma perk de Far Flung não deve converter o escalar de movimento em aumento automático da AABB, puxar alvos extras, burlar colisão nem duplicar dano ou procs. `getHookedPosition` e `getHookedEntityUUID` descrevem estados distintos de movimento e de alvo.

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

**Resultado:** `SHA_EXACT_JSON_AND_SELECTED_JVM_WINDOWS` + `PARTIAL_ENCHANTMENT_DOSSIER` / ⚠️; **+1 ficha individual parcial, +0 certificados estáticos adicionais, +0 hooks mutadores, +0 raízes mágicas, +0 promoção de Stage.** Próximo recurso alfabético: `alexscaves:ferrous_haste`.
