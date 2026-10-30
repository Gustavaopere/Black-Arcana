# Desolate Dagger — equipamento, gatilho de melee e dagas vinculadas

Provider **Alex's Caves Continued**; item `alexscaves:desolate_dagger`; implementação `server.item.DesolateDaggerItem`, subclasse de `SwordItem` e implementação de `ACRepairableItem`. Arma de melee cujo callback solicita entidades adicionais vinculadas à vítima. Este contrato de equipamento complementa a [ficha de dano e entidade](../damage-types/desolate-dagger.md); não acrescenta raiz ao inventário histórico de oito ações sobrenaturais.

Autoridade: JAR **1.0.10**, publisher `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A [prova comum](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.md) e seu [manifesto](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.json) selam ficha, classes, recursos e localizadores JVM. A fonte pública `523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, sem paridade demonstrada com este artefato. Parâmetros `VERIFIED_EXACT_BINARY`; hook mutador `NOT_VERIFIED`; QA física `NOT_TESTED`; configuração/dados efetivos do pack `NOT_VERIFIED`.

## 1. Registro, atributos e propriedades declaradas

`ACItemRegistry.<clinit>()V @2327–2341` registra `desolate_dagger`. O bootstrap do `invokedynamic` liga o supplier a `lambda$static$127()Lnet/minecraft/world/item/Item; @0–7`, que constrói `DesolateDaggerItem`. Os seis métodos próprios dessa classe estão cobertos pela inspeção.

| Propriedade no construtor `DesolateDaggerItem.<init>()V` | Valor / limite |
|---|---|
| Tier passado ao `SwordItem` | `Tiers.DIAMOND` (`@1`, `@23`, `@35`) |
| Durabilidade declarada | **360**, por `Properties.durability(360)` (`@11–14`) |
| Raridade | `ACItemRegistry.RARITY_DEMONIC` (`@17–20`) |
| Factory de atributos | `SwordItem.createAttributes(DIAMOND,0,-2F)` (`@23–32`): bônus inteiro `0` e argumento de velocidade `-2F` |
| Construção nativa | `SwordItem(Tier,Properties)` (`@35`) |

Os argumentos da factory são valores compilados, não o dano total recebido, alcance, DPS ou velocidade final de ataque. A implementação do Minecraft, atributos da entidade e outros mods resolvem os resultados finais. Não há override próprio de encantabilidade, cooldown ou tempo de uso nesta classe; não importar números de outra versão de `SwordItem`/Diamond como se fossem constantes deste JAR.

## 2. Gatilho e ordem do callback

`hurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z` recebe, na ordem, **stack, vítima e atacante**. Chama `super.hurtEnemy(stack,victim,attacker)` (`@0–4`). Somente se o retorno for verdadeiro chama `acSpawnDaggers` (`@7–14`) e retorna `true`; caso contrário retorna `false` (`@19–20`). O corpo não chama diretamente `Entity.hurt` para o ataque primário. O booleano desse hook de item não é uma nova prova de que determinado pedido de dano tenha sido aceito.

O item não tem `use` próprio que selecione um novo alvo. O callback já recebe duas `LivingEntity`; não acrescenta testes locais de distância, linha de visão, aliança, tipo Player, PvP ou proteção territorial. Também não contém guarda própria `isClientSide`. O combate nativo e os consumidores externos decidem quando chamar o hook; compatibilidade efetiva com Epic Fight, Better Combat ou o RPG precisa de validação específica. Invocar o callback manualmente após o ataque pode duplicar a produção de entidades.

## 3. Quantidade, vínculo e geometria de produção

O método privado `acSpawnDaggers` tem descritor `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)V`:

| Etapa | Contrato exato |
|---|---|
| Impending Stab | Lê seu nível **uma vez** antes do loop, por `ACCompat.enchantLevel(stack,IMPENDING_STAB)` (`@0–7`) |
| Condição do loop | Inicia `i=0` e reconsulta `DOUBLE_STAB` em **cada comparação**: continua enquanto `i < 1 + level` (`@9–23`, incremento/retorno `@109–115`) |
| Factory | Obtém `ACEntityRegistry.DESOLATE_DAGGER` e chama `ACCompat.createEntity(type,attacker.level())` (`@26–47`). O wrapper apenas delega `EntityType.create(level)`; não adiciona fallback |
| Alvo | `setTargetId(victim.getId())` (`@49–55`): vínculo por ID inteiro da entidade, sem busca em área neste item |
| Origem | `copyPosition(attacker)` (`@58–61`); não é uma origem sorteada ao redor do alvo nem alcance de cast |
| Stack | `setItemStack(stack)` (`@64–67`); o setter da entidade passa essa referência a `SynchedEntityData.set`, sem `ItemStack.copy()` no próprio setter ou caller |
| Tempo inicial | `orbitFor = (cachedImpendingLevel > 0 ? 40 : 20) + attacker.getRandom().nextInt(10)` (`@70–96`): **40–49** ou **20–29** conforme aquele teste inicial |
| Inserção | `attacker.level().addFreshEntity(dagger)` (`@99–108`), com booleano descartado |

Para nível estável e não negativo de Double Stab, são **`1+level` tentativas de produção**: uma sem o encantamento e duas com seu máximo JSON `1`. Esse número não certifica spawns aceitos ou impactos. A reconsulta por iteração é relevante se um listener modifica o stack durante a inserção. Não há clamp próprio do nível nem guarda de retorno nulo da factory antes dos setters.

O nível de Impending aqui só escolhe a faixa de `orbitFor`: níveis positivos `1/2/3` compartilham a faixa inicial **40–49**, em vez de somar dez ticks por nível. O timer e o momento de stab são processados pela entidade; esses valores iniciais não prometem duração física total do ataque. A magnitude de dano é consultada no consumidor posterior e não é calculada por esse método do item.

O produtor **não chama `setPlayerId`**. Portanto, copiar a posição do atacante não define, por si, autoria do dano, vínculo persistente ou autorização para efeitos de recuperação. O contrato da entidade documenta o fallback e a condição Player do Sated Blade. Como o próprio caminho de `setItemStack` não congela uma cópia, não presumir snapshot imutável de nível, durabilidade ou componentes até o impacto; sincronização, substituição do stack e efeitos de alteração exigem QA.

## 4. Encantamentos e parâmetros por consumidor

As chaves `IMPENDING_STAB`, `SATED_BLADE`, `DOUBLE_STAB` são ligadas aos IDs do mesmo nome por `ACEnchantmentRegistry.<clinit>()V @356–380`; `key(String)ResourceKey @0–12` usa namespace `alexscaves` e o registry de encantamentos. `ACCompat.enchantLevel(ItemStack,ResourceKey)I @0–61` lê `ItemStack.getEnchantments()`, compara `Holder.is(key)` e retorna o valor encontrado ou zero.

| JSON exato | Máximo / peso | Custo mínimo | Custo máximo | Bigorna / slot | Consumidor relevante |
|---|---|---|---|---|---|
| `double_stab` | 1 / 2 | `1+12*(L-1)` | `41+10*(L-1)` | 4 / mainhand | Condição de quantidade de entidades no item |
| `impending_stab` | 3 / 10 | `1+6*(L-1)` | `41+10*(L-1)` | 1 / mainhand | Faixa inicial de espera no item; magnitude no consumidor da entidade |
| `sated_blade` | 2 / 10 | `1+11*(L-1)` | `41+10*(L-1)` | 1 / mainhand | Consumidor de saturação na entidade, condicionado à fonte resolvida |

Todos referenciam `#alexscaves:enchantable/desolate_dagger`; esse tag contém diretamente o item. O JSON de **Impending Stab** declara `exclusive_set: [alexscaves:double_stab]`; o de Double Stab não repete esse campo. O corpo do item não testa exclusividade, e os limites JSON não fazem clamp de níveis externos nos métodos. A aplicação efetiva de exclusividade e custos no pack pertence ao sistema de encantamentos/bigorna e seus dados resolvidos.

Duração inicial, quantidade de entidades e magnitude/recuperação posterior são superfícies distintas. Alterar amplifier de um status genérico não modifica esses níveis ou filtros. Cada perk futura precisa escolher o consumidor certo e preservar a liquidação nativa.

## 5. Custos, reparo e aquisição

O item delega o callback base a `SwordItem.hurtEnemy`; seus corpos próprios não contêm débito adicional de durabilidade, mana, fome, munição ou cooldown por dagger gerada. **360** é a capacidade declarada, não uma prova de desgaste fixo por ataque. O valor efetivo e o caminho de desgaste herdado dependem da implementação 1.21.1 e dos hooks de combate. Não reproduzir custo base mais um custo fictício por cada entidade.

`acExtraRepairMaterials()[Item] @0–18` retorna um array contendo somente `ACItemRegistry.PURE_DARKNESS`; `acReplacesTierRepairMaterials()Z @0–1` retorna `true`. `isValidRepairItem(ItemStack,ItemStack)Z @0–5` passa **o segundo stack** ao helper `ACRepairableItem.isExtraRepairMaterial(ACRepairableItem,ItemStack)Z`. O helper percorre o array e usa `ItemStack.is(item)` (`@0–43`). Esse override não chama o reparo de tier da superclasse: aceita o match de Pure Darkness nesse caminho. Quantidade reparada, custo de XP e resultados finais da bigorna não são constantes desses métodos.

O loot exato `data/alexscaves/loot_table/entities/underzealot.json` tem pool `underzealot_dagger`, um roll, item Desolate Dagger e duas condições: **`minecraft:killed_by_player`** e **`minecraft:random_chance_with_enchanted_bonus`**. Declara chance sem encantamento **0.025**, Looting linear com base **0.035** e **0.01 por nível acima do primeiro**: 3,5%/4,5%/5,5% para níveis usuais I/II/III. São parâmetros JSON, não frequência medida nem loot final após overrides. A busca dos JSONs `data/` deste JAR não encontrou receita direta do item; isso não exclui receitas ou aquisições acrescentadas por outros mods/dados.

O advancement `data/alexscaves/advancement/alexscaves/desolate_dagger.json` observa `minecraft:inventory_changed` para esse item, parent `discover_underzealot`. Seu texto traduzido descreve obtenção ao matar Underzealot, mas o trigger observa posse, sem provar o caminho de obtenção da instância.

## 6. Dados de compatibilidade, autoridade e validação

`data/minecraft/tags/item/swords.json` inclui diretamente o Dagger. O arquivo `data/alexscaves/weapon_attributes/desolate_dagger.json` contém somente **`{"parent":"bettercombat:dagger"}`**: há uma referência de dados de compatibilidade, sem alcance, animações ou valores numéricos próprios nesse arquivo. A presença do recurso não prova carregamento ou resolução desse parent na versão instalada de Better Combat. Não importá-los de uma versão pública arbitrária.

O tag `alexscaves:galena_gauntlet_crystallization_items` também lista o item; esse é um consumidor de equipamento separado, não prova de produção de dagas pelo callback de melee. Não se declara o sistema Galena Gauntlet completo por registrar essa entrada.

Os sete campos estáticos estão cobertos: identidade/obtenção; callback e produção; propriedades e fórmulas; vínculo e filtros; custos/reparo; fronteiras nativas e dados externos; reprodução por bytes e localizadores. Hooks mutadores Black Arcana/Enshrouded/RPG Skill Tree seguem `NOT_VERIFIED`. A fronteira exige observar o ataque liquidado uma vez, preservar callbacks e não repetir dano, spawn ou custo por conta própria.

QA física permanece `NOT_TESTED`: callback em servidor dedicado/cliente; combate vanilla/Epic Fight/Better Combat; spawn rejeitado/factory nula; alteração de nível durante o loop e após o spawn; troca/dano do stack; alvo morto/descarregado e IDs reutilizados; autoria e Sated Blade; exclusividade e níveis externos; loot, reparo e dados finais do pack. Nenhuma falha em jogo ou compatibilidade executável é declarada demonstrada.

## Localizadores JVM próprios

| Método | Descritor / offsets |
|---|---|
| `DesolateDaggerItem.<init>` | `()V @0–38` |
| `hurtEnemy` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z @0–20` |
| `acSpawnDaggers` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)V @0–115` |
| `acExtraRepairMaterials` | `()[Lnet/minecraft/world/item/Item; @0–18` |
| `acReplacesTierRepairMaterials` | `()Z @0–1` |
| `isValidRepairItem` | `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;)Z @0–5` |

Descritores e offsets são da build 1.0.10, inspecionados por `javap -p -c -s`. A [prova comum](../EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.md) fixa os hashes e o escopo da revisão; a interpretação não homologa mutação por perks nem substitui testes físicos.
