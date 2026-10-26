# Ars Nouveau 5.13.1 — lote Effects: troca, processamento e menu

**Escopo:** quatro contratos `STATIC_TECHNICAL_CATALOG_ONLY` de glyph Effects existentes — Exchange, Crush, Smelt e Craft. Não houve criação de spells, itens, código Java ou adapter de integração Black Arcana/RPG Skill Tree. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.

## Fonte e estado da prova

- Modlist física do sibling RPG Skill Tree: `ars_nouveau-1.21.1-5.13.1.jar`, ID `ars_nouveau`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, Minecraft 1.21.1/NeoForge.
- Source exato de referência: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`. O [manifesto publisher de 109 IDs](EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md) prova identidade classe/ID, **não** equivalência do método no classfile ou efeito em execução no modpack.
- A documentação baseada em código não certifica um hook mutador externo. `EffectResolveEvent.Pre` e eventos vanilla/NeoForge não são, por si, aprovação para alterar range/loot/recipe outputs nem progressão causal de itens processados.

| Ficha | Fluxo e superfície | Risco que bloqueia perks sem adapter |
|---|---|---|
| [Exchange](glyphs/effects/exchange.md) — `EffectExchange` | EntityHitResult realiza até dois `EventHooks.onEnderTeleport`, cada um independente; BlockHitResult percorre `calcAOEBlocks` e processa `InventoryManager`, `LootUtil.getDefaultFakeTool` (Silk Touch), `breakExtraBlock`, `world.setBlock`, `ExtractedStack.replaceAndReturnOrDrop` | Teleport swap não é atômico. `firstBlock` é fixado depois da extração, **antes** do sucesso de placement; `setBlock` tem retorno ignorado antes de `stack.shrink(1)`, componentes e ShapersFocus. Não contabilizar quebra, reinsert ou troca como transação invariável. |
| [Crush](glyphs/effects/crush.md) — `EffectCrush` / `CrushRecipe` | `IDamageEffect` CRUSH, base3 e AMP1, base triplicada underwater; branch Sensitive AABB cap `(int)(4+4*AOE+4*Pierce)`; outputs RNG `chance`, `maxRange`, `skip_block_place` | `onResolveBlock` não aplica `destroyRespectsClaim` ou harvest gate diretamente, nem verifica o retorno de `setBlockAndUpdate` antes de gerar itens/propagar. Receita, rolls e outputs permanecem provider-owned; não duplicar drops. |
| [Smelt](glyphs/effects/smelt.md) — `EffectSmelt` | Block mode requer harvest/claim; SMELTING para blocos. Item mode cap `Math.round(4*(1+AOE+Pierce))`, Dampen→SMOKING, senão Amplify→BLASTING, senão SMELTING | **O ramo de output não-BlockItem não verifica `destroyBlockSafely`** após novo BreakEvent: mesmo se a remoção é negada, chama `addFreshEntity` do resultado. Condicionado a proteção/outputs, é risco de descompasso; não alegar exploit comprovado no cliente. BlockItem replacement também ignora `setBlockAndUpdate` return. |
| [Craft](glyphs/effects/craft.md) — `EffectCraft` | `shooter instanceof Player && isNotFakePlayer` abre `SimpleMenuProvider` com `CustomWorkbench extends CraftingMenu`; `stillValid(Player)` sempre true; augments vazios | Abrir UI não comprova craft nem consumo. Nada autoriza autocrafting, transmutação ou Mastery por slot/click com identidade do spell. Testes reais de menu continuam pendentes. |

## Guardrails arquiteturais

1. **Authority:** Ars retém mana, resolução, inventários, receitas, drops, teleport e `ShapersFocus`. `WorldEffectPolicy` aplica-se somente às mutações próprias do Black Arcana, não intercepta automaticamente os métodos provider-native aqui catalogados. RPG Skill Tree oferece apenas atributos/Mastery/perks/gates por contrato real.
2. **Causalidade:** em Exchange, parte do swap pode ser cancelada; em Crush, roll/placement/output não é uma transação atômica; em Smelt, claim preflight e destruição real podem divergir; em Craft, menu aberto não é produção concluída. Nenhum desses resultados pode creditar Mastery sem confirmação por destinatário apropriado.
3. **Custos e expansão:** defaults de mana Exchange **50**, Crush **30**, Smelt **100**, Craft **50**. AOE/Pierce influenciam tanto volume quanto limites de unidades; não inferir cooldown de spell individual nem custo por target.
4. **Clean-room:** somente documentação de interoperabilidade a partir de comportamento e assinaturas pinadas; nenhum corpo de implementação/asset do provider é incorporado ao Black Arcana.
5. **Gates:** hooks e adapters externos **NOT_VERIFIED**, QA in-game/provider-native **NOT_TESTED**; stages `06.05` e `09` permanecem sem promoção. CI/GameTests do Black Arcana não certificam gameplay de Ars.

## QA pendente
Confirmar classfile de métodos, listas e outputs de receita/datapack, eventos de bloco/teleporte, retorno `destroyBlockSafely=false`, resultado `world.setBlock`, proteção de claims por fake player, duplicação/rollback de inventário, recipe smelting case, server/client menu, configs, unload/reload, Source/mana e multiplayer.

**Contadores projetados após merge:** Effects **43/67**, Glyphs **61/85**, Ars Nouveau **85/138**, catálogo global **85/2075**, providers integralmente certificados **0/164**. Recortes por fichas identificadas não são total do universo mágico instalável.
