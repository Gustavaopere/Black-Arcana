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

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `minecraft:prismarine_shard` ×2 + `minecraft:totem_of_undying`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns fang entity lifecycle, timing and damage. Black Arcana summoned hazards must use its own bounded scheduler/damage contracts and cannot treat provider fang timing as a general hazard API.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.