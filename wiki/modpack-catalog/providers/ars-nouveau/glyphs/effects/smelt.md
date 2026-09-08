# Ars Nouveau — Smelt

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_smelt`
- Display name: Smelt
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 100
- Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive

## Provider-native behavior

Smelt processes blocks through normal smelting recipes and world items through recipe lookup. Source caps item processing at `round(4 * (1 + AOE multiplier + Pierce count))`. Sensitive limits the effect to item entities. Dampen switches item processing to Smoking recipes; Amplify switches item processing to Blasting recipes and also raises harvest capability for block targets. Claim/harvest checks precede block conversion.

## Authority / deduplication

Ars Nouveau owns this remote magical processing path. Black Arcana must not double-convert blocks/items or duplicate output generation when Ars is causal. A separate Black Arcana transmutation effect would require a materially different forbidden-magic contract, not a cosmetic furnace replacement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSmelt`).
