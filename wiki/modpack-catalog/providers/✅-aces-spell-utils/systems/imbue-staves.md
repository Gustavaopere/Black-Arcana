# ImbueableStaffItem e PresetImbueStaffItem

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`ImbueableStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/staves/ImbueableStaffItem.java) — `items/staves/ImbueableStaffItem.java`
- [`PresetImbueStaffItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/staves/PresetImbueStaffItem.java) — `items/staves/PresetImbueStaffItem.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`ImbueableStaffItem extends StaffItem implements IPresetSpellContainer`: stack nulo retorna; exige `stack.getItem() instanceof StaffItem` e ausência de container para gravar `ISpellContainer.create(1, true, false)` por `ISpellContainer.set`. É um slot vazio com wheel true e mustEquip false; o container não executa a spell.

`PresetImbueStaffItem` recebe `SpellDataRegistryHolder[]`. `getSpells()` resolve uma lista lazy compartilhada pelo singleton Item, depois zera os holders. Com stack não nulo e sem container, cria `ISpellContainer.create(spells.size(), true, false).mutableCopy()`, adiciona cada spell/nível com **locked=true** e grava o component `ComponentRegistry.SPELL_CONTAINER` imutável. A capacidade é o número de presets; wheel true/mustEquip false são flags do container, sem provar que o host encontra o item em qualquer slot do inventário.

Containers existentes são preservados; não há migração automática, reset nem side-check explícito nestes inicializadores. Não mutar o cache global como perk por jogador. QA pendente: novo/preexistente/null, count/locked, mão e equipamento, cópia/save+load e compatibilidade do casting implement herdado de `StaffItem` com o host efetivo.

## Targeting, geometria, custos e duração

O ItemStack do cajado e spells definidos por quem registra o item, não um cast ou seleção de alvo nativos desta API. A quantidade de slots observada para ImbueableStaffItem é 1; não extrapolar para Preset.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não atribuir staffId, spells, mana, damage, range e cooldown sem classe concreta. Alterar container por UI/perk requer integração com os componentes reais Iron's no host 3.16.3, sem segunda representação de slots.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
