# Wilden Hunter — Ars Morph 2.0.0 / Identity2 ability

**Status: ✅ fonte por habilidade documentada · ⚠️ runtime e JAR físico pendentes · ⛔ perks sem contrato homologado.** Habilidade provider-native Identity2; NÃO constitui novo glifo, cast root Black Arcana ou forma independente de mana. `ars_morph-1.21.1-2.0.0.jar` SHA-1 físico documentado `68ff47cc58c0ffe9570bb907f65c2910311ed45f`; release-aligned source `Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`. Fatos abaixo **SOURCE_CAUSALITY**, não comparação de bytecode do JAR.

## Registro e valores do pack source-pinned

- **Identidade da habilidade/forma:** `ars_nouveau:wilden_hunter` (ID de Ars ou Ars Elemental/Identity2, **não** `ars_morph:*` spell).
- **Config de Identity2 no arquivo de atribuição:** `cooldown=800`, `use_duration=20`. São **inteiros brutos nos JSONs upstream**; a interpretação da unidade (ticks, segundos), consumo no cancelamento, skill gates e sincronização são do Identity2 **2.2.4**, ainda não medidos no runtime do pack.
- **Admissão:** Registro por `ModEntities.WILDEN_HUNTER.get()` (ID natural da EntityType). O wrapper só executa se o morph atual for `WildenHunter`.

## Matriz causal para perks

| Eixo | Observação fixa em source | Status de adaptação |
|---|---|---|
| Entrada | `MorphBoundAbility.execute(Entity host)` exige que host seja `Player`, `IdentityApi.getCurrentMorph(player)` não-null e seja instância da classe esperada; exceptions em `use` são capturadas/logadas. | `⛔` Não transpor gate de morph ou duplicar os eventos do Identity2. |
| Efeito ativo | Invoca som de uivo e constrói `Spell` de Ars com `EffectSummonWolves` + `AugmentExtendTime`, com `SpellResolver` e `LivingCaster(player)`. Executa `resolver.onResolveEffect` no próprio jogador somente se `postEvent` não foi cancelado e depois remove `SUMMONING_SICKNESS_EFFECT` do jogador. | `⚠️` Runtime/settlement efetivo do host não foi testado. |
| Target / geometria | Resolve Ars em `EntityHitResult(player)`. Quantidade, AI, duração, HP, alvo e DamageSource dos lobos são definidos pelos mecanismos Ars e pela magia, não por esta bridge. | `⛔` Sem hook provado para alterar tipo de alvo, AOE, range, dano ou hitbox. |
| Passivo e tempo | Sem `passiveTick` próprio; o som é anterior à checagem do cancelamento. | Efeito contínuo/callback passivo não corresponde a casts adicionais. |
| Causalidade | Remoção de Summoning Sickness não é consequência separada autorizada para Mastery. `postEvent` não mede se cada lobo foi criado. | Uma ativação Identity2 pode originar spell Ars, projétil, potion ou status: não criar segunda cobrança/cooldown/XP. |
| Bounds | Identidade depende da forma atual, servidor/cliente e dependências. Qualquer número de entities/hits ou change de bloqueio só é efetivo se o pipeline host o aceitar. | `⚠️` Testar cancelamento, persistência e resolução de efeito com versões atuais. |

## Evidência de código e arquivo de atribuição

- [java](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/WildenHunterAbility.java#L17-L35)
- [registry](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/IdentityReg.java#L56-L67)
- [Identity2 `wilden_hunter.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_nouveau/identity2/identity_ability/wilden_hunter.json)
- [Base MorphBoundAbility](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/MorphBoundAbility.java#L15-L62 ).

**QA requerido:** Testar evento cancelado (som sem summon), summon com/sem Sickness, 0/N lobos de fato criados, owner, custo de Ars, perda de morph, PvP e atribuição de XP. Versões físicas usadas como alvo: Ars Nouveau 5.13.1, Identity2 2.2.4, Ars Elemental 0.7.10.1 quando presente, Gabou's Libs 1.8.7. **+0 novas raízes mágicas; 0 adapters implementados.**
