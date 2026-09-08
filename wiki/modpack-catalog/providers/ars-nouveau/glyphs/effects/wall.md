# Ars Nouveau — Wall

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

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

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dragon_breath` + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Wall is a provider-owned persistent spell-execution surface, not merely a barrier graphic. Black Arcana must not create a second settlement/casting path around Ars Wall execution.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectWall`).
