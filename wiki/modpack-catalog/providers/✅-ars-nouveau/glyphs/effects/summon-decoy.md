# Ars Nouveau — Summon Decoy

Status: `SOURCE-PINNED 5.13.1 / GLYPH + DUMMY LIFECYCLE AUDITED / CONFIG + PHYSICAL QA PENDING`

- Registry id: `ars_nouveau:glyph_summon_decoy`; classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectSummonDecoy`.
- Release **5.13.1**, Conjuration; tier default **III**, mana default **200**.
- Augments nativos Extend Time e Reduce Time (`glyph_duration_down`) [decoy-config] [summon-augments].

## Entrada, alvo e atração real

[EffectSummonDecoy.onResolve][decoy] usa o gate `canSummon`: jogador real, sem Summoning Sickness, ou creative que ignora essa sickness; FakePlayer não é aceito por esse helper [summon-helper] [real-player]. Cria **um** `EntityDummy`, usando `safelyGetHitPos`: posição atual da entidade para EntityHitResult, senão localização do hit; spawn em **pos.y+1**. O override aceita HitResult diretamente, não se limita ao dispatcher bloco/entidade do AbstractEffect. Sem alcance ou projétil próprios; a Form governa aquisição.

Define `ticksLeft=(int)(20*(B+M*E))`, defaults B=30s e E=15s, nominal **600+300M ticks**, sem clamp final local [decoy] [decoy-config]. Passa pelo helper `summonLivingEntity` para owner, spawn, possível child context de Focus e `SummonEvent`. O helper ignora o retorno de `addFreshEntity`; a sequência posterior do glyph não prova que o spawn foi aceito [summon-helper].

Em seguida faz `getEntitiesOfClass(Mob.class,dummy.boundingBox.inflate(20,10,20))` e chama **uma vez `setTarget(dummy)` para cada Mob** [decoy]. Com tipo1×2, é uma caixa nominal **41×22×41 blocos**, não raio20 ou apenas20×10×20 [dummy-type]. Sem filtro local explícito de hostil, aliado, owner, LOS ou claims; ser candidato Mob não garante que AI, eventos/addons ou o próximo tick mantenham o alvo. Não é taunt permanente nem obrigação de todos os mobs atacarem até o fim.

O glyph aplica `applySummoningSickness(shooter,1)` após a busca. O helper constrói `MobEffectInstance(...,time)` diretamente: **1 tick nominal**, não1segundo, sem vínculo automático com o tempo restante do dummy [summon-helper]. Config de status/eventos pode modificar a manifestação em jogo.

## Consumidor EntityDummy

[EntityDummy.registerGoals][dummy-goals] registra Float, LookAtPlayer, RandomLookAround e WaterAvoidingRandomStroll; não há goal de ataque local nessa classe. Registro de atributos: HP **20**, movimento **0,25**; não fornece uma fórmula de ataque própria [dummy-attributes]. Skin/nome/equipamento são apresentação derivada do owner; `getItemBySlot` retorna EMPTY no servidor e `setItemSlot` é vazio. Logo não é cópia funcional do equipamento/inventário do caster [dummy-visual].

No tick servidor, **a cada world.getGameTime()%10==0**, se `level.getPlayerByUUID(getOwnerUUID())==null`, remove e publica `SummonEvent.Death(...,didExpire=false)`; essa condição inclui owner não encontrado no nível atual, não apenas desconexão global. Caso contrário, decrementa ticksLeft e ao chegar **<=0** remove e publica Death com `didExpire=true` [dummy-tick]. É contador de ticks processados, não deadline absoluto do mundo. Ausência do owner e expiração têm causas distintas; client cosmetics não criam créditos de combate.

`die` chama o pai e `onSummonDeath(...,false)`; `onDispel` seta ticksLeft=0 e retorna true, aguardando tick para remoção. Não há remoção imediata garantida pelo retorno de Dispel [dummy-die] [dummy-dispel]. Ao desaparecer, esta classe não percorre novamente os mobs para restaurar alvos anteriores; retargeting é responsabilidade downstream da AI/engine/addons.

Save/read registra `left` e `owner` por `ISummon.writeOwner`/`setOwnerID`; owner também tem SynchedEntityData própria. A entidade não serializa os antigos targets dos mobs atraídos nem um token global do cast [dummy-save] [summon-interface]. Não transformar cada target alterado ou Death em cast/Mastery adicional.

## Focus, custos e aquisição

[SummoningFocus][focus] tem listener que, sob condição de owner com o Curio, dobra `getTicksLeft`, aplica Strength500ticks/amplifier2 e Speed500ticks/amplifier1. O helper pode resolver receita restante no novo caster dummy; Self simpático pode propagar futuras composições a summons do owner numa AABB inflada30. Não é nova aprendizagem/pagamento nem prova de sucesso de dano; o Curio não cria goal de ataque no dummy por esse método [summon-helper].

Receita: `ars_nouveau:conjuration_essence` + `minecraft:armor_stand` ×4 [recipe]. TierIII/**160XP** [xp], starter default **não** [starter], [aquisição85/85](../../ACQUISITION.md). Mana200 default está separado do custo configurado total, descontos e fases de admissão/pagamento [part] [resolve]. Summoning Sickness1tick, TTL do dummy e qualquer cooldown de casting não são o mesmo parâmetro.

A semântica já ocupada é um decoy temporário que recebe targets na criação. Nova magia original precisaria de outro contrato, por exemplo uma política de ameaça com confirmação/retorno explícitos; mudar nome/VFX ou repetir o mesmo setTarget por outro mod não cria uma mecânica nova nem uma integração validada.

## Certificação estática individual — 25/10/2026

| Campo | Contrato e limites |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_summon_decoy`, EffectSummonDecoy, Ars5.13.1, Conjuration/tierIII; EntityDummy auditado. |
| Comportamento e causalidade | Gate canSummon→um dummy→setTarget único por Mob candidato→sickness1tick; tick/owner/Dispel/morte controlam término. |
| Parâmetros e caps | T=(int)(20*(30+15M)) default; HP20/speed0,25; busca inflate20/10/20; owner check worldtime%10; sem clamp final de T. |
| Targeting e resultado | Pos do hit/entidade+1Y; caixa nominal41×22×41; sem filtro local hostil/LOS/aliado, sem sustained taunt ou dano próprio. |
| Custos e aprendizagem | Mana200, tierIII,160XP, conjuration essence+armorstand×4, starternão; TTL e sickness distintos de custo/cooldown. |
| Integração e autoridade | Atração, AI e owner são Ars; spawn/evento não garantem alvo mantido, dano ou cast pago adicional. Preservar dedup e cause/expiry. |
| Evidência e validação | Source pinado+ID/classe SHA-exatos, NOT_VERIFIED/NOT_TESTED; persistência/source behavior não equivale a gameplay/bridge RPG aprovado. |

## Evidência, API e autoridade

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Grau `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. A [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) comprova ID/classe, não equivalência integral dos métodos Java/bytecode, config instalada ou gameplay.

[SpellStats.Builder.build][builder] publica `SpellModifierEvent` depois dos augments/itens e devolve os stats do builder original; mutação *in-place* tem superfície pública real. Reatribuir `event.builder` não troca o objeto retornado. [EffectResolveEvent.Pre][event] permite veto; [o resolver][resolve] consulta cancelamento, mas não relê substituições de payload `spellStats`, `rayTraceResult`, `resolveEffect` ou `context` como novos locais. `Post` pode ser publicado em `STOP_ALL`/skip; não confirma captura, dano, spawn ou restauração bem-sucedidos.

Ars mantém casting, mana de jogador, aprendizagem e entidades/estados nativos. Source de mundo não é mana do jogador. RPG Skill Tree fornece progressão apenas por contrato comprovado; Black Arcana conserva seu próprio casting, Corruption, Strain, WorldEffectPolicy e causalidade; Enshrouded conserva seus efeitos ambientais. Nenhum tick, passageiro, alvo adicional, callback de morte ou contexto derivado é automaticamente outro cast pago ou crédito de Mastery. Adapter seguro, custos/caps configurados, listeners, claims/PvP, save/reload, multiplayer e QA físico continuam pendentes. Mudança de JAR, source, configuração ou consumidores exige reauditoria. Nenhum hook executável foi implementado nesta ficha.

[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L220-L279
[event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50
[part]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L150
[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[decoy]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonDecoy.java#L18-L35
[decoy-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonDecoy.java#L38-L76
[summon-helper]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L69-L89
[real-player]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L104-L114
[summon-augments]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L225-L231
[dummy-goals]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityDummy.java#L40-L76
[dummy-tick]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityDummy.java#L90-L108
[dummy-die]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityDummy.java#L177-L180
[dummy-visual]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityDummy.java#L183-L222
[dummy-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityDummy.java#L230-L265
[dummy-dispel]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityDummy.java#L274-L277
[dummy-type]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L176-L181
[dummy-attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L365-L367
[summon-interface]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/entity/ISummon.java#L19-L49
[focus]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/curios/SummoningFocus.java#L66-L98
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L105-L105
