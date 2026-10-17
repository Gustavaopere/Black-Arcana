# Weald Walker — Ars Morph 2.0.0 / Identity2 ability

**Status: ✅ fonte por habilidade documentada · ⚠️ runtime e JAR físico pendentes · ⛔ perks sem contrato homologado.** Habilidade provider-native Identity2; NÃO constitui novo glifo, cast root Black Arcana ou forma independente de mana. `ars_morph-1.21.1-2.0.0.jar` SHA-1 físico documentado `68ff47cc58c0ffe9570bb907f65c2910311ed45f`; release-aligned source `Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`. Fatos abaixo **SOURCE_CAUSALITY**, não comparação de bytecode do JAR.

## Registro e valores do pack source-pinned

- **Identidade da habilidade/forma:** `ars_nouveau:weald_walker` (ID de Ars ou Ars Elemental/Identity2, **não** `ars_morph:*` spell).
- **Config de Identity2 no arquivo de atribuição:** `cooldown=100`, `use_duration=20`. São **inteiros brutos nos JSONs upstream**; a interpretação da unidade (ticks, segundos), consumo no cancelamento, skill gates e sincronização são do Identity2 **2.2.4**, ainda não medidos no runtime do pack.
- **Admissão:** Identidade ativa deve ser uma instância de `WealdWalker`; o registry usa um ID literal (`ars_nouveau:weald_walker`) e cinco atribuições de variante compartilham esse `predef`.

## Matriz causal para perks

| Eixo | Observação fixa em source | Status de adaptação |
|---|---|---|
| Entrada | `MorphBoundAbility.execute(Entity host)` exige que host seja `Player`, `IdentityApi.getCurrentMorph(player)` não-null e seja instância da classe esperada; exceptions em `use` são capturadas/logadas. | `⛔` Não transpor gate de morph ou duplicar os eventos do Identity2. |
| Efeito ativo | SpellCaster do Weald Walker é lido do morph atual (`morph.spell` e `morph.color`); `EntitySpellResolver` com player como caster; se `resolver.postEvent()` cancelar, não cria projétil. Em caso contrário cria `EntityProjectileSpell`, aplica `shoot` com velocidade nominal **1.0** e imprecisão **0.8**, e chama `level.addFreshEntity`. | `⚠️` Runtime/settlement efetivo do host não foi testado. |
| Target / geometria | Alvo final, alcance, hitbox, DamageSource, efeitos da spell armazenada e verificação de spawn não são definidos no adaptador. O conteúdo depende da NBT/forma Ars. | `⛔` Sem hook provado para alterar tipo de alvo, AOE, range, dano ou hitbox. |
| Passivo e tempo | Não sobrepõe `passiveTick` do adaptador comum. | Efeito contínuo/callback passivo não corresponde a casts adicionais. |
| Causalidade | Cinco variantes têm cooldown e use_duration iguais, mas são cinco assignments Identity2 e uma implementação Java compartilhada; NÃO são cinco novas magias. | Uma ativação Identity2 pode originar spell Ars, projétil, potion ou status: não criar segunda cobrança/cooldown/XP. |
| Bounds | Identidade depende da forma atual, servidor/cliente e dependências. Qualquer número de entities/hits ou change de bloqueio só é efetivo se o pipeline host o aceitar. | `⚠️` Testar cancelamento, persistência e resolução de efeito com versões atuais. |

## Evidência de código e arquivo de atribuição

- [java](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/WealdWalkerAbility.java#L14-L34)
- [registry](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/identity/IdentityReg.java#L56-L67)
- [Identity2 `blazing_weald_walker.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_nouveau/identity2/identity_ability/blazing_weald_walker.json)
- [Identity2 `cascading_weald_walker.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_nouveau/identity2/identity_ability/cascading_weald_walker.json)
- [Identity2 `flourishing_weald_walker.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_nouveau/identity2/identity_ability/flourishing_weald_walker.json)
- [Identity2 `vexing_weald_walker.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_nouveau/identity2/identity_ability/vexing_weald_walker.json)
- [Identity2 `flashing_weald_walker.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_elemental/identity2/identity_ability/flashing_weald_walker.json)
- [Base MorphBoundAbility]( https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/MorphBoundAbility.java#L15-L62 ).

**QA requerido:** Validar as cinco variants incluindo Flashing (condicionada a Ars Elemental), postEvent canceled, conteúdo spell de cada morph, owner e danos de projétil, client/server, cooldown Identity2 versus cast interno, chunks e target. Versões físicas usadas como alvo: Ars Nouveau 5.13.1, Identity2 2.2.4, Ars Elemental 0.7.10.1 quando presente, Gabou's Libs 1.8.7. **+0 novas raízes mágicas; 0 adapters implementados.**
