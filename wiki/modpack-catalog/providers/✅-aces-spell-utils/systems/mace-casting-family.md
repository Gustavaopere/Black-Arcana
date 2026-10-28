# Maces e mace-staves — casting implement

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`MaceCastingItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/MaceCastingItem.java) — `items/weapons/maces/MaceCastingItem.java`
- [`MaceStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/MaceStaffItem.java) — `items/weapons/maces/MaceStaffItem.java`
- [`ImbueableMaceStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ImbueableMaceStaffItem.java) — `items/weapons/maces/ImbueableMaceStaffItem.java`
- [`ActiveAndPassiveAbilityMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ActiveAndPassiveAbilityMaceItem.java) — `items/weapons/maces/ActiveAndPassiveAbilityMaceItem.java`
- [`ActiveAndPassiveAbilityMagicMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ActiveAndPassiveAbilityMagicMaceItem.java) — `items/weapons/maces/ActiveAndPassiveAbilityMagicMaceItem.java`
- [`ExtendedMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/ExtendedMaceItem.java) — `items/weapons/maces/ExtendedMaceItem.java`
- [`PresetImbueMaceItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/PresetImbueMaceItem.java) — `items/weapons/maces/PresetImbueMaceItem.java`
- [`PresetImbueMaceStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/maces/PresetImbueMaceStaffItem.java) — `items/weapons/maces/PresetImbueMaceStaffItem.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`MaceCastingItem extends MaceItem` adiciona ao item o componente Iron's `ComponentRegistry.CASTING_IMPLEMENT`, e a regra de animação de re-equipamento observa mudança de slot. `MaceStaffItem` estende a base, marca `isEnchantable` verdadeiro e valor de enchantment 20. `ImbueableMaceStaffItem` inicializa um `ISpellContainer.create(1, true, false)` em stack de mace-staff sem container. `ActiveAndPassiveAbilityMaceItem` expõe cooldowns ativos/passivos default 0. Outras subclasses na família compõem opções de mace mágica, imbue e presets, não spells registrados.

## Targeting, geometria, custos e duração

Mace ItemStack concreto, consumo e casting Iron's via item; impacto melee, raio, cooldown e comportamento de magia são providos por subclasses/host.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não contar cada subclasse como habilidade. Registrar casting implement não garante cast bem-sucedido nem define magias disponíveis; condicionamentos com Epic Fight e Iron's 3.16.3 exigem teste físico.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. Código-fonte Ace compilou contra Iron's `3.16.2` no build pinado; pack usa `3.16.3` segundo inventário, exigindo teste efetivo.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
