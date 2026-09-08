# Ars Nouveau — Harvest

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_harvest`
- Display name: Harvest
- School: Elemental Earth
- Default tier: 1
- Default mana cost: 10
- Compatible augments: AOE, Pierce, Fortune

## Provider-native behavior

Harvest operates on mature crops and similar harvestable vegetation, obtains drops and replants/reset states where appropriate. Source handling includes CropBlock, Nether Wart, Cocoa and provider harvest-stem tags. Fortune changes the loot context when present.

## Authority / deduplication

Ars Nouveau owns this crop-harvest spell, its loot handling and replant semantics. Black Arcana should not duplicate generic remote crop harvesting or double-award drops when Ars is the causal provider.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectHarvest`).
