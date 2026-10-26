# Ars Nouveau — Item Pickup

Status: `SOURCE-PINNED 5.13.1 / STATIC_TECHNICAL_CATALOG_ONLY / RUNTIME+CONFIG QA PENDING`.

- Registry ID: `ars_nouveau:glyph_pickup`.
- Classe: `com.hollingsworth.arsnouveau.common.spell.effect.EffectPickup`.
- Escola: Manipulation; tier default **1**, mana default **10**.

## Certificação estática individual — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Não certifica perk implementada, config física ou execução de modpack.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e release | `ars_nouveau:glyph_pickup`, `EffectPickup`, Ars Nouveau **5.13.1**, Manipulation. [Classe e execução][effect]. |
| Comportamento e causalidade | `onResolve` consulta itens na level do contexto, zera pickup delay **antes** de Pre, respeita canPickup().isFalse, insere via manager e grava remainder no ItemEntity. Post recebe esse remainder, não quantidade adquirida. XP tem ramo independente com evento cancelável [effect]. |
| Parâmetros, defaults e caps | Somente AOE compatível. `expansion=2+AOE`; AABB de canto BlockPos(hit) ±expansion, sem teste de esfera/distância adicional e sem teto local de entidades por passagem. Manager recebe extractSlotMax(-1), embora esta operação use inserção [effect]. |
| Targeting, geometria e resultado | Override onResolve vale para o HitResult que chega ao callback; não exige bloco/entidade específicos. Centro é canto inteiro BlockPos, não centro+0.5 nem coordenada fracionária. Sem LOS/owner/ally/pickup-delay gate local antes de busca; Pre e handler/inventário podem vetar. Sem DamageType/status/projétil/cooldown próprios. |
| Custos e aprendizagem | Mana default **10**, tier **1**, recipe XP default **27**; tier I é herdado quando não há override [default-tier], starter default **não** [starter]. Receita: `minecraft:hopper` ×2 [recipe]. [XP por tier][xp] e [aquisição85/85](../../ACQUISITION.md). Custo configurado, composição, descontos, admissão e pagamento são separados [defaults] [cost]; mana de jogador e Source de automação não são o mesmo recurso. Sem cooldown adicional autônomo definido nesta classe. |
| Integração e autoridade | Ars mantém casting, recurso e inventários. [SpellModifierEvent pelo builder][builder] é superfície pública real para mutação in-place do builder original; reatribuir o campo do evento não troca os stats retornados. [EffectResolveEvent.Pre][effect-event] admite veto, mas [o resolver][resolver] usa seus objetos locais, não substituições dos campos do payload. Post também pode ocorrer sem ação bem-sucedida. Adapter RPG Skill Tree/Black Arcana com caps, recursos, causalidade e deduplicação seguros continua **não verificado**. Black Arcana mantém seu casting, Corruption, Strain e WorldEffectPolicy; RPG mantém progressão por contrato, sem repetir o efeito Ars. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. [Auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) comprova ID/classe entre109 registros, não equivalência integral dos métodos ou gameplay. Config instalada, listeners, addons, cliente/servidor e QA física permanecem pendentes: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Eventos e contabilidade efetiva

A busca usa `spellContext.level`; Pre faz `getPlayer(shooter,(ServerLevel)world)`, enquanto Post usa casterWorld. O fluxo normal de resolver é servidor; a anotação nullable no shooter não torna segura chamada direta com null, pois getPlayer usa a entidade. Não chamar callback no cliente ou com level arbitrária por analogia [effect] [get-player].

`i.setPickUpDelay(0)` já alterou o ItemEntity quando Pre ocorre. Se o stack está vazio ou canPickup().isFalse, pula a inserção, **sem restaurar o atraso anterior**. Senão `manager.insertStack(stack)` retorna sobra; o glyph usa `i.setItem(sobra)` e publica `ItemEntityPickupEvent.Post(player,i,sobra)`. Ele não mede original−remainder nem testa se houve uma única unidade inserida. O callback não chama explicitamente discard do ItemEntity após stack vazio; cleanup subsequente é externo [effect]. Não inferir pickup integral, XP, refund de mana ou proc confirmado a partir de Post.

`InventoryManager.insertStackWithReference` tenta cada FilterableItemHandler elegível, passa `simulate=false` e interrompe quando remainder fica vazio. `preferredForStack` produz PriorityQueue, porém a execução percorre essa coleção com for-each; não garante ordenação estrita por prioridade. `extractSlotMax(-1)` não é budget de entidades, unidades ou slots de inserção [insert] [priority]. Não confundir inventário do caster com o ItemEntity do mundo nem executar inserção novamente em um listener.

Para cada ExperienceOrb na mesma caixa, exige shooter Player real e `spellContext.castingTile==null`; publica PickupXp cancelável, dá `orb.value` via giveExperiencePoints e remove DISCARDED. Caster tile não recebe essa experiência mesmo se houver um shooter/fake. O glyph não usa PlayerXpEvent para novo cast ou Mastery: número de orbs não é número de conjurações [effect].

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
[effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectPickup.java#L28-L94
[get-player]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L92-L94
[insert]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L59-L94
[priority]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L234-L246
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L97-L97
