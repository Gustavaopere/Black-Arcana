# Green Soylent

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45748227744/job/139669398914), HEAD `247a4c7adec94b3c99a28fd1aadb668b07dc3ef3`, dois relatórios byte-idênticos de 156.541 bytes, SHA-256 `2bd27341d274f749e8c80b0a0e77e6f37571a92545293d910e7b47deb1cdb945`. [Dossiê](../EXACT-QUARRY-RADIANT-FOOD-1.0.10.md). Sem novo dump instalado ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:green_soylent`; owner `RadiationRemovingFoodItem`; factory `ACItemRegistry.lambda$static$66`, Code SHA-256 `aaf8577259d92e748676d4b3a21900a43c36ee085c844bc9c7f8ddf9185d7ef2`. [Registro](../systems/item-registry.md). Alimento que solicita recuperação de vida condicionada à irradiação. Descrição interpretativa do binário.

## Perfil e ativação

A factory usa ACFoodBuilder.food(Properties, ACFoods.SOYLENT_GREEN); N=3, m=0.35. alwaysEat, meat, sound:HONEY_DRINK; sem efeito declarado pelo builder. use @15 chama ItemUtils.startUsingInstantly, getUseAnimation retorna DRINK, getDrinkingSound e getEatingSound retornam HONEY_DRINK. A identidade é conferida por comparação com GREEN_SOYLENT em cada método. Tempo padrão nominal 32 ticks pela referência FoodProperties; início imediato não é consumo instantâneo. [ACFoods](../systems/foods.md) e [Food Builder](../systems/food-builder.md) têm contratos estáticos próprios; meat/sound não chegam ao builder de FoodProperties; som explícito é do owner quando aplicável. Sem bowl declarado. Quantidade consumida, autoridade de lado, aceite efetivo de efeitos, cancelamento e conversões de recipiente pertencem ao caminho herdado, não verificados fisicamente.

## Recuperação de vida e Irradiated

finishUsingItem(ItemStack,Level,LivingEntity) lê IRRADIATED via ACCompat.effect e getEffect @15, propriedades ACCompat.food @22. Se qualquer um nulo, delega Item.finishUsingItem. Se presentes, calcula min(maxHealth, health + ceil(nutrition×1.5F+1F)), float no produto e soma antes do ceil double; conversão f2d/d2f e Math.min(float,float). Solicita setHealth @70 **antes** de Item.finishUsingItem @77. Recuperação nominal com N=3: +6 HP, limitada à vida máxima; sem leitura de amplifier/duração, sem removeEffect, sem chamada heal. Não há guarda explícita de lado nesse corpo. Não assumir cura de irradiação, execução em vítima remota ou recepção efetiva. [Irradiated](../effects/irradiated.md) documenta cancelamento de LivingHealEvent em não resistentes; setHealth não é a chamada heal aqui, não certifica todos os hooks/eventos externos. O efeito nativo permanece sujeito ao seu próprio lifecycle.

## Integração e pendências

Target é consumidor LivingEntity. Sem projétil, dano, AOE, LOS, mana, cooldown ou XP próprios demonstrados. Não duplicar setHealth, não reexecutar finishUsingItem, não transformar recuperação em remoção/amplifier de status. Verificar engine, alteração de componentes, limites e autoridade do consumo, emissão de eventos, coexistência com efeitos, cancelamento e Mastery. Perks de recuperação/nutrição são apenas conceituais; NO_MUTATION. Advancement eat_radiation_foods declara os três IDs em critérios consume_item; não é prova de cura ou pagamento de Mastery.

## Aquisição declarativa

Sem receita localizada pelo filename no recorte; não é prova de inexistência. Loot/trade e referências transitivas pendentes.

## Localizadores de evidência

Classfile SHA-256 `589f2f1732b353a52aed025d20b29d0f4e8234e58c4cb0fe9072df6a5d975dc4`.

| Método e descritor | Instruções | Code SHA-256 |
|---|---:|---|
| `<init>(Lnet/minecraft/world/item/Item$Properties;)V` | 4 | `405f81f0b51683db4ab14a729fb164a2c889439967d0bfe6248ebe8183a4873d` |
| `finishUsingItem(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;)Lnet/minecraft/world/item/ItemStack;` | 41 | `550d0a5d6b4b79d401fbde187bc6e83f1467035d88784d44135bce79f6d9ec50` |
| `use(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/player/Player;Lnet/minecraft/world/InteractionHand;)Lnet/minecraft/world/InteractionResultHolder;` | 15 | `810904916f3dd43bc1974ab9e157520d1923b9409611687cd3cf7b1f5ad80568` |
| `getUseAnimation(Lnet/minecraft/world/item/ItemStack;)Lnet/minecraft/world/item/UseAnim;` | 8 | `e53be8f21a6e791b319aa27e1a766f828f2a1d7df5c867ec27c4b98d061b054d` |
| `getDrinkingSound()Lnet/minecraft/sounds/SoundEvent;` | 9 | `36a176cc7735c7e2fcb124863d65acf689fb87ec524794370353d877db61304c` |
| `getEatingSound()Lnet/minecraft/sounds/SoundEvent;` | 9 | `01180b25ba8578fc01fdab577670421cbb36a035fabcba9c0a24f9144e71aab5` |

## Evidência complementar — #1235

[Prova nativa](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259/job/139828495853), HEAD `9c16b9c73452706148f666156a815b75696311de`, dois relatórios 765.144 bytes SHA-256 `6c8e0c98af51b60fe40d3bd0b326fb909525f1780b2086740748e158b6bd20ea`; [referência vanilla](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45796533259/job/139828496659), 149.285 bytes SHA `41e941487c560cc8deb700af7952801d31731c83986e56770c13f29d0dea8e67`. [Dossiê](../EXACT-FOOD-IDENTITY-KEYBIND-CLOSURE-1.0.10.md). 1555 classfiles, Fieldref exato e valores JSON; sem inferência de tags transitivas ou modpack transformado. Permanece parcial.

ACCompat.food Code `49c3062c4a6ee9829b530154697caa1dd8dc98766d46b57c24b5f08d61a3ab0c` lê DataComponents.FOOD diretamente da stack @4, não lê LivingEntity. nutrition Code `38bea96f4f8b84f6c701adb5a85836930a6c46a57dd3e9885192ee4d55422781` chama nutrition() @1. Referência vanilla setHealth(F)V Code `e34add7af630cfd86f0b5d3f20d4cf9f3100f0d95568e030c434876a3faa3e43`: clamp 0..maxHealth @13, escrita SynchedEntityData @19; sem chamada heal ou gate vida>0. heal tem gate vida>0 separado. Não estender essa prova a patches externos. Green Soylent: ItemUtils.startUsingInstantly inicia uso e retorna consume result sem finalizar. CommonEvents.livingDie Code `3dd919f82cf80b2b0a9251e34c2e37bfec88b39d913608ae6772d710f06e83e2`, produtor específico de morte com comparação de UUID @454, solicita 1+nextInt(9) unidades @495 e spawnAtLocation @498; não prova drop efetivo nem condição genérica. Identidade do produtor não é parâmetro de perk. Pendentes recursos/loot e patches NeoForge pertinentes.
