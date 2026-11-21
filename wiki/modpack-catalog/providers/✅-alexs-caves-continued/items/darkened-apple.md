# Darkened Apple — `alexscaves:darkened_apple`

**Estado individual** ✅ Contrato técnico estático do publisher 1.0.10. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`, perk executável `NOT_CERTIFIED` e `NO_MUTATION`. O item prolonga Darkness Incarnate ativo. [Selo e reprodução](../EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.md)

## Identidade, descrição e proveniência

A **Maçã Obscura** (nome publisher em pt-BR) é o item consumível `alexscaves:darkened_apple`, class `com.github.alexmodguy.alexscaves.server.item.DarkenedAppleItem` (SHA-256 `58e4bd35322bbedbc654519d8a76577f79d964d498a22d372ea452f683b715cb`), subclasse direta `Item`, zero campos e dois corpos próprios: construtor e `finishUsingItem(ItemStack,Level,LivingEntity)` (Code SHA-256 `6bcad1fc366ded0dc84e2eb54f7ebfe3974913725c1086088f77d7a2a195b622`). O item pede estender Darkness Incarnate da entidade consumidora, mantendo o amplificador; a descrição é inferência do bytecode, não texto oficial.

Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1 / NeoForge / Java 21, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Factory `ACItemRegistry.lambda$static$136` (Code SHA-256 `4804ddcbcc419efb87881c1f26eab54e769a43cb3ca100a843c21b0cbbc8893e`). Prova em [manifesto](../EXACT-DARKNESS-PRESENTATION-DISCOVERY-1.0.10.json), [prova de efeitos existente](../EXACT-EFFECT-CONTRACTS-1.0.10.md) e [ficha Darkness Incarnate](../effects/darkness-incarnate.md).

## Ativação, condições, cálculos e custos

`finishUsingItem(stack,level,livingEntity)` solicita `livingEntity.getEffect(DARKNESS_INCARNATE)` via `ACCompat.effect`, depois lê `ACCompat.food(stack,livingEntity)`. **A alteração requer os dois resultados não nulos**. Quando satisfeitos:

1. calcula `newDuration = existingEffect.getDuration() + 600` (**600 ticks** no inteiro local, equivalente nominal a 30 segundos em 20 TPS);
2. instancia `MobEffectInstance(DARKNESS_INCARNATE, newDuration, existingEffect.getAmplifier())`, sem clamp ou ramo explícito para a representação de efeito infinito;
3. solicita `livingEntity.forceAddEffect(newInstance, null)` e o criterion `ACAdvancementTriggerRegistry.EAT_DARKENED_APPLE.triggerForEntity(livingEntity)`;
4. em todos os ramos retorna `Item.finishUsingItem(stack,level,livingEntity)`. **A chamada herdada é responsável pelo consumo físico conforme engine e condições; não existe `shrink` próprio.**

O código local **não** adiciona Darkness Incarnate quando o usuário não tem esse efeito; também não especifica novo cooldown, dano, alcance ofensivo, AOE, projétil, mana, duração de outra poção ou escalonamento pelo amplificador. O alvo é a própria `LivingEntity` que terminou de comer. O critério de advancement só é disparado por `ACAdvancementTrigger.triggerForEntity` quando o portador é `ServerPlayer`. A aceitação final da atualização de efeito, do avanço e da subtração de stack depende dos consumers/engine; nenhuma QA física foi executada.

O `ACFoods` do publisher define **nutrição 4**, modificador de saturação **0.35F** e `alwaysEat`. São **2,8** de saturação nominal antes dos limites de FoodData. A lista de efeitos alimentares está vazia. A referência do [ACFoodBuilder](../systems/food-builder.md) dá **32 ticks** para o padrão sem `fast`, com possibilidade de iniciar o uso com fome cheia. A raridade solicitada é `RARITY_DEMONIC`, alias de `EPIC`. Receita `data/alexscaves/recipe/darkened_apple.json` do tipo `minecraft:crafting_shaped`, resultado `alexscaves:darkened_apple`, quatro `alexscaves:pure_darkness` e uma `minecraft:apple`, SHA-256 `69ee3d764bbc896ba4b08155f3dd73af7456c0164210f87f7637d488b5dd40a3`. Advancement `eat_darkened_apple` usa gatilho `alexscaves:eat_darkened_apple`, SHA-256 `dd1518ada2aaec6b1c369eb2a467eace0e7ddf447cd79c2d19c89efee9d84d4a`. O padrão empacotado coloca a maçã no centro e os quatro Pure Darkness em cruz. Modelagem e tradução são recursos separados. A receita ativa no datapack está pendente de verificação.

## Persistência, integração e pendências

Não declara campo ou NBT próprio no item. A duração/amplificador são parte da instância do efeito gerida pela engine e pelo provider, com limpeza e voo detalhados na [ficha do efeito](../effects/darkness-incarnate.md); o `forceAddEffect` é **solicitação**, não evidência de efeito aceito em cada contexto. A extensão pode interferir com caps e restauração de voo de outros providers, sem hook de perk certificado.

**Candidatos conceituais a perks:** extensão de duração, custo de craft/consumo e elegibilidade. Não reexecutar `forceAddEffect`, advancement ou consumo pelo Black Arcana; aguardar boundary server-authoritative real. A referência Mojang usa `-1` para duração infinita, portanto a operação local pede `599` ticks nesse caso. Com duração acima de `Integer.MAX_VALUE - 600`, a soma inteira pode transbordar. O construtor recebe o amplificador anterior, usa defaults de apresentação e não transfere a instância oculta. Aceitação da substituição, integração com outras fontes de voo, consumo e QA multiplayer continuam pendentes. [Referência do engine e prova dos sete eixos](../EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.md#referências-do-engine)
