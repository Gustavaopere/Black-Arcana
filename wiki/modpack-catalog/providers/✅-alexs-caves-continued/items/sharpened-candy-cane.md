# Sharpened Candy Cane

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:sharpened_candy_cane`, owner `SharpenedCandyCaneItem`, factory `ACItemRegistry.lambda$static$172`, Code SHA-256 `8566af6220458047a5bcd4b371172601c61fac9f8574338bf463d0220a9469f1`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-LATE-CONCRETE-ITEMS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089694/job/139820167569), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 425337 bytes, SHA-256 `aa6b3b052b975590f56dd2fa62773fe907346495093ef1842b0405de17b585a2`. Sem dump físico novo.

## Ativação, atributos, alimentação e custo
Factory ACFoodBuilder.food(Properties,ACFoods.CANDY_CANE). [ACFoods](../systems/foods.md): N2, m0.1, SUGAR_RUSH p=0.01, 200 ticks; [Food Builder](../systems/food-builder.md) descreve resolução; consumo físico e efeitos aceitos pendentes. Construtor ADD_VALUE ATTACK_DAMAGE +3D e ATTACK_SPEED +4D, via acModifiers MAINHAND e ACCompat.itemAttributes; não confundir modificador com dano ou cadência finais. hurtEnemy delega acHurtEnemy. Se atacante (arg3) é Player não criativo, shrink(1) @23 e ITEM_BREAK @34; outros atacantes não passam esse débito. Knockback target strength 0.15000000596046448D, argumentos de diferença X/Z target−attacker @59, fora da guarda de custo. ServerLevel e !client geram partículas ITEM com stack SHARPENED_CANDY_CANE: posições centrais a meia altura de target/attacker, direção normalizada entre elas escalada pela largura do target×0.6F; sendParticles count15, deslocamentos e velocidade conforme @191–244. Não há hurt próprio nesse corpo, dano depende do ataque herdado. Sem guarda explícita de lado no custo/knockback; partículas separadas. Retorna true. Sem projétil, AOE, mana, cooldown ou Mastery próprios demonstrados. Pendências: engine de atributos/ataque/food, aceitação de knockback, slots, proteção/PvP, mundo e QA. Não duplicar custo ou efeito.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/sharpened_candy_cane.json` SHA-256 `23c6a853fa9a31c85fe571a831f58adcfe274ce293b731c1d6b5a615b62198e5`.
Classfile SHA-256 `e3c3520856d39179f5be0bb8c8ae878db404e1a2ce1cdb3a99a292bf7b099fb5`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;)V` | 30 | `af6f5fea728f38268b4d857741f77f205560d3d4775b97832dc5604fe31d4d5b` |
| `hurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z` | 6 | `24f385150b2c0625d91aac8e3bcf1f2b4e4502740afb2f7514040acaa3d79b45` |
| `acHurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z` | 117 | `846aed2005084fd14dfd24232378a9c34d80c6496806bed40f463a33936b2daa` |
| `acModifiers(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;)Lcom/google/common/collect/Multimap;` | 8 | `3bd5e22a894aa23700f10b1d26dcb897caba1f231d7d9e71e80735a9fd88eb7a` |
| `getDefaultAttributeModifiers(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;` | 8 | `afba6bc090b81b45065246fac7916fc043e383ce018b851b232ae895069d466e` |
| `lambda$getDefaultAttributeModifiers$0(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;` | 4 | `e0b654c4894a46bfed1eac6e45134ec4708967610a893ab2ee931dcd7cf423e9` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.
