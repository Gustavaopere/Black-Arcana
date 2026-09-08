# Ars Nouveau — Cut

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_cut`
- Display name: Cut
- School: Manipulation
- Default tier: 1
- Default mana cost: 0
- Compatible augments: Extract, Fortune, Amplify, Dampen
- Default Amplify limit: 2
- Source default base damage: 1
- Source default Amplify scalar: +1 damage

## Provider-native behavior

Cut simulates shears on shearable entities/blocks. Against non-shearable entities it deals small spell damage. Amplify changes block interaction to an axe-like strip/use path; Extract/Fortune apply tool enchantment semantics where supported. The source includes explicit duplicate-prevention checks around item-handler/container block entities before fake-player tool interaction.

## Authority / deduplication

Ars Nouveau owns this magical shearing/stripping utility. Black Arcana should not add a generic duplicate zero-cost cutting/shearing spell or double-spawn shear drops.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCut`).
