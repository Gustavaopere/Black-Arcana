# Diving Leggings — `alexscaves:diving_leggings`

**Contrato técnico estático** ✅ `STATIC_TECHNICAL_CATALOG_ONLY`, grau `SHA_EXACT_BINARY_BEHAVIOR`. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`, perk executável `NOT_CERTIFIED`, política `NO_MUTATION`. Peça passiva, **+0 raízes mágicas**. [Prova do publisher](../EXACT-DIVING-ARMOR-CATALOG-1.0.10.md)

## Identidade, slot e parâmetros

`ACItemRegistry.DIVING_LEGGINGS` registra as Calças de Mergulho. A fábrica `lambda$static$101:()Lnet/minecraft/world/item/Item;` (Code SHA-256 `eebdd0659953be4bb91c294e3f4a682c85a6f2621e1dd175eb714304ae565b07`) constrói `DivingArmorItem(DIVING_SUIT_ARMOR_MATERIAL, ArmorItem.Type.LEGGINGS)`. O owner tem SHA-256 `6c4ea04559e2e2425bbc842f02cb9a89a2ea9009b7f43e2d71d05c336c64c334` no JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge file **8856293**, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`). [Registro](../systems/item-registry.md) · [Material](../systems/armor-material.md)

O ordinal **2** de `LEGGINGS` na referência 1.21.1 seleciona defesa **5** e durabilidade **16 × 20 = 320**. Encantabilidade **25**, toughness e knockback do material **0F**. O construtor monta `ARMOR +5 ADD_VALUE` e, no ramo exclusivo `LEGGINGS @77–110`, acrescenta **+0.5D ADD_VALUE** para o atributo fornecido por `ACPlatform.swimSpeedAttribute()`, que lê `NeoForgeMod.SWIM_SPEED` (`@0–11`). O valor é uma adição ao atributo. O movimento final depende dos demais modificadores, do meio e do cálculo de deslocamento do motor. [Referência do enum](../EXACT-DARKNESS-ITEMS-CATALOG-1.0.10.md#referências-do-engine)

## Comportamento, recebedor e apresentação

`DivingArmorItem.acModifiers(EquipmentSlot,ItemStack) @0–21` devolve o mapa pré-construído ao consultar `LEGS` e um mapa vazio nos demais slots. A stack não é lida no cálculo. `getDefaultAttributeModifiers(ItemStack) @0–17` chama o bridge `ACCompat.itemAttributes`, que converte o mapa em entradas por grupo de slot. O retorno vazio conta como resposta no bridge e não aciona fallback da superclasse. `ACCompat.attributeModifier` usa o ID `alexscaves:diving_armor.leggings`, formado com `ArmorItem.Type.getName()`. O UUID e o label legados não participam do ID. [Atributos dinâmicos](../systems/dynamic-attributes.md)

A adição é para o portador no slot de pernas, sem teste de fluido, outra peça, alvo remoto ou operação de cast no corpo do item. Os modificadores são estáticos na construção, sem temporizador próprio, área, impacto, dano, projétil ou alteração de hitbox. O renderer escolhe `DivingArmorModel` e, para o slot `LEGS`, `diving_suit_1.png`. Renderização e deslocamento do portador têm owners distintos. [Extensão cliente](../systems/client-extension.md) · [Renderização da armadura](../systems/custom-armor-post-render.md)

## Obtenção e custos

O publisher inclui as calças em `alexscaves:chests/abyssal_ruins` com peso **5** no pool de **8–10 rolls**. A varredura dos resultados de receita empacotados não encontrou produção desse ID. `CommonEvents.onEntityJoinWorld(FinalizeSpawnEvent) @43–134` restringe o fluxo a Drowned em `ABYSSAL_CHASM` com os quatro slots de armadura vazios. O terceiro sorteio (`@262–325`) equipa esta peça quando `nextFloat() < drowned_diving_gear_spawn_chance` (default **0.2**, faixa **0..1**) e pede `setDropChance(LEGS,0.5F)`. As taxas físicas dependem da configuração e da lógica externa de drops. O avanço `alexscaves:alexscaves/diving_armor` usa o critério de inventário `pants`. O guia do bioma mostra a peça.

`ACItemRegistry.setup @70` define `Ingredient.of(Items.COPPER_INGOT)` como ingrediente do material. O recurso `repairs_diving_suit_armor` também lista cobre. O modificador de natação não possui cooldown, reserva de mana, stamina, carga ou desgaste por tick no owner. A cobrança de durabilidade e de reparo permanece no engine. [Prova de aquisição e reparo](../EXACT-DIVING-ARMOR-CATALOG-1.0.10.md)

## Validação e limites para perks

O selo reproduz a ligação entre tipo, atributo e operação, os consumidores, o gate de spawn e os recursos do publisher. Uma perk que altere natação precisa tratar o modificador do slot e a composição com atributos externos, incluindo remoção quando o portador troca a peça. O mapa construído no singleton de item não demonstra isolamento de uma mutação por jogador. QA física pendente para equipar/remover, entrar e sair de água, coexistência com encantamentos de movimento, sincronização e reconexão. Nenhum hook mutador foi validado para essas calças.
