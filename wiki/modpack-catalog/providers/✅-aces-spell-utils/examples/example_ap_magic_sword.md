# example_ap_magic_sword — objeto demonstrativo de Ace's Spell Utils 1.2.7.2

**Registry ID:** `aces_spell_utils:example_ap_magic_sword` · **Status:** ⚠️ source-pinned; não certificado como perk nem como spell próprio.

## Implementação e parâmetros específicos

- [Registro em `ExampleItemRegistry`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java) invocado em produção pelo construtor do mod; creative tab separadamente dev-only.
- [Classe concreta `items/example/items/weapons/ExampleAPMagicSwordItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/weapons/ExampleAPMagicSwordItem.java); consumidor relevante nas bases de Ace/Iron's.
- **Comportamento demonstrado:** `ActiveAndPassiveAbilityMagicSwordItem`, tier `ASWeaponTiers.EXAMPLE_AP_MAGIC_SWORD`, rarity Sculk, presets `TELEKINESIS_SPELL` nível **10** e `ABYSSAL_SHROUD_SPELL` nível **10**; getters cooldown ativo/passivo **200 ticks**.
- **Targeting / range / duração / custos / tipo de dano / projétil:** SpellData e casting pertencem ao host Iron's; item traz slots com spells já registrados em Iron's, não IDs Ace.
- **Risco de integração:** Não assumir que cooldown da subclasse substitui cooldown das magias ou que a arma é um segundo spell provider.

## Evidência e QA

Revisão `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; instalado anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, source/JAR parity ainda não demonstrada. Iron's na dependência source **3.16.2** e no modpack **3.16.3**, compatibilidade host não comprovada. O Black Arcana não substitui código/contratos do addon; RPG Skill Tree só progressão/gates por contrato verificado. Testar registro e fluxo real em servidor, cliente, item context, recursos, sync e efeitos aplicáveis.

`mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `COMPLETE_PERK_READY=false` · **+0 magias registradas**.
