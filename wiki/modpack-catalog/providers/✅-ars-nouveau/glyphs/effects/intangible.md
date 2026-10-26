# Ars Nouveau — Intangible

Status: `SOURCE-PINNED 5.13.1 / STATIC TECHNICAL CONTRACT / RUNTIME QA PENDING`

- Registry id: `ars_nouveau:glyph_intangible`; classe `com.hollingsworth.arsnouveau.common.spell.effect.EffectIntangible`.
- Manipulation, tier default **III**, mana default **30**; augments Amplify/Dampen, Extend/Reduce Time, AOE e Pierce [config].
- Substitui blocos elegíveis por Intangible Air e guarda seu BlockState; o consumidor de restauração é IntangibleAirTile, não um status aplicado à entidade.

## Colocação, geometria e seleção

[onResolveBlock][resolve-block] calcula `duration=(int)(GENERIC_INT.get()+EXTEND_TIME.get()*durationMultiplier)` em segundos, com defaults **3 e1** [config]. O cast para int ocorre **antes** de `maxLength=duration*20`; fracionários de duração são truncados primeiro. Não lê contagens individuais de Extend/Reduce, não faz clamp final nem tratamento próprio de overflow/config não inicializada. Duration negativa ou zero não significa permanente.

[SpellUtil.calcAOEBlocks][grid] recebe AOE scalar e contagem Pierce: dimensões antes da orientação **1+floor(AOE)**, **1+ceil(AOE)**, profundidade **1+Pierce**; a face, direção do caster e parte do bloco atingida orientam/alinham a grade [grid-orientation]. Origem fica no fim da lista. Por exemplo AOE1 com Pierce0 dá grade2×2×1, não raio3×3. O alcance de aquisição pertence à Form, sem raycast/LOS ou projétil próprios. Não há budget adicional de blocos neste glyph além da lista resultante.

Cada posição é rejeitada se possui block entity, é air, está em `INTANGIBLE_BLACKLIST`, não é colhível ou `destroyRespectsClaim` falha. Harvest usa `destroySpeed>=0` e tier derivado de `(int)(3+amp)` [harvest]; não há fórmula numérica de dureza máxima proporcional ao dano. O [helper de claim][claims] publica BreakEvent com jogador/fake player, sem destruir bloco; permissão depende dos listeners. O código registra Block.getId(state), chama setBlockAndUpdate para INTANGIBLE_AIR **sem testar seu retorno**, então tenta configurar stateID/maxLength no tile. Não prova substituição bem-sucedida ou persistência durável somente por chegar ao fim do callback.

## Restauração, colisão e NBT

[IntangibleAirTile.tick][tile] roda no servidor: incrementa `duration` e restaura `Block.stateById(stateID)` quando `duration>maxLength`. Partindo de duration0 e maxLength=N≥0, a primeira tentativa é no **tick processado N+1**; N≤0 restaura no primeiro tick. São ticks de tile processados, não deadline absoluto de mundo: chunk sem ticking não consome esse contador. O tile envia update flag2 a cada tick; não há novo teste de claim, entidade ocupando o espaço ou compare-and-set explícito do estado esperado no trecho de restauração. Normal remoção do tile por substituição tem regras externas: não inferir que um tile já removido continuará restaurando mundo arbitrariamente.

`saveAdditional/loadAdditional` guardam **state_id, duration e max_length**, não snapshot completo de bloco/entidade/owner/receita. NBT usa ID numérico do BlockState; não é ledger portátil entre mudanças de registry/modpack. As atribuições no glyph e incrementos do tick não chamam setChanged explicitamente, ao contrário do [helper updateBlock][sync]; serialização disponível não comprova que cada valor foi salvo em crash ou unload real. `getUpdateTag` do ModdedTile usa saveAdditional, mas sincronização não equivale a durabilidade física.

[IntangibleAirBlock][air] tem `noCollission`, shapes de seleção/interação/oclusão vazios, shape de suporte cheio, `isAir=false`, PushReaction.BLOCK e rejeita líquidos. É um bloco provider-owned sem colisão, não ausência literal de bloco nem garantia de que fluidos/pathfinding/addons o tratem como ar. Blocos com block entity foram excluídos antes da transformação; não alegar preservação geral de inventários.

## Custos e aprendizagem

Receita [recipe]: `ars_nouveau:manipulation_essence + minecraft:phantom_membrane×3 + #c:ender_pearls×2`; **160XP**, starter **não** [xp] [starter]. Mana30/tierIII são defaults [config]; composição, config e preço efetivo Ars. Sem dano, DamageType, buff de entidade ou cooldown próprios. O ciclo de restauração não é novo cast/XP e não deve ser duplicado por Black Arcana. [Aquisição completa](../../ACQUISITION.md).

## Certificação estática individual — 25/10/2026

| Campo | Contrato e limite verificado |
|---|---|
| Identidade e versão | `ars_nouveau:glyph_intangible`, EffectIntangible, Ars5.13.1, Manipulation/tierIII. |
| Comportamento e causalidade | Grade de blocos filtrados → estado substituto + stateID → tile restaurador; sem ledger genérico de rollback [resolve-block] [tile]. |
| Parâmetros e caps | Segundos truncados antes de×20, defaults3+M; restore após ++counter>N. AOE/Pierce são grade orientada; Amplify altera harvest tier, não dano/dureza escalar [grid] [harvest]. |
| Targeting e resultado | Somente callback de bloco, sem block entity/blacklist/air/claimnegada; nenhum efeito de entidade, raio de aquisição ou projétil próprio. |
| Custos e aquisição | Mana30, tierIII, 160XP, essência+3membranes+2pearls, starter não; restauração não paga outro cast. |
| Integração e autoridade | Tile/BlockState/claim nativos Ars; API de stats não autoriza duplicar restauração ou usar o stateID como ledger Black Arcana. Adapter, durabilidade e dedup não validados. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, sem teste físico de colisão/restore/NBT. |

## Fronteira de perks e validade

`SpellModifierEvent` oferece uma API pública real no [builder original][builder]; mutação *in-place* é uma superfície distinta de substituir `event.builder`, que não é relido no retorno. [EffectResolveEvent.Pre no resolver][resolve] permite veto; trocar campos do payload não substitui os locais de alvo, effect, stats ou contexto. `Post` pode ocorrer sem aplicação efetiva. Uma lista de augments modificada não recalcula automaticamente scalars/flags já construídos.

Ars governa composição, estados, inventários e aprendizagem; RPG Skill Tree fornece progressão por contrato comprovado. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; Enshrouded mantém seus sistemas ambientais. Aplicação, tick, renderização, atualização de tile e callback não são novos casts pagos ou créditos de Mastery. [Admissão e pagamento][payment] são separados; custo default de um glyph não é preço final da composição e mana de jogador não é Source.

**✅ `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Fonte oficial `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; a [auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova **ID/classe**, sem correspondência integral dos métodos Java/bytecode. Config instalada, addons, proteção, persistência física, cliente/servidor e gameplay em modpack não foram validados. Mudanças de JAR, configuração, código ou consumidores exigem reauditoria.

[costs]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L127-L150
[starter]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractSpellPart.java#L307-L310
[xp]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L142-L157
[builder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellStats.java#L138-L152
[resolve]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L203-L270
[payment]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/SpellResolver.java#L273-L298
[resolve-block]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectIntangible.java#L25-L53
[config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectIntangible.java#L55-L101
[grid]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java#L33-L71
[grid-orientation]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java#L74-L160
[harvest]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java#L174-L180
[harvest-tier]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java#L47-L62
[claims]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java#L99-L105
[air]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/IntangibleAirBlock.java#L22-L76
[tile]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/IntangibleAirTile.java#L11-L46
[sync]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/ModdedTile.java#L26-L52
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L85-L85
