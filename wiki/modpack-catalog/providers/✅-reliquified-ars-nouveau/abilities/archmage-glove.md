## Engenharia causal adicional — source 0.8.1 (2026-10-13)

**Limite da prova:** o binário físico tem SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` e a identidade `AbilityTemplate` foi comprovada em auditoria Java 21; os comportamentos detalhados abaixo foram lidos do source público versionado `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc`, declarado 0.8.1. **Não foi demonstrada equivalência byte-a-byte das implementações de métodos ao JAR físico.** Defaults são templates do Relics, não configuração efetiva/estado de jogador.

**Habilidade:** `multicasted` (Echo Spell); item `reliquified_ars_nouveau:archmage_glove`, classe [`ArchmageGloveItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/hands/ArchmageGloveItem.java), métodos `CommonEvents.onSpellCast(SpellCastEvent)`, `onSpellCostCalcPre(SpellCostCalcEvent)` e `onLivingDamagePre(LivingDamageEvent.Pre)`.

### Admissão da repetição

- O handler só aceita **ServerPlayer**, evento no servidor e `SpellContext` primário (`getPreviousContext()==null`), sem tags de filho `ran_archmage_glove_multicast_child` nem de já processado `ran_archmage_glove_multicast_processed`.
- Exige **exatamente uma ocorrência** do `AugmentMulticast` na spell, na posição **1**, precedida de `AbstractCastMethod` em posição 0; falha nesse alinhamento torna o handler inerte. Exige Curios com Archmage Glove equipada.
- Marca contexto original como processado **antes** de iterar os itens. Chance nativa do template `multicast_chance`: faixa de início `0.05..0.1`, target scaling `0.74999` (não inferir valor final). Modificador `adaptive_multicast` aumenta chance após fracassos; o resultado é limitado a `[0,1]`. `max_multicasts` é arredondado e limitado a pelo menos 1 pelo handler.

### Filhos, mana e causalidade

- Para cada multicast, o provider agenda `ITimedEvent` no `EventQueue` com delay `(i+1)*5` **ticks**. Ao disparar, salva/restaura rotação do player via `try/finally`, instancia **novo** `SpellContext` com cópia do caster tool e tags de filho/processado, e chama o `SpellResolver` por trajetória de entidade, bloco ou cast simples; há nova seleção de alvo em cada filho.
- `onSpellCostCalcPre` faz `event.currentCost=0` **somente** para contexto com tag de multicast-filho. O custo original é consultado com `new SpellResolver(event.context).withSilent(true).getExpendedCost()`. Não prometer custo zero universal da spell original nem do provider.
- Só após filho retornar `casted=true`, aumenta XP `multicast_trigger` e estatística `extra_casts`; o modifier `mana_refund` pode restaurar fração do custo original usando `CapabilityRegistry.getMana(player)`, com chance e fração limitadas a `[0,1]`.
- `multicast_resistance` ativa janela por `max(5,multicasts*5)` ticks e no `LivingDamageEvent.Pre` reduz `event.getNewDamage()` pela fração `multicast_damage_reduction` (clamp `[0,1]`). A mitigação se baseia no estado da luva, não em novo feitiço.
- **Deduplicação:** cast original, filhos gerados e reembolso não são três iniciativas independentes para o Black Arcana. Recompensa de Mastery por filho exigiria contrato explícito com identificação parent/child, admissibilidade e retorno de cast.


### Implicações para Black Arcana e RPG

- Reliquified Ars Nouveau/Relics são autoridades do item, habilidade, ranks, experiência, efeitos e dados; Ars Nouveau mantém autoridade por mana, resolver, spell context e spells. Black Arcana não repete cast, recurso ou consequência. RPG Skill Tree só pode consultar/conceder perks mediante boundary comprovado.
- **Perk A:** estatísticas nativas e eventos *observados na fonte* não autorizam escrita arbitrária. **Perk B:** nenhum evento de integração Black Arcana/RPG com garantia de causalidade foi homologado. **Perk C/D:** adapter/rate caps e token de cast exigem contrato, **⛔ fail-closed** até confirmação.
- QA pendente: instância física atual de Relics 0.12.8, Ars Nouveau 5.13.1, Curios atual, config, save/restart, multiplayer, equipamento duplicado, eventos cancelados, custos e Mastery. Nenhum GameTest ou Survival desse item foi executado nesta etapa.
- **Clean-room:** relatamos fatos de execução em nossas palavras; não copiamos código-fonte/asset do provider para o Black Arcana.

[Matriz desta etapa](../PERK-ENGINEERING-MATRIX-0.8.1.md) · [Índice do provider](../README.md).
