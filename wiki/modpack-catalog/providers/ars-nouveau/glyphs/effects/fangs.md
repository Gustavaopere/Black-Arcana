# Fangs

- Registry ID: `ars_nouveau:glyph_fangs`
- Source class: `EffectFangs`
- School: Conjuration
- Default tier: **3**
- Default mana: **35**
- Default damage config: **6.0** base + **3.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Creates provider Evoker Fang entities along a line toward the target. Self-targeting switches to two radial rings around the caster. Duration changes the fang timing and Accelerate shortens the per-fang delay; the exact class notes no Decelerate support in this line.

Compatible augments: Amplify, Dampen, Extend Time, Reduce Time, Accelerate. Amplify is limited to 2 by default.

## Boundary

Ars owns fang entity lifecycle, timing and damage. Black Arcana summoned hazards must use its own bounded scheduler/damage contracts and cannot treat provider fang timing as a general hazard API.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.