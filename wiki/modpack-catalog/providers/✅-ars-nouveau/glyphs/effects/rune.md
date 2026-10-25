# Ars Nouveau — Rune

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_rune`
- Display name: Rune
- School: Manipulation
- Default tier: 1
- Default mana cost: 30
- Compatible augments: Sensitive
- Default Sensitive limit: 1

## Provider-native behavior

Rune creates an Ars rune block, cancels the current spell context, creates a child context, prepends `Touch` to the remaining spell recipe and stores that resulting spell on the `RuneTile`. The rune is temporary and triggers the stored spell when a target touches it. Sensitive changes inventory ownership behavior for pickup/usage according to provider semantics.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `ars_nouveau:runic_chalk` + `minecraft:tripwire_hook`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

This is a provider-owned delayed/triggered spell-execution surface. Black Arcana must not route Ars rune execution through a second Black Arcana casting pipeline or duplicate costs/effects. Black Arcana rituals/traps require their own canonical server-authoritative contracts.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectRune`).

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectRune.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRune.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectRune` no Ars 5.13.1, método `onResolve`.
- **Lifecycle:** `SpellContext newContext=spellContext.makeChildContext()` e `spellContext.setCanceled(true)` transferem a cadeia para execução posterior; isso não é cancelamento global de magia por erro. **Colocação:** posição do hit (corrigida se `BlockHitResult.isInside`), exige replaceable, world bounds e `BlockUtil.destroyRespectsClaim`; coloca `RUNE_BLOCK`. **Armazenamento:** em `RuneTile` persiste UUID do jogador caster, `isTemporary=true`, cópia do child spell com `MethodTouch.INSTANCE` inserido no começo e `isSensitive`. Sensitive limit 1. **Perks:** progresso/recursos de colocação e trigger posterior exigem deduplicação e auditoria `RuneTile`; sem autorização para criar uma segunda transação no Black Arcana.
- **Limite de integração:** ✅ source pin da lógica local, ⚠️ config/gameplay dependem do provider real; ⛔ adapter externo seguro não comprovado, embora APIs provider-native existam. Black Arcana só governa suas world mutations; RPG Skill Tree depende de bridge real. QA Survival PENDING.

## Auditoria do executor secundário — limitações verificáveis

- **Java:** [`common/block/tile/RuneTile.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/RuneTile.java).
- **Executor `RuneTile`:** `castSpell(entity)` verifica alvo, `isCharged`, spell não-vazio, `ServerLevel`, primeira Form `MethodTouch` e estado `disabled` em runas não temporárias; cria `EntitySpellResolver` em novo `SpellContext` com `RuneCaster`. **Runa temporária:** destrói o próprio bloco depois da invocação; **runa persistente:** marca `isCharged=false` e `ticksUntilCharge=40`, depois tenta recuperar Source por `SourceUtil.takeSourceMultipleWithParticles(...,10,spell.getCost())`; se falha, posterga nova tentativa por `60` ticks. **Perks:** a reserva/custo da invocação inicial e as recargas posteriores não podem ser unificadas em um débito Black Arcana sem contrato provado.

**Limite:** fatos lidos do source pin, não prova de comportamento no JAR físico ou de adapter RPG. QA no modpack ainda pendente.

## Certificação estática: entidades, gravidade e runa — 25/10/2026

**✅ `COMPLETE_PERK_READY` no escopo `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** A certificação é da documentação estática. A identidade de ID/classe no publisher JAR foi auditada separadamente da lógica lida no source pin.

| Campo | Contrato técnico e limite de evidência |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_rune`; `com.hollingsworth.arsnouveau.common.spell.effect.EffectRune`; Ars Nouveau **5.13.1**, Manipulation, tier I herdado. Consumidores `RuneBlock`, `RuneTile`, `RuneCaster`, `EntitySpellResolver` [rune-identity][rune-identity] [rune-school][rune-school]. |
| Comportamento e causalidade | `onResolve` obtém `BlockPos.containing(hit.location)`; se block hit inside, desloca pela face. Faz child context **antes** de `setCanceled(true)` no atual; cancelamento acontece mesmo se a colocação posterior falhar. Exige replaceable, world bounds, claim e estado de placement não nulo. Se encontrar `RuneTile`, grava UUID quando shooter é Player, `isTemporary=true`, `isSensitive=stats.isSensitive()` e recipe do child precedida de `MethodTouch` [rune-effect][rune-effect]. `makeChildContext` também consulta `IContextManipulator` do remainder; não é sempre mera cópia da lista [child-context][child-context]. |
| Parâmetros, escala e caps | Único augment compatível: Sensitive, limite default **1**. Não há duração em segundos, dano, raio ou contagem extra nativos neste glyph; **temporária significa descartada após a invocação**, sem TTL local contado para expiração. `RuneTile` nasce charged; cast requer alvo não nulo, charged, spell não vazio iniciado por Touch, ServerLevel; disabled barra somente runa persistente [rune-tile][rune-tile]. A runa temporária destrói o próprio bloco após chamar o resolver, mesmo que o cast retorne false; o resultado booleano não é consultado. |
| Targeting, geometria e efeito posterior | `RuneBlock.entityInside` consulta entidades no shape bounds da placa (base `16×0,5×16` em unidades de modelo, rotacionada pela face [rune-shape][rune-shape] [rune-shape-rotation][rune-shape-rotation]), exclui spectator/ignoringBlockTriggers e escolhe `entities.getFirst()`; não é AoE nem seleção de mais próximo. Filtros `IFilter` no começo da cadeia verificam **entityIn do callback**, enquanto o alvo armazenado pode ser `entities.getFirst()`; para no primeiro Effect não-filter. Guarda `touchedEntity` e agenda tick de bloco em **1 tick**, onde executa e limpa o campo [rune-trigger][rune-trigger]. Dano/duração/recipients finais vêm dos Effects guardados; Rune não causa dano próprio. |
| Custos, aprendizagem e recurso posterior | Mana default **30**, tier I, receita **27 XP**, starter default não. Receita: `ars_nouveau:manipulation_essence` + `ars_nouveau:runic_chalk` + `minecraft:tripwire_hook` [rune-recipe][rune-recipe] [recipe-xp][recipe-xp]. `RuneTile.castSpell` usa `EntitySpellResolver`, cujo `enoughMana` retorna true [rune-resolver][rune-resolver]; seu caster é RuneCaster/TileCaster de RuneTile, e `TileCaster.expendMana` só tem débito para `BasicSpellTurretTile`, não RuneTile [rune-tilecaster][rune-tilecaster]. Não inferir novo débito de mana do owner no trigger. Runa persistente fica uncharged, espera **40 ticks**, tenta Source com alcance/parâmetro **10** e custo `spell.getCost()`; falha adia **60 ticks** [rune-persist][rune-persist]. Isso é recarga de runa persistente, não cooldown de Rune glyph. |
| Integração, inventory e deduplicação | A API nativa **existe**: `SpellStats.Builder.build` publica `SpellModifierEvent` com o builder original mutável [stat-build][stat-build] [modifier-event][modifier-event]; depois `EffectResolveEvent.Pre` é cancelável [resolve-event][resolve-event]. O resolver consome `stats` local e `this.hitResult`, não qualquer campo público substituído no objeto de evento [resolve-consumer][resolve-consumer]. Isso identifica superfícies para auditoria, sem provar adapter RPG Skill Tree, caps, pagamento, autoridade, target replacement ou deduplicação seguros. Black Arcana mantém sua própria `WorldEffectPolicy`, casting, Corruption e Strain. Trigger cria novo `SpellContext`/resolver, não preserva automaticamente o token do cast original; UUID do owner sozinho não é causal dedup. Sem Sensitive, `RuneCaster` usa inventários adjacentes herdados; com Sensitive, usa inventário do owner online ou lista vazia quando indisponível [rune-inventory][rune-inventory]. `castSpell` usa FakePlayer do UUID ou ANFakePlayer; Sensitive pode trocar para Player online [rune-tile][rune-tile]. Não reconstruir custos/loot/mastery no Black Arcana nem atribuir automaticamente dano de rune ao cast de colocação. |
| Evidência e validação | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria binária de identidades](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova registro ID/classe, não equivalência de todos os métodos, config instalada ou gameplay. Integração RPG/Black Arcana, ordem dos listeners, cliente/servidor e Survival: não testados. |

**Livro versus execução:** `EffectRune.getBookDescription()` diz que runas temporárias não podem recarregar; isso descreve o caminho temporário, não um bloqueio de conversão. `RuneBlock.useItemOn` com **Runic Chalk no servidor altera `isTemporary=false`**, retornando SUCCESS; este caminho pode tornar a runa persistente [rune-convert][rune-convert]. O mesmo método permite redefinir spell via Spell Parchment começando em Touch. Não afirmar que a runa gerada será eternamente incapaz de recarga.

**Persistência e falhas:** NBT guarda spell, charged, redstone, temp, cooldown, uuid, sensitive e pattern. `castSpell` captura Exception, envia mensagem de erro e destrói o bloco [rune-persist][rune-persist] [rune-tile][rune-tile]. Isso não prova transação atômica/reembolso ou deduplicação de effects parcialmente executados. VFX, `EffectResolveEvent.Post` da colocação e o tick agendado não são três casts confirmados nem hits de dano.

**Localizadores imutáveis adicionais:**

[rune-identity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRune.java#L28-L34
[rune-effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRune.java#L36-L80
[rune-school]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectRune.java#L89-L98
[rune-shape]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/RuneBlock.java#L51-L65
[rune-shape-rotation]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/RuneBlock.java#L152-L162
[rune-trigger]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/RuneBlock.java#L109-L141
[rune-convert]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/RuneBlock.java#L68-L93
[rune-tile]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/RuneTile.java#L59-L103
[rune-persist]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/RuneTile.java#L109-L162
[rune-inventory]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/wrapped_caster/RuneCaster.java#L20-L30
[rune-tilecaster]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/wrapped_caster/TileCaster.java#L86-L109
[rune-resolver]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/EntitySpellResolver.java#L7-L23
[child-context]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellContext.java#L143-L164
[rune-recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L98-L101
[stats-duration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L48-L58
[stat-build]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[modifier-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SpellModifierEvent.java#L13-L32
[resolve-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L49
[resolve-consumer]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L220-L279
[cost-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L149
[recipe-xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L156
