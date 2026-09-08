# Launch

- Registry ID: `ars_nouveau:glyph_launch`
- Source class: `EffectLaunch`
- School: Elemental Air
- Default tier: **1**
- Default mana: **30**
- Default vertical strength config: **0.8** base + **0.25** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Adds upward motion to entity targets and resets their fall distance. On blocks it may convert provider-calculated blocks into enchanted falling-block entities and launch them; Sensitive disables the block-moving path.

Compatible augments: Amplify, Dampen, AOE, Sensitive, Pierce. Sensitive is limited to 1 by default.

## Boundary

Ars owns Launch motion and falling-block conversion. Black Arcana launch/movement remains server-authoritative, and any Black Arcana block movement must pass world-safety and bounded-work gates.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.