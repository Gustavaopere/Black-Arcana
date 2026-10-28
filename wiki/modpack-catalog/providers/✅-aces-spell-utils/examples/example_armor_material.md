# example_armor — ArmorMaterial de Ace's Spell Utils 1.2.7.2

**Registry ID:** `aces_spell_utils:example_armor` · **Registry:** `minecraft:armor_material` · **Status:** ⚠️ source-pinned; recurso de armadura, não spell ou perk já implementada.

## Registro, atributos e consumidores

[`ExampleArmorMaterialRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExampleArmorMaterialRegistry.java) registra um `ArmorMaterial` com `DeferredRegister<ArmorMaterial>`; construtor `AcesSpellUtils` chama `ExampleArmorMaterialRegistry.register(modEventBus)` inclusive em production.

- Defense por slot: `HELMET=4`, `CHESTPLATE=9`, `LEGGINGS=7`, `BOOTS=4`.
- Enchantment value: `25`; equip sound `SoundEvents.ARMOR_EQUIP_NETHERITE`.
- Repair ingredient: `ItemRegistry.MITHRIL_INGOT` do Iron's.
- Toughness `3`; knockback resistance `0.1`.
- Texture `ArmorMaterial.Layer(AcesSpellUtils.id("example_armor"))`.
- Consumidor: [`ExampleWarlockArmorItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExampleWarlockArmorItem.java), registrado para os quatro slots em `ExampleItemRegistry`.

**Targeting:** jogador que equipa as peças consumidoras; material não executa cast, dano, projétil ou buff autônomo nem fixa mana/cooldown/duração. Não equivale ao conjunto de quatro items e não deve ser contado como um quinto item de armadura.

## QA e ownership

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR físico documentado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, paridade de bytecode não comprovada. Build source usa Iron's 3.16.2 e modpack 3.16.3. Validar registro do material, armor values, reparo e consistência em servidor. Black Arcana não toma posse desse ArmorMaterial; RPG Skill Tree progressão só por hook real. `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`, `COMPLETE_PERK_READY=false`.
