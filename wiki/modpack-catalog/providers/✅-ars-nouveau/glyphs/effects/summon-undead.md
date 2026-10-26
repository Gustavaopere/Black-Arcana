# Ars Nouveau — Summon Undead

Status: `SOURCE-PINNED 5.13.1 / STATIC CONTRACT AUDITED / RUNTIME CONFIG QA PENDING`

`ars_nouveau:glyph_summon_undead`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectSummonUndead`; Conjuration, tierIII, mana default150. Invoca skeletons aliados com arma selecionada pelos augments. A duração estabelece quando começam a sofrer dano de expiração, **não um despawn imediato garantido**. [Glyph][glyph].

## Execução, fórmula e equipamento

Gate `canSummon`: jogador real não FakePlayer, sem sickness salvo creative [gate]. Usa `safelyGetHitPos`: posição da entidade quando EntityHitResult, senão localização do hit. **`T=(int)(20*(D+E*M))`**, defaults D=15s/E=10s e M=durationMultiplier; se T<=0, retorna sem emissões ou nova sickness. Os getters são diretos e não têm fallback local. Compatíveis Extend/Reduce, Amplify, Split e Pierce. [Glyph][glyph].

Loop de **`N=3+getBuffCount(Split)`**; sem teto local adicional. Cada posição é o bloco do ponto resolvido, com offsets inteiros X/Z de−2…+2 e Y=+2, amostrados independentemente. Não há no callback validação própria de chão/ocupação/claims/LOS. `finalizeSpawn(...MOB_SUMMONED)`, `setOwner`, `setLimitedLife(T)` e helper de summon precedem sickness do caster por Tticks, independentemente do retorno ignorado de spawn.

Loadout por **presença de Pierce**, scalar a=`getAmpMultiplier()`:

- Com Pierce: BOW; se a>0, Power nível **`max(4,(int)a)−1`** (mínimo3 nesse ramo), não a+1 nem aumento gradual1porAmplify desde zero.
- Sem Pierce: iron sword default; a>=3→netherite axe; senão a>2→netherite sword; senão a>1→diamond sword. A ordem importa para a fracionário. Dampen não consta na compatibilidade, mas um listener pode alterar scalar; não presumir mesmo valor que buffCount(Amplify).
- Amp escolhe loadout, não define HP/dano percentual/velocidade deste glyph. Não é um `IDamageEffect.attemptDamage` que liquida dano no cast.

## IA, dano e duração reais

[`SummonSkeleton`][skeleton-init] instala a arma e reavalia goals. Bow goal recebe velocidade1, intervalo20 e parâmetro15blocos; melee goal velocidade1,5. Esses são parâmetros de IA, não cooldown do glyph ou garantia de acerto. Há CopyOwnerTargetGoal, retaliação excluindo owner, seleção de mobs que têm owner como alvo/kill credit e FollowSummonerGoal [skeleton-ai]. O follow usa velocidade1,20, parâmetros6/12, path recalc10ticks e fallback de reposicionamento próximo ao owner; os filtros concretos do helper não são autorização genérica de teleport ou LOS [follow].

Não há fórmula própria de dano de arma/flecha nesta classe auditada: ataques/atributos são entrypoints vanilla e dependem do equipamento/engine. Tipo registrado **1,0×1,8 blocos** e atributos por `SummonSkeleton.createAttributes()` herdado [registration] [attributes]. O override `hurt` só veta `MOB_ATTACK` de outro ISummon de mesmo UUIDowner; não imuniza universalmente a flechas/explosões/friendly fire. `isAlliedTo` inclui owner, aliados do owner e summons de mesmo UUID [skeleton-ai] [skeleton-life]. Loot/equipment drops são suprimidos e XP base0 [skeleton-ai] [skeleton-save].

[`tick`][skeleton-life] decrementa `limitedLifeTicks`; se <=0, redefine contador para20 e chama **`hurt(starve,20F)`**. Não remove por DISCARDED nem consulta `limitedLifespan` nesse loop. `onDispel` só zera esse contador; não prova morte imediata se o dano puder ser recusado/modificado. Morte efetiva chama super e publica Death com **`wasExpiration=false`**, inclusive se a fonte fatal veio desse starvation. Não inferir que toda expiração gere um evento marcado true [skeleton-api].

## Owner e persistência

Owner direto `LivingEntity` e owner UUID sincronizado são dados distintos. `getSummoner/getOwnerFromID` resolve **jogador presente no mesmo level**; não é busca arbitrária cross-dimension de entidades [skeleton-save]. Reader tenta `OwnerUUID` somente com `contains(...,8)` e senão converte a string `Owner`; writer usa `putUUID("OwnerUUID",...)`. A simetria desse gate de tipo com UUID gravado não está comprovada por execução e precisa de reloadQA. O campo direto owner não é explicitamente reatribuído no reader.

Writer grava `LifeTicks` apenas se `limitedLifespan` é true; o construtor com owner define esse boolean, mas `setLimitedLife`/reader não o definem. O construtor usado para carga pode assim divergir do caminho inicial, sobretudo em nova gravação após reload. Não prometer preservação irrestrita de timer/owner/IA só pela existência de campos NBT. `BoundX/Y/Z` também são condicionais [skeleton-init] [skeleton-save].

## Custos e aprendizagem

Receita **`ars_nouveau:conjuration_essence` + `minecraft:bone` + `minecraft:wither_skeleton_skull`** [recipe]; XP default160/tierIII [xp], starter não [starter], [aquisição85/85](../../ACQUISITION.md). Mana default150 pertence à composição Ars. N de criaturas, T de sickness e dano de ataques posteriores não são cobranças ou casts novos.

## Certificação estática individual — 25/10/2026

| Campo | Contrato documentado e limite |
|---|---|
| Identidade e release | `ars_nouveau:glyph_summon_undead`, EffectSummonUndead, Ars5.13.1; classe/ID compilados e source pinado. |
| Comportamento e consumidores | SummonSkeleton armado, IA owner-aware; expiração por dano starve e Death false, não descarte imediato. |
| Parâmetros e caps | N=3+Split; T=trunc(20*(15+10M)), T<=0 aborta; thresholds de arma e Power max(4,trunc(a))−1; sem cap local de emissões. |
| Targeting e resultado | Hit→bloco+offsets−2…2,Y+2; mob1×1,8, goals20/15 e melee1,5; dano final herdado não inventado. |
| Custos e aquisição | Mana default150,tierIII,160XP, essência+bone+skull; sicknessT e learning separados. |
| Integração e authority | ISummon setter atua no contador consumido; stats de receita não são atributos automáticos; reload/owner/custos/dedup requerem contrato. |
| Evidência e validação | Identidade binária SHA-exata+source; não whole-method parity/runtime; mutating_hook=NOT_VERIFIED, physical_qa=NOT_TESTED. |

## Eventos, autoridade e integração

O [helper nativo][gate] grava owner UUID, chama `world.addFreshEntity` sem consultar o retorno, pode resolver a receita restante sobre o summon via Summoning Focus e publica [SummonEvent][summon-event]. O evento não implementa `ICancellableEvent`; reatribuir seus campos depois do spawn não refaz as operações anteriores. Alterar o objeto original por `ISummon.setTicksLeft` é uma API real, mas seu consumidor precisa ser verificado por classe: o caso Vex não equivale aos demais. Spawn/evento/retomada não comprovam novo cast pago ou aplicação de dano. Falha no gate de summon ou no spawn também não estabelece estorno do mana da composição.

[SummoningFocus][focus] pode dobrar `getTicksLeft` e adicionar Strength III por500ticks e Speed II por500ticks **quando** `summon.getOwner()` é um jogador com o Focus. Esse getter difere de `getOwnerAlt()`, usado pela réplica de Self numa AABB de bloco inflada30 e pelo listener de morte. O listener de morte aplica `thorns`5 ao atacante não-owner quando há fonte elegível; uma expiração com fonte nula não entra nesse ramo. Não generalizar esses caminhos para todo ISummon nem atribuir dano posterior ao glyph como `SpellDamageEvent` próprio. O helper também pode criar um child context e continuar a cadeia no summon antes de publicar o evento.

[SpellStats.Builder.build][builder] publica `SpellModifierEvent` com builder mutável; mutação *in-place* do original é uma superfície real. [EffectResolveEvent.Pre no resolver][resolve] consome cancelamento, mas substituir campos do payload não troca os locais já usados pelo resolver. `Post` pode ocorrer com Effect pulado/STOP_ALL e não é sucesso físico. O adapter seguro RPG Skill Tree/Black Arcana, com caps, fase, custos, ownership e deduplicação, **não foi comprovado**: `mutating_hook=NOT_VERIFIED`.

Ars mantém casting, mana do jogador, aprendizagem, summons e estados nativos; Source é outro recurso. [Custo de glyph configurável][part] e [admissão/pagamento da composição][cost] são operações separadas. RPG Skill Tree mantém progressão/perks por contrato; Black Arcana conserva seu casting, Corruption, Strain e WorldEffectPolicy. Não duplicar controle de owner, sickness, dano, recursos ou mastery a cada summon, ataque, tick, evento ou contexto filho.

## Evidência e validade

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Source oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release5.13.1. A [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) usa publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, e comprova **ID/classe**, sem equivalência integral de métodos Java/bytecode, configuração instalada ou gameplay. Grau `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`.

Source de vanilla herdado não foi integralmente auditado: valores finais de atributos, pathfinding, danos de arma/projétil, imunidades e ciclo de save/load exigem evidência adicional ou QA. São identificados os entrypoints e os limites concretos do source Ars, sem inventar fórmulas herdadas. Mudança de JAR, source, config, NBT, listeners ou consumidores exige reauditoria. Não houve implementação de perk, alteração de runtime ou promoção de Stage.

[gate]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L69-L114
[summon-api]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/entity/ISummon.java#L19-L50
[summon-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/SummonEvent.java#L14-L43
[focus]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/curios/SummoningFocus.java#L44-L99
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L270
[cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L273-L298
[part]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L150
[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[glyph]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonUndead.java#L27-L113
[skeleton-init]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonSkeleton.java#L43-L95
[skeleton-ai]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonSkeleton.java#L101-L175
[skeleton-life]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonSkeleton.java#L181-L206
[skeleton-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonSkeleton.java#L224-L306
[skeleton-api]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonSkeleton.java#L308-L345
[follow]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/goal/FollowSummonerGoal.java#L29-L132
[registration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L154-L158
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L375-L384
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L111-L115
