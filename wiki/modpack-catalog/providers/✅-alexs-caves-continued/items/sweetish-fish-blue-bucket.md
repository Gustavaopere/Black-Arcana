# Sweetish Fish Blue Bucket

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

## Identidade e autoridade
`alexscaves:sweetish_fish_blue_bucket`, owner `SweetishFishBucketItem`, factory `ACItemRegistry.lambda$static$151`, Code SHA-256 `2cf146833c4613f3c6038bd925527e834d419dad1399b796fa484062d7341773`. [Registro](../systems/item-registry.md). Alex's Caves Continued 1.0.10, Minecraft 1.21.1/NeoForge/Java21, modlist sibling #19; JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. [Dossiê](../EXACT-LATE-CONCRETE-ITEMS-1.0.10.md), [run/job](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45794089694/job/139820167569), HEAD `27c5bbc7780abbb2efe9bf2c4db615be5d0e7b3c`, dois replays byte-idênticos 425337 bytes, SHA-256 `aa6b3b052b975590f56dd2fa62773fe907346495093ef1842b0405de17b585a2`. Sem dump físico novo.

## Ativação, variante e efeitos
Construtor GummyColors.BLUE; super ModFishBucketItem com ACEntityRegistry.SWEETISH_FISH, ACFluidRegistry.PURPLE_SODA_FLUID_SOURCE, craftRemainder(Items.BUCKET), stacksTo(1); campo color. addExtraAttributes(Entity,ItemStack) @0–20: se SweetishFishEntity, setGummyColor(color) @17; não consulta tag da stack nesse override. appendHoverText delega super, usa color.name().toLowerCase() e componente traduzível GRAY; não é efeito. [Dossiê de baldes](../EXACT-MARINE-FISH-MOTH-1.0.10.md): ModFishBucketItem.checkExtraContent servidor solicita spawn via tipo BUCKET, carrega tag Bucketable e setFromBucket e chama addExtraAttributes; não presumir spawn aceito ou variant persistida. [Registro](../systems/item-registry.md) setup declara FluidContainerDispenseItemBehavior para cada cor; callback de dispenser em [helpers](../EXACT-TERMINAL-ITEM-HELPERS-1.0.10.md). Custo/débito/fluido/placement e recipiente dependem de engine; craftRemainder não prova settlement de uso. Sem dano próprio, mana, cooldown, AOE, targeting ofensivo, Mastery ou owner fixado pelo subclass. Pendentes entidade, variante, NBT, fluido, proteção, callbacks e QA física. NO_MUTATION.

## Recursos e evidência reproduzível
- `assets/alexscaves/models/item/sweetish_fish_blue_bucket.json` SHA-256 `ea5ce7c732353a5e8237f272e40f93cd0b6d7ff4d520894d50e2d6bf5c9752cd`.
Classfile SHA-256 `9fd9bd7b962a79db9251ca238cb6493a3959772a435b4cabbcb1bd6b48297d1c`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lcom/github/alexmodguy/alexscaves/server/entity/util/GummyColors;)V` | 15 | `0964beee8a7b550e67e5f93df776f04138d1ff055d83535ffeca8e109ee74d2e` |
| `appendHoverText(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/item/Item$TooltipContext;Ljava/util/List;Lnet/minecraft/world/item/TooltipFlag;)V` | 18 | `afe7605f44a4ac074d7bae44bda6d8158235b36d4c77fbf96453a15f6dc737cf` |
| `addExtraAttributes(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/item/ItemStack;)V` | 11 | `40ccad96da10e456de182ccc77f76c7b23c6fc222917da7d6357ea9a07933209` |

Limites gerais: inspeção estática do publisher, sem prova de runtime transformado, aceitação de chamadas, compatibilidade ou proteção de mundo. `NO_MUTATION / FAIL_CLOSED / PHYSICAL_QA_NOT_TESTED`.
