# ActiveAndPassiveAbilitySwordItem — espadas

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`ActiveAndPassiveAbilitySwordItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/ActiveAndPassiveAbilitySwordItem.java) — `items/weapons/ActiveAndPassiveAbilitySwordItem.java`
- [`ActiveAndPassiveAbilityMagicSwordItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/ActiveAndPassiveAbilityMagicSwordItem.java) — `items/weapons/ActiveAndPassiveAbilityMagicSwordItem.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`ActiveAndPassiveAbilitySwordItem extends ExtendedSwordItem`; `ActiveAndPassiveAbilityMagicSwordItem extends MagicSwordItem`. Ambas expõem `getPassiveCooldownTicks()` e `getActiveCooldownTicks()` com retorno default **0**; método de tooltip mostra descrição. A variante MagicSword recebe `SpellDataRegistryHolder[]` no construtor host.

## Targeting, geometria, custos e duração

Espada concreta, usuário, alvo e SpellData passados por subclass/consumidor; funções base não criam habilidade ativa ou projétil automaticamente.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não converter `0` default em cooldown garantido de qualquer arma real; classes concretas podem sobrescrever. Diferenciar uso da arma, passivo e cast do Iron's para impedir múltiplos gatilhos e recompensas Mastery.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. Código-fonte Ace compilou contra Iron's `3.16.2` no build pinado; pack usa `3.16.3` segundo inventário, exigindo teste efetivo.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**
