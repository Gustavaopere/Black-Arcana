# Bonking — `alexscaves:bonking` (1.0.10)

**Contrato técnico individual:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. A ficha conclui a identidade publisher, o ramo nativo de morte/loot e as fronteiras dos helpers e do Primitive Club no recorte estático descrito. **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **integração:** `NO_MUTATION`. O runtime transformado do pack permanece não verificado. Bonking é um modificador de loot do equipamento: **+0 raízes mágicas**, nenhuma nova ação de cast e nenhuma perk executável.

## 1. Identidade, registro e proveniência

- **Provider / ID:** Alex's Caves Continued / `alexscaves:bonking`; encantamento do `alexscaves:primitive_club`.
- **Publisher:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**. O `META-INF/neoforge.mods.toml` declara mod ID `alexscaves`, versão `1.0.10`, Minecraft `[1.21.1]`, NeoForge e dependência obrigatória `codxlib >=1.3.6`; a análise usa Java 21.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Consumer:** `com/github/alexmodguy/alexscaves/server/event/CommonEvents.class`, SHA-256 `d132caad67ecab68844091ee396d37fecc4860440d338dcd82384f1555f8ad43`.
- **Equipamento:** `com/github/alexmodguy/alexscaves/server/item/PrimitiveClubItem.class`, SHA-256 `92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac`.
- **Nome / descrição literais em `en_us.json`:** “Bonking” / “Primitive Club has a chance to drop heads from slain mobs, as if a charged Creeper killed them”. O `pt_br.json` contém “Porrete Primitivo” para o item, mas **não contém nome nem descrição de Bonking**. Paráfrase técnica em português: o porrete pode solicitar loot da vítima com contexto de Creeper eletrificado; o resultado depende do caminho nativo de loot. Essa paráfrase não é uma tradução oficial nem uma garantia de cabeças.
- **Prova atual:** [manifesto individual SHA-exato](../EXACT-BONKING-CONTRACT-1.0.10.json), [contrato técnico consolidado](../EXACT-BONKING-CONTRACT-1.0.10.md) e [regressão semântica da ficha](../../../../../docs/qa/alexscaves_1010_bonking_cards_test.py). O manifesto sela recursos, classes, âncoras e a ficha final.

O inicializador de `ACEnchantmentRegistry` liga `bonking @132` a `key @134` e ao campo `BONKING @137`; `key(String)` completo constrói a ResourceKey em `Registries.ENCHANTMENT` com namespace `alexscaves`. O registro do item em `ACItemRegistry.<clinit> @967–981` liga `primitive_club @970` ao supplier de bootstrap **52**. Seu handle resolve `lambda$static$40`, cujo corpo completo de **9 instruções** cria `PrimitiveClubItem` com **durabilidade 120**.

O censo de Fieldrefs com owner, nome `BONKING` e descriptor `Lnet/minecraft/resources/ResourceKey;` exatos percorre **1.555 classfiles** e encontra somente `ACEnchantmentRegistry` e `CommonEvents`. O primeiro registra a chave; `livingDie` é o leitor direto identificado. O Primitive Club não contém essa referência direta. O censo não exclui reflexão, consumidores indiretos, transformações ou mods externos.

A fonte pública [Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37](https://github.com/Codx-org/AlexsCavesContinued/tree/523308608422ab8e31974befa7111ecdf495dd37) declara **1.1.1** e serve somente de contexto adjacente. Valores, offsets e predicados desta ficha têm autoridade no publisher **1.0.10**.

## 2. Definição, aquisição e aplicação

| Campo de `data/alexscaves/enchantment/bonking.json` | Valor publisher 1.0.10 | Significado delimitado |
|---|---|---|
| Recurso / SHA-256 | 362 bytes / `f03c4e8c2f8b00b3668b8d7bf14276647b3e0324c159c6336b189a258571a86a` | Identidade da definição |
| `description.translate` | `enchantment.alexscaves.bonking` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/primitive_club` | Tag publisher contém somente `alexscaves:primitive_club` |
| `weight` / `max_level` | `1` / `1` | Peso declarativo e nível nativo I; peso não é chance de proc |
| `min_cost` | `base=1`, `per_level_above_first=18` | `1 + 18 × (L−1)`; para I: **1** |
| `max_cost` | `base=41`, `per_level_above_first=10` | `41 + 10 × (L−1)`; para I: **41** |
| `anvil_cost` / `slots` | `8` / `mainhand` | Dados de aplicação, sem custo por tentativa de loot |

O JSON não declara `effects` nem `exclusive_set`; a implementação está em Java. A varredura das **51 definições nativas de encantamento** não encontra `exclusive_set` reverso mencionando Bonking. Isso fecha as exclusões declaradas no publisher; compatibilidade efetiva e aplicação por datapacks permanecem dependentes do pack.

A tag de suporte `data/alexscaves/tags/item/enchantable/primitive_club.json` tem **54 bytes**, SHA-256 `71829c384be93b8cef1e090b6afafa621dcd4eeb520c7a66ab0e6524e8a6ae43`. Bonking aparece nas quatro tags nativas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable`; cada arquivo tem **1.631 bytes**, SHA-256 `6472c976d755f1481506f3f113368081aa487eaff3ce977a1f7c93a400f39bb1`. São dados de disponibilidade, sem probabilidade observada de mesa, loot ou trade.

A receita shaped `data/alexscaves/recipe/primitive_club.json` usa o padrão diagonal `  C` / ` C ` / `B  `: **dois `alexscaves:cycad` e um `alexscaves:heavy_bone`**, resultado `alexscaves:primitive_club`, com `count` omitido. O recurso tem **330 bytes**, SHA-256 `b93f005c5632388ca6f34e3a114a8e0a4cf1c2ae99ae9bb0ed2edc2c73dddcc0`. A receita fabrica a arma; mesa, bigorna e materiais não são débitos de mana, XP ou durabilidade por proc.

## 3. Evento, vítima, ator direto e stack atual

`CommonEvents.livingDie(Lnet/neoforged/neoforge/event/entity/living/LivingDeathEvent;)V` completo contém **229 instruções JVM**, **21 branches no método inteiro** e **zero handlers de exceção**. O digest do parser histórico é `03c56101acdb5aa18c6d253f49b914bef1c1f2723aa5de548b126d4d864020dd`; ele não é hash do classfile nem substitui o fingerprint do normalizador do manifesto atual. A anotação nativa é `net.neoforged.bus.api.SubscribeEvent`, sem argumentos explícitos. Isso não certifica registro do listener, prioridade, política para evento cancelado ou ordem efetiva do dispatch.

O prefixo `@0–72` trata o caso independente de Frog primordial/Magma Cube; `@432+` contém `GREEN_SOYLENT` e `STINKY_FISH`. Esses trechos compõem a identidade do método completo, mas seus spawns e regras não pertencem a Bonking. Os offsets abaixo pertencem ao ramo `@73–429`.

| Porta de entrada | Evidência nativa | Consequência delimitada |
|---|---|---|
| Lado da vítima | `victim.level().isClientSide @80`; `ifne @83 → 432` | O ramo exige nível não cliente |
| Tipo da vítima | `instanceof Mob @94`; `ifeq @97 → 432`; `astore_2 @105` | Conserva a **vítima original Mob na local 2**; Player não satisfaz esse tipo |
| Fonte | `getSource @107`; `ifnull @110 → 432` | Fonte ausente rejeitada |
| Ator direto | `DamageSource.getDirectEntity @117`; `instanceof LivingEntity @124`; `ifeq @127 → 432`; `astore_3 @135` | Ator direto **LivingEntity na local 3**; não exige explicitamente Player |
| Item da mão principal | `getItemInHand(MAIN_HAND) @140`; `ItemStack.is(PRIMITIVE_CLUB) @154`; `ifeq @157 → 432` | Testa o item concreto da mão principal atual |
| Encantamento da mão principal | **Segunda leitura** `getItemInHand(MAIN_HAND) @164`; `BONKING @167`; `enchantLevel @170`; `ifle @173 → 432` | Exige nível positivo na stack obtida nessa segunda leitura |

São **duas leituras da mão principal atual**, não uma stack salva do golpe original ou um snapshot imutável da arma da kill. O código conserva o ator, mas não guarda a primeira stack para a consulta de nível. A elegibilidade vem da fonte do evento; o ramo não troca `getDirectEntity` por `getEntity`, não resolve dono de projétil e não demonstra autoria indireta. Não há allowlist própria de espécies além de `Mob`, teste de proximidade, LOS, aliado, claim ou requisito explícito de Player nesse ramo. Isso não garante que todo Mob produza cabeça nem que uma morte tenha sido aceita pelo pipeline final.

`ACCompat.enchantLevel(ItemStack,ResourceKey)I` completo tem **24 instruções**: percorre os encantamentos, retorna o primeiro nível cujo Holder corresponde à chave, ou zero. Não aplica clamp próprio de máximo, tag ou slot. Bonking testa somente **nível >0**: I e níveis positivos forçados seguem a mesma condição, **sem escala por nível**; zero ou negativo são rejeitados.

## 4. RNG, entidades temporárias e fonte sintética

Após as guardas, a rotina lê o RNG do nível da vítima (`getRandom @183`, `nextFloat @186`) e exige **`nextFloat() < 0.33F`** (`ldc @191`, `fcmpg @193`, `ifge @194 → 432`). É um guard nominal de tentativa de aproximadamente 33% com RNG uniforme; não é a probabilidade final de cabeça, spawn aceito, item coletado ou crédito de recompensa. Não há multiplicador por nível.

1. `EntityType.CREEPER @197` e `ACCompat.createEntity @204` constroem uma referência temporária de Creeper, guardada na **local 4 @210**. Se for null, `ifnull @214 → 432` pula todo o callback de Bonking.
2. A rotina testa `level instanceof ServerLevel @228`; se falhar (`@231 → 274`), segue sem o preparo por raio. Quando passa, tenta `EntityType.LIGHTNING_BOLT @241` / `createEntity @246`. Raio null (`@256 → 274`) também pula somente esse preparo e continua no caminho de loot.
3. Com ambas as referências válidas e ServerLevel, marca `LightningBolt.setVisualOnly(true) @262` e solicita `fakeCreeper.thunderHit(serverLevel,fakeThunder) @271`. Isso prepara o contexto semelhante a Creeper eletrificado, sem certificar a execução interna da engine ou seu resultado transformado.
4. `DamageSources.mobAttack(fakeCreeper) @283` cria a **fonte sintética na local 5 @286**. Essa fonte é passada somente ao callback de loot descrito abaixo. Não reatribui a fonte original do evento nem chama um segundo ataque/dano contra a vítima.

`ACCompat.createEntity(EntityType,Level)Entity` completo tem **4 instruções** e delega a `EntityType.create(Level)`. Nem esse helper nem o ramo de Bonking contém `addFreshEntity` ou inserção equivalente das referências temporárias no mundo. Portanto o Creeper e o raio são contexto auxiliar de loot, sem projétil de Bonking, trajetória, tamanho/hitbox próprio ou summon persistente certificado. `setVisualOnly(true)` não comprova um raio visível lançado no mundo, dano elétrico ou morte por raio.

## 5. Backup, chamada de loot e restauração normal

A vítima continua sendo o **Mob original da local 2**. `checkcast EntityDropChanceAccessor @298` cria a referência de bridge na **local 7 @301**; não substitui a vítima pelo Creeper. Um `HashMap` temporário é guardado na **local 6 @295** para backup das chances de equipamento.

| Sequência do ramo | Evidência completa | Efeito local demonstrado |
|---|---|---|
| Primeiro loop | `EquipmentSlot.values @303`; teste `@320 → 366`; retorno `goto @363 → 316` | Percorre todos os slots retornados |
| Backup por slot | `ac_getEquipmentDropChance @338`; `Float.valueOf @343`; `HashMap.put @346` | Salva a chance anterior do slot na local 6 |
| Zero temporário | `fconst_0 @354`; `ac_setDropChance @355` | Solicita chance de equipamento `0F` antes do callback |
| Callback de loot | `ac_dropCustomDeathLoot @372`, sobre a vítima, com fonte sintética e argumentos compilados **`0,false`** (`@370–371`) | Solicita loot customizado da vítima com o novo contexto de fonte |
| Segundo loop | `EquipmentSlot.values @377`; teste `@394 → 432`; retorno `goto @429 → 390` | Percorre os slots novamente após retorno normal do callback |
| Restauração | `HashMap.get @412`; `Float.floatValue @418`; `ac_setDropChance @421` | Reaplica as chances capturadas no backup no fluxo normal |

É uma chamada adicional à rotina de loot da vítima, não prova de segunda morte, de execução original anterior, de tabela dedicada a Bonking ou de equipamento definitivamente suprimido. A prova não reauditou o despacho vanilla de loot: tipo da vítima, loot tables, dados, regras de morte e outros mods continuam sendo fronteiras delegadas.

**Exceções:** há **zero entradas na tabela JVM de handlers** de `livingDie`; não há `try/finally` compilado protegendo `backup → zero → callback → restauração`. Se um callback lançar exceção após algum zero e antes da restauração correspondente, poderá interromper esse fluxo normal. Trata-se de **observação estática condicional de exception-safety**, não de bug físico reproduzido, corrupção permanente demonstrada ou ausência provada de rollback/tratamento externo. Tampouco a ausência de reprodução autoriza mutação segura desse estado.

## 6. Bridge de Mob e aplicação do Mixin

`EntityDropChanceAccessor` declara as três operações de chance/loot. O publisher `alexscaves.mixins.json`, SHA-256 `6e120e2d2cf226a25cbe3d0605968a184384194354eac0b1153108f74632c140`, declara `MobMixin` no grupo `mixins`, package `com.github.alexmodguy.alexscaves.mixin`. `MobMixin.class`, SHA-256 `38381f9b5b3908e813711f031161a1e25b46e68d220ed34c137948e6b59dac3e`, implementa a interface, declara target `net.minecraft.world.entity.Mob` e shadows das operações delegadas.

| Corpo completo | Instruções | Delegação e limite |
|---|---:|---|
| `ac_getEquipmentDropChance(EquipmentSlot)F` | 4 | Chama `getEquipmentDropChance(slot)` e retorna o float |
| `ac_setDropChance(EquipmentSlot,float)V` | 5 | Chama `setDropChance(slot,chance)` |
| `ac_dropCustomDeathLoot(DamageSource,int,boolean)V` | 8 | Obtém seu próprio `level()`, faz cast para `ServerLevel` e chama `dropCustomDeathLoot(ServerLevel,DamageSource,boolean)` |

A bridge de loot **ignora o argumento int**: não carrega sua local 2; encaminha a fonte e `iload_3`, o boolean. O `0` compilado no callsite não é, por isso, um parâmetro efetivo de looting demonstrado. O cast para ServerLevel pertence ao corpo da bridge; a guarda anterior de nível não cliente não prova por si esse cast nem sua aceitação no runtime.

Declaração de target, shadows, configuração e corpos são evidências estáticas do publisher. **Aplicação e ordem do Mixin no runtime transformado:** `NOT_VERIFIED`. Não se certificam prioridade entre listeners, cancelamento da morte, proteção, alterações de loot por terceiros ou execução bem-sucedida dos shadows.

## 7. Mecânicas do Primitive Club separadas de Bonking

O selo atual cobre **todos os 16 corpos / 381 instruções** do `PrimitiveClubItem`, inclusive `hurtEnemy` (**6**) e `acHurtEnemy` (**171**), para separar a arma do modificador de loot. Nenhum desses corpos lê diretamente `BONKING`.

- **Atributos da arma:** `getStatsForEnchantmentLevel` declara **+8 ATTACK_DAMAGE**, `ADD_VALUE`, e modificador de attack speed `Math.min(0F,-3.75F+0.15F×L)`. `acModifiers` seleciona `L` a partir de **Swiftwood**, limitado a `0..3`, somente em `MAINHAND`. São contribuições da arma/Swiftwood, sem dano ou velocidade escalados por Bonking; não são dano final ou DPS certificado.
- **Desgaste ao acertar:** `hurtEnemy` delega a `acHurtEnemy`; `acHurtEnemy @0–6` solicita **1 de durabilidade** via `ACCompat.hurtAndBreak(stack,1,actor,MAINHAND)` **antes** da guarda servidor do stun. É um callback da arma, não um débito por tentativa de Bonking nem prova de desgaste final aceito.
- **Mineração:** `mineBlock` solicita **2 de durabilidade** quando `getDestroySpeed` é diferente de zero. É outro callback da arma, independente do RNG e do loot de Bonking.
- **Stun / Dazing Sweep:** o ramo servidor de `acHurtEnemy` tem sua própria guarda RNG `0.8F`, aplicação de STUNNED e consulta `DAZING_SWEEP`; o caminho de sweep contém sua própria área e chamada `hurt(...,1F)`. Esses efeitos, mensagens e sons não pertencem ao ramo de Bonking. Não importar seu alcance, duração, dano ou chance para Bonking.
- **Outras superfícies:** callbacks de swing/ataque/inventário, reparo por `HEAVY_BONE`, enchanting e apresentação cliente pertencem ao equipamento. `getEnchantmentValue=1` e `isEnchantable(stack)` com `count==1` são dados da arma, sem garantia de aquisição efetiva.

Durabilidade 120, receita e custos de enchanting descrevem o equipamento/aplicação. No ramo de Bonking não aparece débito próprio de mana, XP, munição, durabilidade, charges ou cooldown por proc. A engine e os helpers de desgaste permanecem fronteiras delegadas; não se certificam Unbreaking, quebra, reembolso ou cobrança autoritativa no pack.

## 8. Sete eixos do contrato estático individual

| Eixo | Contrato nativo consolidado | Limite para perks |
|---|---|---|
| **Targeting** | Vítima Mob original, lado não cliente, fonte existente, ator direto LivingEntity; item concreto na primeira leitura de mão principal, nível positivo na segunda, depois RNG | Não transforma autoria indireta em kill de Player nem certifica morte aceita, allowlist final de cabeças ou proteção |
| **Range / area** | **N/A como parâmetro próprio:** o ramo recebe a vítima do evento e não executa busca espacial, distância, LOS ou área | Alcance do ataque e área de Dazing Sweep pertencem a outras mecânicas |
| **Speed / direction** | **N/A:** nenhum movimento, steering, vetor ou velocidade é calculado no ramo de loot | Swing/attack speed da arma e Swiftwood não são parâmetros de Bonking |
| **Projectile / size** | **N/A como projétil/hitbox próprio:** Creeper e raio são referências temporárias; não há inserção no mundo nesse ramo/helper | Não autoriza spawn, summon, trajetória ou área de raio de Bonking |
| **Damage / type** | Fonte sintética `mobAttack(fakeCreeper)` somente para o callback; nenhuma segunda aplicação de dano demonstrada | Sem fórmula nova de dano, stun, eletricidade ou autorização para alterar o golpe original |
| **Duration / resources** | Oportunidade no evento de morte; nível positivo sem escala; guard `<0.33F`; backup/zero/restauração normal por slot. **N/A para duração/cooldown próprio:** não há buff temporizado ou contador nesse ramo | Custos de aquisição e desgaste da arma separados; cleanup sob exceção e débitos efetivos não certificados |
| **Authorship / protection / procs** | Ator direto, vítima original e Creeper sintético são papéis distintos; stack atual consultada duas vezes; nenhum recibo persistente local de Bonking | Callback, loot, spawn, coleta e XP/Mastery exigem resultados autoritativos e deduplicados; proteção e replay permanecem não verificados |

## 9. Resultado, autoria e limites de integração

As etapas **callback invocado → loot avaliado → ItemEntity inserido no mundo → item coletado → XP/Mastery creditados** são resultados distintos. A prova fecha o callsite e sua delegação; não fornece confirmação das etapas posteriores, porcentagem final, quantidade/tipo de cabeça ou concessão em inventário. O evento de morte, o guard RNG e a fonte de Creeper fictício não autenticam uma recompensa final de Bonking.

Não há escrita local de recibo de loot, ID de proc, marcador persistente dedicado ou deduplicação no ramo de Bonking. O HashMap é um backup transitório por slot, não um recibo. Isso não prova ausência de mecanismos externos, mas impede tratar este ramo como hook idempotente, seguro para replay ou reentrada. **Não reexecutar** o evento/callback, simular outro Creeper, editar drop-chances ou conceder cabeças diretamente para implementar uma perk.

O **Black Arcana** só poderá observar resultados confirmados por um contrato real do provider. O **RPG Skill Tree** continua responsável por progressão, atributos, Mastery e gates; não passa a ser autoridade da morte ou do loot. Crédito de kill/XP/Mastery exige correlação com ator autorizado, resultado aceito e concessão única. Vida terminando, callback solicitado ou fonte sintética não são esse recibo. PvP, claims, alianças, cancelamento, outros mods de loot e ordem dos mixins permanecem `NOT_VERIFIED`; integração fica `NO_MUTATION`, com comportamento fail-closed.

## 10. Cobertura, provas históricas e pendências físicas

A prova atual sela o método `livingDie` **inteiro**, os **16 corpos inteiros** do Primitive Club, `ACCompat.enchantLevel` e `createEntity`, as três bridges de Mob, `ACEnchantmentRegistry.key` e o supplier do clube. Os inicializadores compartilhados de registro têm apenas as janelas **PARTIAL** `ACEnchantmentRegistry.<clinit> @132–137` e `ACItemRegistry.<clinit> @967–981`; não se declara fechamento dessas classes ou de todo o provider. As 21 branches de `livingDie` incluem regiões independentes e não representam 21 condições exclusivas de Bonking.

A [prova histórica inicial](../EXACT-BONKING-1.0.10.json) e a [prova causal histórica](../EXACT-BONKING-CAUSAL-1.0.10.json), com a [sonda inicial](../../../../../docs/qa/alexscaves_1010_bonking_probe.py) e a [sonda causal](../../../../../docs/qa/alexscaves_1010_bonking_causal_probe.py), conservam seus bytes, hashes e limites **PARTIAL**. Seus selected windows, roster e metadados de branches não são relabelados como selo completo; o novo contrato individual tem manifesto próprio. O estado parcial dessas provas históricas não é o estado atual desta ficha.

A regressão estática atual e suas mutações negativas protegem identidade, recursos, corpos/âncoras e os limites semânticos desta ficha. Não executam Minecraft, CFG interprocedural ou loot real. Não há reauditoria da engine-base ou autenticação de um hook de runtime. A conclusão estática independe de reproduzir uma cabeça física ou uma exceção em jogo; afirmações físicas exigem evidência própria.

**QA física continua `NOT_TESTED`:** níveis 0/I/forçados; mão principal atual versus arma do golpe; ator direto versus dono de projétil; tipos de Mob e cabeças elegíveis; evento cancelado e ordem dos listeners; nulls e entidades temporárias; Mixin aplicado; loot normal versus chamada adicional; chances customizadas de equipamento antes/depois; exceções e tratamento externo; reentrada/replay; datapacks e mods de loot; cliente/servidor dedicado, multiplayer, PvP/claims; unload/reload; itens aceitos, coleta e crédito único de XP/Mastery. São limites de runtime, não lacunas ocultas do contrato estático documentado.

**Contabilidade:** uma ficha individual concluída em `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; **+1 contrato estático individual**, **+0 raízes mágicas** e **+0 providers integrais concluídos**. Provider e contratos de Stage/equipamento permanecem abertos; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Próximo encantamento parcial alfabético: `alexscaves:bouncing_bolt`.
