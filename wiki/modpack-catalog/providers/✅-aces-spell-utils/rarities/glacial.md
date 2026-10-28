# glacial — extensible Rarity de Ace's Spell Utils 1.2.7.2

**Enum symbol declarado:** `ACES_SPELL_UTILS_RARITY_GLACIAL` · **display ID:** `aces_spell_utils:glacial` · **cor de apresentação:** `#4fc6ff`.

[`ASRarities.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/utils/ASRarities.java) declara `EnumProxy<Rarity>` com argumento ordinal `-1` e `UnaryOperator<Style>` que usa a cor indicada. [`src/main/templates/META-INF/enumextensions.json`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/templates/META-INF/enumextensions.json) declara a extensão de enum `net/minecraft/world/item/Rarity`, o símbolo e o proxy `GLACIAL_RARITY_PROXY` com assinatura `(ILjava/lang/String;Ljava/util/function/UnaryOperator;)V`. É um registro de metadata/presentation e não um `DeferredRegister<Item>` ou `AbstractSpell`.

**Target/range/mana/cooldown/dano:** não se aplicam; atribuição a itens depende de subclass e addon. Não inferir bônus mágicos, probabilidades, perks ou mecânica do nome/cor da raridade.

**Proveniência/QA:** source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; JAR `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` não comparado. ExtensibleEnum necessita validar template gerado/loader no artifact. `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`.
