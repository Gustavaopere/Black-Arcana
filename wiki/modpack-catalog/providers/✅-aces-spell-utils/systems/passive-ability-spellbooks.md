# PassiveAbilitySpellbook — livros passivos e presets

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`PassiveAbilitySpellbook.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/curios/PassiveAbilitySpellbook.java) — `items/curios/PassiveAbilitySpellbook.java`
- [`PassiveAbilityUniqueSpellbook.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/curios/PassiveAbilityUniqueSpellbook.java) — `items/curios/PassiveAbilityUniqueSpellbook.java`
- [`SpellbookAbilities.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/SpellbookAbilities.java) — `events/SpellbookAbilities.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`PassiveAbilitySpellbook extends SpellBook` oferece `maxSpellSlots` e `getCooldownTicks()` default 0, mais `tryProcCooldown(Player)` usando o cooldown do item. `PassiveAbilityUniqueSpellbook extends PassiveAbilitySpellbook implements UniqueItem`; recebe `SpellDataRegistryHolder[]` e slots opcionais adicionais, inicializa spell container com presets via `ISpellContainer.create(getMaxSpellSlots(), true, true).mutableCopy()` e `addSpell`. `SpellbookAbilities` registra exemplos de proc para livros demonstrativos, incluindo invocação de Comet em eventos qualificantes.

## Targeting, geometria, custos e duração

Player com item concreto, `SpellDataRegistryHolder` definido no addon e evento de dano do exemplo. Nenhum novo spell automaticamente é registrado pelo helper; o exemplo não é prova de equip/cast para todos os livros.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

`getCooldownTicks=0` no helper base não certifica ausência de cooldown nas subclasses; não reproduzir passivo, entidade Comet ou custo além do handler real. Checar side, equipment lookup, proc damage e titularidade de cast.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
