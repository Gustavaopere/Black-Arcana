# Ars Nouveau — Flare

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_flare`
- Display name: Flare
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 40
- Compatible augments: Amplify, Dampen, AOE, Fortune, Randomize
- Source default base damage: 7
- Source default Amplify damage scalar: +3
- Default Amplify limit: 2

## Provider-native behavior

Flare only damages living targets already burning, standing in fire, or carrying Ars' Blasting effect. Successful use spawns damaging Cinder entities around the target; block casts can trigger from nearby fire. If the target has Blasting, Flare removes that effect and immediately detonates the provider Blasting explosion at increased strength. AOE increases the number of spawned Cinders. Cinders use Mage Fire and do not spread normal fire to terrain.

## Authority / deduplication

Flare occupies conditional fire detonation/cinder territory. Black Arcana Black Flame content must not be a cosmetic copy of this ignition-conditioned burst or duplicate Blasting settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFlare`).
