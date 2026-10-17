# Firenando (condicional Ars Elemental) — Ars Morph 2.0.0 / Identity2 ability

**Status: ✅ fonte por habilidade documentada · ⚠️ runtime e JAR físico pendentes · ⛔ perks sem contrato homologado.** Habilidade provider-native Identity2; NÃO constitui novo glifo, cast root Black Arcana ou forma independente de mana. `ars_morph-1.21.1-2.0.0.jar` SHA-1 físico documentado `68ff47cc58c0ffe9570bb907f65c2910311ed45f`; release-aligned source `Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`. Fatos abaixo **SOURCE_CAUSALITY**, não comparação de bytecode do JAR.

## Registro e valores do pack source-pinned

- **Identidade da habilidade/forma:** `ars_elemental:firenando_entity` (ID de Ars ou Ars Elemental/Identity2, **não** `ars_morph:*` spell).
- **Config de Identity2 no arquivo de atribuição:** `cooldown=120`, `use_duration=40`. São **inteiros brutos nos JSONs upstream**; a interpretação da unidade (ticks, segundos), consumo no cancelamento, skill gates e sincronização são do Identity2 **2.2.4**, ainda não medidos no runtime do pack.
- **Admissão:** É condicional: `ElementalModule.initAbilities()` somente se `ModList.isLoaded("ars_elemental")`. Esse mod consta da modlist; não implica sucesso de execução. Registro por `FIRENANDO_ENTITY.getId()`.

## Matriz causal para perks

| Eixo | Observação fixa em source | Status de adaptação |
|---|---|---|
| Entrada | `MorphBoundAbility.execute(Entity host)` exige que host seja `Player`, `IdentityApi.getCurrentMorph(player)` não-null e seja instância da classe esperada; exceptions em `use` são capturadas/logadas. | `⛔` Não transpor gate de morph ou duplicar os eventos do Identity2. |
| Efeito ativo | Lê `firenandoEntity.spell` e escolhe cor em função da variante MAGMA; usa Ars `EntitySpellResolver` com player como caster. Se postEvent não cancelado, cria `EntityHomingProjectileSpell`, carrega `MethodHomingProjectile.basicIgnores`, adiciona predicado que **ignora todo LivingEntity que não seja `Enemy`**, dispara nominal velocity **0.8**, inaccuracy **0.8**, e chama `addFreshEntity`. | `⚠️` Runtime/settlement efetivo do host não foi testado. |
| Target / geometria | Somente `Enemy` elegíveis, ainda sujeitos aos filtros herdados `basicIgnores`. Alcance, hitbox, dano e efeitos dependem da spell armazenada e do Ars Elemental 0.7.10.1 (host físico), não inferidos. | `⛔` Sem hook provado para alterar tipo de alvo, AOE, range, dano ou hitbox. |
| Passivo e tempo | Não há callback passivo específico. | Efeito contínuo/callback passivo não corresponde a casts adicionais. |
| Causalidade | Não equiparar `Enemy` a todo PvP/mob hostil modded; o filtro tem efeito de targeting, mas setters de retarget per-caster não são APIs de perk aprovadas. | Uma ativação Identity2 pode originar spell Ars, projétil, potion ou status: não criar segunda cobrança/cooldown/XP. |
| Bounds | Identidade depende da forma atual, servidor/cliente e dependências. Qualquer número de entities/hits ou change de bloqueio só é efetivo se o pipeline host o aceitar. | `⚠️` Testar cancelamento, persistência e resolução de efeito com versões atuais. |

## Evidência de código e arquivo de atribuição

- [java](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/FirenandoAbility.java#L19-L43)
- [conditional registration](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ElementalModule.java#L11-L27)
- [Identity2 `firenando_entity.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_elemental/identity2/identity_ability/firenando_entity.json)
- [Base MorphBoundAbility]( https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/MorphBoundAbility.java#L15-L62 ).

**QA requerido:** Validar Ars Elemental runtime, variante MAGMA, Enemy vs criaturas neutras/jogadores, filters herdados, postEvent cancel, projectile hit, client/loaded chunk e Mastery sem double-credit. Versões físicas usadas como alvo: Ars Nouveau 5.13.1, Identity2 2.2.4, Ars Elemental 0.7.10.1 quando presente, Gabou's Libs 1.8.7. **+0 novas raízes mágicas; 0 adapters implementados.**
