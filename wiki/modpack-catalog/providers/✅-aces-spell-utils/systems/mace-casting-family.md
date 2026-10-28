# Maces e mace-staves — casting implement

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`MaceCastingItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/MaceCastingItem.java) — `items/weapons/maces/MaceCastingItem.java`
- [`MaceStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/MaceStaffItem.java) — `items/weapons/maces/MaceStaffItem.java`
- [`ImbueableMaceStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ImbueableMaceStaffItem.java) — `items/weapons/maces/ImbueableMaceStaffItem.java`
- [`ActiveAndPassiveAbilityMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ActiveAndPassiveAbilityMaceItem.java) — `items/weapons/maces/ActiveAndPassiveAbilityMaceItem.java`
- [`ActiveAndPassiveAbilityMagicMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ActiveAndPassiveAbilityMagicMaceItem.java) — `items/weapons/maces/ActiveAndPassiveAbilityMagicMaceItem.java`
- [`ExtendedMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ExtendedMaceItem.java) — `items/weapons/maces/ExtendedMaceItem.java`
- [`ImbueableMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ImbueableMaceItem.java) — `items/weapons/maces/ImbueableMaceItem.java`
- [`PresetImbueMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/PresetImbueMaceItem.java) — `items/weapons/maces/PresetImbueMaceItem.java`
- [`PresetImbueMaceStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/PresetImbueMaceStaffItem.java) — `items/weapons/maces/PresetImbueMaceStaffItem.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

| Classe da família (9) | Contrato local observado |
|---|---|
| `ExtendedMaceItem extends MaceItem` | `createAttributes(IronsWeaponTier)` constrói ATTACK_DAMAGE=tier.damage e ATTACK_SPEED=tier.speed como ADD_VALUE, mais `additionalAttributes`, todos MAINHAND. A factory **não é aplicada automaticamente** pelo construtor que recebe só Properties; a mecânica smash é herdada de vanilla. |
| `ImbueableMaceItem extends ExtendedMaceItem` | Recebe Tier, mas não o aplica localmente. Stack null retorna; exige ExtendedMaceItem e ausência de container para criar um slot vazio `create(1,true,false)`. |
| `PresetImbueMaceItem extends ExtendedMaceItem` | Tier também não aplicado localmente; presets lazy dos holders; sem container cria `create(spells.size(),true,false)`, adiciona slots locked=true e grava component imutável. |
| `MaceCastingItem extends MaceItem` | Adiciona `ComponentRegistry.CASTING_IMPLEMENT=Unit.INSTANCE` às Properties. `shouldCauseReequipAnimation` retorna **apenas slotChanged**. |
| `MaceStaffItem extends MaceCastingItem` | `isEnchantable=true`, enchantmentValue **20**, `hasCustomRendering=false`. |
| `ImbueableMaceStaffItem extends MaceStaffItem` | Null retorna; exige MaceStaffItem e ausência de container para um slot vazio `create(1,true,false)`. |
| `PresetImbueMaceStaffItem extends MaceStaffItem` | Presets lazy, capacidade `spells.size()`, wheel=true, mustEquip=false, slots locked=true e component imutável. |
| `ActiveAndPassiveAbilityMaceItem extends ImbueableMaceItem` | Herda o slot vazio; getters de cooldown ativo/passivo **0**, usados no tooltip. |
| `ActiveAndPassiveAbilityMagicMaceItem extends PresetImbueMaceItem` | Herda presets; mesmos getters **0** e tooltip. |

Nas duas variantes active/passive, Shift mostra passivo/.desc, senão Alt mostra ativo/.desc2; não há `use`, `hurtEnemy`, proc ou cooldown executado por esses métodos. Presets resolvem a lista uma vez no singleton Item e descartam os holders; inicializadores retornam para null e preservam containers existentes. Container e marcador de casting são contratos distintos: ExtendedMace/ImbueableMace/PresetImbueMace não adicionam CASTING_IMPLEMENT localmente. Não há mace de exemplo registrado no `ExampleItemRegistry` desta revisão para atribuir dano, presets ou habilidades concretas a estas bases.

## Targeting, geometria, custos e duração

Mace ItemStack concreto, consumo e casting Iron's via item; impacto melee, raio, cooldown e comportamento de magia são providos por subclasses/host.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não contar cada subclasse como habilidade. Registrar casting implement não garante cast bem-sucedido nem define magias disponíveis; condicionamentos com Epic Fight e Iron's 3.16.3 exigem teste físico.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
