# MagicGunItem — invocação do spell selecionado

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`MagicGunItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/MagicGunItem.java) — `items/weapons/MagicGunItem.java`
- [`AcesSpellUtilsServerEvents.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java) — `events/AcesSpellUtilsServerEvents.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`MagicGunItem extends MagicSwordItem`, com `isHeavyGun()` default `true` e getters de cooldown ativos/passivos default `0`. Esses getters alimentam tooltip; a classe não adiciona cooldown real, balística ou munição. No handler `onUseItem(PlayerInteractEvent.RightClickItem)`, light aceita ambas as mãos; heavy só entra em MAIN_HAND. Heavy em offhand não passa por esses ramos ([base][gun-base], [light][gun-light], [heavy][gun-heavy]).

Cada ramo lê a **seleção atual global** do `SpellSelectionManager`; retorna se null/EMPTY e calcula `getLevelFor(selectedLevel, player)`. Não exige que a seleção pertença ao container da arma. CastSource vem da opção selecionada, enquanto o slot de equipamento vem da mão usada: light MAINHAND/OFFHAND por ordinal, heavy MAINHAND. Cada ramo alcançado chama uma vez `attemptInitiateCast(itemStack, spellLevel, level, player, selectionOption.getCastSource(), true, slot)` ([light][gun-light], [heavy][gun-heavy]).

O trecho cliente retorna cedo por mana visual insuficiente/cooldown/aprendizado quando não está conjurando; se já está conjurando apenas solicita CONSUME e **continua** até a tentativa host. Não há gate servidor global no handler. Após a tentativa, true define CONSUME, false FAIL, e o evento é cancelado; retornos anteriores não chegam a esse cancelamento. Isso descreve o fluxo Ace, sem substituir a autoridade servidor/contrato de retorno do Iron's ([light][gun-light], [heavy][gun-heavy]).

## Targeting, geometria, custos e duração

SpellData selecionado pelo jogador e a mão/arma; alcance e alvo são do spell Iron's, não atributos da magic gun por si.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

Não disparar novo cast ao observar `RightClickItem` ou comando de cast do Black Arcana; efeito e custo já são resolvidos na chamada host. Testar ambos os slots, side cliente/servidor, sucesso/falha e compatibilidade com overrides de isHeavyGun.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**

[gun-base]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/weapons/MagicGunItem.java#L15-L68
[gun-light]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L60-L105
[gun-heavy]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L106-L142
