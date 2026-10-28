# FlatCooldownPassiveAbilityCurio — passivos e bainhas

**Provider:** Ace's Spell Utils `1.2.7.2-1.21.1` · **tipo:** família de API/runtime compartilhado · **estado:** ⚠️ ficha source-pinned, não perk-ready.

## Identidade técnica e fonte

- [`FlatCooldownPassiveAbilityCurio.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/curios/FlatCooldownPassiveAbilityCurio.java) — `items/curios/FlatCooldownPassiveAbilityCurio.java`
- [`SheathCurioItem.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/curios/SheathCurioItem.java) — `items/curios/SheathCurioItem.java`

Pin oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Artefato registrado na modlist: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`; **paridade de bytecode não comprovada nesta tranche**.

## Fluxo causal, estado e parâmetros

`FlatCooldownPassiveAbilityCurio extends SimpleDescriptiveCurio` declara `getCooldownTicks()` abstrato; `tryProcCooldown(Player)` consulta `player.getCooldowns().isOnCooldown(this)` e adiciona `addCooldown(this, getCooldownTicks())` se livre. `SheathCurioItem` é somente subclass abstrata da classe de cooldown, sem poder próprio declarado no corpo de source.

A chave de cooldown é o **Item**, compartilhada entre stacks do mesmo tipo no jogador; o helper retorna true imediatamente após adicionar a duração literal. Não aplica cooldown reduction nem testa equipado, lado servidor, recurso, dano, chance ou sucesso de spawn/efeito. Uma chamada prematura pode consumir o gate antes de o consumidor tentar o efeito; a classe não oferece refund. Tooltip apenas formata a mesma duração ([gate e descrição][curio-flat]).

## Targeting, geometria, custos e duração

`Player` passado pelo consumidor ao chamar `tryProcCooldown`; equipamento/slot precisam ser verificados pelo consumidor. Sem trigger automático de dano, alvo inimigo, range ou proc chance nesta classe-base.

Não há **um registro de `AbstractSpell` próprio** para esta família de helpers. Mana, cooldown, duração, spell level, raio de efeito, damage type, projectile size e consumo dependem da classe consumidora ou de Iron's; somente os parâmetros concretamente declarados acima pertencem ao helper.

## Limites de integração e segurança

O método de cooldown não assegura, por si só, que um proc aconteceu; decisão do addon chama o helper. Não premiar Mastery pela chamada, nem duplicar cooldown em Black Arcana. Slot/efeito da bainha requer subclass e tags do consumidor.

**Black Arcana** permanece autoridade sobre seus próprios casts, domains, rituais, Strain, Corruption e WorldEffectPolicy; **Iron's** permanece autoridade de recursos/casting host; **RPG Skill Tree** apenas de progressão/gates por contrato comprovado. Não duplicar execução de provider. O `build.gradle` do source fixa a dependência Iron's `3.16.2`; o pack informa `3.16.3`. Não há comprovação de compilação/teste desse conjunto de versões.

**Evidência/QA:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Faltam confronto com JAR instalado, contrato host 3.16.3, ordenação dos eventos, datapack/config e QA cliente/servidor. **+0 magias semânticas, +0 certificações estáticas.**

[curio-flat]: https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/items/curios/FlatCooldownPassiveAbilityCurio.java#L12-L41
