# example_roar_ring — item demonstrativo de Ace's Spell Utils 1.2.7.2

**Registry ID:** `aces_spell_utils:example_roar_ring` · **Status:** ⚠️ fonte pinada, não perk-ready.

## Source e comportamento

- [Registro production `ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java), com creative tab apenas dev.
- [`items/example/items/misc/ExampleRoarRingItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/misc/ExampleRoarRingItem.java) define interação de uso.
- **Parâmetros/causalidade:** `RoarHandler.trigger(player, RoarConfig.ring(1.2F,0.18F,0.3F,0.12F,30,Easing.EASE_OUT_QUAD))` ao usar item em lado servidor.
- **Alvo e geometria:** Roar ring VFX, **não é Curios ring equipado** nem entidade/dano registrado.
- **Risco:** O identificador `ring` descreve o visual; não supor spell AoE ou atributo passivo.

## Aceitação

Não cria `AbstractSpell` autônomo, mana nem cooldown de combate. Confirmar runtime do item no JAR `aces_spell_utils-1.2.7.2-1.21.1.jar` (SHA-1 anotado `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`) e cliente/render em modpack Iron's 3.16.3. Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac` usa dependência Iron's 3.16.2. Source/JAR parity **não comprovada**. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `COMPLETE_PERK_READY=false`.
