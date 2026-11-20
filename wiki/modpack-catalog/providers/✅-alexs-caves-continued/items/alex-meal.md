# Alex Meal — alimento e consumo herdado (1.0.10)

**Contrato estático:** ✅ `CERTIFIED_STATIC_7_AXES` / `STATIC_TECHNICAL_CATALOG_ONLY`. **Runtime/hook mutador:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Perk executável:** `NOT_CERTIFIED`. **Política:** `NO_MUTATION`. Provider `OPEN`; **zero novas raízes mágicas**.

## Identidade e descrição

`alexscaves:alex_meal` é um alimento concreto de Alex's Caves Continued **1.0.10**, classe `com.github.alexmodguy.alexscaves.server.item.AlexMealItem`. Sua classe apenas configura propriedades e tooltip; o consumo utiliza a herança e os componentes de alimento. A descrição técnica não implica cura direta nem um cast próprio.

O JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge **1645389/8856293**, **75.279.314 bytes**) tem SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` e SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Minecraft **1.21.1**, Java **21**, referência oficial NeoForge **21.1.250**. A fonte adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37`, versão 1.1.1, não determina os parâmetros de 1.0.10.

Nome inglês empacotado: **“Alex Meal”**. O tooltip oficial inglês é **“You really live like this?”**, chave `item.alexscaves.alex_meal.desc`; o método próprio pede cinza e itálico. O selo conserva os dois textos e o hash do arquivo de idioma. Essas chaves não constam do `pt_br.json` examinado; isso não é prova sobre todos os idiomas ou traduções externas.

## Construção, registro e parâmetros

Classe SHA-256 `6b7046627fb4ec7cd5a6e02e6aa6997ed26a0b2133fdeb808ccaf0178c6065da`: pai `Item`, zero campos/interfaces e nenhuma subclasse nativa no censo de **1.555 classfiles**. Dois métodos próprios, integralmente inspecionados: `<init>()V` (12 instruções) e `appendHoverText(...)V` (16). Nenhum override próprio de uso, consumo, tick ou alimentação foi encontrado nessa superfície completa.

O construtor cria `Item.Properties`, passa `ACFoods.ALEX_MEAL` a `ACFoodBuilder.food` (`@8/11`), solicita `RARITY_RAINBOW` (`@14/17`) e `stacksTo(1)` (`@20/21`), depois chama `Item.<init>` (`@24`). A fábrica `ACItemRegistry.lambda$static$196()Item` cria o item (`@0–7`). O [registro certificado](../systems/item-registry.md) prova o literal `alex_meal`, o bootstrap 198, a chamada de registro `@3460` e o `putstatic ALEX_MEAL @3463`; aceitação pelo loader continua fora da prova.

| Parâmetro | Pedido estático | Limite |
|---|---|---|
| Nutrição | `40` | A referência de FoodData limita fome a 20; não é cura de 40 HP |
| Modificador de saturação | `5F`, bits `40a00000` | Saturação nominal `((float)40 * 5F) * 2F = 400F`, antes dos clamps |
| Pilha | `stacksTo(1)` | Propriedade solicitada, sem provar componentes efetivos após alterações externas |
| Raridade | `RARITY_RAINBOW → Rarity.EPIC` | Alias nativo; não uma raridade nova |
| Tempo de uso | Default referencial `1.6F` segundos, **32 ticks** | Sem `fast`; não é cooldown ou duração de efeito |
| Elegibilidade de fome | Sem `alwaysEat` | A condição efetiva depende do uso herdado/componentes/engine |
| Recipiente | `BOWL` por `usingConvertsTo` | Conversão de consumo; não confundir com sobras da receita |
| CONFUSION | `lambda$static$44`, `p=1F`, **200 ticks** | Amplifier zero provado na referência vanilla, sem aplicação garantida |
| BAD_OMEN | `lambda$static$45`, `p=1F`, **48000 ticks** | Mesma separação entre argumento, aceitação e ciclo do efeito |

Os dois fornecedores são resolvidos durante a construção de FoodProperties, conforme [ACFoodBuilder](../systems/food-builder.md) e [ACFoods](../systems/foods.md). Seus argumentos não são preparados novamente por jogador. Probabilidade 1 é um pedido de efeito no caminho referencial de servidor `u < p`; não prova aceitação por `addEffect`, fusão com status existente, duração efetiva ou transformação instalada. CONFUSION e BAD_OMEN são efeitos vanilla, sem novas identidades mágicas do provider.

## Targeting, custos, estado e consumo

No consumidor externo de referência, o recebedor é a entidade que come. Esta classe não consulta vítima, LOS, alcance, área, projétil, owner de dano, invocação ou edição do mundo. Dano e cura diretos são **N/A aos dois métodos próprios**; regeneração natural, comportamento downstream dos status e regras de raids não são certificados por esta ficha.

As referências já auditadas descrevem `Player.eat`, `LivingEntity.eat/addEatEffect`, `FoodData` e `ItemStack.consume(1,entity)`: atualização nutricional, efeito no servidor, consumo de uma unidade quando não há materiais infinitos e tratamento do recipiente. São referências oficiais pinadas, não um teste do modpack transformado. Mana, stamina, XP e cooldown mágico não são cobrados por método próprio do item. Custo efetivo, inventário cheio, eventos e overrides externos conservam suas fronteiras.

A classe não declara estado customizado de jogador, NBT, pacotes ou cache. FoodProperties e registries são objetos compartilhados. A presença da stack/entidade no caminho herdado não constitui recibo de consumo nem autorização de Mastery.

## Receita e apresentação empacotadas

`data/alexscaves/recipe/alex_meal.json`, SHA-256 `a48cca5e2a86829ac32e7e7c949fcbb0a60bb24f3a2ffae8837ca9eb5342a431`, declara `minecraft:crafting_shapeless`:

| Ingrediente | Quantidade de entradas |
|---|---:|
| `alexscaves:gingerbread_crumbs` | 2 |
| `minecraft:baked_potato` | 1 |
| `minecraft:carrot` | 1 |
| `minecraft:honey_bottle` | 1 |
| `minecraft:cooked_beef` | 1 |
| `minecraft:bowl` | 1 |

Resultado declarado: `alexscaves:alex_meal`. A receita não prova datapack efetivamente selecionado, aquisição em Survival ou sobras de crafting. O modelo `assets/alexscaves/models/item/alex_meal.json` usa `minecraft:item/generated` e a textura `alexscaves:item/alex_meal`; seu hash é `ec65e1facc6a108db2a86eb33c9c85cd6b9e133e1fb77ccb36817da22881c30d`. Apresentação e tooltip não causam os efeitos de gameplay.

## Integração e validação

Perks podem precisar distinguir **nutrição, saturação, elegibilidade, tempo de uso, probabilidade, amplifier/duração e recipiente**. Esses eixos pertencem a camadas diferentes. Não mutar o objeto global `ACFoods.ALEX_MEAL` para representar um bônus individual. Não reaplicar consumo ou status no evento `Finish`, que a referência posiciona após `finishUsingItem`. Preservar autoridade de servidor, componentes, consumo único e resultado real dos efeitos antes de qualquer adapter.

Black Arcana conserva a autoridade mágica; RPG Skill Tree conserva progressão. Hooks mutadores, sincronização, deduplicação, custo final e Mastery continuam `NOT_VERIFIED`/`NOT_CERTIFIED`. Nenhum Stage ou runtime foi alterado.

[Prova dos sete eixos](../EXACT-ALEX-MEAL-ITEM-CERTIFICATION-1.0.10.md), [selo de certificação](../EXACT-ALEX-MEAL-ITEM-CERTIFICATION-1.0.10.json), [auditor](../../../../../docs/qa/alexscaves_1010_alex_meal_item_certification.py), [regressões](../../../../../docs/qa/alexscaves_1010_alex_meal_item_certification_test.py). A [evidência candidata original](../EXACT-ALEX-MEAL-ITEM-CONTRACT-1.0.10.md) é preservada com seu escopo histórico; não recebe promoção retroativa.

Este certificado cobre o item delimitado e sua composição documental com os contratos prévios. Não certifica engine transformado, componentes/datapacks efetivos, lifecycle inteiro dos efeitos, hooks ou QA física. **Uma ficha individual, zero novas raízes.** Próximo símbolo alfabético: `AlwaysCombinableOnAnvil`.
