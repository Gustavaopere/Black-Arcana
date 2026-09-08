# Conjure Mageblock

- Registry ID: `ars_nouveau:glyph_phantom_block`
- Source class: `EffectPhantomBlock`
- School: Conjuration
- Default tier: **1**
- Default mana: **5**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Creates Ars Nouveau Mage Blocks in provider-calculated AOE/depth positions after world-bounds, replacement, collision and claim checks. Without Amplify they are temporary and use the duration modifier; one Amplify makes the created Mage Block permanent. Casting on an entity redirects the placement geometry around/below that entity.

Compatible augments: AOE, Pierce, Amplify, Extend Time, Reduce Time. Amplify is limited to 1 by default.

Identity note: installed-line registry path remains `glyph_phantom_block`; the source class itself notes a possible class rename only for 1.22.

## Acquisition / learning

- Provider-generated Glyph recipe: `#c:glass_blocks` ×8.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Permanent or temporary Ars Mage Blocks remain Ars-owned. Black Arcana cannot use this capability to bypass `WorldEffectPolicy`, restoration ownership or bounded world-mutation budgets.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.