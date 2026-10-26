# Ars Nouveau — Summon Vex

Status: `SOURCE-PINNED 5.13.1 / STATIC CONTRACT AUDITED / RUNTIME CONFIG QA PENDING`

`ars_nouveau:glyph_summon_vex`, `com.hollingsworth.arsnouveau.common.spell.effect.EffectSummonVex`; Conjuration,tierIII,mana default150. Invoca três `EntityAllyVex` com sword e IA aliada. O glyph configura duração pelo método herdado de Vex; a API de duração exposta pela subclasse usa **outro campo**, de modo que Dispel/Focus não podem ser tratados como alterações universais desse lifetime. [Glyph][glyph] [subclasse][vex-init].

## Glyph, posição e tempo solicitado

`canSummon` exige jogador real não FakePlayer, sem Summoning Sickness salvo creative [gate]. O ponto usa `safelyGetHitPos` (posição da entidade para EntityHitResult; senão hitlocation). **`T=(int)(20*(D+E*M))`**, defaults D=15s/E=10s, duration scalarM; T<=0 retorna sem spawn/sickness. Getters da config são diretos, sem fallback local. Compatíveis somente Extend/Reduce (`getSummonAugments`); não lê Split/AOE para a quantidade. [Glyph][glyph].

Laço fixo **3**. Cada spawn parte de BlockPos do hit com X/Z aleatórios−2…2 e Y=+2; chama `finalizeSpawn(MOB_SUMMONED)`, `setOwner(shooter)`, `setBoundOrigin`, **`setLimitedLife(T)` herdado**, depois helper. Não há teste próprio de chão, colisão, LOS ou claims nesse callback. Sickness do caster usa Tticks após o laço, sem checar sucesso de `addFreshEntity`.

## Dois contadores e dois caminhos de owner

[`EntityAllyVex`][vex-init] declara `private limitedLifeTicks` e `limitedLifespan`, mas **não implementa override de `setLimitedLife` nem tick que consuma esse campo privado**. O método chamado pelo glyph é o herdado vanilla Vex. Já `ISummon.getTicksLeft`, `setTicksLeft` e `onDispel` leem/escrevem **o campo privado da subclasse** [vex-save] [vex-goals]. `onDispel` retorna true depois de zerá-lo; esse retorno não prova descarte ou antecipação do lifetime vanilla. Não inferir fórmula final de expiração/morte vanilla sem seu executor auditado ou evidência em jogo.

Da mesma forma, `setOwner(LivingEntity)` da subclasse guarda `owner`; `getOwnerAlt()` o expõe. Esse método não equivale ao `getOwner()` herdado de Vex. SummoningFocus recebe SummonEvent e consulta **getOwner()**, não getOwnerAlt; logo não há prova de que o caminho com jogador preencha a condição de buffs/dobro. Mesmo que um listener chamasse `setTicksLeft`, isso alteraria o contador shadow e não o timer vanilla configurado por setLimitedLife. Os outros callbacks do Focus usam getOwnerAlt e têm condições próprias. [Vex init][vex-init] [getters/Dispel][vex-goals] [API][vex-save] [Focus][focus].

## IA, atributos e dano

Subclasse equipa **diamond sword** com dropChance0. Tipo registrado **0,4×0,8 blocos**, fireImmune e atributos por `Vex.createAttributes()`; esses entrypoints não fornecem aqui valores numéricos finais de HP/attack [vex-init] [registration] [attributes]. Goals incluem follow voador (speed1, parâmetros6/12), CopyOwnerTargetGoal e seleção de mobs cujo target/killCredit é o owner direto.

ChargeAttackGoal inicia se existe alvo, sem destino ativo, teste RNG `nextInt(7)==0` e distância²>4. Persegue olhos do alvo, chama **`doHurtTarget` quando bounding boxes intersectam**, desliga charging; se ainda próximo distância²<9 atualiza destino. Dano de arma/atributos é vanilla, não `IDamageEffect.attemptDamage` do glyph. Movimento customizado soma aceleração `speedModifier*0,05/distance` ao vetor, freia×0,5 perto do destino, e orienta yaw em graus a partir de atan2. Esses parâmetros são comportamento da IA/entidade, não velocidade de projétil ou range do cast [vex-goals] [vex-movement].

Team e `isAlliedTo` consultam **owner direto**; sem ele caem para super. Follow resolve `getSummoner` por UUID de jogador do mesmo level; seu fallback procura locais adequados, e a subclasse flying aceita ladder/leaves mais dois blocos livres [vex-save] [follow] [flying-follow]. Não prometer identificação persistente de aliados, LOS universal ou PvP bypass. Loot/equipamento/XP são suprimidos nos overrides; `die` publica Death com wasExpirationfalse, não um cast novo [vex-loot] [vex-save].

## Persistência e aquisição

Reader chama super, lê BoundX/Y/Z e `LifeTicks` por **`setLimitedLife` herdado**. Writer só grava LifeTicks privado se `limitedLifespan`; o construtor com owner o põe **false**, e não há setter local que o ative. Assim não há simetria demonstrada entre o TTL shadow escrito e o timer herdado lido. OwnerUUID é escrito via `putUUID`, mas reader testa `contains("OwnerUUID",8)` antes da leitura; o fallback é a string antiga Owner. Não há restauração explícita do objeto direto owner. Requer reloadQA; não afirmar NBT/owner/lifetime preservados integralmente [vex-save].

Receita **`ars_nouveau:conjuration_essence` + `minecraft:totem_of_undying`** [recipe]; XP default160/tierIII [xp], starter não [starter], [aquisição85/85](../../ACQUISITION.md). Mana default150 é componente da spell, sem taxa nova por cada Vex/ataque. SicknessT é uma condição do caster e não prova de equivalência ao contador shadow.

## Certificação estática individual — 25/10/2026

| Campo | Contrato documentado e limite |
|---|---|
| Identidade e release | `ars_nouveau:glyph_summon_vex`, EffectSummonVex/EntityAllyVex, Ars5.13.1; ID/classe do glyph compilados, consumidor auditado no source. |
| Comportamento e consumidores | Três Vex com AI/arma; setLimitedLife herdado separado de ISummon TTL/Dispel e getOwnerAlt separado de getOwner. |
| Parâmetros e caps | T=trunc(20*(15+10M)),T<=0 aborta;3fixo; charge RNG1/7 elegível, thresholds distância²4/9 e colisão para hurt. |
| Targeting e resultado | Posições discretas−2…2,Y+2; entidade0,4×0,8/fireImmune; dano do ataque vanilla não inventado. |
| Custos e aquisição | Mana default150,tierIII,160XP,essência+totem,starter não; sicknessT do caster. |
| Integração e authority | Setter público existente não garante alteração do timer vanilla; owner/getters/Focus/NBT precisam de adapter validado, sem novo settlement por hit. |
| Evidência e validação | Source pinado e identidade binária somente; ressalvas de shadow/NBT explícitas; mutating_hook=NOT_VERIFIED,physical_qa=NOT_TESTED. |

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
[glyph]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectSummonVex.java#L22-L91
[vex-init]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityAllyVex.java#L43-L100
[vex-goals]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityAllyVex.java#L103-L202
[vex-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityAllyVex.java#L205-L323
[vex-loot]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityAllyVex.java#L326-L354
[vex-movement]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/EntityAllyVex.java#L356-L383
[follow]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/goal/FollowSummonerGoal.java#L29-L132
[flying-follow]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/goal/FollowSummonerFlyingGoal.java#L9-L19
[registration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L76-L79
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L350-L355
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L105-L108
