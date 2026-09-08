# Ars Nouveau — Fell

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_fell`
- Display name: Fell
- School: Elemental Earth
- Default tier: 1
- Default mana cost: 150
- Compatible augments: AOE, Extract, Fortune, Amplify, Dampen

## Provider-native behavior

Fell performs a bounded depth-first traversal over provider-tagged fellable vegetation. Source defaults cap the harvested set at 50 blocks, with an additional configured 50-block allowance per AOE multiplier. Claim/harvest checks are applied per block. Extract uses a silk-touch loot context; Fortune uses a fortune loot context.

## Authority / deduplication

Ars Nouveau owns this whole-tree/vegetation harvesting primitive. Black Arcana must not introduce a generic duplicate mass-felling spell or duplicate provider loot settlement. Independent destructive vegetation magic remains subject to Black Arcana `WorldEffectPolicy` and bounded-work rules.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFell`).
