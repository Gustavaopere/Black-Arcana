# example_impact_frame_purple — item visual de exemplo de Ace's Spell Utils 1.2.7.2

**Registry ID exato:** `aces_spell_utils:example_impact_frame_purple` · **Estado:** ⚠️ fonte pinada, efeito visual não homologado como perk/spell.

## Registro, parâmetros e consumidor

- [`ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java) registra este item no `DeferredRegister.Items`, invocado também em ambiente production; a aba criativa é dev-only.
- [Classe concreta `items/example/items/misc/ExampleImpactFrameItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/misc/ExampleImpactFrameItem.java).
- **Comportamento do source:** Registro parametriza `ExampleImpactFrameItem` com cor `0xB532FF` e aberration default zero. `use` de ServerPlayer invoca `ImpactFrameHandler.trigger` com segunda cor preta, `0.55f`, `DEFAULT_THRESHOLD`, `10`, `2`.
- **Targeting/forma/custo/dano/cooldown/duração:** VFX sem range, damage, cooldown ou target agressivo no item.
- **Boundary:** Não somar stacks visual ao pipeline de casting/crit.

## Evidência e bloqueios

Source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão `1.2.7.2-1.21.1`; JAR de instalação anotado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem confirmação classfile. Build source referencia Iron's 3.16.2 e modpack usa 3.16.3. VFX pertence ao renderer do provider, não à autoridade do Black Arcana. Validar player/server lifecycle, payload, estados e render em cliente real antes de usar como base de perks. `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`. Não é `AbstractSpell` registrado.
