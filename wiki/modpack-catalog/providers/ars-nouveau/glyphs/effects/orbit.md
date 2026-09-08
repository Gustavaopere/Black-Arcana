# Orbit

Status: `SOURCE-PINNED 5.13.1 / GLYPH EFFECT`

- Registry id: `ars_nouveau:glyph_orbit`
- Display name: `Orbit`
- Default tier: `THREE`
- Default mana cost: `50`
- School: provider-defined by Ars Nouveau spell-part registration/runtime
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Orbit` consumes the remaining spell chain into a child `SpellContext`, prepends `Projectile`, cancels the parent continuation and spawns orbiting projectiles around the target. Base projectile count is `3`; each `Split` adds one more.

The orbit entities retain provider-owned spell resolvers and carry acceleration, radius/AOE and duration state. On hit they resolve the child spell through Ars Nouveau's own spell pipeline.

Compatible augments in the pinned source are:

- Accelerate;
- Decelerate;
- AOE;
- Pierce;
- Split;
- Extend Time;
- Duration Down;
- Sensitive.

## Black Arcana boundary

This is a persistent spell-composition/execution surface owned by Ars Nouveau. Black Arcana must not treat each orbit projectile as a new independent player cast, must not charge a second cost/cooldown, and must not replay child effects through the Black Arcana cast engine.

Any mastery/danger bridge must preserve root-cast causality and bounded attribution rather than multiplying credit by projectile count.

## QA / runtime

Source behavior is pinned to 5.13.1. Full 612-mod runtime/config QA remains separate.