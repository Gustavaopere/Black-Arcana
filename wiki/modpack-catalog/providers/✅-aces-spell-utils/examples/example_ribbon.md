# example_ribbon — item visual de exemplo de Ace's Spell Utils 1.2.7.2

**Registry ID exato:** `aces_spell_utils:example_ribbon` · **Estado:** ⚠️ fonte pinada, efeito visual não homologado como perk/spell.

## Registro, parâmetros e consumidor

- [`ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java) registra este item no `DeferredRegister.Items`, invocado também em ambiente production; a aba criativa é dev-only.
- [Classe concreta `items/example/items/misc/ExampleRibbonItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/misc/ExampleRibbonItem.java).
- **Comportamento do source:** Uso server-side faz toggle `RibbonHandler.isAttached` / `detach` / `attach`. `RibbonConfig` contém `ColorRamp([0x2E1A66,0x66E0FF,0xFFFFFF], LINEAR)`, curvas `(0.18,0.0,EASE_OUT_QUAD)` e `(1.0,0.0,LINEAR)`, argumentos finais `24,true`.
- **Targeting/forma/custo/dano/cooldown/duração:** Ribbon visual anexado ao player; tempo/duração e geometria efetivos dependem do handler/renderer.
- **Boundary:** Render/cleanup multipacket QA; não atribuir hitbox, mana ou cooldown sem código.

## Evidência e bloqueios

Source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão `1.2.7.2-1.21.1`; JAR de instalação anotado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem confirmação classfile. Build source referencia Iron's 3.16.2 e modpack usa 3.16.3. VFX pertence ao renderer do provider, não à autoridade do Black Arcana. Validar player/server lifecycle, payload, estados e render em cliente real antes de usar como base de perks. `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`. Não é `AbstractSpell` registrado.
