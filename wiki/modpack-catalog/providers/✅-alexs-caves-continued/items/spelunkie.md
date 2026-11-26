# Spelunkie

**Estado:** ⚠️ PARCIAL / STATIC_DISCOVERY_ONLY. `static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; NO_MUTATION`. Sem nova raiz semântica certificada.

**Autoridade:** Alex's Caves Continued (alexscaves) 1.0.10, Minecraft 1.21.1 / NeoForge / Java 21; modlist sibling #19. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. [Replay](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45748227744/job/139669398914), HEAD `247a4c7adec94b3c99a28fd1aadb668b07dc3ef3`, dois relatórios byte-idênticos de 156.541 bytes, SHA-256 `2bd27341d274f749e8c80b0a0e77e6f37571a92545293d910e7b47deb1cdb945`. [Dossiê](../EXACT-QUARRY-RADIANT-FOOD-1.0.10.md). Sem novo dump instalado ou configuração efetiva.

## Identidade e descrição funcional

`alexscaves:spelunkie`; owner `RadiationRemovingFoodItem`; factory `ACItemRegistry.lambda$static$64`, Code SHA-256 `1ee7980eccd745100779b6563c43ddf9cb8c0f8184a61b2d52b8c7bee1f6a338`. [Registro](../systems/item-registry.md). Alimento que solicita recuperação de vida condicionada à irradiação. Descrição interpretativa do binário.

## Perfil e ativação

A factory usa ACFoodBuilder.food(Properties, ACFoods.SPELUNKIE); N=2, m=0.1. fast; sem efeito declarado pelo builder. use e sons delegam caminho normal, animação EAT. Tempo nominal 16 ticks pela referência FoodProperties. [ACFoods](../systems/foods.md) e [Food Builder](../systems/food-builder.md) têm contratos estáticos próprios; meat/sound não chegam ao builder de FoodProperties; som explícito é do owner quando aplicável. Sem bowl declarado. Quantidade consumida, autoridade de lado, aceite efetivo de efeitos, cancelamento e conversões de recipiente pertencem ao caminho herdado, não verificados fisicamente.

## Recuperação de vida e Irradiated

finishUsingItem(ItemStack,Level,LivingEntity) lê IRRADIATED via ACCompat.effect e getEffect @15, propriedades ACCompat.food @22. Se qualquer um nulo, delega Item.finishUsingItem. Se presentes, calcula min(maxHealth, health + ceil(nutrition×1.5F+1F)), float no produto e soma antes do ceil double; conversão f2d/d2f e Math.min(float,float). Solicita setHealth @70 **antes** de Item.finishUsingItem @77. Recuperação nominal com N=2: +4 HP, limitada à vida máxima; sem leitura de amplifier/duração, sem removeEffect, sem chamada heal. Não há guarda explícita de lado nesse corpo. Não assumir cura de irradiação, execução em vítima remota ou recepção efetiva. [Irradiated](../effects/irradiated.md) documenta cancelamento de LivingHealEvent em não resistentes; setHealth não é a chamada heal aqui, não certifica todos os hooks/eventos externos. O efeito nativo permanece sujeito ao seu próprio lifecycle.

## Integração e pendências

Target é consumidor LivingEntity. Sem projétil, dano, AOE, LOS, mana, cooldown ou XP próprios demonstrados. Não duplicar setHealth, não reexecutar finishUsingItem, não transformar recuperação em remoção/amplifier de status. Verificar engine, alteração de componentes, limites e autoridade do consumo, emissão de eventos, coexistência com efeitos, cancelamento e Mastery. Perks de recuperação/nutrição são apenas conceituais; NO_MUTATION. Advancement eat_radiation_foods declara os três IDs em critérios consume_item; não é prova de cura ou pagamento de Mastery.

## Aquisição declarativa

`data/alexscaves/recipe/spelunkie.json` SHA-256 `8761dd34f821ab4be7053432b242b7e2658ff7435cb1151f945269ec370f6773`. alexscaves:sulfur_dust, minecraft:sugar, minecraft:sugar Resultado count=2. Não garante aquisição no modpack.

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
