# Ars Technica 2.7.6 — dossiês individuais de engenharia (11/11)

**✅ 10 efeitos + 1 augment source-located e individualizados** na branch PR #796. A `main` já possuía [GLYPHS.md](GLYPHS.md) com os 11 objetos em tabela, mas faltavam arquivos `glyphs/*.md` para cada objeto; estes 11 são novos arquivos, **não 11 novas magias**.

Mod físico: `ars_technica-1.21.1-2.7.6.jar`, SHA-1 `adb2641d538375f6eff6a22f0196bb330ab0b171`. Código Java `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`, versões de compilação Ars 5.11.0 / Create 6.0.8 versus pack Ars 5.13.1 / Create 6.0.10. IDs registry binários já estavam comprovados; source ↔ body JAR/compatibilidade runtime não estão.

| Objeto | Mana/tier default | Branch/limite rastreado | Risco/estado |
|---|---|---|---|
| [EffectCarve](glyphs/carve.md) | 10, I | Stonecutting/Create CUTTING; stairs/walls/slabs; input×output | ⚠️ recipe selection, overflow, duplicate item entities; ⛔ adapter RPG |
| [EffectPack](glyphs/pack.md) | 10, I | grid clamp((int)AMP+2,1,3), floor(items/grid²) | ⚠️ recipe/datapack / residual balance; ⛔ adapter RPG |
| [EffectPolish](glyphs/polish.md) | 120, II | ArcanePolishEntity; max4×(1+roundAOE)×focus2; speed2×focus2.5 | ⚠️ entity lifecycle/depot; ⛔ adapter RPG |
| [EffectObliterate](glyphs/obliterate.md) | 100, III | ArcaneHammerEntity, cancel parent, child resolver; Fortune max4 | ⚠️ world effects/loot/hit descendants; ⛔ adapter RPG |
| [EffectPress](glyphs/press.md) | 100, II | Depot Press; Sensitive Pack; Extract Compact; Superheat/Smelt heat | ⚠️ item/fluid, mode precedence; ⛔ adapter RPG |
| [AugmentSuperheat](glyphs/superheat.md) | 150, III | augment de Fuse e Press, não cast autônomo | ⚠️ Create heating tier configured; ⛔ adapter RPG |
| [EffectFuse](glyphs/fuse.md) | 75, I | ArcaneFusionEntity; regular/Smelt-heated/Superheat-super | ⚠️ child causal dedup; ⛔ adapter RPG |
| [EffectWhirl](glyphs/whirl.md) | 40, II | ArcaneWhirlEntity radius1.5+0.33AOE duration360+40T; 4 fan modes | ⚠️ persistent processing work budget; ⛔ adapter RPG |
| [EffectInsert](glyphs/insert.md) | 15, I herdado | containers cube; IItemHandler, Split distribution | ⚠️ potential validPositions=0 division; ⛔ adapter RPG |
| [EffectTelefeast](glyphs/telefeast.md) | 10, II | item/fluid container, lava drain250 + damage50, forwarding Pierce | ⚠️ resource conservation, harm and ingestion; ⛔ adapter RPG |
| [EffectApply](glyphs/apply.md) | 80, I | offhand or InventoryManager; block/item recipes, cap4(1+roundAOE) | ⚠️ helper count mismatch, block protection; ⛔ adapter RPG |

## Conclusões de integração

- `AbstractItemResolveEffect` escaneia `ItemEntity` em AABB centrada no hit com expansão `2+AOE`, não scan global; `EffectInsert` também percorre cada BlockPos de um cubo com possível amplificação cúbica.
- `EffectInsert.processItemsSplit` divide pelo tamanho da lista `validPositions`, sem cheque local de zero; confirmar garantias de `StorageHelpers.getValidStorePositions` e reprodução em cliente/servidor antes de declarar bug.
- `EffectApply.InventoryApplyItemSource.consumeItems(count)` aparentemente chama extração do InventoryManager para 1 item, independentemente de `count`, enquanto `PlayerApplyItemSource` usa shrink(count); divergência source-only, potencial risco de saldo, sem reproduzir duplicação.
- `EffectApply.handleBlockApplication` modifica blocos com `world.setBlock(...)` sem `destroyRespectsClaim` expresso **no método**. Verificar admissão geral/pacote de proteções; não declarar bypass sem evidência completa.
- `EffectFuse`/`EffectObliterate` cancelam contexto pai e criam child resolver; `EffectPress`/`EffectWhirl` consomem próximo glyph como seletor de processamento; nunca premiar child/processing ticks como novos casts ou aplicar mana duas vezes.
- Nenhum comportamento Create pode ser duplicado pelo RPG Skill Tree; adapters de perks não demonstrados. Black Arcana original conserva casting, hazards/WorldEffectPolicy sobre seus próprios efeitos.

Status: ✅ identificação e engenharia documental / ⚠️ host JAR-config/QA / ⛔ hook/perk não implementado. Nenhum Stage promovido, nenhum teste GameTest/CI/Survival nesta campanha.

[README](README.md) · [registro binário](EXACT-BINARY-GLYPHS-2.7.6.md) · [padrão global](../../meta/PERK-READY-TECHNICAL-STANDARD.md).
