# Ars Nouveau — Reset

Status: `SOURCE-PINNED 5.13.1 / CONTEXT-MANIPULATION STATIC CONTRACT / RUNTIME QA PENDING`

- Registry id: **`ars_nouveau:reset`**, não `glyph_reset`.
- Classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectReset implements IContextManipulator` [S-reset].
- Mana default **0**; tier default **I herdado** [S-cost]; nenhum augment nativo compatível [S-reset]. A classe não declara escola: herda conjunto vazio, sem inferir Manipulation pelo nome/receita [S-schools].

## Ação efetiva: segmentar contextos

O livro descreve voltar ao alvo original depois de um Effect que propagou a magia. O contrato executado é de **contextos**, não um setter geral de alvo [S-description].

1. Um consumidor de propagação chama `SpellContext.makeChildContext()`. Esse método percorre a magia restante procurando `IContextManipulator`, consulta `shouldPushContext`, chama `manipulate` e liga o resultado ao parent com `withParent` [S-child].
2. `EffectReset.manipulate` copia a magia restante em mutable, acha o **primeiro próximo Reset**, cria `context.clone().withSpell(subList(0,index))`, e avança o índice do contexto original por `index` [S-reset]. O segmento antes do Reset fica no filho; o posterior permanece para o parent.
3. Consumidores como Burst/Linger/Wall chamam `setCanceled(true)` no contexto original depois de criar o filho [S-burst] [S-linger] [S-wall]. Isso usa `CancelReason.NEW_CONTEXT` como default. `SpellContext.setCanceled` notifica callbacks dos componentes restantes [S-cancel].
4. `EffectReset.contextCanceled` só para `NEW_CONTEXT` limpa cancelamento, acha o próximo Reset, avança o índice e retorna `false` para parar a cadeia de callbacks. Outros motivos de cancelamento retornam `true` sem esse desbloqueio [S-reset].

**Não existe `EffectReset.onResolve`, `onResolveBlock` ou `onResolveEntity` próprio.** Os dois últimos herdados são vazios [S-dispatch]. Colocar Reset no laço comum não chama `manipulate` por si só. Ele não escreve `resolver.hitResult`, não refaz raycast e não teleporta alvo/caster; a retomada no alvo anterior resulta de conservar o parent/resolver do caminho propagador. O exemplo do livro `Burst → Place Block → Reset → Break` descreve a gramática de segmentos, não uma prova de hook genérico de target [S-description]. Não atribuir a Reset o AOE, range ou LOS do propagador.

## Limites de composição: bypass consumido pelos validadores

`RESET_LIMITS` é um `ConcurrentHashMap.newKeySet()` público. Ambos os métodos `bypassCombinationLimitsFor` e `bypassOccurrenceLimitsFor` devolvem esse mesmo conjunto [S-reset]. No source fixo, **Burst, Linger e Wall** adicionam suas instâncias em seus construtores [S-burst] [S-linger] [S-wall]; addons podem ampliar o conjunto, mas isso não foi auditado no pack.

O bypass tem consumidor concreto: ao encontrar `IContextManipulator`, `GlyphOccurrencesPolicyValidator` remove do mapa os contadores das partes retornadas; `InvalidCombinationValidator` faz o mesmo antes de suas verificações de combinações [S-occurrence] [S-combination]. Assim a remoção vale para esses glyphs naquela fronteira da receita; não desliga toda validação, custo, cap de augment ou limite de Black Arcana. `PER_SPELL_LIMIT` ausente usa `Integer.MAX_VALUE` no validator; configuração efetiva permanece separada [S-occurrence].

Não há fórmula de dano/cura, duração, cooldown próprio, raio ou projétil. `shouldPushContext` retorna **true**. O clone de contexto copia o mapa de attachments, mas seus valores são compartilhados, não um deep-copy geral de sistemas [S-clone]; um observer não deve inventar identidade de cast independente por segmento.

## Custos e aquisição

Receita datagen: **`minecraft:target` ×1** [S-recipe]. XP default **27** do tierI herdado [S-xp] [S-cost]; starter default **não** [S-starter]. O glyph não é magia gratuita inteira: custo0 é default deste componente; config de custo e pagamento da composição continuam provider-owned [S-cost] [S-mana]. Sem augment nativo não implica impossibilidade de addons ou eventos públicos modificarem outro estado; significa que nenhum scalar de augment é consumido por esta classe.

Aprendizagem, consumo Survival e enabled/tier/starter configuráveis: [aquisição85/85](../../ACQUISITION.md). A contagem de contextos não é cobrança, mastery, perigo ou cooldown adicional.

## Certificação estática individual — 25/10/2026

| Campo | Contrato documentado e limite |
|---|---|
| Identidade e release | `ars_nouveau:reset`, `EffectReset`, Ars5.13.1, tierI herdado, escola não declarada; ID/classe compilados separados de equivalência de métodos. |
| Comportamento e causalidade | `IContextManipulator` via `makeChildContext`, segmentação antes do próximo Reset e recuperação de cancelamento `NEW_CONTEXT`; callbacks normais herdados vazios. |
| Parâmetros e caps | Sem scalar/augments próprios; bypass para conjunto `RESET_LIMITS`, consumido em dois validadores; source base inclui Burst/Linger/Wall, não todo glyph. |
| Targeting e resultado | Reusa parent/resolver em composição; não seta target, não adquire alvo, não altera LOS, não tem dano, duração ou área próprios. |
| Custos e aprendizagem | Default0mana, tierI, 27XP, target×1, starter não; composição continua paga/validada por Ars. |
| Integração e authority | Contrato público `IContextManipulator` existe, mas não é bridge RPG nem autorização para reescrever a gramática; preservar parent/cast e deduplicação. |
| Validação e pendências | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; source e roster compilado, não execução/config; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Evidência e fronteira de integração

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A revisão de source não implementa perks nem valida gameplay.

O source é `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**. A [auditoria de identidades compiladas](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) usa publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, e comprova **ID/classe**, não equivalência de todos os corpos Java/bytecode. Config instalada, addons, claims, unload/reload e execução física permanecem não testados.

`SpellModifierEvent` é uma API pública real: `SpellStats.Builder.build` aplica augments/itens, publica o evento com o builder e devolve seu `spellStats` [S-builder]. Uma alteração *in-place* no builder original tem superfície source-verified; apenas substituir `event.builder` não troca o objeto retornado. `EffectResolveEvent.Pre` permite cancelamento antes do callback; `SpellResolver.resume` consulta `isCanceled`, mas passa seus **objetos locais** a `effect.onResolve` [S-resolve]. Reatribuir `event.spellStats`, `rayTraceResult`, `resolveEffect` ou `context` não substitui esses locais. `Post` pode ocorrer sem efeito aplicado e não comprova sucesso físico.

Um adapter de perks RPG Skill Tree/Black Arcana que preserve caps, fase, recurso, identidade causal e deduplicação **não foi comprovado**. Ars conserva casting, mana de jogador, scheduler, contexto e efeitos. Source é recurso separado. Black Arcana mantém sua própria transação, Corruption, Strain e WorldEffectPolicy; observar continuação/tick/contexto filho não cria outro cast, cobrança, cooldown ou prêmio de mastery. Mudança de JAR, configs ou consumidores exige reauditoria.

[S-builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[S-resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L200-L270
[S-cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L150
[S-starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[S-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[S-mana]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L127-L173
[S-reset]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectReset.java#L11-L64
[S-description]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectReset.java#L66-L69
[S-child]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L143-L175
[S-cancel]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L231-L253
[S-clone]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L297-L316
[S-schools]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L189-L195
[S-dispatch]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L55-L67
[S-burst]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBurst.java#L30-L85
[S-linger]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectLinger.java#L18-L43
[S-wall]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectWall.java#L22-L47
[S-occurrence]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/GlyphOccurrencesPolicyValidator.java#L22-L43
[S-combination]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/validation/InvalidCombinationValidator.java#L20-L63
[S-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L122-L127
