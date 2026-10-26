# Ars Nouveau — Harvest

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_harvest`
- Display name: Harvest
- School: Elemental Earth
- Default tier: 1
- Default mana cost: 10
- Compatible augments: AOE, Pierce, Fortune

## Provider-native behavior

Harvest operates on mature crops and similar harvestable vegetation, obtains drops and replants/reset states where appropriate. Source handling includes CropBlock, Nether Wart, Cocoa and provider harvest-stem tags. Fortune changes the loot context when present.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:iron_hoe`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this crop-harvest spell, its loot handling and replant semantics. Black Arcana should not duplicate generic remote crop harvesting or double-award drops when Ars is the causal provider.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectHarvest`).

## Engenharia para perks — caminho causal individual

- **Source pin:** [`EffectHarvest.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarvest.java) do Ars 5.13.1.
- **Targeting:** `onResolveBlock` usa `SpellUtil.calcAOEBlocks(shooter,hitPos,hit,stats)`; pode redirecionar FarmBlock e posições com Crop/NetherWart/`HARVEST_STEMS` acima. Seleciona Cocoa (AGE 2), Nether Wart (AGE 3), stem elegível ou `CropBlock.isMaxAge`.
- **Drops/replant:** `processAndSpawnDrops` usa `Block.getDrops` ou Fortune loot context com `count(Fortune)`, reduz 1 stack de seed/bloco que replanta quando apropriado, exclui `MAGE_BLOOM_CROP` do drop e gera `ItemEntity`. Restaura AGE 0 para Cocoa/NetherWart, AGE 1 para Crop; stem é quebrado por `destroyBlockSafely`.
- **Proteção/QA:** não há `destroyRespectsClaim` explícito no corpo deste `onResolveBlock`; não inferir bypass sem auditar pipeline de events/modpack. **Perks:** cada cultura é world mutation/loot do Ars, não multiplicador universal de rendimentos ou uma nova raiz de Mastery.
- **Estado:** ✅ origem e lógica source-pinned; ⚠️ helpers, itens externos e runtime QA pendentes; ⛔ adapter de perks do RPG sem teste nem contrato para duplo settlement. Ars conserva mana, inventário e efeitos.

## Certificação técnica estática — Harvest (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Classe `EffectHarvest` ↔ `ars_nouveau:glyph_harvest` comprovados no registry/binário do JAR Ars 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`; **não** se provou equivalência de método compilado. Fonte imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectHarvest.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHarvest.java), [BlockUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/BlockUtil.java), [LootUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/LootUtil.java).

| Campo para perks | Contrato source-pinned e incertezas |
|---|---|
| Seleção e deslocamento | `onResolveBlock` percorre `SpellUtil.calcAOEBlocks(...,spellStats)`. Se `FarmBlock` está na posição **ou** a posição `above()` contém `CropBlock`, `NetherWartBlock` ou `BlockTagProvider.HARVEST_STEMS`, move `blockpos=blockpos.above()`. Alvos AOE podem convergir para a mesma posição após deslocamento; não contabilizar por entrada de loop como colheita distinta. |
| Cocoa / Nether Wart | `harvestPods` exige `CocoaBlock.AGE==2`; `harvestNetherwart` exige `NetherWartBlock.AGE==3`. Após `processAndSpawnDrops(...,true)`, chama `world.setBlockAndUpdate` para reset `AGE=0`. **Não verifica o boolean da atualização** antes de considerar o ciclo executado; spawn de itens acontece antes do reset. |
| CropBlock | Se `crop.isMaxAge(state)` e `world instanceof ServerLevel`, chama `processAndSpawnDrops(...,true)` e `world.setBlockAndUpdate(blockpos,crop.getStateForAge(1))` — reset para **AGE=1**, não 0. `setBlockAndUpdate` não tem retorno verificado. Esse caminho difere de Cocoa/Wart, e o sucesso real depende de bloco e proteção do pack. |
| Stems | Se `state.is(BlockTagProvider.HARVEST_STEMS)` e `state.getBlock()==world.getBlockState(blockpos.below()).getBlock()`, chama `processAndSpawnDrops(...,false)` e depois `BlockUtil.destroyBlockSafely(world,blockpos,false,shooter)`. A classe **não checa o boolean de destroyBlockSafely**; `BlockEvent.BreakEvent` pode cancelar remoção mesmo após loot ser emitido. |
| Loot / Fortune / sementes | `processAndSpawnDrops` obtém `Block.getDrops(state,(ServerLevel)world,pos,world.getBlockEntity(pos))`; com `AugmentFortune` muda para `state.getDrops(LootUtil.getFortuneContext(...,count(AugmentFortune)))`. Para `takeSeedToReplant=true`, reduz com `i.shrink(1)` **somente a primeira stack BlockItem cujo bloco equivale ao bloco colhido**; não é garantia de consumo de semente para toda cultura modded. Filtra `BlockRegistry.MAGE_BLOOM_CROP.asItem()` e drops vazios antes de `world.addFreshEntity(new ItemEntity(...))`. Retorno do spawn não é verificado. |
| Claims, sides e autoridade | O `onResolveBlock` de Harvest **não chama diretamente** `BlockUtil.destroyRespectsClaim`. Stems usam `destroyBlockSafely` com `BlockEvent.BreakEvent` mas Cocoa, Wart e CropBlock fazem `setBlockAndUpdate` sem um preflight de claims explícito nesta classe; não inferir bypass confirmado no modpack. Os auxiliares `harvestPods`/`harvestNetherwart` fazem cast para `ServerLevel` em `processAndSpawnDrops`, sem guarda `ServerLevel` local nesses métodos; invocação pelo resolver/side deve ser confirmada, não assumida. `WorldEffectPolicy` de Black Arcana rege apenas mudanças próprias, RPG Skill Tree fornece progressão por bridge comprovada. |
| Custo | `getDefaultManaCost()=10`; augments compatíveis `AOE`, `Pierce`, `Fortune`. Não existe fórmula de XP/Mastery ou cooldown individual nesta classe. Drops e resets não são transações indivisíveis, e a AOE não deve multiplicar recompensas externamente. |

**Gates fail-closed:** World safety nos quatro tipos de bloco, callback de claims e server-side, chance de duplicação se reset/quebra cancelados, tags datapack HARVEST_STEMS, MAGE_BLOOM_CROP, diferenças da capacidade ItemEntity, harvest de mods de agricultura, limite de AOE e multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Nenhum Stage promovido.
