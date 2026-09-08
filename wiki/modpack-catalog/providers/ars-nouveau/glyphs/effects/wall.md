# Ars Nouveau — Wall

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_wall`
- Display name: Wall
- School: Manipulation
- Default tier: 3
- Default mana cost: 500
- Compatible augments: Sensitive, AOE, Accelerate, Decelerate, Extend Time, Reduce Time (`glyph_duration_down`), Dampen
- Default Sensitive limit: 1
- Per-spell occurrence limit: exactly 1
- Default invalid combination: Linger

## Provider-native behavior

Wall converts the remaining spell into an `EntityWallSpell`: it creates a child context, cancels the original continuation, installs a new resolver, orients the wall from caster facing and stores area, speed, duration, targeting and gravity behavior. Sensitive targets blocks instead of entities; Dampen suppresses gravity. Wall is registered in `EffectReset.RESET_LIMITS`.

## Authority / deduplication

Wall is a provider-owned persistent spell-execution surface, not merely a barrier graphic. Black Arcana must not create a second settlement/casting path around Ars Wall execution.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectWall`).
