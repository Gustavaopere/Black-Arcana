# Decelerate

- Registry ID: `ars_nouveau:glyph_decelerate`
- Source class: `AugmentDecelerate`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **5**

## Source-pinned behavior

Adds **-0.5** to Ars Nouveau's acceleration modifier. Compatible provider glyphs interpret that value; Projectile uses it to reduce projectile velocity.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:soul_sand` + `minecraft:cobweb` + `minecraft:clock`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns compatible-glyph selection, acceleration semantics and configured mana cost. This is not a Black Arcana-wide speed modifier.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.