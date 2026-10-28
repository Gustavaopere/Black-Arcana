# example_sheath — item de exemplo Ace's Spell Utils 1.2.7.2

**Item ID real:** `aces_spell_utils:example_sheath` · **Categoria:** Curios sheath passiva · **Estado:** ⚠️ fonte comprovada, runtime/QA física não validados.

## Identidade e contrato de execução

- [`ExampleItemRegistry.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ExampleItemRegistry.java): registro `DeferredRegister.Items` da entrada; o mod chama `ExampleItemRegistry.register(modEventBus)` inclusive em produção, independente da aba criativa dev-only.
- [Classe concreta `items/example/items/curios/ExampleSheathCurioItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/example/items/curios/ExampleSheathCurioItem.java) e classes-base do Iron's/Ace referenciadas nela.
- **Comportamento/parametrização demonstrados:** `ExampleSheathCurioItem extends SheathCurioItem`; ao receber `LivingIncomingDamageEvent` com causador `ServerPlayer`, verifica `isEquippedBy`, cooldown de **100 ticks**, e cria `Comet` do Iron's no alvo. Dados do exemplo: `comet.setDamage(5)`, posição alvo Y+7, trajetória `(0.05,-0.85,0)` normalizada, speed `0.045` e explosion radius `4.5`. Atributos equipados: `ENDER_SPELL_POWER +0.10 ADD_MULTIPLIED_BASE`, `EVASIVE +50 ADD_VALUE`, `ATTACK_SPEED +0.05 ADD_MULTIPLIED_BASE`. Rarity `cosmic`.
- **Targeting, range, duração, projétil, cooldown, mana:** Causador lógico ServerPlayer, vítima de incoming damage; Comet é entidade host, não spell novo Ace.
- **Riscos de integração e causalidade:** Proc ocorre em fase incoming, sem guarda explícita de dano liquidado; não atribuir Mastery nem disparar segundo Comet. A soma do Evasive deve respeitar dois caminhos de invulnerability da Ace.

## Proveniência, autoridade e verificações

Fonte `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`; source version `1.2.7.2-1.21.1`. JAR registrado `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`, **não confrontado com bytecode**. Build upstream usa dependência literal Iron's 3.16.2, modpack físico registra 3.16.3. **QA:** confirmar ItemRegistry no JAR, presença no server/client, tags e equip slot reais, eventos, dano final, custos/cooldowns e artefatos VFX onde aplicável. Black Arcana mantém autoridade sobre runtime próprio; RPG Skill Tree gates/perks via contrato real; eventos e recursos do Iron's permanecem host-owned.

**`physical_qa=NOT_TESTED`; `mutating_hook=NOT_VERIFIED`; `COMPLETE_PERK_READY=false`.** Não é um spell standalone registrado na Ace.
