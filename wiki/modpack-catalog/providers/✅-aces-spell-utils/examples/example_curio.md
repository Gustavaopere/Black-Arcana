# example_curio — item de exemplo Ace's Spell Utils 1.2.7.2

**Item ID real:** `aces_spell_utils:example_curio` · **Categoria:** Curio predefinido necklace · **Estado:** ⚠️ fonte comprovada, runtime/QA física não validados.

## Identidade e contrato de execução

- [`ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java): registro `DeferredRegister.Items` da entrada; o mod chama `ExampleItemRegistry.register(modEventBus)` inclusive em produção, independente da aba criativa dev-only.
- [Classe concreta `items/example/items/curios/ExamplePresetCurioItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/curios/ExamplePresetCurioItem.java) e classes-base do Iron's/Ace referenciadas nela.
- **Comportamento/parametrização demonstrados:** `ExamplePresetCurioItem extends PresetImbueCurio`; slot `Curios.NECKLACE_SLOT`, preset `SpellRegistry.RAISE_DEAD_SPELL` nível **10**, stack 1 e fire resistance.
- **Targeting, range, duração, projétil, cooldown, mana:** Slot de colar e SpellData do Iron's; summon e duração pertencem a Raise Dead quando consumido.
- **Riscos de integração e causalidade:** Equipar item não autoriza invocação automática nem segundo consumo de mana; exigir container/host real.

## Proveniência, autoridade e verificações

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; source version `1.2.7.2-1.21.1`. JAR registrado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, **não confrontado com bytecode**. Build upstream usa dependência literal Iron's 3.16.2, modpack físico registra 3.16.3. **QA:** confirmar ItemRegistry no JAR, presença no server/client, tags e equip slot reais, eventos, dano final, custos/cooldowns e artefatos VFX onde aplicável. Black Arcana mantém autoridade sobre runtime próprio; RPG Skill Tree gates/perks via contrato real; eventos e recursos do Iron's permanecem host-owned.

**`physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`.** Não é um spell standalone registrado na Ace.
