# example_armor_leggings — armadura de exemplo Ace's Spell Utils 1.2.7.2

**Item registry:** `aces_spell_utils:example_armor_leggings` · **ArmorItem.Type:** `LEGGINGS` · **defense do material:** `7` · **Estado:** ⚠️ source-pinned, sem perk certification.

## Source, material e atributos

- [Registro de item em `ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java): `ExampleWarlockArmorItem(ArmorItem.Type.LEGGINGS, ...)`, `fireResistant()`, durability `ArmorItem.Type.LEGGINGS.getDurability(40)`.
- [`ExampleWarlockArmorItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExampleWarlockArmorItem.java) usa o material `EXAMPLE_ARMOR`, shader/renderer emissivo em client e o helper `schoolAttributesWithResistance(AttributeRegistry.ELDRITCH_SPELL_POWER, AttributeRegistry.MANA_REGEN,150,0.10F,0.05F,0.05F)`. Os parâmetros são observados, **não** reinterpretados como percentuais garantidos sem ler a implementação do helper.
- [`ExampleArmorMaterialRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/armor/ExampleArmorMaterialRegistry.java): ArmorMaterial `aces_spell_utils:example_armor` com defense `HELMET=4`, `CHESTPLATE=9`, `LEGGINGS=7`, `BOOTS=4`; enchantment value `25`, toughness `3`, knockback resistance `0.1`, repair ingredient `ItemRegistry.MITHRIL_INGOT` do Iron's, equip sound `ARMOR_EQUIP_NETHERITE`.
- **Targeting:** usuário que equipa esta peça; esta definição de item não registra spell, projétil, cast ou raio. Cooldown, mana e duração de efeitos mágicos autônomos: **não há declaração nesta classe**.

## Risco e QA

A classe concreta pode fornecer modificadores por item, mas fórmula/aplicação e scaling do `schoolAttributesWithResistance` devem ser comprovados na versão exata do source/host. Não somar o bônus novamente no RPG Skill Tree nem conceder Mastery por equip. Render é somente cliente, atributos e NBT exigem teste dedicado.

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. JAR anotado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem classfile parity. Iron's upstream build 3.16.2 vs modpack 3.16.3. `physical_qa=NOT_TESTED`, `mutating_hook=NOT_VERIFIED`, `COMPLETE_PERK_READY=false`.
