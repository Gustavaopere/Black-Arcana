# Diving Boots — `alexscaves:diving_boots`

**Contrato técnico estático** ✅ `STATIC_TECHNICAL_CATALOG_ONLY`, grau `SHA_EXACT_BINARY_BEHAVIOR`. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`, perk executável `NOT_CERTIFIED`, política `NO_MUTATION`. Peça passiva, **+0 raízes mágicas**. [Prova do publisher](../EXACT-DIVING-ARMOR-CATALOG-1.0.10.md)

## Identidade e atributos

`ACItemRegistry.DIVING_BOOTS` registra as Botas de Mergulho. A fábrica `lambda$static$102:()Lnet/minecraft/world/item/Item;` (Code SHA-256 `1c5056eeb3274285c2026d3af92ee741e8706da73774c758904117ccba0c5e31`) constrói `DivingArmorItem(DIVING_SUIT_ARMOR_MATERIAL, ArmorItem.Type.BOOTS)`. O owner tem SHA-256 `6c4ea04559e2e2425bbc842f02cb9a89a2ea9009b7f43e2d71d05c336c64c334` no JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge file **8856293**, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`). [Registro](../systems/item-registry.md) · [Material](../systems/armor-material.md)

O ordinal **3** de `BOOTS` na referência 1.21.1 seleciona defesa **2** e durabilidade **11 × 20 = 220**. Encantabilidade **25**, toughness e knockback do material **0F**. O mapa construído pede `ARMOR +2 ADD_VALUE`. `acModifiers(EquipmentSlot,ItemStack) @0–21` devolve esse mapa para `FEET` e um mapa vazio nos demais slots, sem ler a stack. `getDefaultAttributeModifiers(ItemStack) @0–17` encaminha para o bridge de grupos de slot da `ACCompat`. O ID de modificador é `alexscaves:diving_armor.boots`, formado a partir de `ArmorItem.Type.getName()`. O cliente escolhe `DivingArmorModel` e `diving_suit_0.png` no slot `FEET`. [Referência do enum](../EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.md#referências-do-engine) · [Atributos dinâmicos](../systems/dynamic-attributes.md) · [Renderização da armadura](../systems/custom-armor-post-render.md)

## Colisão do Muck, recebedor e limites

`MuckBlock.isOceanEntity(Entity) @0–57` retorna verdadeiro para tipo na tag `alexscaves:seafloor_denizens` **ou** `LivingEntity` com a stack **exata** de `DIVING_BOOTS` em `FEET`. O ramo de item vale para qualquer entidade viva equipada, independentemente do restante do conjunto. Há dois consumidores distintos desse predicado no bloco `alexscaves:muck`:

| Chamador | Seleção e resultado solicitado |
| --- | --- |
| `getCollisionShape @0–55` | Contexto de colisão com uma entidade que satisfaz o predicado recebe `Shapes.block()`. `FallingBlockEntity` também tem caminho próprio para a forma cheia. O fallback `SHAPE` vem de `Block.box(0,0,0,16,13,16)`. O efeito é na forma de colisão do bloco consultado. |
| `entityInside @0–93` | Para um `LivingEntity`, o corpo exige `getInBlockState().is(this)` antes do ramo de movimento. Com predicado verdadeiro, mantém X/Z, solicita Y igual a `blockPos.y + 1` e acrescenta **+0.1D** ao delta vertical. Com predicado falso, multiplica o delta por **(0.85D, 1D, 0.85D)**. |

A movimentação solicitada pertence ao contato com o bloco e é aplicada à própria entidade processada. O predicado não concede `SWIM_SPEED`, Water Breathing, imunidade genérica de terreno, dano, ataque em área, duração de cast ou alcance remoto. As duas formas do Muck também não alteram diretamente as dimensões do portador. A ordem física de colisão e `entityInside`, a frequência dos callbacks e o resultado depois de integração de movimento dependem do engine. [Prova dos consumidores do Muck](../EXACT-DIVING-ARMOR-CATALOG-1.0.10.md)

## Obtenção e custos

O publisher inclui as botas em `alexscaves:chests/abyssal_ruins` com peso **5** no pool de **8–10 rolls**. A varredura dos resultados de receita empacotados não encontrou produção desse ID. `CommonEvents.onEntityJoinWorld(FinalizeSpawnEvent) @43–134` exige Drowned em `ABYSSAL_CHASM` e quatro slots de armadura vazios antes de qualquer atribuição. O quarto sorteio (`@326–389`) usa `nextFloat() < drowned_diving_gear_spawn_chance` (default **0.2**, faixa **0..1**) para equipar as botas e pedir **0.5F** de drop chance em `FEET`. A tag nativa do fundo do mar contém `minecraft:drowned`, que já pode satisfazer o predicado de Muck sem as botas. O avanço `alexscaves:alexscaves/diving_armor` tem critério `boots` de inventário, e o guia do bioma mostra a peça.

`ACItemRegistry.setup @70` fornece `Ingredient.of(Items.COPPER_INGOT)` ao material. O recurso `repairs_diving_suit_armor` também lista cobre. Os ramos do Muck não cobram mana, stamina, carga, cooldown ou desgaste explícito da peça ao consultar colisão e movimento. A cobrança de durabilidade, o reparo e o drop físico dependem das camadas externas. [Prova de aquisição e reparo](../EXACT-DIVING-ARMOR-CATALOG-1.0.10.md)

## Validação e limites para perks

O selo cobre o item, a tag nativa e o predicado compartilhado pelos dois consumidores. Uma perk de terreno precisa tratar colisão e movimento conjuntamente, preservar entidades da tag e manter a coordenação entre cliente e servidor. O corpo local não homologa substituir o predicado nem reaplicar o impulso. QA física pendente para contato com Muck usando botas em `FEET` e em inventário, tipos da tag, `FallingBlockEntity`, bordas de bloco, troca de equipamento, desgaste e multiplayer.
