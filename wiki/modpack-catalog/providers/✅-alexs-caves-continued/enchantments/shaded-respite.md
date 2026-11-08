# Shaded Respite — `alexscaves:shaded_respite` (1.0.10)

**Contrato técnico estático:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. **Hooks mutadores:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Integração:** `NO_MUTATION`. O recorte conclui este encantamento e os predicados de isenção de custo do Dreadbow. Não conclui factories externas, o combate integrado, o protocolo de sincronização ou o provider integral.

## 1. Identidade e descrição original

- **Provider / versão:** Alex's Caves Continued / `alexscaves`, Minecraft 1.21.1; `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**.
- **JAR SHA-1:** `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; **SHA-256:** `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Recurso:** `data/alexscaves/enchantment/shaded_respite.json`, 362 bytes; SHA-256 `0c5bc4a73c8779c7bc0da2eb47a59e1263ac6c2ef6dead0cbfe5223c73e05872`.
- **Tag de item:** `data/alexscaves/tags/item/enchantable/dreadbow.json`, 48 bytes; SHA-256 `f22db4f6335af0cc185f0478c482c3c666a86afa430f06bdabc78ccc662076d5`; contém somente `alexscaves:dreadbow`.
- **Descrição literal de `en_us.json`:** “Dreadbow will not consume normal arrows or durability if fired in darkness”. Tradução explicativa: disparar o Dreadbow na escuridão pode dispensar o desgaste e o consumo de flechas comuns, conforme os gates abaixo. Não há chave própria no `pt_br.json` examinado.
- **Consumidor:** `server/item/DreadbowItem.class`, SHA-256 `b9cd6e843f923877775e38b89214e8649c10d4d5be704ed9dd377900439d44ae`. **Helper de luz:** `server/potion/DarknessIncarnateEffect.class`, SHA-256 `b591db32bebd79410b62e140f649b194cab3248109e5e6d0f05b855e97f247eb`. Prefixo de classes: `com/github/alexmodguy/alexscaves/`.
- **Provas:** [manifesto individual](../EXACT-SHADED-RESPITE-CONTRACT-1.0.10.json), [reprodução](../EXACT-SHADED-RESPITE-CONTRACT-1.0.10.md), [equipamento Dreadbow](../equipment/dreadbow.md), [Relentless Darkness](relentless-darkness.md) e [Dark Arrow](../damage-types/dark-arrow.md).

A busca de Fieldrefs exatos do campo `SHADED_RESPITE` nos 1.555 classfiles do JAR localizou `ACEnchantmentRegistry` e `DreadbowItem`; não exclui reflexão, transformações ou consumidores externos. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1** e serve apenas de corroboração adjacente. Os parâmetros abaixo pertencem ao binário e aos recursos **1.0.10**.

## 2. JSON, nível e aquisição

| Campo | Valor publisher | Significado / limite |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.shaded_respite` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/dreadbow` | Elegibilidade declarada do equipamento |
| `weight` | `1` | Peso de dados; não é chance de isenção |
| `max_level` | `1` | Apenas I publicado |
| `min_cost` | base `1`, incremento por nível acima do primeiro `9` | Nível I: 1 |
| `max_cost` | base `41`, incremento `10` | Nível I: 41 |
| `anvil_cost` | `8` | Custo do encantamento, separado do disparo |
| `slots` | `mainhand` | Slot declarado nos dados |
| `effects` / `exclusive_set` | Ausentes neste JSON | O comportamento está em Java; ausência local não prova compatibilidade global |

`ACEnchantmentRegistry.<clinit>` liga o literal `shaded_respite` à chave `SHADED_RESPITE` em `@419–425`. `ACCompat.enchantLevel` procura o primeiro nível correspondente na stack atual ou retorna zero, sem clamp próprio ao máximo I ou validação própria de slot/tag. **Qualquer nível positivo habilita o mesmo predicado:** níveis externos II ou maiores não ampliam o limiar de luz, a isenção ou o fallback nesses consumidores.

As quatro tags empacotadas `minecraft:in_enchanting_table`, `minecraft:non_treasure`, `minecraft:on_random_loot` e `minecraft:tradeable` incluem o ID. O scan dos 51 JSONs publisher não encontrou exclusão reversa deste ID. Essas constatações não garantem compatibilidade, obtenção ou dados efetivos do modpack.

O construtor do Dreadbow declara durabilidade **500** e usa o campo `ACItemRegistry.RARITY_DEMONIC`. A receita `data/alexscaves/recipe/dreadbow.json`, linhas literais `" VS"`, `"P S"`, `" VS"`, pede **1 Pure Darkness, 2 Vesper Wings e 3 Shadow Silk** para um Dreadbow. É aquisição do equipamento, sem garantir Shaded Respite no item produzido.

## 3. Elegibilidade: nível e medição de luz

Os dois caminhos de disparo calculam o booleano local:

```text
eligible = enchantLevel(bow, SHADED_RESPITE) > 0
           && !DarknessIncarnateEffect.isInLight(player, 11)
```

O método estático `isInLight(LivingEntity,int)Z` usa **a posição de bloco do veículo raiz** (`getRootVehicle().blockPosition()`) e o Level da entidade recebida. Lê brilho de `LightLayer.BLOCK`; se `canSeeSky(pos)` e `ACCompat.sunAboveHorizon(level,pos)` forem verdadeiros, substitui esse valor por **15**. Retorna `brightness>=threshold`; a negação com threshold 11 exige o **valor calculado `<11`**. Luz artificial, cobertura e montaria são superfícies relevantes; aparência escura na tela ou um efeito visual não é essa medição.

`ACCompat.sunAboveHorizon` lê `Level.getTimeOfDay(1F)`: retorna true para fase **`<0.259F` ou `>0.74F`**, com igualdades falsas. Seu argumento BlockPos não é usado. Os corpos não leem chuva/clima diretamente; a interpretação física de tempo/dimensão e de `canSeeSky` continua delegada à engine. Não converter esses limites em um horário universal.

Chamar o helper da classe Darkness Incarnate **não exige que esse efeito esteja ativo**: o predicado observado não consulta `hasEffect`. A stack e a luz são lidas quando cada caminho alcança o cálculo, não congeladas por `use` no início do carregamento. O booleano capturado é reutilizado no fallback e nos custos daquela invocação; não há nova consulta de luz por cada flecha da salva.

## 4. Gate inicial, fallback e dois caminhos de disparo

`DreadbowItem.use` aceita início de uso com **creative ou munição não vazia**, obtida por `Player.getProjectile(bow)`. Não lê Shaded Respite. Assim, a existência do fallback posterior não comprova início de uso survival sem munição. A seleção efetiva de munição continua delegada à engine/outros sistemas.

| Consumidor | Gates e momento de Shaded Respite | Fallback / limite |
|---|---|---|
| `releaseUsing(ItemStack,Level,LivingEntity,int)V` | Exige Player e `RELENTLESS_DARKNESS<=0`. Calcula a potência nativa, captura elegibilidade Shaded em `@59–84` e só continua se `p>0.1` (`@110–117`) | Seleciona munição em `@136–142`; se elegível e vazia, substitui o local por novo `ItemStack(Items.ARROW)` (`@144–167`). Cria protótipo em `@169–178`; null retorna em `@182`, antes do restante da salva/cobrança |
| `onUseTick(Level,LivingEntity,ItemStack,int)V` | Chama super; exige Player, `RELENTLESS_DARKNESS>0` e `remainingUseTicks%3==0`. Captura elegibilidade Shaded em `@39–63` | Seleciona munição em `@81–87`; fallback comum se elegível e vazia em `@89–112`; factory em `@114–123`. Não repete o gate inicial, não chama `stopUsingItem` por falta de munição e não contém o retorno antecipado de null do release normal |

Shaded Respite não escolhe o modo normal ou Relentless e não cria uma cadência própria. O módulo `%3` pertence ao callback de Relentless, não a uma chance de isenção ou a DPS medido. O item não recebe um segundo cast só porque os dois encantamentos estão presentes.

`createArrow(Player,bow,ammo)` relê `player.getProjectile(bow)` quando o argumento ammo está vazio; usa o ArrowItem dessa stack, ou a factory de `Items.ARROW` se o item não for ArrowItem, e delega a `ArrowItem.createArrow`. Essa factory pode ter comportamento externo; sua existência ou o fallback não garantem protótipo válido, inserção aceita, autoria, hit ou disparo gratuito.

`isConvertibleArrow` testa `instanceof Arrow` e `getColor()==−1`. **É um contrato distinto do teste de custo `ammo.is(Items.ARROW)`**: conversibilidade de uma entidade não concede por si isenção para munição especial. As decisões de criação e configuração de Dark Arrow continuam nos contratos do Dreadbow e do projétil.

## 5. Custos, limites e estado

Para cada invocação que alcança o bloco final de custo, os dois caminhos aplicam a mesma regra:

| Estado no bloco de custo | Pedido de desgaste do arco | Pedido de consumo da munição selecionada |
|---|---|---|
| `Player.isCreative()==true` | Não executa débito nesse bloco | Não executa shrink nesse bloco |
| Survival, Shaded não elegível | `hurtAndBreakUsedHand(bow,1,player)` | `ammo.shrink(1)` |
| Survival, Shaded elegível e `ammo.is(Items.ARROW)` | Pula pedido de desgaste | Pula shrink |
| Survival, Shaded elegível e outra munição | Pula pedido de desgaste | `ammo.shrink(1)` |

No release normal, os custos estão em `@857–899`: creative retorna; o booleano local 9 controla o pedido de desgaste em `@865–874`, e seu valor mais `ammo.is(Items.ARROW)` controlam o shrink em `@877–896`. No callback Relentless, os equivalentes estão em `@340–382`, usando local 6. São cobranças **por salva/callback que alcançou esse bloco**, sem cobrar um item de munição ou um desgaste por cada entidade tentada. A elegibilidade Shaded poupa desgaste também com munição especial, mas a isenção de consumo exige o Item exato `Items.ARROW`.

`ACCompat.hurtAndBreakUsedHand` delega o valor 1 a `ItemStack.hurtAndBreak` no slot da mão em uso. Valor efetivamente aplicado, quebra, shrink de stack vazia, hooks de munição e sincronização pertencem às respectivas fronteiras da engine. O código não usa a aceitação dos spawns como recibo para liquidar os custos. Não conceder Mastery por um débito evitado ou tentativa de spawn sem um resultado autorizado.

Esses consumidores não acrescentam débito próprio de mana, stamina, fome ou XP, nem timer, carga, duração, cooldown ou chance de proc Shaded. O custo de bigorna 8 é dado de aquisição do encantamento, não XP por disparo. A elegibilidade é um booleano local transitório; não há estado persistente próprio de Shaded Respite nesses blocos. Encantamentos, munição e damage conservam a persistência da stack/engine, e os dados de carga/tiro perfeito do Dreadbow têm consumidores separados.

## 6. Parâmetros úteis para perks e autoridade

| Superfície | Contrato individual de Shaded Respite |
|---|---|
| Equipamento / portador | JSON declara Dreadbow/mainhand; os dois consumidores exigem Player e leem a stack recebida. Não presumir que a declaração de slot revalide mão/tag em cada execução |
| Limiar / nível | Nível positivo e luz calculada `<11`, com override de céu/sol para 15; não escala por níveis positivos |
| Munição / custo | Elegibilidade, tipo do item de munição, protótipo conversível e creative são decisões separadas |
| Tempo / frequência | Sem intervalo ou duração próprios. Momento de release e módulo de Relentless permanecem nativos |
| Dano / tipo de dano / targeting / alcance / área / tamanho / velocidade | N/A como modificadores próprios: o ID habilita isenção/fallback; não altera diretamente esses parâmetros nos consumidores identificados. Eles conservam os owners e contratos de Dreadbow/Dark Arrow |
| Estado / persistência | Luz e nível relidos por invocação; booleano sem NBT próprio. Não criar uma segunda contabilização ao salvar/carregar |

Os corpos próprios de `use`, `releaseUsing` e `onUseTick` **não contêm guarda direta `Level.isClientSide`** para as operações descritas. Não concluir exclusividade servidor a partir do callback, nem classificar ausência de guarda local como falha física reproduzida: despacho vanilla, super, factories e inserção no Level mantêm fronteiras externas.

Uma futura perk de custo/condição precisa preservar o gate inicial, a medição na posição correta, o booleano capturado, a cobrança única e a distinção `Items.ARROW`/conversibilidade. O [contrato do equipamento](../equipment/dreadbow.md) também delimita `CUSTOM_DATA`, carga visual e rede; campos/getters públicos ou uma animação positiva não são autorização. Black Arcana, Enshrouded e RPG Skill Tree não recebem um adapter executável nesta ficha. **`NO_MUTATION`**; hooks `NOT_VERIFIED` e QA física `NOT_TESTED`.

## 7. Evidência, contabilidade e QA

O [manifesto individual](../EXACT-SHADED-RESPITE-CONTRACT-1.0.10.json), a [reprodução](../EXACT-SHADED-RESPITE-CONTRACT-1.0.10.md) e os [testes semânticos](../../../../../docs/qa/alexscaves_1010_shaded_respite_cards_test.py) ligam identidade, JSON/registro, gate inicial, predicados de luz, fallback e custos. Os corpos completos selecionados dos helpers e do callback não tornam todo `releaseUsing` completo: esse método tem **391 instruções**, e o recorte sela **janelas locais completas e delimitadas** para entrada/predicado, seleção/factory e custos, mantendo o limite de 256 âncoras por método. Não se declara o CFG integral do release auditado por essas janelas.

As provas anteriores de [Dreadbow](../EXACT-DREADBOW-CONTRACTS-1.0.10.json), [Relentless Darkness](../EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.json) e [Precise Volley](../EXACT-PRECISE-VOLLEY-CONTRACT-1.0.10.json) mantêm seus bytes e escopos. A presença dos consumidores irmãos no mesmo corpo não certifica outro encantamento por associação.

**Contabilidade:** uma ficha individual, **+0 raízes mágicas novas**. `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider integral aberto. As vinte fichas parciais anteriores continuam parciais; não há promoção de Stage.

QA física pendente: luz 10/11, céu/cobertura/fase e root vehicle; níveis 0/I/externos; survival/creative e munição vazia/comum/especial; mudança de luz/stack durante uso; callbacks com Relentless; factories externas/null, reentrada e spawn recusado; mãos, cliente/dedicado, sincronização, save/load, PvP e proteção conforme consumidor. A fila atual é mantida no [crosswalk alfabético](../ENCHANTMENT-PERK-CROSSWALK-1.0.10.md).
