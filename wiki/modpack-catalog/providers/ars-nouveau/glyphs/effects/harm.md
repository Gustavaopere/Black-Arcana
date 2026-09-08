# Harm

- Registry ID: `ars_nouveau:glyph_harm`
- Source class: `EffectHarm`
- School: Elemental Earth
- Default tier: **1**
- Default mana: **15**
- Default damage config: **5.0** base + **2.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Without a Time augment, Harm attempts provider-owned magic damage against a non-item target. If Extend Time or Reduce Time is present and the target is living, Harm switches to a Poison application path instead of immediate damage. Amplify increases immediate damage or Poison strength. The exact source caps Amplify to 2 by default.

Compatible augments: Amplify, Dampen, Extend Time, Reduce Time, Fortune, Randomize. Harm is explicitly a default starter glyph.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:iron_sword` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **yes**.
- When starter remains enabled by config, Ars treats Harm as already known; otherwise its Glyph-learning path remains provider-owned.
- Runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns this damage/Poison branch, invulnerability-frame interactions and provider damage source. Black Arcana must not double-process damage, lifesteal, mastery or Arcane Danger when observing Ars-owned Harm damage.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.