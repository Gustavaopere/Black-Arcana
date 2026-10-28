# example_trail — item visual de exemplo de Ace's Spell Utils 1.2.7.2

**Registry ID exato:** `aces_spell_utils:example_trail` · **Estado:** ⚠️ fonte pinada, efeito visual não homologado como perk/spell.

## Registro, parâmetros e consumidor

- [`ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java) registra este item no `DeferredRegister.Items`, invocado também em ambiente production; a aba criativa é dev-only.
- [Classe concreta `items/example/items/misc/ExampleTrailItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/misc/ExampleTrailItem.java).
- **Comportamento do source:** Uso server-side verifica `TrailHandler.isAttached(player)`: se sim, detach; caso contrário attach com `TrailConfig(TrailParticleOptions.of(0x39FF6A,1.0F),3,1.0F,0.05F,0.0F)`.
- **Targeting/forma/custo/dano/cooldown/duração:** Trilha VFX associada ao jogador, alterna no uso; não cria dano, projectile de combate ou cast.
- **Boundary:** Rever limpeza em logout/dimension/death antes de integrar. Não inferir unidades dos números da configuração sem fonte do TrailConfig.

## Evidência e bloqueios

Source `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, versão `1.2.7.2-1.21.1`; JAR de instalação anotado `aces_spell_utils-1.2.7.2-1.21.1.jar` SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` sem confirmação classfile. Build source referencia Iron's 3.16.2 e modpack usa 3.16.3. VFX pertence ao renderer do provider, não à autoridade do Black Arcana. Validar player/server lifecycle, payload, estados e render em cliente real antes de usar como base de perks. `physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`. Não é `AbstractSpell` registrado.
