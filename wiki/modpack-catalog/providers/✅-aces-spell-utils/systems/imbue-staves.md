# ImbueableStaffItem e PresetImbueStaffItem

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`ImbueableStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/staves/ImbueableStaffItem.java) — `items/staves/ImbueableStaffItem.java`
- [`PresetImbueStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/staves/PresetImbueStaffItem.java) — `items/staves/PresetImbueStaffItem.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`ImbueableStaffItem extends StaffItem implements IPresetSpellContainer` inicializa `ISpellContainer.create(1, true, false)` quando o stack ainda não é container. `PresetImbueStaffItem` usa `SpellDataRegistryHolder[]` e obtém SpellData por `getSpells()` para inicialização de presets; ambos usam o contrato de containers do Iron's.

## Targeting, geometria, custos e duração

O ItemStack do cajado e spells definidos por quem registra o item, não um cast ou seleção de alvo nativos desta API. A quantidade de slots observada para ImbueableStaffItem é 1; não extrapolar para Preset.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não atribuir staffId, spells, mana, damage, range e cooldown sem classe concreta. Alterar container por UI/perk requer integração com os componentes reais Iron's no host 3.16.3, sem segunda representação de slots.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. Código-fonte Ace compilou contra Iron's `3.16.2` no build pinado; pack usa `3.16.3` segundo inventário, exigindo teste efetivo.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
