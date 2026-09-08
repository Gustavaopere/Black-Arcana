# Extend Time

- Registry ID: `ars_nouveau:glyph_extend_time`
- Source class: `AugmentExtendTime`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **10**

## Source-pinned behavior

Adds **+1.0** to Ars Nouveau's duration modifier. Compatible effects use that stat for provider-owned duration behavior, including effects, summons and other timed spell results.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:clock` + `#c:storage_blocks/redstone`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Duration scaling is provider-owned. Black Arcana durations/cooldowns remain separate server-owned policy values and cannot be silently multiplied by this Ars stat.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.