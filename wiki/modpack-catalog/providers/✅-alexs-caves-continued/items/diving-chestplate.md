# Diving Chestplate — `alexscaves:diving_chestplate`

**Contrato técnico estático** ✅ `STATIC_TECHNICAL_CATALOG_ONLY`, grau `SHA_EXACT_BINARY_BEHAVIOR`. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`, perk executável `NOT_CERTIFIED`, política `NO_MUTATION`. Peça passiva, **+0 raízes mágicas**. [Prova do publisher](../EXACT-DIVING-ARMOR-CATALOG-1.0.10.md)

## Identidade e atributos da peça

`ACItemRegistry.DIVING_CHESTPLATE` registra o Colete de Mergulho. A fábrica `lambda$static$100:()Lnet/minecraft/world/item/Item;` (Code SHA-256 `bb759be18025281f8a946a5f6fd1fe312accf4cf80ecc8b2595dcf7c8f113ff8`) constrói `DivingArmorItem(DIVING_SUIT_ARMOR_MATERIAL, ArmorItem.Type.CHESTPLATE)`. O owner tem SHA-256 `6c4ea04559e2e2425bbc842f02cb9a89a2ea9009b7f43e2d71d05c336c64c334` no JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge file **8856293**, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`). [Registro](../systems/item-registry.md) · [Material](../systems/armor-material.md)

O ordinal **1** de `CHESTPLATE` na referência do engine 1.21.1 seleciona defesa **6** e durabilidade **15 × 20 = 300**. Encantabilidade **25**. O construtor pede `ARMOR +6 ADD_VALUE` (`@51–76`) e entra no ramo `CHESTPLATE @113–144` que acrescenta explicitamente `ARMOR_TOUGHNESS +0 ADD_VALUE`, pois `material.toughness()` devolve **0F**. `material.knockbackResistance()` é **0F** e não aciona o ramo `>0F` (`@145–178`). O tipo de equipamento e os valores são argumentos de atributos, sem fórmula própria de dano mitigado. [Referência do enum](../EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.md#referências-do-engine)

## Aplicação ao slot, recebedor e apresentação

`DivingArmorItem.acModifiers(EquipmentSlot,ItemStack) @0–21` consulta o tipo fixado na construção e devolve o mapa do item para `CHEST`, vazio para outros slots. O corpo não lê a stack nem calcula os atributos a cada tick. `getDefaultAttributeModifiers(ItemStack) @0–17` usa `ACCompat.itemAttributes` para montar o componente por grupo de slot. Um mapa vazio ainda conta como resposta ao bridge. A chamada de fallback da superclasse só ocorre com todos os mapas nulos. O ID de modificador é `alexscaves:diving_armor.chestplate`, formado a partir de `ArmorItem.Type.getName()`. A composição com outros modificadores e a defesa efetiva no portador dependem do engine. [Atributos dinâmicos](../systems/dynamic-attributes.md)

O portador tem resposta de atributo contínua enquanto a peça contribui no slot. Os consumidores tipados deste ID no publisher cobrem registro, aba criativa e inserção no equipamento inicial de Drowned. O censo não encontrou uso desse ID como gate para aplicar Water Breathing, selecionar a movimentação em Muck ou acrescentar `SWIM_SPEED`. Essas funções pertencem a outras peças e não exigem o colete nos ramos comprovados. O colete não declara dano causado, projétil, alvo remoto, AOE, duração de cast, tempo de recarga ou tamanho de hitbox. O cliente seleciona `DivingArmorModel` e a textura `diving_suit_0.png` para `CHEST`. [Extensão cliente](../systems/client-extension.md) · [Renderização da armadura](../systems/custom-armor-post-render.md)

## Obtenção e custos

O publisher inclui o colete em `alexscaves:chests/abyssal_ruins` com peso **5** no pool de **8–10 rolls**. A varredura dos resultados de receita empacotados não encontrou produção desse ID. `CommonEvents.onEntityJoinWorld(FinalizeSpawnEvent) @43–134` testa Drowned em `ABYSSAL_CHASM` e os quatro slots de armadura vazios antes dos sorteios. O segundo sorteio (`@198–261`) equipa o colete se `nextFloat() < drowned_diving_gear_spawn_chance` (default **0.2**, faixa **0..1**), e pede **0.5F** via `setDropChance(CHEST,...)`. A chance de drop final e o valor instalado da configuração dependem do engine e do modpack. O avanço `alexscaves:alexscaves/diving_armor` inclui o critério de inventário `shirt`. O guia do bioma apresenta o item.

`ACItemRegistry.setup @70` atribui `Ingredient.of(Items.COPPER_INGOT)` ao reparo, também indicado no recurso `repairs_diving_suit_armor`. O mapa de atributos não reserva mana, stamina, carga ou desgaste por aplicação. Durabilidade de combate e reparo são regidos pela engine. [Prova de aquisição e reparo](../EXACT-DIVING-ARMOR-CATALOG-1.0.10.md)

## Validação e limites para perks

O contrato estático sela a identidade, o slot, os ramos de construção, o bridge, os consumidores e os recursos do publisher. Perks de defesa ou toughness precisam operar no ciclo real de equipamento e isolar o ID de modificador por jogador, sem alterar o material de registry compartilhado. A QA física permanece pendente para equipar/remover, combates com atributos externos, encantamento, desgaste, reparo, spawn configurado e multiplayer. Nenhum hook mutador foi validado para esse colete.
