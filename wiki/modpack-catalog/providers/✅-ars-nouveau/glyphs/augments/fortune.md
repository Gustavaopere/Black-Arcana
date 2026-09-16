# Fortune / Luck

- Registry ID: `ars_nouveau:glyph_fortune`
- Source class: `AugmentFortune`
- Source display name: `Luck`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **2**
- Default mana: **80**

## Source-pinned behavior

Increases relevant drop chances for compatible provider behavior, including mobs killed through the provider damage path and blocks broken through Break. It is declared incompatible with Extract.

## Acquisition / learning

- Provider-generated Glyph recipe: `minecraft:rabbit_foot`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns its loot/fortune calculations and compatible-glyph semantics. Black Arcana must preserve provider causal identity and must not double-apply external Fortune/Looting-style rewards.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.