# Wind Burst

Status: `SOURCE-PINNED 5.13.1 / AIR CONTROL EFFECT`

- Registry id: `ars_nouveau:glyph_wind_burst`
- Display name: `Wind Burst`
- Default mana cost: `30`
- School: Elemental Air
- Exact source pin: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

`Wind Burst` resolves a wind-charge-style explosion at the target location using Minecraft's explosion pipeline with `Level.ExplosionInteraction.TRIGGER`.

Pinned defaults:

- base explosion radius term: `1.2`;
- AOE multiplier contribution: `1.0`;
- base knockback strength term in the damage calculator: `1.22`;
- Amplify contribution: `0.25`;
- default mana: `30`.

Compatible augments are AOE, Amplify, Dampen and Sensitive. Sensitive sets the caster as explosion owner so the caster can ignore the provider's knockback behavior.

## Black Arcana boundary

This is an Ars Nouveau world/entity effect. Black Arcana must not replay the explosion or knockback. An independent Black Arcana wind/explosion effect would still require Black Arcana's own `WorldEffectPolicy`; provider behavior is not a waiver of project safety rules.

## QA

Exact spell-entry behavior is source-pinned to 5.13.1. Full-pack interaction with protection/claims and other wind-charge hooks remains runtime QA.