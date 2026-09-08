# Slowfall

- Registry ID: `ars_nouveau:glyph_slowfall`
- Source class: `EffectSlowfall`
- School: Elemental Air
- Default tier: **2**
- Default mana: **30**
- Default duration config: base **30**, Extend Time increment **8**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Applies Minecraft Slow Falling through Ars Nouveau's configurable potion-effect path.

Compatible augments: Extend Time, Reduce Time.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `ars_nouveau:wilden_wing` + `minecraft:feather` ×3 + `#c:rods/blaze` + `#c:crops/nether_wart`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns duration/config and effect application. Black Arcana mobility/fall-safety mechanics remain independent unless a supported adapter explicitly consumes provider state.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.