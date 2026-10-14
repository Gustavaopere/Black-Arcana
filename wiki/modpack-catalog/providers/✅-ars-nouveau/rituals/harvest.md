# Harvest

Status: `SOURCE-PINNED 5.13.1 / CROP-PROCESSING RITUAL`

- Registry id: `ars_nouveau:ritual_harvest`
- Class: `RitualHarvest`
- Source cost declaration: `100`
- Processing cadence: every `200` game ticks
- Horizontal range: `4` blocks; inspected vertical band: `-1..+1`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every 200 ticks, Harvest scans its bounded crop volume and handles provider-supported crop forms:

- mature Nether Wart: rolls drops, retains one replant unit, resets age to `0`;
- mature Cocoa: rolls drops, retains one replant unit, resets age to `0`;
- tagged harvest stems: processes drops and safely destroys the upper stem block;
- mature `CropBlock`: rolls drops, retains one matching seed/block item where available, then resets the crop to age `1`.

Generated drops are first inserted through the ritual tile's `InventoryManager` into connected/available storage. Remainders are spawned into the world. Mage Bloom Crop items are explicitly excluded from this insertion/drop path.

The processing helper calls `setNeedsSource(true)` on successful crop processing; the ritual's Source cost declaration is `100`. Because `needsSource` is provider state rather than a local integer debit in this class, this page does not infer one 100-Source payment per individual crop.

## Authority / Black Arcana boundary

Crop maturation checks, drop calculation, replanting, adjacent inventory insertion and Source settlement are Ars Nouveau authority. Black Arcana must not duplicate outputs, replant twice or grant per-crop cast/progression credit.

## QA

Source behavior is pinned to 5.13.1. Effective Source debit batching and compatibility with modded crop/drop/storage hooks remain runtime QA.

## Engenharia para perks — execução do ritual

- **Source pin:** [`RitualHarvest.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualHarvest.java), versão Ars Nouveau 5.13.1.
- **Volume/cadência:** `RitualHarvest.tick` roda a cada `200` ticks, percorrendo blocos de `pos.offset(4,-1,4)` a `pos.offset(-4,1,-4)` (9×3×9 posições candidatas antes de redirecionar para blocos acima). Não é varredura ilimitada, mas cada tentativa de drops e inventário tem custo.
- **Culturas:** Nether Wart AGE=3, Cocoa AGE=2, `HARVEST_STEMS` e `CropBlock.isMaxAge`. `processAndSpawnDrops` usa `Block.getDrops`, reduz uma seed/bloco quando replantando, tenta `tile.getInventoryManager().insertStack` e emite `ItemEntity` para sobras; exclui `MAGE_BLOOM_CROP` desse caminho.
- **Custo:** `setNeedsSource(true)` após work e `getSourceCost=100`; não inferir pagamento 100 a cada cultura a partir deste boolean. **Perks:** quantity, seed/loot/replant e Source pertencem à transação Ars; observer não pode duplicar drops.
- **Status:** ✅ código fonte exato; ⚠️ configurações e comportamento físico dos providers adicionais pendentes; ⛔ mutabilidade em ritual ou integração com Mastery não é provada pelos eventos de glyph. Ritual runtime permanece Ars Nouveau.
