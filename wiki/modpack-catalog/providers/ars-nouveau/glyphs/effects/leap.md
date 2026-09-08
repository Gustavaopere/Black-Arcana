# Ars Nouveau — Leap

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_leap`
- Display name: Leap
- School: Elemental Air
- Default tier: 1
- Default mana cost: 25
- Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive
- Source default base movement scalar: 1.5
- Source default Amplify scalar: +1.0
- Source default `force_ground`: false

## Provider-native behavior

Leap sets target motion in its look direction and resets fall distance. It can also convert eligible block targets into Ars `EnchantedFallingBlock` entities and launch them; Sensitive suppresses block movement. Tile casters derive direction from their configured facing/rotation.

## Authority / deduplication

Ars Nouveau already owns a directional launch/mobility primitive. Black Arcana should not clone generic leap/launch traversal; any mobility spell must have a materially different forbidden-magic identity and preserve server-owned targeting/movement validation.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectLeap`).
