# ACFoodBuilder — construção de propriedades de alimentação (1.0.10)

**Contrato técnico estático:** ✅ CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY, candidato ao merge #1120. **Hook:** NOT_VERIFIED. **Runtime transformado:** NOT_VERIFIED. **QA física:** NOT_TESTED. **Perk:** NOT_CERTIFIED. **Policy:** NO_MUTATION. Provider OPEN, +0 raízes mágicas.

## 1. Identidade e escopo

Helper de construção de `FoodProperties`, não feitiço nem alimento registrado individualmente. Descrição editorial própria. Provider alexscaves, Minecraft 1.21.1, Java 21, NeoForge físico 21.1.250. JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge 1645389/8856293), 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Classe `com.github.alexmodguy.alexscaves.server.item.ACFoodBuilder` SHA-256 `e9f064e00c45b84250c3cc88e6150810b160495f209f89aa9c8a423bbee17493`; record interno Effect SHA-256 `d3bb61ebe47a9b01b37f88bb691bfd2ce548f4ac08245f725840db56c3a11e87`. Censo completo de 1.555 classfiles quanto às referências tipadas aos três símbolos de alimentação e ao record. [Prova](../EXACT-FOOD-BUILDER-CONTRACT-1.0.10.md) e [selo](../EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json).

## 2. API nativa e estado

| Método | Entrada e saída | Efeito estático |
|---|---|---|
| of() | ACFoodBuilder | Novo objeto; construtor cria ArrayList de efeitos |
| nutrition(I) | builder | Escreve int @2, sem clamp local |
| saturationMod(F) | builder | Escreve float @2, sem clamp local |
| alwaysEat(), fast(), bowl() | builder | Liga flag correspondente @2 |
| meat() | builder | Liga flag meat @2; não lida em resolve |
| sound(SoundEvent) | builder | Armazena referência @2; não lida em resolve |
| effect(Supplier,F) | builder | Cria record Effect(instance,probability) @10; append @13 |
| resolve() | FoodProperties | Cria builder vanilla, repassa campos/flags, resolve suppliers e retorna propriedades |
| build() | FoodProperties | resolve @1, Map.put(properties,this) @10, retorna propriedades @17 |
| food(Item.Properties,FoodProperties) | Item.Properties | Encaminha argumentos para Properties.food @2 |

O construtor não atribui outros campos explícitos: defaults JVM: nutrition=0, saturationMod=0F, flags false, sound null; effects lista nova. `BUILT` é privado static final Map, inicializado com IdentityHashMap em clinit @0–7. Não é um cache de consulta comprovado: build insere identidade do objeto produzido, sem lookup/clear em qualquer método declarado; no censo de Fieldref publisher não há referência externa tipada a BUILT, meat ou sound. Ausência de reflexão/mixins externos não é comprovada. Não usar esse mapa global como estado de jogador. Effect é record com supplier + probability float; demais métodos são acessores e métodos de Record por ObjectMethods, sem cast ou efeito temporizado.

## 3. Causalidade e parâmetros

`resolve()FoodProperties` (53 instruções, Code SHA-256 `689f9ff3124509b8d43d3467a0708029bf06b983e18b5b38369a57cd8e8944d4`): nutrition @8–11, saturationModifier @15–18; se alwaysEat, alwaysEdible @30; se fast, fast @42; se bowl, Items.BOWL/usingConvertsTo @54–57. Itera a lista @61–111: obtém supplier @92, chama Supplier.get @95, converte para MobEffectInstance @100, carrega probability @104, chama Builder.effect(MobEffectInstance,float) @107; Builder.build @115. A resolução é **eager**, não sorteio na ingestão ou supplier específico de jogador. Não há deduplicação, validação de magnitude/probabilidade ou controle de exceções próprio nesse método. Os campos meat e sound não chegam ao builder de FoodProperties.

Referência oficial Mojang vanilla 1.21.1 (não runtime instalado): FoodConstants.saturationByModifier(IF)F calcula `((float)nutrition * saturationModifier) * 2F`, nessa ordem em float; FoodProperties.Builder.build chama @8. Tempo padrão 1.6F s; fast grava 0.8F s; FoodProperties.eatDurationTicks aplica fmul 20F e f2i (32/16 ticks nominais). alwaysEdible configura canAlwaysEat; usingConvertsTo cria Optional de ItemStack; effect adiciona PossibleEffect. Nenhum desses parâmetros representa dano, mana, cooldown mágico ou duração de um MobEffect. Duração, amplifier e tipo do efeito pertencem ao supplier nativo específico: consultar [Sugar Rush](../effects/sugar-rush.md) e [Irradiated](../effects/irradiated.md), sem recontar suas raízes.

## 4. Produtores e consumidores identificados

ACFoods possui 63 campos FoodProperties; clinit tem 63 chamadas de of/nutrition/saturationMod/build, 46 de effect, 6 fast, 6 bowl, 5 meat, 3 alwaysEat e 3 sound. São **campos/chamadas**, não 63 magias, 46 efeitos distintos ou inventário de itens completo. Contrato individual de ACFoods e conteúdos permanece pendente. Bridge food: ACItemRegistry 40 callsites, ACBlockRegistry 1, construtores AlexMealItem, BiomeTreatItem, DarkenedAppleItem, HotChocolateBottleItem, JellyBeanItem 1 cada. Os registries e os equipamentos têm auditoria própria; não inferir elegibilidade, receitas ou IDs a partir de contagem de callsites.

| Camada externa (referência oficial) | Comportamento |
|---|---|
| NeoForge IItemStackExtension.getFoodProperties(LivingEntity) | virtual Item.getFoodProperties(stack,living) @16 |
| NeoForge IItemExtension.getFoodProperties | default lê DataComponents.FOOD @1–4; permite referência de entidade na assinatura, não na implementação default |
| Vanilla Item.use | food ausente -> pass; quando presente, Player.canEat(canAlwaysEat) @31; true inicia uso/consume result, false fail |
| Vanilla Item.getUseDuration / finishUsingItem | consulta propriedades, duração ou 0; finish chama LivingEntity.eat se presentes |
| Vanilla Player.eat | FoodData.eat @5 antes da super @87; stats e advancement; retorno de recipiente descrita abaixo |
| Vanilla LivingEntity.eat | sound nativo, addEatEffect @53, stack.consume(1,this) @59, GameEvent.EAT |
| Vanilla LivingEntity.addEatEffect | retorna antes do loop no client; u=nextFloat @47, p=probability @54, compara u<p; copia efeito por PossibleEffect.effect @64 e solicita addEffect @67, descarta booleano |
| NeoForge EventHooks | Start/Tick postam evento e retornam -1 se cancelado, senão duração; Finish posta após finishUsingItem e retorna resultStack |

NeoForge userdev Item e LivingEntity substituem acessos diretos ao componente FOOD por getFoodProperties(stack/living); FoodProperties patch adiciona efeito por Supplier, mas ACFoodBuilder chama a sobrecarga de **instância**: patch encapsula a instância recebida em supplier; PossibleEffect.effect retorna cópia de MobEffectInstance. Não reexecuta o supplier original do ACFoodBuilder por consumo. Referência vanilla não prova implantações modificadas, aceitação de addEffect nem ordem de listeners.

## 5. Custos, targeting, owner e persistência

Builder não consome stack, XP, mana ou stamina. Na referência vanilla FoodData.eat lê nutrition/saturation e add: foodLevel = clamp(foodLevel+nutrition,0,20), saturationLevel = clamp(saturationLevel+saturation,0,foodLevel atualizado). LivingEntity solicita consume(1,this); ItemStack.consume não chama shrink quando entidade com materiais infinitos; caso contrário shrink(amount). Player com usingConvertsTo presente e sem materiais infinitos: se stack resultante vazia, retorna uma cópia do recipiente; se não vazia e servidor, solicita Inventory.add da cópia (retorno ignorado). Isso é referência, não garantia de inventário cheio ou override de item.

Alvo externo: entidade consumidora, não caster em combate; AOE, LOS, projéteis, dano/tipo, HP, cooldown, duração de efeito e Mastery N/A no helper de construção. Sem campos próprios de mundo, NBT, rede, owner ou XP; mapa BUILT e lista são estado JVM, não persistência de jogador. Fusão de componentes, reload, resolução de efeitos e liquidação de consumo em execução instalada não verificados.

## 6. Perks e limites

Black Arcana conserva autoridade do runtime mágico; RPG Skill Tree é provider de progressão. Possibilidades conceituais separadas: nutrição/saturação, duração de uso, condicional de fome, chance de efeito, magnitude/duração de MobEffect, recipiente. Não mutar o builder/BUILT global por jogador, não modificar a stack inteira para alterar um parâmetro e não reaplicar efeito no Finish: evento ocorre depois de finishUsingItem, podendo duplicar benefício ou consumo. getFoodProperties e eventos de uso são superfícies reais da referência NeoForge, não contratos de mutação homologados. QA física, compatibilidade, sidedness instalada, ownership/segurança, custos e deduplicação permanecem NOT_VERIFIED/NOT_TESTED. NO_MUTATION/fail-closed.

## 7. Validação

[Relatório e prova](../EXACT-FOOD-BUILDER-CONTRACT-1.0.10.md), [manifesto](../EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json), [auditor nativo](../../../../../docs/qa/alexscaves_1010_food_builder_probe.py), [auditor de referência](../../../../../docs/qa/alexscaves_1010_food_builder_reference.py), [regressões](../../../../../docs/qa/alexscaves_1010_food_builder_probe_test.py). Nativo SHA-256 `e6453ae5631a104314f67c9d9e337cced60da511e56f226b2b13fb4f39054a77`; referência `7eeb6cfcb82dbe38406c5c5241d6955a10826a66610fe8d1d732e7906189fb50`. CI final obrigatória antes do merge. Próximo símbolo sem disposição ACFoodPropertiesItem. ACFoods, alimentos específicos, conteúdos do modpack e suas mutações permanecem abertos. 
