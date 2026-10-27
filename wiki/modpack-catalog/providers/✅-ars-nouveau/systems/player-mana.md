# Ars Nouveau — mana do jogador, reserva e settlement

**Estado:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.

Fonte `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, Ars Nouveau **5.13.1**. JAR de referência `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. Grau `PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`: source imutável e proveniência da release; os109 IDs compilados de glyphs/rituais não provam a identidade ou os corpos binários deste sistema. Esta ficha agrega contratos, sem criar um glyph, Thread ou registry ID autônomo.

## Identidade e escopo

Sistema agregado de `com.hollingsworth.arsnouveau.api.mana.IManaCap`, `common.capability.ManaCap/ManaData`, `api.util.ManaUtil` e `common.event.ManaCapEvents`. A entity capability é `ars_nouveau:mana`; o attachment persistente é `ars_nouveau:mana_cap`. [CapabilityRegistry][capability] registra o wrapper para EntityType.PLAYER. Isso não é um glyph nem define uma escola/dano/projétil; Source de mundo é outro recurso ([limite de Source](source-resource.md)).

| Campo de certificação | Contrato estático e limite |
|---|---|
| Identidade e versão | Capability mana + attachment ManaData, Ars5.13.1 source-pinned; sem registry ID único de spell e sem prova compilada específica do sistema. |
| Comportamento e causalidade | Estado persistente → fórmulas/cache de atributos → eventos → cap/reserve; tick regenera e sincroniza. Admissão e pagamento de spell recalculam custos em fases diferentes. |
| Parâmetros e caps | Defaults:100mana base,+15 por glyphBonus,+50 por bookTier; regen5+.33*g+t; intervalo5ticks. Atributos, eventos, reserva e ordenação alteram o resultado final. |
| Targeting e resultado | Estado do próprio Player/caster; sem targeting geométrico, projétil, dano, cooldown ou status temporal próprio. Curios/armadura/familiars contribuem por consumidores específicos. |
| Custos e aquisição | Mana rege casts Ars; glyphBonus e bookTier são caches persistidos atualizados por learning/bookuse. Admissão usa Pre; pagamento usa Post e o wrapper. Não é novo preço fixo por sistema. |
| API e integração | IManaCap tem get/set/add/remove, eventos públicos têm setters; APIs existem. Sync, clamps, fase, concorrência e settlement entre mods continuam sem adapter validado. |
| Evidência e validação | PINNED_SOURCE_WITH_RELEASE_SHA_ONLY, proveniência de release e source; mutating_hook NOT_VERIFIED e physical_qa NOT_TESTED, sem homologia de gameplay ou todos os bytecodes. |

## Estado persistente, caches e mutadores

[ManaData][data] serializa `current` double, `max` int, `glyph` int, `book_tier` int e `reserved` float. O attachment [mana_cap][attachment] é serializable e copyOnDeath; isso não prova o comportamento de todos os clones/reloads do pack. A deserialização chama setters de ManaData sem os clamps de ManaCap.

O g usado na fórmula é **getGlyphBonus armazenado**, não uma leitura direta de knownGlyphCount em cada cálculo. [Glyph.use][glyph] e [SpellBook.use][book] aumentam g até o tamanho do set conhecido quando este é maior; bookTier só aumenta nessa rotina e Creative não o eleva a99. Remover conhecimentos por outra API não comprova redução automática desses caches. Não confundir maior livro já usado com o livro atualmente na mão.

[ManaCap][cap] expõe mutadores reais. `setMana(x)` testa primeiro `x>max`, depois `x<0`, depois grava x e reescreve o attachment. Para max não negativo isso faz clamp usual; `setMaxMana`, `setGlyphBonus`, `setBookTier` e `setReserve` não fazem clamp local nem reclamp de current. `removeMana` transforma entrada negativa em0; `addMana` aceita incremento negativo e passa por setMana. Não são uma API de débito atômico com reserva/rollback ou sincronização automática. `syncToClient` é operação separada; o [packet][packet] restaura ManaData e o cache visual de reserva no cliente.

## Fórmulas e atributos

| Termo de ServerConfig | Default e unidade declarada |
|---|---|
| INIT_MAX_MANA / baseMax |100 unidades de mana |
| GLYPH_MAX_BONUS / glyphmax |15 por g armazenado |
| TIER_MAX_BONUS / tierMax |50 por t armazenado |
| INIT_MANA_REGEN / baseRegen |5, base de regen por segundo pretendida |
| GLYPH_REGEN_BONUS / glyphRegen |0.33 por g |
| TIER_REGEN_BONUS / tierRegen |1 por t |
| REGEN_INTERVAL / updateInterval |5 ticks; faixa de config1…20 |

[Defaults de config][config] são separados dos valores implantados. [calcMaxMana][max] constrói `raw=100+15*g+50*t` sob esses defaults. Se o atributo existe, mantém um modificador transitório ADD_VALUE `ars_nouveau:max_mana_mod`, substituindo-o somente quando amount difere, e usa o valor final de `PerkAttributes.MAX_MANA`. Trunca para int, publica MaxManaCalcEvent e lê max/reserve. O [RangedAttribute][attributes] MAX_MANA tem default0 e faixa0…10000; isso limita o atributo, não qualquer valor que listeners posteriores inventem.

[getManaRegen][regen] calcula `R0=5+0.33*g+t`, mantém ADD_VALUE transitório `ars_nouveau:max_regen_mod` e usa `PerkAttributes.MANA_REGEN_BONUS`, default0/faixa0…2000. Publica ManaRegenCalcEvent e lê getRegen. O [setter do evento][regen-event] usa max(newRegen,0), mas o construtor recebe o valor preliminar diretamente. Não duplicar os modificadores de cache nem interpretar R0 como todo o resultado após addons.

## Reserva, ordenação e regeneração

`Mana.getRealMax()` retorna `(int)(Max*(1.0-Reserve))` [max]. [MaxManaCalcEvent][max-event] inicia reserve0; setMax usa max(newMax,0). **setReserve contém literalmente `Mth.clamp(0,newReserve,1)`**, com o novo valor na posição do segundo argumento. O texto não certifica um clamp superior normal em1: a ordem dos argumentos precisa de auditoria do helper/binário e teste, especialmente para reserve>1. Uma extensão não deve assumir um intervalo seguro só porque o método chama clamp. Capmax negativo também invalida a afirmação universal de current≥0, pois setMana testa x>max antes de x<0.

[FamiliarEvents.maxManaCalc][familiar] adiciona o modificador do primeiro familiar matching e retorna; não soma arbitrariamente todas as instâncias. O default.15 fica em FamiliarEntity, mas callbacks de addons e ordem de dispatch podem modificar a reserva. Ver [familiares](../FAMILIAR-STATIC-SIX-5.13.1.md).

[PlayerTickEvent.Pre][tick] só processa ServerPlayer nos worldticks divisíveis pelo intervalo I. Primeiro regenera contra o capmax anterior, se current difere de max ou worldtime%60==0, adicionando `R/max(1,((int)MEAN_TPS/I))`; a divisão interna é inteira. Com TPS20/I5, isso dá R/4 por processamento, aproximadamente R por segundo a20TPS. Não é uma garantia contínua de R/s sob qualquer I/TPS. **Depois** recalcula max/reserve e usa setMaxMana sem reclamp imediato de current. Mudança de cap pode deixar estado temporariamente acima do novo máximo até outro setMana.

[MEAN_TPS][sync] é static, começa20 e é atualizado em Post a cada600worldticks pela média de tickTime da dimensão, limitado1…20 nesse caminho. Force sync ocorre em60worldticks, mas ainda dentro do gate de intervalo I; para I que não divide60 não presumir sync em todo múltiplo de60. Login, respawn e troca de dimensão recalculam cap/reserve e sincronizam. O antigo handler explícito de clone está comentado; copyOnDeath pertence ao attachment.

## Admissão e pagamento da spell

[Spell.getCost][spell-cost] soma custos configurados de parts, usando override de custo do augment para o receptor anterior. [Descontos][discount] acumulam IManaDiscountEquipment de Curios, armor e casterStack; itens presentes em mais de uma origem precisam de causalidade própria, sem promessa de dedup global.

[SpellResolver.enoughMana][admission] usa getResolveCost (SpellCostCalcEvent.Pre) e o wrapper; creative pode passar a admissão mesmo sem mana suficiente. [Casts][cast] só chamam expendMana quando o retorno da Form é CastResolveType.SUCCESS. [Pagamento][cost] recalcula custo em SpellCostCalcEvent.Post e faz max(0,currentCost); o caminho de turret TileCaster retorna antes do débito. [LivingCaster][living] compara current para admissão e chama removeMana para pagamento. Admissão, sucesso da Form, dano/mutação do mundo e pagamento não são uma operação indivisível. Um observer não deve cobrar de novo por resume, projétil ou proc.

## Autoridade e validade

Ars Nouveau mantém composição, recursos, itens, atributos e dados do jogador. RPG Skill Tree governa sua progressão por contrato real; Black Arcana mantém casting, Corruption, Strain, WorldEffectPolicy e causalidade próprios; Enshrouded mantém seus sistemas ambientais. APIs nativas existem, mas um adapter que preserve fase, caps, custos, persistência e deduplicação não foi validado. Não duplicar cast, cobrança, XP ou Mastery por tick, refresh, item equipado ou alteração de metadados.

Mudança de source, JAR, config, receitas, listeners ou codecs exige reauditoria. Config instalada, compatibilidade de addons, multiplayer, cliente/servidor, reload e persistência física permanecem pendentes. Não houve alteração de runtime, implementação de bridge ou promoção de Stage.

[cap]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ManaCap.java#L11-L102
[data]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ManaData.java#L20-L79
[interface]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/mana/IManaCap.java#L3-L29
[capability]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/CapabilityRegistry.java#L32-L68
[attachment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/AttachmentsRegistry.java#L22-L33
[max]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/ManaUtil.java#L52-L100
[regen]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/ManaUtil.java#L103-L128
[discount]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/ManaUtil.java#L24-L42
[config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/config/ServerConfig.java#L35-L45
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkAttributes.java#L23-L26
[max-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/MaxManaCalcEvent.java#L11-L35
[regen-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/ManaRegenCalcEvent.java#L6-L21
[tick]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/ManaCapEvents.java#L18-L47
[sync]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/ManaCapEvents.java#L50-L105
[packet]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/network/PacketUpdateMana.java#L32-L42
[familiar]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/FamiliarEvents.java#L67-L76
[spell-cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/Spell.java#L275-L290
[admission]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L86-L112
[cast]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L127-L171
[cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L273-L298
[living]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/wrapped_caster/LivingCaster.java#L57-L69
[book]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/SpellBook.java#L80-L100
[glyph]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/Glyph.java#L51-L68
