# ImbueableCurioItem e PresetImbueCurio

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`ImbueableCurioItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/curios/ImbueableCurioItem.java) — `items/curios/ImbueableCurioItem.java`
- [`PresetImbueCurio.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/curios/PresetImbueCurio.java) — `items/curios/PresetImbueCurio.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

Ambas herdam `SimpleDescriptiveCurio` e recebem `slotIdentifier` do consumidor; não fixam slot universal. `ImbueableCurioItem` implementa `IPresetSpellContainer`: stack nulo retorna; exige `CurioBaseItem` e ausência de container antes de gravar `ISpellContainer.create(1, true, false)` por `ISpellContainer.set`.

`PresetImbueCurio` recebe `SpellDataRegistryHolder[]`; `getSpells()` resolve a lista uma vez no singleton Item e zera a referência aos holders. Com stack não nulo e sem container, cria **`ISpellContainer.create(1, true, true).mutableCopy()`**, adiciona cada preset com `addSpell(spell, level, true)` e grava `ComponentRegistry.SPELL_CONTAINER` imutável. Portanto esta base declara capacidade **1**, wheel **true**, mustEquip **true** e slots adicionados locked **true**, diferentemente dos presets de staff, cuja capacidade deriva da lista e mustEquip é false. Vários holders não autorizam presumir expansão da capacidade: o resultado de cada `addSpell` e a política de overflow pertencem ao host.

Nenhuma das bases sobrescreve container já presente, faz migração de presets, executa cast ou cobra recurso na inicialização. O cache é do Item, não estado individual do jogador; não usá-lo como armazenamento mutável de perks. QA específica pendente: stack novo/preexistente/null, equip/unequip no slot real, múltiplos presets com capacidade 1, cópia e save/load do component.

## Targeting, geometria, custos e duração

O item curio e a lista de SpellData entregues pelo addon; a seleção/nível dos spells é identificada pelo próprio consumidor, não por Ace como um novo registro.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

O slot, possíveis spells e recursos não são universais; não criar automaticamente um cast, bônus ou mana por equipar e não duplicar os containers de Iron's.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
