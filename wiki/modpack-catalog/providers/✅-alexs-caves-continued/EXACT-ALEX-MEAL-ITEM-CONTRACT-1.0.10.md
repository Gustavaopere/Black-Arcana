# Alex Meal — contrato individual candidato de consumo (1.0.10)

**Estado:** candidato a contrato técnico estático individual, ainda não inserido no ledger; replay e ordem alfabética #1127 pendentes. NO_MUTATION / NOT_VERIFIED / NOT_TESTED / NOT_CERTIFIED; provider OPEN. Escopo: alimento com efeitos declarados; não novo cast nem raiz adicional de efeito.

## Identidade e proveniência

alexscaves:alex_meal, classe com.github.alexmodguy.alexscaves.server.item.AlexMealItem, SHA-256 6b7046627fb4ec7cd5a6e02e6aa6997ed26a0b2133fdeb808ccaf0178c6065da. Minecraft 1.21.1, Java 21, NeoForge 21.1.250 (referência oficial). JAR publisher 1.0.10, 75279314 bytes, SHA-1 6960b299a39a039ac8a5eb9b07be4ad0e3e0a570, SHA-256 36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c. Modlist sibling main 3e39ecd559a6e1ad65502331aa42bb473d2029b8. Censo de 1555 classfiles: estende Item, zero campos e interfaces, zero subclasses nativas. Dois corpos próprios e dois owners com typed refs à classe.

## Ativação, estado e efeitos próprios

Construtor ()V (12 instruções) cria Item.Properties, lê ACFoods.ALEX_MEAL @8, chama ACFoodBuilder.food @11, aplica ACItemRegistry.RARITY_RAINBOW @14–17 (alias EPIC na classe de registry), stacksTo(1) @21, Item.<init> @24. O corpo appendHoverText (16 instruções) adiciona componente traduzível item.alexscaves.alex_meal.desc, estilo cinza e itálico; chama super @30. Não determina dano/efeito de gameplay. Não declara use, finishUsingItem, onUseTick, getFoodProperties ou tick próprios; o contrato de consumo herdado é a referência [ACFoodBuilder](systems/food-builder.md) e [ACFoods](systems/foods.md), não um segundo pipeline.

| Parâmetro | Valor estático e limite |
|---|---|
| FoodProperties | ACFoods.ALEX_MEAL, write @1634, segmento SHA-256 5d291749a752f3e7a004cef7e1cde0a8befd3b166728f0a295c537c095f8f378 |
| Nutrição N | 40 |
| Saturation modifier m | 5F |
| Saturação nominal | ((float)40 * 5F) * 2F = 400F; engine limita FoodData à fome atualizada, não equivale a 400 pontos efetivos |
| Tempo de uso | default 1.6 F s -> 32 ticks na referência; sem fast, sem alwaysEat |
| Recipiente | BOWL via usingConvertsTo |
| CONFUSION | supplier lambda$static$44, p=1F, 200 ticks, amplifier bruto 0 na referência |
| BAD_OMEN | supplier lambda$static$45, p=1F, 48000 ticks, amplifier bruto 0 na referência |
| Pilha | stacksTo(1) solicitado |
| Raridade | RAINBOW -> EPIC, alias local |

Os suppliers são resolvidos durante construção das propriedades, não por jogador. Efeitos vanilla solicitados ao consumidor em LivingEntity.eat e addEatEffect, sorteio servidor u<p e cópia de instância; p=1 não prova aceitação, merge ou resultado final de eventos. CONFUSION e BAD_OMEN são as identidades dos campos vanilla no crosswalk, não status novos do provider; comportamento downstream de cada efeito vanilla permanece escopo externo.

## Targeting, custo e persistência

Alvo da solicitação é a própria entidade que consome, sem consulta de alvo, alcance, AOE, projétil ou dano direto. Ativação por uso de alimento herdado, elegibilidade de fome e propriedades efetivas no engine; não marca alwaysEat. Referência vanilla Player.eat atualiza FoodData, chama pipeline de consumo e faz tratamento do recipiente; ItemStack.consume(1,this) solicita shrink se materiais não infinitos. Sem mana, cooldown mágico, XP, owner persistido ou estado custom da classe. N/A para parâmetros de cast, knockback, world edit e summons. Receita publisher shapeless: duas gingerbread_crumbs, baked_potato, carrot, honey_bottle, cooked_beef e bowl; resultado alexscaves:alex_meal. Não é prova de datapack ativo ou cálculo das sobras de craft. Recurso data/alexscaves/recipe/alex_meal.json SHA-256 a48cca5e2a86829ac32e7e7c949fcbb0a60bb24f3a2ffae8837ca9eb5342a431; modelo visual separado.

## Consumidores e integrações

ACItemRegistry.lambda$static$196()Item cria AlexMealItem @0–7, construtor @4; code SHA e559a38fd03a5f06618574de17f28978ef49c402eaa1abe4c78b8f5ae583a84f. ACItemRegistry.<clinit> @3463 escreve ALEX_MEAL, binding literal já selado no [contrato de registro](systems/item-registry.md). Duas referências de membro selecionadas, sem outras leituras tipadas nativas ao campo ALEX_MEAL no censo do probe. Recursos por caminho contendo alex_meal: model e recipe, não censo de referências textuais indiretas em todos os dados. Classe com zero overrides do caminho de ativação; dispatch externo por Item/ItemStack e engine. Eventos NeoForge Start/Tick/Finish e getFoodProperties(stack,living) são fronteiras reais auditadas no contrato do builder; não são autorização de mutação. Perks de nutrição, duração, amplificador, chance e custo devem preservar objeto FoodProperties compartilhado, consumo único e resultado de efeitos; não reaplicar no Finish. Nenhum hook verificado nem QA física. Black Arcana autoridade mágica, RPG Skill Tree progressão.

## Validação

[Auditor](../../../../docs/qa/alexscaves_1010_alex_meal_item_probe.py), [job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44671670490/job/136073823658) aprovado, relatório SHA-256 7259e2bedc779f0f21574ddb599e06038bd62aa2344d591f34ad89483e34c25e. [Selo](EXACT-ALEX-MEAL-ITEM-CONTRACT-1.0.10.json) fixa corpos, classe, fábrica, censo de consumidores, recursos e crosswalk ACFoods. Os sete eixos acima permanecem **candidatos** até replay e reconciliação da fila. Uma ficha individual de item, sem nova raiz semântica. Ainda não foi inserida no índice/ledger nesta branch para evitar conflito com #1127.
