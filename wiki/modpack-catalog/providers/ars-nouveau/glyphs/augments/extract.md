# Extract

- Registry ID: `ars_nouveau:glyph_extract`
- Source class: `AugmentExtract`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **30**

## Source-pinned behavior

Provides Silk-Touch-like behavior to compatible Break usage. The exact source also describes an Explosion interaction that preserves blocks that would drop rather than destroying them. Extract is declared incompatible with Fortune/Luck.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:emerald`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns loot/extraction semantics and its compatibility matrix. Black Arcana destructive block effects remain governed by `WorldEffectPolicy`; this glyph cannot be used as a generic bypass for protection, drops or world-mutation policy.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.