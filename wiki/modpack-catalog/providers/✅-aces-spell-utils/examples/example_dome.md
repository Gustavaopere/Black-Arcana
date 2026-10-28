# example_dome — item demonstrativo de Ace's Spell Utils 1.2.7.2

**Registry ID:** `aces_spell_utils:example_dome` · **Status:** ⚠️ fonte pinada, não perk-ready.

## Source e comportamento

- [Registro production `ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java), com creative tab apenas dev.
- [`items/example/items/misc/ExampleDomeItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/misc/ExampleDomeItem.java) define interação de uso.
- **Parâmetros/causalidade:** Em `ServerLevel`, calcula vetor de olhar horizontal e centro à frente do jogador a 12 blocos; quando olhar horizontal quase zero usa offset `(0,0,12)`. Invoca `DomeHandler.trigger(serverLevel, center, DomeConfig.of(0xFF2020,3.0F,200))`.
- **Alvo e geometria:** Visual shell/domínio VFX centrado à frente; argumentos exatos declarados no método, sem proof de colisão, bloqueio ou dano.
- **Risco:** **Não** confundir dome visual com `AbstractDomainEntity` de Ace ou com spell domains autoritativos de Black Arcana; não assumir interação WorldEffectPolicy sem ação física.

## Aceitação

Não cria `AbstractSpell` autônomo, mana nem cooldown de combate. Confirmar runtime do item no JAR `aces_spell_utils-1.2.7.2-1.21.1.jar` (SHA-1 anotado `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`) e cliente/render em modpack Iron's 3.16.3. Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac` usa dependência Iron's 3.16.2. Source/JAR parity **não comprovada**. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `COMPLETE_PERK_READY=false`.
