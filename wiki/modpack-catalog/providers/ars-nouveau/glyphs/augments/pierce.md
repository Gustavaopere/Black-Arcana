# Pierce

- Registry ID: `ars_nouveau:glyph_pierce`
- Source class: `AugmentPierce`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **40**

## Source-pinned behavior

On compatible glyphs, Pierce adds depth/continuation semantics. Projectile explicitly permits additional traversal after colliding with a mob or block; some effects such as Break may extend to blocks behind the first target. AOE may combine with Pierce to add depth to affected geometry.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:arrow` + `ars_nouveau:wilden_spike`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns Pierce interpretation per glyph. Black Arcana penetration/linked-target geometry remains explicitly bounded by its own server targeting and work budgets.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.