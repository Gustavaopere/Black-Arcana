# AOE

- Registry ID: `ars_nouveau:glyph_aoe`
- Source class: `AugmentAOE`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **35**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's AOE spell stat. Compatible glyphs interpret the stat to expand their affected area around a target.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:firework_star`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns this AOE stat and its per-glyph interpretation. Black Arcana area geometry remains explicitly server-bounded and cannot inherit an unbounded Ars radius contract.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.