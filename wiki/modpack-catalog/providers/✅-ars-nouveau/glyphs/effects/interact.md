# Ars Nouveau — Interact

Status: `SOURCE-PINNED 5.13.1 / STATIC_TECHNICAL_CATALOG_ONLY / RUNTIME+CONFIG QA PENDING`.

- Registry ID: `ars_nouveau:glyph_interact`.
- Classe: `com.hollingsworth.arsnouveau.common.spell.effect.EffectInteract`.
- Escola: Manipulation; tier default **1**, mana default **10**.

## Certificação estática individual — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Não certifica perk implementada, config física ou execução de modpack.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e release | `ars_nouveau:glyph_interact`, `EffectInteract`, Ars Nouveau **5.13.1**, Manipulation. [Classe e execução][effect]. |
| Comportamento e causalidade | Emula chamadas de interação por Player real ou ANFakePlayer, com caminhos de entidade/bloco distintos. Dampen é presença que aplica Shift/CROUCH temporário; Amplify seleciona attack **só no ramo bloco**; Sensitive tem decisões de mão próprias por ramo [entity] [block]. |
| Parâmetros, defaults e caps | Compatíveis Sensitive/Amplify/Dampen, limite default1 cada [interact-config]. Não usa amplification numérico para dano/quantidade: hasBuff(Amplify) chama BlockState.attack e retorna. Dampen pode estar presente mesmo com amp líquido0. Nenhuma AOE, duração, cooldown ou budget de multi-target próprio. |
| Targeting, geometria e resultado | Um hit de entidade ou bloco adquirido pela Form. Em bloco valida destroyRespectsClaim(pos) e INTERACT_BLACKLIST; essa validação emite BreakEvent e não equivale a um gate universal de uso/PvP [block] [claim]. Entidade não tem esse gate local. Sem dano, cura ou projétil próprios; callbacks de blocos/itens/entidades podem produzir resultados externos. |
| Custos e aprendizagem | Mana default **10**, tier **1**, recipe XP default **27**; tier I é herdado quando não há override [default-tier], starter default **não** [starter]. Receita: `ars_nouveau:manipulation_essence` + `minecraft:lever` + `#minecraft:wooden_pressure_plates` + `#minecraft:buttons` [recipe]. [XP por tier][xp] e [aquisição85/85](../../ACQUISITION.md). Custo configurado, composição, descontos, admissão e pagamento são separados [defaults] [cost]; mana de jogador e Source de automação não são o mesmo recurso. Sem cooldown adicional autônomo definido nesta classe. |
| Integração e autoridade | Ars mantém casting, recurso e inventários. [SpellModifierEvent pelo builder][builder] é superfície pública real para mutação in-place do builder original; reatribuir o campo do evento não troca os stats retornados. [EffectResolveEvent.Pre][effect-event] admite veto, mas [o resolver][resolver] usa seus objetos locais, não substituições dos campos do payload. Post também pode ocorrer sem ação bem-sucedida. Adapter RPG Skill Tree/Black Arcana com caps, recursos, causalidade e deduplicação seguros continua **não verificado**. Black Arcana mantém seu casting, Corruption, Strain e WorldEffectPolicy; RPG mantém progressão por contrato, sem repetir o efeito Ars. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. [Auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) comprova ID/classe entre109 registros, não equivalência integral dos métodos ou gameplay. Config instalada, listeners, addons, cliente/servidor e QA física permanecem pendentes: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Entidade e seleção de mão

No ramo normal, `player.interactOn(target,MAIN_HAND)`. Com Sensitive, usa `getHand`: MAIN_HAND para **ANFakePlayer**, OFF_HAND para os demais Players. Para LivingEntity chama primeiro `item.interactLivingEntity`; se o retorno não for exatamente SUCCESS, chama também `target.interact`, inclusive para outros resultados que podem consumir ação. Em entidade não viva chama target.interact diretamente. Não chamar isso de uma única interação efetiva garantida [entity] [entity-use].

`Dampen` liga Shift e Pose.CROUCHING e depois escreve o estado salvo no retorno normal. Na entidade, esse backup é capturado **antes** de substituir `player` pelo ANFakePlayer de setup; um não-player pode obter inicialmente FakePlayerFactory por UUID e depois usar o singleton ANFakePlayer. No ramo bloco, o backup do fake é atualizado depois dessa troca. Logo a restauração não prova preservar o estado anterior de toda instância fake, e não há try/finally para exceções de item/addon [entity] [block] [fake-player]. Amplify não substitui interações de entidade por ataques; sua leitura está em `useOnBlock` [block].

## Bloco, bucket e fake inventory

`useOnBlock` escolhe OFF_HAND quando Sensitive, MAIN_HAND caso contrário, **inclusive para o fake player**. Se há Amplify, chama `blockstate.attack` e retorna, sem executar uso/bucket. No fluxo normal tenta `blockstate.useItemOn`; se consumesAction registra critério. Caso contrário BucketItem tem precedência e chama handleBucket; só depois PASS_TO_DEFAULT_BLOCK_INTERACTION com MAIN_HAND tenta `useWithoutItem` [block]. O retorno de interação não é exposto como confirmação de efeito pelo callback do glyph.

Bucket vazio busca BucketPickup na posição ou adjacente à face, chama pickupBlock e produz filled result/estatísticas/critério conforme retorno e infinite materials. Bucket cheio usa emptyContents; o retorno controla recipiente vazio e efeitos de critério. Algumas inserções de recipiente podem dropar ItemEntity se Player.addItem falhar [bucket]. A permissão prévia é do bloco original; não inferir uma segunda validação de claim em toda posição adjacente modificada pelo item.

Para caster não real, `setupFakeInventory` obtém ANFakePlayer, limpa inventário/mãos, extrai uma unidade pelo manager e coloca uma cópia na MAINHAND; OFFHAND fica vazia [fake]. Portanto Sensitive no bloco não promete usar o item extraído: escolhe a OFFHAND vazia. Sensitive na entidade usa getHand(fake)=MAIN_HAND. Jogador real usa as próprias mãos e **não passa por essa extração de setup**; o limite9 de extração do manager PlayerCaster não muda essa seleção de mãos [player]. Casters tile normalmente fornecem inventários adjacentes.

Após uso fake, o ramo bloco percorre `player.inventory.items` **e offhand**, devolvendo cada stack por `manager.insertOrDrop`. O ramo entidade percorre somente `items`, sem loop equivalente de offhand [entity] [block]. A referência ExtractedStack original não é devolvida diretamente e a ação pode transformar/consumir itens. Não prometer restituição exatamente uma vez, preservação de itens em addons ou conservação em exceção sem um contrato e teste próprios. InsertOrDrop tenta inventários e solta remainder; a lista de preferências usa PriorityQueue percorrida por iterator, não poll ordenado, logo a preferência declarada não prova ordem estrita de todas as inserções [insert].

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
[effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInteract.java#L45-L87
[entity]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInteract.java#L53-L87
[bucket]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInteract.java#L90-L140
[entity-use]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInteract.java#L143-L157
[block]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInteract.java#L159-L223
[fake]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInteract.java#L225-L235
[fake-player]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/ANFakePlayer.java#L26-L61
[interact-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectInteract.java#L238-L274
[claim]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java#L99-L105
[insert]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L59-L94
[priority]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L234-L246
[player]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/wrapped_caster/PlayerCaster.java#L21-L31
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L86-L86
