# Ars Nouveau — Access Ender Inventory

Status: `SOURCE-PINNED 5.13.1 / STATIC_TECHNICAL_CATALOG_ONLY / RUNTIME+CONFIG QA PENDING`.

- Registry ID: `ars_nouveau:glyph_ender_inventory`.
- Classe: `com.hollingsworth.arsnouveau.common.spell.effect.EffectEnderChest`.
- Escola: Manipulation; tier default **2**, mana default **50**.

## Certificação estática individual — 25/10/2026

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** Não certifica perk implementada, config física ou execução de modpack.

| Campo | Contrato e limites source-pinned |
|---|---|
| Identidade e release | `ars_nouveau:glyph_ender_inventory`, `EffectEnderChest`, Ars Nouveau **5.13.1**, Manipulation. [Classe e execução][effect]. |
| Comportamento e causalidade | `onResolveEntity` abre o **Ender Chest do caster**, se shooter é Player e não FakePlayer. O alvo atingido não é consultado como dono do inventário; `openMenu` recebe `SimpleMenuProvider` com `ChestMenu.threeRows` [effect]. |
| Parâmetros, defaults e caps | `getCompatibleAugments()` vazio; nenhum consumo de AOE, amplification, duração ou contagem. `ChestMenu.threeRows` fixa o tipo de menu; a classe não implementa slots extras, cópia de itens nem um inventário próprio [effect]. |
| Targeting, geometria e resultado | Requer resolução com EntityHitResult, mas o callback não filtra nem usa a entidade do hit. Bloco herda callback vazio [dispatch]. Sem dano, status, projétil, área, alcance ou duração próprios; aquisição é da Form. Não promete acesso a baú de terceiro nem que qualquer hit de bloco abra a interface. |
| Custos e aprendizagem | Mana default **50**, tier **2**, recipe XP default **55**; tier I é herdado quando não há override [default-tier], starter default **não** [starter]. Receita: `ars_nouveau:manipulation_essence` + `minecraft:ender_chest` [recipe]. [XP por tier][xp] e [aquisição85/85](../../ACQUISITION.md). Custo configurado, composição, descontos, admissão e pagamento são separados [defaults] [cost]; mana de jogador e Source de automação não são o mesmo recurso. Sem cooldown adicional autônomo definido nesta classe. |
| Integração e autoridade | Ars mantém casting, recurso e inventários. [SpellModifierEvent pelo builder][builder] é superfície pública real para mutação in-place do builder original; reatribuir o campo do evento não troca os stats retornados. [EffectResolveEvent.Pre][effect-event] admite veto, mas [o resolver][resolver] usa seus objetos locais, não substituições dos campos do payload. Post também pode ocorrer sem ação bem-sucedida. Adapter RPG Skill Tree/Black Arcana com caps, recursos, causalidade e deduplicação seguros continua **não verificado**. Black Arcana mantém seu casting, Corruption, Strain e WorldEffectPolicy; RPG mantém progressão por contrato, sem repetir o efeito Ars. |
| Evidência e validação | `PINNED_SOURCE_PLUS_SHA_EXACT_BINARY_IDENTITY`: source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, release **5.13.1**; publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`. [Auditoria compilada](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) comprova ID/classe entre109 registros, não equivalência integral dos métodos ou gameplay. Config instalada, listeners, addons, cliente/servidor e QA física permanecem pendentes: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. |

## Execução e inventário efetivamente aberto

`onResolveEntity` lê `player.getEnderChestInventory()` e passa essa referência existente ao menu vanilla com nome traduzido `container.enderchest` [effect]. Não busca um bloco Ender Chest no mundo nem exige tal bloco nesse método. A descrição “from anywhere” não autoriza aumentar alcance da Form, ignorar regras de outro menu ou mudar o proprietário.

O retorno de `player.openMenu(...)` não é inspecionado pelo callback. Portanto retorno normal do glyph ou `EffectResolveEvent.Post` não comprova abertura efetiva, acesso autorizado por todos os addons, alteração de slot ou transferência. Distância de validade, lifecycle do menu e persistência do Ender inventory pertencem às classes vanilla chamadas; esta auditoria não inventa fórmula ou prazo que não existe no glyph.

Não há `onResolveBlock` próprio. [AbstractEffect.onResolve][dispatch] só despacha EntityHitResult ao método acima; um hit de bloco segue o método vazio herdado. “Remote storage” aqui é acesso à UI pessoal, não leitura/mutação remota de inventários arbitrários. Para uma mecânica Black Arcana original, diferenciar a semântica do simples acesso que Ars já fornece.

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
[effect]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectEnderChest.java#L18-L61
[dispatch]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/spell/AbstractEffect.java#L55-L67
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/datagen/GlyphRecipeProvider.java#L67-L67
