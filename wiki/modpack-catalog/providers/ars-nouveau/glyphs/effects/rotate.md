# Ars Nouveau — Rotate

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_rotate`
- Display name: Rotate
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: Amplify, Sensitive, AOE, Pierce, Dampen, Randomize
- Default Sensitive limit: 1
- Default Randomize limit: 1

## Provider-native behavior

Rotate changes entity/block orientation. Amplification adds clockwise rotations; Dampen produces counter-clockwise rotation; Sensitive changes block axis where possible or forces entity look direction; Randomize selects arbitrary rotation. Projectile velocity is rotated alongside projectile orientation. AOE/Pierce expand block coverage.

## Authority / deduplication

Ars Nouveau owns this orientation/projectile-direction utility. Black Arcana should not duplicate generic rotation control or replay provider projectile movement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectRotate`).
