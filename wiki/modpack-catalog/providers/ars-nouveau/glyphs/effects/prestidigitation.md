# Prestidigitation

Status: `SOURCE-PINNED 5.13.1 / CONJURATION-PRESENTATION EFFECT / SEMANTICS+ACQUISITION AUDITED`

- Registry id: `ars_nouveau:glyph_prestidigitation`
- Display name: `Prestidigitation`
- Default mana cost: `0`
- School: Conjuration
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Prestidigitation` emits configured particle timelines on entities or places a provider `Particle Block` at a block target.

For temporary entity/block presentation, the pinned source derives duration from `(5 + 3 × durationMultiplier) × 20 ticks`. On block targets, `Amplify` makes the particle block permanent and bypasses duration modifiers. The block can preserve waterlogging and stores the provider particle timeline in `ParticleTile`.

Compatible augments are Extend Time, Duration Down and Amplify.

The class also drives inventory-tick particle presentation for items carrying the provider `PRESTIDIGITATION` data component.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Black Arcana boundary

This glyph is primarily provider-owned presentation/world-object state. Visual emission never becomes Black Arcana gameplay authority. Black Arcana must not infer damage, costs, ownership or progression from particles alone and must not duplicate the provider `ParticleTile` lifecycle.

Any independent permanent Black Arcana placement remains subject to Black Arcana world-effect policy even when the Ars visual block is harmless/provider-owned.

## QA

Source behavior is pinned to 5.13.1. Client rendering/accessibility and full-pack runtime behavior remain separate QA surfaces.