# Ars Nouveau — Rewind

Status: `SOURCE-PINNED 5.13.1 / HISTORY+CONTINUATION STATIC CONTRACT / RUNTIME CONFIG QA PENDING`

- Registry id: **`ars_nouveau:rewind`**, não `glyph_rewind`.
- Classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectRewind` [S-rewind].
- Escola Manipulation; tier default **III**; mana default **100**.
- Augments nativos: Extend Time e Reduce Time (`glyph_duration_down`) [S-config].

## Target, elegibilidade e cadeia causal

O livro descreve voltar por posições/vida anteriores e reverter blocos movidos por spells; glyphs posteriores resolvem no fim do rewind. O caminho efetivo exige dados de história **já gravados**, não um snapshot universal do mundo [S-rewind] [S-config].

`onResolveEntity` só agenda se a entidade implementa `IRewindable`, seu tipo não está em `EntityTags.REWIND_BLACKLIST` e `!isRewinding()`. Cria `DelayedSpellEvent`, marca contexto atrasado e enfileira **primeiro `RewindEvent`, depois Delay**. Para Player envia também `PacketClientRewindEffect`; este agenda rewind visual/movimento no cliente, sem continuação de spell [S-rewind] [S-packet]. O callback de bloco agenda `RewindEvent(null,...,spellContext)` e Delay sem adquirir entidade naquela posição [S-rewind]. Não faz busca de área, nova seleção, raycast ou teste local de LOS/claims; isso não autoriza ignorar os gates do pipeline/consumidores.

A cada tick de `RewindEvent`, `eventGameTime=startGameTime-rewindTicks`; se há `IRewindable`, marca rewinding e faz `pop` do snapshot mais recente disponível, quando existir. Em seguida visita callbacks do attachment do **contexto da magia** naquele game time, trava o timestamp contra adicionar novos callbacks durante a visita, incrementa contagem e para ao atingir `ticksToRewind` [S-event]. Um buffer vazio não inventa snapshots; o intervalo do evento pode continuar mesmo sem dado a restaurar.

`RewindEntityData.onRewind` retorna se removida ou LivingEntity morta/morrendo: **não ressuscita**. Temporariamente remove a flag de bloqueio, aplica weight modifier `-1 ADD_MULTIPLIED_TOTAL` ou `setNoGravity(true)` conforme entidade/gravidade, chama `setPos(position)`, inverte velocidade registrada `deltaMovement.scale(-1)`, zera fallDistance, repõe flag e, no servidor, **`living.setHealth(health)`** [S-data]. Não chama `heal` nem `hurt`: não assumir eventos/atributos de cura/dano, mastery ou procs normais. O fim limpa flag, zera movimento e remove weightlessness; há limpeza em server stop/logout e limpeza do buffer ao mudar dimensão quando evento não cancelado [S-event-stop]. Isso não certifica persistência de uma sessão de rewind através de restart/unload.

## História de entidade e blocos: limites distintos

`RewindEntityMixin` injeta em `Entity.baseTick` e inicializa `FixedStack` com o limite configurado. Grava posição, deltaMovement, gameTime e vida de LivingEntity; enquanto rewinding, intercepta as duas variantes de `setDeltaMovement` para bloquear escritas externas [S-mixin]. `shouldRecordData` exclui não-Players no cliente, glyph desabilitado, blacklist e entidade já rebobinando [S-record]. No servidor a classe documenta tracking de entidades **em qualquer lugar**, não apenas perto do caster. Isso cria custo de memória/tick que uma perk de tempo não pode ampliar sem orçamento/performance QA.

Histórico default **60 ticks**; `FixedStack.push` remove os mais antigos antes de inserir [S-stack]. O tamanho é fixado ao criar o stack, portanto mudar config não redimensiona automaticamente os stacks existentes. `entityRewindTracking` usa `addGenericInt`, que admite zero; `FixedStack.push` com maxSize0 tenta remover índice0 até de stack vazio: **zero não está comprovado como opção segura de desativação** [S-stack] [S-config-helper]. Não inferir gravação em NBT/restart dessa estrutura em memória.

Os blocos usam outro mecanismo: `RewindAttachment` guarda callbacks por gameTime no contexto [S-attachment]. `EnchantedFallingBlock.fall` registra `BlockToEntityRewind`; a recolocação bem-sucedida registra `EntityToBlockRewind` no ramo apropriado, quando há contexto/resolver [S-block-fall] [S-block-land]. O primeiro só chama `groundBlock(true)` se entidade é fallingblock válida e estado corresponde; o segundo exige que o bloco atual corresponda ao estado salvo, recria fallingblock e transfere a história disponível [S-to-block] [S-to-entity]. Isso não restaura blocos arbitrários ou todas as mudanças feitas por outros mods. AOE, geometria de queda/colisão e damage source desses consumidores não se tornam parâmetros universais do Rewind.

## Fórmula, unidades, configurações e caps

`M=stats.getDurationMultiplier()` é scalar líquido, **não contagem separada** [S-rewind]:

```text
M > 0 : T = (int)(BASE_REWIND_TIME + EXTEND_TIME*M)
M < 0 : T = (int)(BASE_REWIND_TIME - DURATION_DOWN_TIME*abs(M))
M = 0 : T = BASE_REWIND_TIME
```

Defaults: base **40 ticks**, Extend **20 ticks por unidade positiva**, Down **10 ticks por unidade negativa**, história60ticks [S-config]. O helper de Extend tem comentário genérico «seconds», mas **nesta fórmula não há `*20`**: o consumidor usa o número20 diretamente como ticks [S-config-helper]. Base tem faixa1…60; o resultado final não recebe clamp a1, a60 ou ao tamanho do histórico. Base40 e `M=-5` dão **−10ticks**, sem transformar isso numa espera positiva segura. Configs são acessadas diretamente; não há fallback numérico local para getters não inicializados.

**Ressalva dos supostos caps1/5:** o override `buildAugmentLimitsConfig` chama `super` **antes** de inserir Extend1/Down5 no mapa [S-config]. `SpellPartConfigUtil.buildAugmentLimitsConfig` serializa esse mapa imediatamente para uma lista; depois `AbstractEffect.buildConfig` ainda constrói `augment_limits` novamente a partir de outro mapa [S-cap-util] [S-build-config]. Logo1/5 são valores **declarados nesse trecho**, não prova de caps efetivos por default neste release. A leitura de cap ausente retorna `Integer.MAX_VALUE` [S-cap-read]. Verificar config gerada e gates de crafting/cast no pack antes de usar esses números como limite de perk; esta ficha não presume enforcement.

Para `T<=0`, contexto não fica atrasado (`isDelayed` exige `duration>0`); Delay já expira antes do tick na fila, enquanto `RewindEvent` não está expirado inicialmente e ainda pode executar um tick antes de parar [S-context-delay] [S-queue] [S-event] [S-delayed]. A continuação pode ocorrer no laço atual; não alegar que todo rewind sempre espera completar. Para `T>0`, Delay retoma o mesmo resolver, salvo entidade-hit removida; efeitos/callbacks, restauração e retomada continuam uma cadeia causal provider-owned.

## Custos e aquisição

Receita datagen: `ars_nouveau:manipulation_essence` + **`minecraft:clock` ×3** [S-recipe]. XP default **160** (tierIII) [S-xp]; starter default **não** [S-starter]; aquisição completa [85/85](../../ACQUISITION.md). Default100mana é do glyph, sujeito à config; composição, descontos e cobrança têm autoridade Ars [S-cost] [S-mana]. Duração de rewind não é cooldown extra. Não dar XP/cura/mastery por cada snapshot, tick, callback, pacote ou continuação.

## Certificação estática individual — 25/10/2026

| Campo | Contrato documentado e limite |
|---|---|
| Identidade e release | `ars_nouveau:rewind`, `EffectRewind`, Ars5.13.1, tierIII/Manipulation; classe/ID compilados, source de comportamento pinado. |
| Comportamento e causalidade | Evento rebobina snapshots e callbacks do contexto; `setHealth`, inversão de movimento, flag/gravidade e Delay de continuação; sem ressurreição ou rollback mundial geral. |
| Parâmetros e caps | `40+20M` se M positivo ou `40−10abs(M)` se negativo, ticks/truncamento; tracking60, base1…60; sem clamp final; declarações1/5 não comprovam cap efetivo. |
| Targeting e resultado | Entidade IRewindable fora de blacklist e não rewinding; bloco agenda com entidade nula; sem range, área, projétil, dano ou heal event próprios. |
| Custos e aprendizagem | 100mana default, tierIII, 160XP, essência+3clocks, starter não; composição/tempo/custo e config separados. |
| Integração e authority | API pública existe, mas scalar de duração, buffer global e callbacks têm riscos diferentes; adapter RPG, cap e deduplicação não validados; Ars owns history/scheduler. |
| Validação e pendências | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; source e109IDs compilados, sem equivalência integral de métodos/config/gameplay; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

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
[S-rewind]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRewind.java#L26-L74
[S-record]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRewind.java#L76-L88
[S-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRewind.java#L90-L144
[S-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/timed/RewindEvent.java#L21-L84
[S-event-stop]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/timed/RewindEvent.java#L86-L140
[S-data]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/rewind/RewindEntityData.java#L24-L54
[S-mixin]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/rewind/RewindEntityMixin.java#L20-L87
[S-stack]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/debug/FixedStack.java#L5-L20
[S-attachment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/rewind/RewindAttachment.java#L11-L55
[S-block-fall]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L156-L169
[S-block-land]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EnchantedFallingBlock.java#L257-L266
[S-to-block]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/rewind/BlockToEntityRewind.java#L8-L23
[S-to-entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/rewind/EntityToBlockRewind.java#L17-L46
[S-packet]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketClientRewindEffect.java#L32-L43
[S-config-helper]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L162-L177
[S-cap-util]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/util/SpellPartConfigUtil.java#L101-L106
[S-cap-read]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/util/SpellPartConfigUtil.java#L44-L64
[S-build-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L136-L147
[S-context-delay]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L265-L275
[S-queue]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EventQueue.java#L24-L47
[S-delayed]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/DelayedSpellEvent.java#L32-L67
[S-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L122-L127
