# example_loot_bag — objeto demonstrativo de Ace's Spell Utils 1.2.7.2

**Registry ID:** `aces_spell_utils:example_loot_bag` · **Status:** ⚠️ source-pinned; não certificado como perk nem como spell próprio.

## Implementação e parâmetros específicos

- [Registro em `ExampleItemRegistry`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java) invocado em produção pelo construtor do mod; creative tab separadamente dev-only.
- [Classe concreta `items/example/items/misc/ExampleLootBagItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/misc/ExampleLootBagItem.java); consumidor relevante nas bases de Ace/Iron's.
- **Comportamento demonstrado:** `ExampleLootBagItem extends LootBagItem`; loot table `irons_spellbooks:entities/fire_boss`, rarity Cinderous do Iron's, equipamento stack até 8. A classe-base usa loot registry server, cria loot params do jogador e dropa stacks próximos; partículas happy villager se não configurada outra partícula.
- **Targeting / range / duração / custos / tipo de dano / projétil:** `LootBagItem.use` é interação no ItemStack, não cast mágico nem ritual. No modo sobrevivência o código usa `player.getMainHandItem().shrink(1)`, inclusive se interação veio por outra mão.
- **Risco de integração:** Risco source-level de consumir item errado em uso offhand; QA necessária. Não adicionar drops em segundo pipeline de loot.

## Evidência e QA

Revisão `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; instalado anotado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, source/JAR parity ainda não demonstrada. Iron's na dependência source **3.16.2** e no modpack **3.16.3**, compatibilidade host não comprovada. O Black Arcana não substitui código/contratos do addon; RPG Skill Tree só progressão/gates por contrato verificado. Testar registro e fluxo real em servidor, cliente, item context, recursos, sync e efeitos aplicáveis.

`mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `COMPLETE_PERK_READY=false` · **+0 magias registradas**.
