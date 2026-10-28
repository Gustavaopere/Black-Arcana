# example_gun — objeto demonstrativo de Ace's Spell Utils 1.2.7.2

**Registry ID:** `aces_spell_utils:example_gun` · **Status:** ⚠️ source-pinned; não certificado como perk nem como spell próprio.

## Implementação e parâmetros específicos

- [Registro em `ExampleItemRegistry`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java) invocado em produção pelo construtor do mod; creative tab separadamente dev-only.
- [Classe concreta `items/example/items/weapons/ExampleGunItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/weapons/ExampleGunItem.java); consumidor relevante nas bases de Ace/Iron's.
- **Comportamento demonstrado:** MagicGunItem com preset `BALL_LIGHTNING_SPELL` nível **10**, tier `ASWeaponTiers.EXAMPLE_GUN`, rarity Aquatic; `isHeavyGun()=true`; active/passive cooldowns getters **200 ticks** cada.
- **Targeting / range / duração / custos / tipo de dano / projétil:** `onUseItem` de Ace em `PlayerInteractEvent.RightClickItem` trata arma pesada apenas na mão principal e delega `attemptInitiateCast` à magia Iron's escolhida; não define nova bala mágica ou spell Ace.
- **Risco de integração:** Executar cast outra vez pela perk criaria double mana/cooldown; getters de cooldown do item não comprovam toda execução de runtime do host.

## Evidência e QA

Revisão `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; instalado anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, source/JAR parity ainda não demonstrada. Iron's na dependência source **3.16.2** e no modpack **3.16.3**, compatibilidade host não comprovada. O Black Arcana não substitui código/contratos do addon; RPG Skill Tree só progressão/gates por contrato verificado. Testar registro e fluxo real em servidor, cliente, item context, recursos, sync e efeitos aplicáveis.

`mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `COMPLETE_PERK_READY=false` · **+0 magias registradas**.
