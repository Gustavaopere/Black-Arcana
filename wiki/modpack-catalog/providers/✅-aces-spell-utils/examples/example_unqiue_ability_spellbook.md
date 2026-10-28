# example_unqiue_ability_spellbook — item de exemplo Ace's Spell Utils 1.2.7.2

**Item ID real:** `aces_spell_utils:example_unqiue_ability_spellbook` · **Categoria:** PassiveAbilityUniqueSpellbook (ID typo preservado) · **Estado:** ⚠️ fonte comprovada, runtime/QA física não validados.

## Identidade e contrato de execução

- [`ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java): registro `DeferredRegister.Items` da entrada; o mod chama `ExampleItemRegistry.register(modEventBus)` inclusive em produção, independente da aba criativa dev-only.
- [Classe concreta `items/example/items/curios/ExamplePassiveAbilityUniqueSpellbook.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/curios/ExamplePassiveAbilityUniqueSpellbook.java) e classes-base do Iron's/Ace referenciadas nela.
- **Comportamento/parametrização demonstrados:** **ID registry intencionalmente com typo `unqiue`**; preset `SpellRegistry.ARCANE_SHACKLE_SPELL` nível **5**, **6 slots adicionais** além de 1 slot preset (base total **7**), `MAX_MANA +200 ADD_VALUE`, rarity `accursed`, cooldown passivo **100 ticks**. Em `initializeSpellContainer` define `AffinityData` para Arcane Shackle com valor **2**. `SpellbookAbilities.exampleAbility2` gera Comet com damage **5**, radius **4.5** após evento incoming com item equipado.
- **Targeting, range, duração, projétil, cooldown, mana:** Player equipado, victim do incoming e SpellData preso ao container; não há novo registro de Arcane Shackle nem Comet como spell Ace.
- **Riscos de integração e causalidade:** Não corrigir grafia do ID na documentação ou no resource location; não duplicar passivo de exemplo, nem confundir affinity com tier de magia.

## Proveniência, autoridade e verificações

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; source version `1.2.7.2-1.21.1`. JAR registrado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, **não confrontado com bytecode**. Build upstream usa dependência literal Iron's 3.16.2, modpack físico registra 3.16.3. **QA:** confirmar ItemRegistry no JAR, presença no server/client, tags e equip slot reais, eventos, dano final, custos/cooldowns e artefatos VFX onde aplicável. Black Arcana mantém autoridade sobre runtime próprio; RPG Skill Tree gates/perks via contrato real; eventos e recursos do Iron's permanecem host-owned.

**`physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`.** Não é um spell standalone registrado na Ace.
