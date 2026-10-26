# Ars Nouveau — Infuse

Status: `SOURCE-PINNED 5.13.1 / STATIC_TECHNICAL_CATALOG_ONLY / RUNTIME+CONFIG QA PENDING`.

- Registry ID: `ars_nouveau:glyph_infuse`.
- Classe: `com.hollingsworth.arsnouveau.common.spell.effect.EffectInfuse`.
- Escola: sem override de escola; o default retorna conjunto vazio [school]; tier default **2**, mana default **30**.

## Certificação estática individual — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Não certifica perk implementada, config física ou execução de modpack.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e release | `ars_nouveau:glyph_infuse`, `EffectInfuse`, Ars Nouveau **5.13.1**, sem override de escola; o default retorna conjunto vazio [school]. [Classe e execução][effect]. |
| Comportamento e causalidade | `onResolve` escolhe uma emissão de ThrownPotion quando AOE>0 **ou** durationMultiplier>0; sem isso despacha resolução normal, que somente em LivingEntity obtém e aplica conteúdo. A extração ocorre antes do efeito/entidade, sem transação conjunta comprovada [effect]. |
| Parâmetros, defaults e caps | AOE>0 tem precedência e seleciona SPLASH; senão duração>0 seleciona LINGERING. São seletores de modo, não escalas contínuas de raio/tempo. AOE/Extend Time são os únicos augments compatíveis, defaults de limite1 cada [infuse-config]. Conteúdo e modificadores da flask determinam amplifier/duration dos status [flask]. |
| Targeting, geometria e resultado | Aplicação direta: somente LivingEntity; PotionUtil usa instant effect com fator1.0 ou target.addEffect, sem fórmula universal de dano/cura. Emissão: uma ThrownPotion(owner=shooter), criada exatamente na posição do hit, sem shoot/velocidade explícita. Splash/lingering lifetime/impacto são vanilla, não quantificados aqui [effect] [apply]. |
| Custos e aprendizagem | Mana default **30**, tier **2**, recipe XP default **55**; tier I é herdado quando não há override [default-tier], starter default **não** [starter]. Receita: `ars_nouveau:abjuration_essence` + `minecraft:glass_bottle` + `#c:rods/blaze` [recipe]. [XP por tier][xp] e [aquisição85/85](../../ACQUISITION.md). Custo configurado, composição, descontos, admissão e pagamento são separados [defaults] [cost]; mana de jogador e Source de automação não são o mesmo recurso. Sem cooldown adicional autônomo definido nesta classe. |
| Integração e autoridade | Ars mantém casting, recurso e inventários. [SpellModifierEvent pelo builder][builder] é superfície pública real para mutação in-place do builder original; reatribuir o campo do evento não troca os stats retornados. [EffectResolveEvent.Pre][effect-event] admite veto, mas [o resolver][resolver] usa seus objetos locais, não substituições dos campos do payload. Post também pode ocorrer sem ação bem-sucedida. Adapter RPG Skill Tree/Black Arcana com caps, recursos, causalidade e deduplicação seguros continua **não verificado**. Black Arcana mantém seu casting, Corruption, Strain e WorldEffectPolicy; RPG mantém progressão por contrato, sem repetir o efeito Ars. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. [Auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) comprova ID/classe entre109 registros, não equivalência integral dos métodos ou gameplay. Config instalada, listeners, addons, cliente/servidor e QA física permanecem pendentes: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Seleção e consumo de poção

`getPotionData` usa `spellContext.getCaster().getInvManager()`. Primeiro extrai **uma unidade** de stack cujo `PotionProviderRegistry.from` seja não nulo e `!provider.isEmpty`. Essa rota inclui as flasks **e `Items.POTION`**, mapeado para provider DEFAULT [provider-map]; não há prioridade absoluta “todas as flasks antes das poções normais”. O manager escolhe handler/slot conforme seu algoritmo e filtros, não o tipo desejado pelo designer [extract]. No PlayerCaster esse manager limita extração aos primeiros9 slots; TileCaster usa inventários adjacentes [player] [tile].

No ramo provider, lê `getPotionData`; se o item é PotionFlask, transforma todos os efeitos base/custom por `getModifiedPotionContents`. Depois chama `consumeUses(stack,1,shooter)` e `returnOrDrop`. O componente MultiPotionContents subtrai1 charge sem teste creative nesse método [flask] [charges]. O provider DEFAULT para poção normal subtrai1 do stack salvo Player com infinite materials, mas para Player tenta `player.inventory.add(GLASS_BOTTLE)` **mesmo creative**, sem inspecionar o boolean; não-player subtrai1 e não recebe esse bottle nessa rotina [provider-consume]. Não reexecutar o consumo nem prometer devolução de recipiente independente do ramo.

Somente se a primeira extração estiver vazia tenta `PotionItem`: lê POTION_CONTENTS, `shrink(1)` salvo infinite materials e então **substitui** a referência extraída por glass bottle para retorno/drop, inclusive no caminho creative. Esse fallback pode atingir PotionItem não mapeado ou rejeitado pelo predicate do provider. Não confundir essa substituição com o bottle inserido pelo provider DEFAULT [effect].

Após qualquer ramo, se `potionData==null`, procura tile próximo `PotionJarTile` com `amount>100`, lê seus dados e remove100. Exatamente100 **não** passa; não há busca esférica configurável: o default IWrappedCaster retorna null, TileCaster examina seis vizinhos e escolhe o primeiro elegível [nearby] [tile]. O método não exige `canAccept` nem extrai player mana desse jar; `PotionJarTile.remove` reduz fill, limpa dados se chegar a0 sem lock e atualiza o bloco [jar]. A eventual rota de fallback após payloadnull não desfaz consumo já realizado.

## Aplicação, limites e retorno

`PotionUtil.applyContents` aplica cada MobEffectInstance instantâneo com source/indirect=shooter e fator1.0; os não instantâneos seguem `target.addEffect(instance)` sem um cálculo de duração próprio de Infuse [apply]. Payload, immunities, listeners e a implementação do MobEffect governam o resultado final. Não substituir esse caminho por IPotionProvider.applyEffects, pois o glyph chama **PotionUtil**.

AOE vence quando AOE e duração são positivos juntos. O frasco é posicionado no hit sem tiro explícito; o boolean de `world.addFreshEntity` não é usado para desfazer o consumo. Sem stats positivos e sem LivingEntity, não há rota de conteúdo em bloco herdada. Não há gate local de aliados/LOS/claims no callback; a falta desse gate não certifica permissões globais do pack.

`ExtractedStack.returnOrDrop` tenta slot original e depois o handler original; só dropa remainder. Não é garantia idempotente: ao devolver integralmente, o método não zera sua própria referência `stack` [refund]. Chamar retorno duas vezes por adapter não é seguro por suposição. A seleção também tem limitações: highestPrefInventory inicia cada wrapper em LOW, podendo escolher um handler sem match antes de outro LOW elegível; a prioridade não garante encontrar toda poção disponível em qualquer handler [selection].

## Validade e fronteira de integração

Um menu aberto, evento Post, tentativa de uso, frasco emitido ou quantidade solicitada não confirma o inventário final, cura, dano ou novo cast. Um listener de perk precisa observar a operação realmente liquidada e preservar a identidade causal da composição. Não pagar recursos nem conceder Mastery novamente por item, alvo, retorno, tick ou contexto derivado.

Mudança de JAR, source, configuração, datapack, itens/capabilities externos ou listeners exige reauditoria. Nenhum hook executável ou Stage foi promovido nesta documentação.
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[effect-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/EffectResolveEvent.java#L11-L50
[resolver]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L270
[cost]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L273-L298
[defaults]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L226-L237
[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[default-tier]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L144-L150
[xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInfuse.java#L34-L113
[infuse-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInfuse.java#L116-L148
[school]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L189-L195
[provider-map]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/registry/PotionProviderRegistry.java#L77-L86
[provider-consume]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/registry/PotionProviderRegistry.java#L21-L55
[flask]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/PotionFlask.java#L102-L117
[charges]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/MultiPotionContents.java#L39-L57
[apply]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/util/PotionUtil.java#L56-L64
[extract]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L96-L124
[selection]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L249-L276
[refund]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/ExtractedStack.java#L31-L68
[player]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/wrapped_caster/PlayerCaster.java#L21-L31
[tile]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/wrapped_caster/TileCaster.java#L30-L58
[nearby]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/wrapped_caster/IWrappedCaster.java#L36-L41
[jar]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/PotionJarTile.java#L104-L109
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L116-L116
