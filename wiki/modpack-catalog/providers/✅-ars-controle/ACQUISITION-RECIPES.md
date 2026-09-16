# Ars Controle 1.6.15 — acquisition and learning

Status: `SOURCE-PINNED DEFAULT RECIPES / EFFECTIVE DATAPACK QA PENDING`

Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`.

This page records the generated default recipe surface. Modpack datapacks/configuration can still alter effective runtime reachability.

## Glyph learning — 9/9

All nine use Ars Nouveau glyph/Scribes Table recipes.

| Glyph | XP | Inputs |
|---|---:|---|
| `ars_controle:glyph_precise_delay` | 55 | `ars_nouveau:manipulation_essence`, `minecraft:clock`, `minecraft:comparator` |
| `ars_controle:glyph_filter_above` | 27 | `ars_nouveau:allow_scroll`, `minecraft:feather` |
| `ars_controle:glyph_filter_below` | 27 | `ars_nouveau:allow_scroll`, `minecraft:cobbled_deepslate` |
| `ars_controle:glyph_filter_level` | 27 | `ars_nouveau:allow_scroll`, `minecraft:short_grass` |
| `ars_controle:glyph_filter_or` | 27 | `minecraft:comparator`, `minecraft:redstone` |
| `ars_controle:glyph_filter_xor` | 27 | `minecraft:comparator`, `minecraft:redstone_torch` |
| `ars_controle:glyph_filter_xnor` | 27 | `minecraft:comparator`, `minecraft:redstone`, `minecraft:redstone_torch` |
| `ars_controle:glyph_filter_not` | 27 | `ars_nouveau:allow_scroll`, `minecraft:redstone_torch` |
| `ars_controle:glyph_filter_random` | 27 | `ars_nouveau:allow_scroll`, `ars_nouveau:glyph_randomize` |

Precise Delay's Tier II default aligns with the generated 55 XP. Filters are Tier I and use 27 XP.

## Enchanting Apparatus systems — 5/5

All five generated Apparatus recipes have `sourceCost: 0`. Operational use costs, where present, are separate.

### Warping Spell Prism

- reagent: `ars_nouveau:spell_prism`;
- 4 × `c:ender_pearls`;
- 4 × `minecraft:popped_chorus_fruit`.

### Scryer's Linkage

- reagent: `ars_nouveau:scryers_crystal`;
- 4 × `c:ender_pearls`;
- 4 × `minecraft:popped_chorus_fruit`.

### Temporal Stability Sensor

- reagent: `minecraft:clock`;
- 1 × `minecraft:ender_eye`;
- 1 × `ars_nouveau:source_gem_block`.

### Remote

- reagent: `ars_nouveau:dominion_wand`;
- 4 × `c:ender_pearls`;
- 4 × `minecraft:popped_chorus_fruit`.

### Portable Brazier Relay

- reagent: `ars_nouveau:brazier_relay`;
- 2 × `c:ender_pearls`;
- 2 × `minecraft:popped_chorus_fruit`;
- 2 × `ars_nouveau:manipulation_essence`;
- 1 × `minecraft:nether_star`;
- 1 × `ars_nouveau:wilden_tribute`.

## Warp Scroll Holder

Vanilla shaped recipe:

`sss / s s / sss`

with `s = ars_nouveau:sourcestone_slab`.

Result: 1 × `ars_controle:scroll_holder`.

## Runtime resource distinction

Default crafting `sourceCost: 0` for the five Apparatus recipes does **not** mean the resulting systems are free to operate:

- Warp Scroll Holder defaults to `1000` Source on fresh portal formation;
- Warping Spell Prism has configurable distance/dimension Source routing cost on its block-target path;
- all other Ars/ritual/portal resource semantics remain owned by their native Ars systems.

Black Arcana must never convert these recipe/runtime costs into a second resource ledger.
