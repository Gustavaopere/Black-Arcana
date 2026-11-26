# Primitive Club

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Não constitui nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45745854148/job/139661611420), HEAD `41b0080f4a161c9fa82fdb3dc5ed57c3b77f0d82`, dois relatórios byte-idênticos de 384.061 bytes, SHA-256 `4c9aefbfedf99868ae394f1a77dfaaa85cd3c5e8b6d1554b44ed41a902d569b1`. [Dossiê](../EXACT-ORTHOLANCE-MIXTURE-CLUB-1.0.10.md). Sem novo dump físico ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:primitive_club`; owner `PrimitiveClubItem`; factory `ACItemRegistry.lambda$static$40`, Code SHA-256 `f88517fec12d13fcfc61890e09e7310f0a000ab35eea36adc82ddd7af3bab032`. [Registro](../systems/item-registry.md). Arma contundente com atordoamento nativo. Descrição interpretativa do binário.

## Ativação, parâmetros, targeting e efeitos

Durabilidade 120; enchantment value 1; isEnchantable exige count=1. Atributos MAINHAND ADD_VALUE: +8D ATTACK_DAMAGE; ATTACK_SPEED=min(0F,−3.75F+0.15F×clamp(SWIFTWOOD,0,3)). Não são dano final nem velocidade final. Quatro tabelas estáticas, seleção por stack. [Swiftwood](../enchantments/swiftwood.md).

hurtEnemy → acHurtEnemy pede desgaste 1 MAINHAND. Servidor: nextFloat do alvo <0.8F tenta Stunned 150+nextInt(150) ticks, amp0, ambient/visible/icon false. Se addEffect aceito, envia notificação visual, escolhe som HIT; caso contrário MISS. Dazing Sweep positivo e efeito inicial aceito: f=L+1.2F, AABB.ofSize na posição do alvo primário com lado f, consulta Entity.canBeHitByProjectile, exclui alvo primário e candidatos aliados ao atacante, exige distanceTo<=f e LivingEntity. Por secundário, pede mobAttack(attacker) 1F e Stunned 80+nextInt(80) ticks, mesmo se hurt falhar. Sem nova chance de 80% por secundário; sem teto numérico próprio. [Dazing Sweep](../enchantments/dazing-sweep.md) e [Stunned](../effects/stunned.md). Bonking atua na morte/loot em CommonEvents, não no corpo de Club; ver [Bonking](../enchantments/bonking.md).

onLeftClickEntity retorna true quando attackStrengthScale(0)<0.95D ou attackAnim!=0. onEntitySwing de Player retorna true quando strength<1 e attackAnim>0; demais caminhos Player escrevem swingTime=-1 e retornam false. acInventoryTick de Player selecionado, strength<0.95 e attackAnim>0, decrementa swingTime (offset50). Isso é gate/estado de animação, não duração fixa de cooldown. mineBlock destroySpeed!=0 pede desgaste 2; material extra de reparo HEAVY_BONE. Receita 2 cycad + heavy_bone.

## Integração e pendências

Sem mana, projétil ou AOE persistente próprios demonstrados. Stunned é lifecycle nativo do efeito; Bonking altera loot nativo em contrato separado. Candidatos: atributos, chance, duração, custo e alcance do sweep; manter caps e não duplicar hit, efeito, loot ou Mastery. Eventos de melee, ordem e cancelamento de swing, effective attack speed, reparo, integração com terceiros e QA física permanecem não verificados.

Receita empacotada `data/alexscaves/recipe/primitive_club.json`, SHA-256 `b93f005c5632388ca6f34e3a114a8e0a4cf1c2ae99ae9bb0ed2edc2c73dddcc0`; ingredientes ver padrão acima. Não garante aquisição efetiva.

## Localizadores de evidência

Classfile SHA-256 `92bfb58cb5ed2c84dd6f989afad22c98209542889e30b6214c502dbff42fa1ac`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;)V` | 22 | `8d6f357f2ff073f1472f344523f26c27416a1f6dc5a4c251b26247b916538eac` |
| `getStatsForEnchantmentLevel(I)Lcom/google/common/collect/ImmutableMultimap;` | 33 | `9c31676befa4395ff3870a4da211519bdfc6f7c3e3ea36517372c6c1ad5c40db` |
| `getEnchantmentValue()I` | 2 | `95ef737cd8a13db65e3eb3c18e8816a5179dcbdf341309522ab00e95d5aae6d2` |
| `isEnchantable(Lnet/minecraft/world/item/ItemStack;)Z` | 8 | `b5b80a3a9ce3fa19f117440d689591e78db5d712b5d4085aae038d6fe1f1c5bb` |
| `hurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z` | 6 | `aa77f82a10305a6ad440520c5df2da56f82ade5b08915ca7917ff2d38c2c60e3` |
| `acHurtEnemy(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z` | 171 | `2dfe1ed79d983af9d5192c7ad0f651631aa2577b98f8a54bd30a3bf92954c67f` |
| `mineBlock(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/level/block/state/BlockState;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/entity/LivingEntity;)Z` | 15 | `9167ee2256d02c59215cfb15bedfe5c57fca4c08476b486fdbd5ba0c9fca3111` |
| `acExtraRepairMaterials()[Lnet/minecraft/world/item/Item;` | 9 | `4b5705437ef1cc51db983eb6ee32a6cf2d1a2615e35ae52d58c3f80210e1a42d` |
| `isValidRepairItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/ItemStack;)Z` | 13 | `9378b5970892fb11c24e8695db43f1e5b9bed907a20ace6049576f3fa74d4bc6` |
| `acModifiers(Lnet/minecraft/world/entity/EquipmentSlot;Lnet/minecraft/world/item/ItemStack;)Lcom/google/common/collect/Multimap;` | 17 | `4ac265cccbde09cbcd95261bd83e24b2f226434f5970fb0ef078f2152a696c81` |
| `getDefaultAttributeModifiers(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;` | 8 | `aa1a2da7c087aeb50186b7c81b96baf6ce433a8db3ae6b4f905ab4f24d3b8a96` |
| `initializeClient(Ljava/util/function/Consumer;)V` | 6 | `c8d0b31b2bcc9dc0cc0163ca26fe176a53a2229a95d6f45c91748c001627062e` |
| `onLeftClickEntity(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/entity/Entity;)Z` | 16 | `75e83d6fe7dd4728cb7f87ae628e4f97ed334f009b014cf49a03930f43199aec` |
| `onEntitySwing(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;)Z` | 24 | `f16063b00ac8e4db92a30a2f65f2f5d928538b4bf04637f1876ee219be75ab7d` |
| `acInventoryTick(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/Entity;Z)V` | 27 | `1a322e4d6ab62679b0be78b1585524fe130e7a06ddafd5818302db7dfd6aa078` |
| `lambda$getDefaultAttributeModifiers$0(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/component/ItemAttributeModifiers;` | 4 | `3e9eb4a444f406ea4a2ad6d5f730249e5a94b88f4e5a8da71f58f2ad166500a0` |
