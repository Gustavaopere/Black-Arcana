# Ars Nouveau — Summon Wolves

Status: `SOURCE-PINNED 5.13.1 / STATIC CONTRACT AUDITED / RUNTIME CONFIG QA PENDING`

`ars_nouveau:glyph_summon_wolves`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectSummonWolves`; Conjuration,tierI,mana default100. Invoca dois lobos domesticados, com variante do bioma e alvo inicial derivado do combate recente do caster. Contagem, lifetime de entidade e Summoning Sickness são eixos diferentes. [Glyph][glyph].

## Gate, duração, alvo e emissão

`onResolve` testa `canSummon(shooter)` e shooter não nulo; o helper permite só Player real, excluindo FakePlayer, sem Summoning Sickness salvo creative [gate]. O cast a Player usado por tame é protegido por esse gate. **`T=(int)(20*(D+E*M))`**, defaults D=60s/E=60s, M=durationMultiplier; se T<=0 retorna. Compatíveis apenas Extend/Reduce (`getSummonAugments`); sem scalar Amplify, AOE ou Split consumidor de quantidade nesse glyph. Os getters de config são diretos, sem fallback local [glyph].

Obtém variante de Wolf por bioma no BlockPos da **hitlocation**; laço fixo **2** cria lobos e coloca ambos exatamente nessa hitlocation. Define `ticksLeft=T`, variante, target **lastHurtMob**, ou lastHurtByMob se aquele é nulo, aggressive=true, tame=true e `tame((Player)shooter)`; delega ao helper. Não há neste callback filtro extra de aliados do alvo inicial, raycast, chão, espaço livre, claims ou LOS. Engine/AI pode rejeitar/substituir target; flags iniciais não garantem dano ou agressividade permanente.

Depois do laço aplica sickness por **Tticks**, independentemente de retorno de spawn ignorado. Se Focus dobrar o timer da entidade no SummonEvent, não reescreve automaticamente essa sickness do caster. O glyph não calcula dano de mordida, alcance de ataque, imunidades ou velocidade final.

## Consumidor, Dispel e save/load

[`SummonWolf.tick`][wolf-life] chama super e, no servidor, decrementa ticksLeft; <=0→poof, remoção DISCARDED e Death com fonte nula/wasExpirationtrue. `onDispel` zera o contador e retorna true, aguardando o tick para descarte. `die` publica Death com fonte e wasExpirationfalse. Não confundir esse contador real com a API shadow do Vex nem tratar todos os eventos como confirmação única de morte para mastery.

Tipo registrado **0,6×0,85 blocos**, atributos por `Wolf.createAttributes()`; os valores finais vanilla de HP/ataque/movimento não foram quantificados nesta auditoria [registration] [attributes]. A subclasse não substitui o executor de mordida; dano e IA de tame/owner são herdados. Veta canBreed/canMate/isFood e XP base0; não há aqui os mesmos overrides extensos de loot/equipamento de SummonSkeleton, logo não importar garantias de drops de outro summon [wolf-save].

NBT local salva/restaura **`left`** e **`wildenSummon`**. Owner customizado usa `OWNER_UUID` sincronizado, defaultNIL, que o helper define ao invocar; não há gravação/restauração explícita desse campo customizado nos métodos locais. A superclass tem seu próprio tame/owner state, cuja simetria com esse override de getOwnerUUID precisa de reloadQA. Não prometer UUID customizado persistente só porque a tame base é salva. Não há deadline de tempo absoluto neste consumidor: lifetime é contado em ticks de entidade processados [wolf-save] [summon-api].

## Custos e aprendizagem

Receita **`ars_nouveau:conjuration_essence` + `minecraft:bone`×3 + `ars_nouveau:wilden_wing`×4** [recipe]; XP default27/tierI [xp], starter não [starter], [aquisição85/85](../../ACQUISITION.md). Mana default100 é parcela configurável da composição Ars. Não debitar/certificar um novo cast por lobo, mordida, retarget ou tick.

## Certificação estática individual — 25/10/2026

| Campo | Contrato documentado e limite |
|---|---|
| Identidade e release | `ars_nouveau:glyph_summon_wolves`, EffectSummonWolves/SummonWolf, Ars5.13.1; ID/classe do glyph compilados, consumidor auditado no source. |
| Comportamento e consumidores | Dois lobos tame, variante de bioma, target inicial do caster; contador server, Dispel e Death separados. |
| Parâmetros e caps | T=trunc(20*(60+60M)),T<=0 aborta; N2fixo; sicknessT não acompanha necessariamente Focus no timer. |
| Targeting e resultado | Dois spawns no ponto do hit; tipo0,6×0,85; AI/dano herdados, sem range/área/dano autônomos do glyph. |
| Custos e aquisição | Mana default100,tierI,27XP,essência+bone×3+wing×4,starter não; sem custo próprio por cada ataque. |
| Integração e authority | ISummon setter atua no contador real; ownership customizado/tamebase/target/causalidade precisam de contrato validado. |
| Evidência e validação | Source pinado+identidade binária SHA-exata, config/UUIDreload/AIphysical pendentes; mutating_hook=NOT_VERIFIED,physical_qa=NOT_TESTED. |

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
[glyph]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonWolves.java#L23-L92
[wolf-life]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonWolf.java#L24-L62
[wolf-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonWolf.java#L65-L119
[registration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L144-L146
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L350-L364
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L105-L109
