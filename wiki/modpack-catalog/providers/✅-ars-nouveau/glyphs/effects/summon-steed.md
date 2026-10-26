# Ars Nouveau — Summon Steed

Status: `SOURCE-PINNED 5.13.1 / STATIC CONTRACT AUDITED / RUNTIME CONFIG QA PENDING`

`ars_nouveau:glyph_summon_steed`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectSummonSteed`; Conjuration, tierI, mana default100. Invoca, por padrão, um cavalo domesticado e selado no ponto resolvido. AOE altera **quantidade**, não raio; a descrição de desaparecimento após alguns minutos corresponde ao contador da entidade, não a um cooldown do caster. [Glyph][glyph].

## Execução, parâmetros e targeting

`onResolve` exige `canSummon`: jogador real, excluindo FakePlayer, sem Summoning Sickness salvo creative [gate]. Só depois converte o caster para Player em `tameWithName`. O ponto é **`rayTraceResult.getLocation()`**, para hit de bloco ou entidade; o glyph não faz raycast, LOS, busca de chão, claims ou checagem própria de espaço livre. Todos os cavalos são inicialmente posicionados no mesmo ponto; a geometria/collision posterior pertence à entidade. [Glyph][glyph].

- Lifetime solicitado **`T=(int)(20*(D+E*M))`**, defaults D=300s, E=120s e M=`getDurationMultiplier()`. Se **T<=0**, substitui T por20ticks; T positivo entre1e19 não é elevado a20. Getters de config são usados diretamente, sem fallback local se ainda não inicializados. A config de D/E permite0…Integer.MAX_VALUE; o cast trunca para int.
- Loop literal `i<1+Math.round(AOE)`; baseline1, q=1→2cavalos. Não há mínimo/máximo explícito da quantidade no callback; q negativo injetado pode produzir zero emissões. Não aceitar isso como raio universal ou budget de entidades.
- Define `ticksLeft`, `tameWithName`, saddle no slot0 do horse inventory, owner UUID e dropChance CHEST0; delega ao helper por cavalo. Após o loop aplica Summoning Sickness **600ticks**, mesmo se o loop produzir zero cavalos; não consulta sucesso de `addFreshEntity`.
- Compatíveis: Extend Time, Reduce Time (`glyph_duration_down`) e AOE. O scalar de duração vem dos augments/stats; não muda a sickness600. Nenhum dano, projétil, canalização ou cooldown autônomo é calculado aqui.

## Consumidor, expiração e persistência

[`SummonHorse.tick`][horse-life] chama super e, no servidor, decrementa `ticksLeft`; quando <=0, remove por `DISCARDED` e publica `SummonEvent.Death` com fonte nula e `wasExpiration=true`. `onDispel` só zera o contador e retorna true; a remoção é no tick posterior, não sincronamente no callback. `die` publica Death com fonte e `wasExpiration=false`. Os eventos não constituem um token global que garanta uma única liquidação entre todos os caminhos.

O tipo tem tamanho registrado **1,3964844×1,6 blocos**, atributos base por `AbstractHorse.createBaseHorseAttributes()` [registration] [attributes]; valores finais vanilla/Curios/config não foram quantificados. Não há ataque/dano próprio no glyph ou nessa subclasse. A subclasse veta reprodução/comida/aceitar itens, fornece XP base0, esvazia `dropEquipment` e `openCustomInventoryScreen`; `mobInteract` apenas delega ao superclass, sem novo bloqueio explícito de owner. Não prometer exclusividade de montaria ou um segundo item saddle entregue ao caster [horse-restrictions].

O NBT local grava **`left`** e chama `ISummon.writeOwner` (chave **`owner`**); leitura local restaura apenas `left` após super. O owner customizado usa `OWNER_UUID` sincronizado, defaultNIL; não há chamada local `readOwner`/`setOwnerID` no reader. Portanto lifetime salvo é demonstrado, mas a simetria completa do owner customizado com o owner herdado do cavalo exige teste de reload; não declarar ownership persistente garantido [horse-save] [summon-api]. O contador é de ticks processados, sem deadline absoluto de mundo neste código.

## Custos e aprendizagem

Receita datagen **`minecraft:leather`×4** [recipe]; XP default **27**, tierI [xp]; starter default **não** [starter]. A [aquisição85/85](../../ACQUISITION.md) não prova config ou desbloqueio efetivo. Mana default100 é uma parcela da composição Ars, não custo adicional por cada cavalo nem Source de mundo.

## Certificação estática individual — 25/10/2026

| Campo | Contrato documentado e limite |
|---|---|
| Identidade e release | `ars_nouveau:glyph_summon_steed`, EffectSummonSteed, Ars5.13.1; source e classe/ID compilados. |
| Comportamento e consumidores | Invoca SummonHorse selado/domesticado; helper, evento, contador server e Dispel separados. |
| Parâmetros e caps | T=trunc(20*(300+120M)), T<=0→20; loop1+round(AOE), sem clamp local; sickness600ticks independente. |
| Targeting e resultado | Ponto do hit, todas emissões no mesmo ponto; entidade1,3964844×1,6; sem dano/range/área de ataque próprios. |
| Custos e aquisição | Mana default100, tierI,27XP, leather×4, starter não; custo efetivo provider-owned. |
| Integração e authority | ISummon setter nativo atua no contador real; owner, Focus, evento e settlement exigem contrato próprio; adapter não verificado. |
| Evidência e validação | Source pinado+identidade binária SHA-exata; config/owner reload/gameplay pendentes; mutating_hook=NOT_VERIFIED, physical_qa=NOT_TESTED. |

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
[glyph]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonSteed.java#L25-L98
[horse-life]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonHorse.java#L29-L86
[horse-restrictions]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonHorse.java#L89-L124
[horse-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/SummonHorse.java#L126-L160
[registration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L154-L158
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L350-L364
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L105-L108
