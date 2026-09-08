# Knockback

- Registry ID: `ars_nouveau:glyph_gust`
- Source class: `EffectKnockback`
- Display name: `Knockback`
- School: Elemental Air
- Default tier: **1**
- Default mana: **15**
- Default strength config: **1.5** base + **1.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Knocks entities according to provider caster orientation/position and target knockback resistance. On blocks it can convert affected blocks into Ars enchanted falling-block entities and move them. Sensitive prevents the block-moving path. Extract changes entity knockback direction to be away from the caster rather than following the caster look direction.

Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive, Extract. Sensitive is limited to 1 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:piston` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns `glyph_gust` motion/block conversion. Black Arcana movement remains server-validated and block movement remains subject to its own world-safety policy and bounded work.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.