# Ars Nouveau — Crush

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_crush`
- Display name: Crush
- School: Elemental Earth
- Default tier: 2
- Default mana cost: 30
- Compatible augments: Amplify, Dampen, AOE, Pierce, Fortune, Sensitive
- Default Amplify limit: 2
- Default Sensitive limit: 1
- Source default base damage: 3
- Source default Amplify scalar: +1 damage

## Provider-native behavior

Crush uses Ars `CrushRecipe` data to transform eligible blocks into recipe outputs, optionally placing a block result and spawning remaining outputs. Sensitive enables processing nearby dropped items, with a source cap of `4 + 4*AOE + 4*Pierce` items per resolution. Against entities it deals provider Crush damage; underwater targets take triple the base component before amplification.

## Authority / deduplication

Ars Nouveau owns this recipe-driven magical crushing/processing path and its outputs. Black Arcana should not clone generic ore/block crushing or double-generate recipe outputs; any forbidden transmutation must define a distinct cost/hazard/progression contract.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCrush`).
