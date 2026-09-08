# Grow

- Registry ID: `ars_nouveau:glyph_grow`
- Source class: `EffectGrow`
- School: Elemental Earth
- Default tier: **2**
- Default mana: **70**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Applies bone-meal-style growth to provider-calculated block targets, including the water-plant fallback path where applicable. The exact source checks the provider claim-respect helper before attempting growth.

Compatible augments: AOE, Pierce.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:earth_essence` + `minecraft:bone_block` ×5 + `#c:seeds` ×3.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Grow semantics. Black Arcana must not duplicate generic crop acceleration without a material forbidden-domain distinction, and any Black Arcana world mutation remains policy-controlled.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.