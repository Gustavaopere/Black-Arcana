# Ars Nouveau — Toss

Status: `SOURCE-PINNED 5.13.1 / STATIC_TECHNICAL_CATALOG_ONLY / RUNTIME+CONFIG QA PENDING`.

- Registry ID: `ars_nouveau:glyph_toss`.
- Classe: `com.hollingsworth.arsnouveau.common.spell.effect.EffectToss`.
- Escola: Manipulation; tier default **1**, mana default **10**.

## Certificação estática individual — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Não certifica perk implementada, config física ou execução de modpack.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e release | `ars_nouveau:glyph_toss`, `EffectToss`, Ars Nouveau **5.13.1**, Manipulation. [Classe e execução][effect]. |
| Comportamento e causalidade | Retira stacks do inventário do caster, tenta inserção no handler do bloco atingido ou cria ItemEntity no destino. O budget reduz a **quantidade pedida**, não quantidade realmente extraída; a rotina continua mesmo com extração vazia [effect]. |
| Parâmetros, defaults e caps | Com presença de Extract, total1. Senão `(int)(64*Math.pow(2,amp))`; truncamento Java para finitos, subunidade vira0 e valor positivo acima do int satura Integer.MAX_VALUE. Não há clamp local de trabalho menor que isso. Cada iteração pede min(amount,64). Randomize é flag para escolha de slot, não altera total [effect]. |
| Targeting, geometria e resultado | EntityHit: blockPosition da entidade; criação em x+0.5,y,z+0.5. BlockHit: capability ItemHandler.BLOCK no bloco atingido com face null; sem ela, drop na posição adjacente à face. Sem raycast/velocidade de lançamento/raio/dano/status próprios; a Form define aquisição [effect]. |
| Custos e aprendizagem | Mana default **10**, tier **1**, recipe XP default **27**; tier I é herdado quando não há override [default-tier], starter default **não** [starter]. Receita: `ars_nouveau:manipulation_essence` + `minecraft:dropper` [recipe]. [XP por tier][xp] e [aquisição85/85](../../ACQUISITION.md). Custo configurado, composição, descontos, admissão e pagamento são separados [defaults] [cost]; mana de jogador e Source de automação não são o mesmo recurso. Sem cooldown adicional autônomo definido nesta classe. |
| Integração e autoridade | Ars mantém casting, recurso e inventários. [SpellModifierEvent pelo builder][builder] é superfície pública real para mutação in-place do builder original; reatribuir o campo do evento não troca os stats retornados. [EffectResolveEvent.Pre][effect-event] admite veto, mas [o resolver][resolver] usa seus objetos locais, não substituições dos campos do payload. Post também pode ocorrer sem ação bem-sucedida. Adapter RPG Skill Tree/Black Arcana com caps, recursos, causalidade e deduplicação seguros continua **não verificado**. Black Arcana mantém seu casting, Corruption, Strain e WorldEffectPolicy; RPG mantém progressão por contrato, sem repetir o efeito Ars. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. [Auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) comprova ID/classe entre109 registros, não equivalência integral dos métodos ou gameplay. Config instalada, listeners, addons, cliente/servidor e QA física permanecem pendentes: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Budget, seleção e fragmentação

`getStackSize` testa `hasBuff(Extract)` antes de ler amplification. Dampen/Amplify atuam através do scalar líquido; Extract força1 mesmo quando esse scalar seria maior/menor. O método não lê AOE, duração ou Pierce. Sem Extract, para quantidade positiva T há `ceil(T/64)` iterações; com scalar extremo a saturação em int ainda permite trabalho muito grande, até33.554.432 pedidos. Isso é limite aritmético, não cap seguro de gameplay [effect].

Cada loop escolhe size, chama extrator e consumer e **sempre** faz amount−=size. Um handler que retorna menos ou vazio não causa retry para completar a mesma parcela, nem encerra os próximos pedidos. Com isso o total nominal não garante quantidade transferida. Não transformar número de loops, pedidos, stacks ou drops em novo cast pago/mastery.

TileCaster aceita qualquer stack não vazia. Para não-tile, só aceita shooter Player e exclui stacks para os quais `ItemStack.matches(mainHand,i)` é true; essa comparação por conteúdo/count não é referência à identidade de um slot, e pode excluir stacks iguais em outras posições. `new InventoryManager(caster)` usa `getInventory()`, não `getInvManager()`; portanto **não herda** o extractSlotMax9 de PlayerCaster [effect] [player] [extract].

Sem Randomize, seleciona primeiro slot elegível do handler escolhido; Randomize escolhe uniformemente entre slots válidos **desse handler**, não entre todas as unidades/handlers do caster. `highestPrefInventory` inicia cada wrapper em LOW mesmo sem match e pode escolher um handler LOW não correspondente antes de outro LOW válido; a busca não garante achar qualquer item existente em outro inventário [selection] [random].

## Destino, sobra e prova de transferência

`summonStack` cria ItemEntity com cópia do extracted stack e depois seta count0 na referência, sem verificar boolean de addFreshEntity e sem testar extração vazia antes de criar a entidade. O código não configura shoot/deltaMovement: “Toss” não define parábola ou velocidade própria de projétil [effect]. Falha no spawn não desencadeia refund nessa rotina.

Quando o bloco possui handler, passa `simulate=false` em insertItemStacked e substitui stack pela sobra; `returnOrDrop` tenta slot original, depois o handler de origem e dropa o resto. Não é uma operação atômica nem idempotente comprovada: o helper não limpa sua própria referência após uma devolução integral, e o glyph não emite confirmação de quantidade liquidada [refund]. Não duplicar retirada/inserção/retorno num adapter. Nenhum teste local de claim/LOS é adicionado pelo glyph no destino; controles do handler, eventos e pack precisam de validação própria.

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
[effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectToss.java#L30-L127
[extract]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L37-L47
[selection]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L249-L276
[random]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L101-L124
[random-slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/InventoryManager.java#L200-L227
[refund]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/item/inv/ExtractedStack.java#L19-L68
[player]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/wrapped_caster/PlayerCaster.java#L21-L31
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L109-L109
