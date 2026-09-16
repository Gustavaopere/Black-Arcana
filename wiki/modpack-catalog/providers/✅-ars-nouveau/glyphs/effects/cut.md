# Ars Nouveau — Cut

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

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

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:shears` + `minecraft:iron_sword`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this magical shearing/stripping utility. Black Arcana should not add a generic duplicate zero-cost cutting/shearing spell or double-spawn shear drops.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCut`).
