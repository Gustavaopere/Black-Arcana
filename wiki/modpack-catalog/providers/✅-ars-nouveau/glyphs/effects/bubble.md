# Ars Nouveau — Bubble

Status: `SOURCE-PINNED 5.13.1 / BUBBLE + EVENT CONSUMERS AUDITED / CONFIG + PHYSICAL QA PENDING`

- Registry id: `ars_nouveau:glyph_bubble`; classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectBubble`.
- Release **5.13.1**, Elemental Water; tier default **I**, mana default **20** [part] [bubble-glyph].
- Compatíveis Extend Time, Reduce Time (`glyph_duration_down`), Amplify e Dampen [bubble-config].

## Criação e parâmetros realmente consumidos

[EffectBubble][bubble-glyph] cria uma `BubbleEntity` no ponto do hit. No ramo entidade, faz `addFreshEntity` e depois `tryCapturing(target)`; não testa o resultado do spawn nem da captura. No bloco só posiciona/spawna; a captura pode ocorrer em ticks posteriores. Owner é atribuído quando `isNotFakePlayer(shooter)`; esse método rejeita FakePlayer, não exige que todo caster seja Player [real-player]. A Form governa aquisição do hit, sem alcance/raycast/área autônomos do glyph.

Construtor recebe **maxAge=(int)(100+M*E)** e **damage=(float)(D+A*a+d)**: M=`durationMultiplier`, a=`ampMultiplier`, d=`damageModifier`; defaults E=3, D=5, A=2 [bubble-glyph] [bubble-config]. O comentário genérico de `addExtendTimeConfig` fala em segundos, mas esse consumidor **não multiplica E por20** [config-helper]. maxAge é comparado com `age` incrementado uma vez por tick servidor: nominal **100+3M ticks**, não100+60M. Sem clamp final de maxAge/damage no glyph. A contribuição Extend e o bônus de dano são eixos diferentes; duração da animação de pop é outra contagem.

## Captura, movimento e término

[BubbleEntity.tryCapturing][capture] exige `!HAS_POPPED`, passageiros vazios e `canHitEntity`; chama `startRiding` e retorna se conseguiu passageiro. `canHitEntity` não delega ao filtro padrão de Projectile: veta UUID registrado em `hasDismounted`, Player dormindo, tag `BUBBLE_BLACKLIST` ou alvo já montado em Bubble. Não há veto local universal a owner/aliados nem verificação explícita de LOS/claims [filters].

O tick servidor incrementa age e chama `pop` quando **age>maxAge**; depois, se está vazio, varre sua bounding box inflada0,5 em todas as direções e tenta montar os candidatos, zerando boardingCooldown e restaurando o anterior somente se `startRiding` falhar [bubble-tick]. Esse laço **não passa por `tryCapturing` nem verifica HAS_POPPED**, de modo que o pop não estabelece bloqueio de nova captura durante a remoção diferida. O tipo registrado mede0,5×0,5; a busca inflada mede1,5×1,5×1,5 nos defaults geométricos [bubble-type]. Não é um raio de captura contínuo nem um orçamento universal de alvos.

A cada tick atribui delta `(R[-0,01;0,01],0,1,R[-0,01;0,01])` e move diretamente por `setPos(position+delta)`; este trecho não faz raycast de colisão. `pop()` apenas seta HAS_POPPED e toca som uma vez; não causa dano por si. `poppingTicks` sobe enquanto a flag está true; remove no servidor quando **poppingTicks>5**, portanto expiração/captura/bonificação de dano não são liquidadas no mesmo instante [bubble-tick] [pop]. Dismount registra UUID para evitar nova captura pelo filtro local; posição do passageiro é a da bolha, exceto item com +0,25Y [capture] [filters].

## Dano: bônus ao evento existente, não golpe novo

`ArsNouveau` registra os três listeners estáticos da entidade: `onAttacked`, `entityHurt` e `preEntityRemoval` [registration]. Em [LivingDamageEvent.Pre][damage-handler], se a vítima está montada numa Bubble, age>1, `!bubble.hasPopped` e o primeiro passageiro é diferente do owner, soma o damage calculado à **nova damage do evento já em curso**. Se owner é LivingEntity com `PerkAttributes.SPELL_DAMAGE_BONUS`, soma também esse atributo. A fonte/atacante do dano original não são trocados aqui; não há novo `IDamageEffect.attemptDamage` ou `SpellDamageEvent` emitido por esse método. A contribuição calculada não possui clamp positivo local e pode ser não positiva conforme os stats; não criar um golpe positivo separado a partir dela. Listener ordering, imunidades e settlement final permanecem downstream.

**Flag divergente:** o teste lê o boolean comum `hasPopped`; `pop()` escreve o dado sincronizado **HAS_POPPED**, e não há atribuição ao campo comum na classe inspecionada. Não é comprovado um bônus “uma única vez por bolha”: eventos adicionais enquanto a vítima permanece passageira podem passar pelo guard. `entityHurt` chama pop mesmo se a bonificação não foi aplicada; `preEntityRemoval` também seta a flag sincronizada. Um adapter deve observar dano realmente liquidado, preservar sua causa e deduplicar, sem somar outra bonificação [pop] [damage-handler].

Ataque de Player à bolha vazia/com item/ou consigo como primeiro passageiro chama pop e cancela `AttackEntityEvent`; se o passageiro é outro LivingEntity, chama `player.attack(passenger)`. `hurt` na própria Bubble apenas chama pop quando vazia/com item e retorna true. Não confundir retorno true com dano próprio aplicado à bolha [attacked]. `canBeHitByProjectile` tem precedência `empty || (firstIsItem && alive && age>1)`, distinta da condição de bônus de dano [bubble-save].

## Persistência, aquisição e fronteira

`save/load` escreve/lê **maxAge, damage e age** além da herança. HAS_POPPED, poppingTicks, plain hasPopped e hasDismounted não são gravados explicitamente nesses métodos. Owner/passageiros dependem da herança; não foi validada recuperação coerente de captura/pop/dedup em reload físico [bubble-save].

Receita: `#c:feathers` ×3 + `minecraft:water_bucket` + `#minecraft:boats` + `ars_nouveau:water_essence` [recipe]. TierI/**27XP** [xp], starter default **não** [starter], [aquisição85/85](../../ACQUISITION.md). Mana20 é default, sujeito a config e composição [part]; maxAge e poppingTicks não são cooldown. Uma nova magia não deve duplicar a mesma prisão/elevação e bônus sem uma diferença mecânica explícita.

## Certificação estática individual — 25/10/2026

| Campo | Contrato e limites |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_bubble`, EffectBubble, Ars5.13.1; ElementalWater, tierI; BubbleEntity concreta auditada. |
| Comportamento e causalidade | Hit→spawn→captura/montaria→ticks/pop→remoção; dano usa listener do passageiro e evento original, não pop() isolado. |
| Parâmetros e caps | maxAge=(int)(100+3M)ticks default; damage=5+2a+d, mais atributo do owner no listener; age>maxAge/poppingTicks>5; sem clamp final local. |
| Targeting e resultado | Ponto/entidade selecionado pela Form, tentativa imediata e busca AABB inflada0,5; filtros próprios, sem LOS/ally veto universal; deltaY0,1/tick. |
| Custos e aprendizagem | Mana20, tierI,27XP, receita feathers×3/waterbucket/boat/wateressence; starternão; custo/config e duration separados. |
| Integração e autoridade | Não assumir once-only por HAS_POPPED; duas flags divergem e captura automática tem outro gate. Preservar damage source/cast e evitar novo golpe/XP por pop/passenger/tick. |
| Evidência e validação | Source pinado + ID/classe no publisher SHA-exato; NOT_VERIFIED/NOT_TESTED; event ordering, reload, imunidade e modpack físico pendentes. |

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
[bubble-glyph]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBubble.java#L20-L55
[bubble-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectBubble.java#L58-L87
[bubble-tick]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/BubbleEntity.java#L36-L102
[capture]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/BubbleEntity.java#L104-L121
[pop]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/BubbleEntity.java#L124-L132
[attacked]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/BubbleEntity.java#L134-L183
[damage-handler]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/BubbleEntity.java#L148-L169
[filters]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/BubbleEntity.java#L195-L216
[bubble-save]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/entity/BubbleEntity.java#L225-L249
[bubble-type]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/ModEntities.java#L307-L311
[real-player]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L104-L114
[registration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/ArsNouveau.java#L102-L104
[config-helper]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L150-L176
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L128-L128
