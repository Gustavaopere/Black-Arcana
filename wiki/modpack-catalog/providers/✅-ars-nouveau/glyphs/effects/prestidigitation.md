# Ars Nouveau — Prestidigitation

Status: `SOURCE-PINNED 5.13.1 / STATIC TECHNICAL CONTRACT / RUNTIME QA PENDING`

- Registry id: `ars_nouveau:glyph_prestidigitation`; classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectPrestidigitation`.
- Conjuration, tier default **I herdado**, mana default **0**; augments Extend Time, Reduce Time e Amplify [config] [defaults].
- Cria apresentação por entidade, bloco ou componente de item. Esses três caminhos não partilham a mesma persistência, relógio ou admissão.

## Entidade: pacote e duração visual

[onResolveEntity][entity] envia PacketPrestidigitation com **T=(int)((5+3*durationMultiplier)*20)** ticks; o cast int é depois da multiplicação, diferente de Intangible. A timeline é PRESTIDIGITATION_TIMELINE.onTickEffect. Não cria buff/status, dano, efeito físico ou ligação persistente de gameplay. Amplify não torna esse caminho permanente: o teste de presença só existe no ramo de bloco.

[PacketPrestidigitation.onClientReceived][packet] procura entityId no nível do cliente. Se existe, redefine a posição do emitter para o centro da bounding box da entidade e agenda ParticleTimelineEvent na fila cliente. [EventQueue][queue] testa expiração **antes** do tick; [ParticleTimelineEvent][event] expira com ticks<=0 e decrementa antes de chamar emitter.tick. T≤0 não emite por essa fila; T>0 fornece T ticks de emitter se a fila for processada normalmente. Não há serialização desse evento de fila para reload nem confirmação de que a entidade continuará presente; o pacote inicial perdido/entidade ausente não produz o mesmo resultado visual. Ticks de partículas não são procs/mastery.

## Bloco: permanência por presença e consumidor do tile

[onResolveBlock][block] escolhe posição adjacente à face atingida e testa replaceable, unobstructed para defaultstate de Particle Block e world bounds. Preserva WATERLOGGED quando o fluido é WATER; chama setBlockAndUpdate sem ler o retorno e, se o tile for ParticleTile, instala a timeline. O player local criado no callback não é usado para uma checagem de claim; não há EntityPlaceEvent ou destroyRespectsClaim explícito aqui. Isso não comprova bypass da admissão/listeners externos.

**Presença de AugmentAmplify**, via hasBuff, evita marcar o tile temporário; não é `ampMultiplier>0`. Sem Amplify, `isTemporary=true` e `ticksRemaining=T`. ParticleTile inicia esses campos com false/0 no objeto novo. Não inferir remoção de estado temporário pré-existente somente porque chegou um Amplify: nesse ramo o glyph simplesmente deixa de escrever os campos. A timeline é instalada antes dessas atribuições e setTimeline chama updateBlock [tile].

[ParticleTile.tick][tile] no servidor testa ticksRemaining<=0 e remove o bloco; caso positivo decrementa. Partindo de T≥0 em tile temporário novo, a tentativa de remoção ocorre no **tick processado T+1**; valores negativos removem no primeiro. Ticks parados por chunk sem ticking não consomem contador. No cliente, somente tick do emitter. NBT guarda timeline, isTemporary e ticksRemaining; load recria emitter no centro do bloco, sem salvar idade/rand/previousPosition do emitter. Isso não promete continuidade visual exata ou durabilidade em cada tick: os decrementos não chamam setChanged, e a marcação inicial de temporário ocorre depois do updateBlock de setTimeline. Save/load físicos pendentes.

[PrestidigitationBlock][particle-block] não tem colisão/oclusão, mas seu shape de seleção (`getShape`) é caixa4..12 nas coordenadas voxel; suporta waterlogging e randomTick chama playSound. Remoção de ParticleTile não armazena/restaura o bloco anterior ou um ledger de água. Não tratar a apresentação como estado sem custo de mundo ou rollback universal.

## Item: componente é outro caminho

[ItemStackMixin][item-mixin] chama onInventoryTick antes do inventoryTick original. O [callback][inventory] retorna no cliente ou sem PRESTIDIGITATION; no servidor usa somente item atual ou slots36..40. Obtém emitter cacheado em PrestidigitationData e chama emitter.tick. [PrestidigitationData][item-data] serializa a timeline; o emitter cacheado nasce na primeira entidade e não é reassociado nesse getter, nem salvo como parte do CODEC. Não prometer transferência de owner/continuidade perfeita em stack compartilhada ou troca de portador.

[ParticleEmitter.tick][emitter] no servidor envia TickEmitterPacket; no cliente executa particleConfig.tick. Depois desse ramo, **ambos os lados** atualizam previousPosition e incrementam age. Logo o early-return cliente do callback não significa ausência de apresentação cliente. O glyph ao atingir uma entidade **não aplica esse componente ao item**. Um caminho real separado é [PrestidigitationRecipe.assemble][item-recipe], que copia o catalyst e instala a timeline do parchment; sourceCost dessa receita de apparatus não é mana0 do glyph. O [registro][component] torna a timeline persistente/network-synchronized, não concede autoridade de dano/owner/progressão por partícula.

## Custos e certificação estática individual — 25/10/2026

Receita de aprendizagem [recipe]: `ars_nouveau:conjuration_essence`, **27XP**, starter **não** [xp] [starter]. Mana0 do componente não garante spell composta gratuita; itens/augments/config têm custo próprio [costs]. Sem cooldown, DamageType, healing, projétil de gameplay ou raio próprios. [Aquisição completa](../../ACQUISITION.md).

| Campo | Contrato e limite verificado |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_prestidigitation`, EffectPrestidigitation, Ars5.13.1, Conjuration/tierI herdado. |
| Comportamento e causalidade | Pacote de entidade, ParticleTile de bloco e componente de item separados; renderização não comprova efeito físico [entity] [block] [inventory]. |
| Parâmetros e caps | T=trunc((5+3M)×20), Amplify por presença só no bloco; fila visual T ticks ou0, remoção de tile T+1 ticks processados para T≥0. Sem clamp local final. |
| Targeting e resultado | Entidade/bounding-boxcenter, bloco adjacente ou portador/slots36..40; sem aquisição de alvo, dano ou projectile size próprios. |
| Custos e aquisição | Mana0, tierI, 27XP, conjurationessence, starter não; custo de apparatus/componente separado de mana do glyph. |
| Integração e autoridade | Timeline/setTimeline/component são superfícies reais; não fornecem autorização de mundo, damage proc, owner ou mastery por emissão. Adapter/custos/claims/causalidade pendentes. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`; clientrender, save/reload e pack não testados. |

## Fronteira de perks e validade

`SpellModifierEvent` oferece uma API pública real no [builder original][builder]; mutação *in-place* é uma superfície distinta de substituir `event.builder`, que não é relido no retorno. [EffectResolveEvent.Pre no resolver][resolve] permite veto; trocar campos do payload não substitui os locais de alvo, effect, stats ou contexto. `Post` pode ocorrer sem aplicação efetiva. Uma lista de augments modificada não recalcula automaticamente scalars/flags já construídos.

Ars governa composição, estados, inventários e aprendizagem; RPG Skill Tree fornece progressão por contrato comprovado. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded mantém seus sistemas ambientais. Aplicação, tick, renderização, atualização de tile e callback não são novos casts pagos ou créditos de Mastery. [Admissão e pagamento][payment] são separados; custo default de um glyph não é preço final da composição e mana de jogador não é Source.

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Fonte oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; a [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova **ID/classe**, sem correspondência integral dos métodos Java/bytecode. Config instalada, addons, proteção, persistência física, cliente/servidor e gameplay em modpack não foram validados. Mudanças de JAR, configuração, código ou consumidores exigem reauditoria.

[costs]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L150
[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L270
[payment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L273-L298
[entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPrestidigitation.java#L38-L58
[block]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPrestidigitation.java#L61-L81
[inventory]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPrestidigitation.java#L83-L96
[config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPrestidigitation.java#L98-L124
[defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L145-L150
[packet]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketPrestidigitation.java#L20-L43
[event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/ParticleTimelineEvent.java#L6-L28
[queue]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EventQueue.java#L24-L42
[tile]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/ParticleTile.java#L18-L79
[particle-block]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/PrestidigitationBlock.java#L26-L85
[item-mixin]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/mixin/ItemStackMixin.java#L11-L18
[item-data]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/PrestidigitationData.java#L13-L36
[emitter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/particle/ParticleEmitter.java#L137-L152
[item-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/crafting/recipes/PrestidigitationRecipe.java#L28-L51
[component]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DataComponentRegistry.java#L59-L59
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L130-L130
