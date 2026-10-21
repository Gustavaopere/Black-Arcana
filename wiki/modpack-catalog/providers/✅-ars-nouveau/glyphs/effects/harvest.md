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
