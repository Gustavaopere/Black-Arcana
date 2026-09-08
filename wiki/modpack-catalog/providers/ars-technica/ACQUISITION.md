# Ars Technica 2.7.6 — glyph acquisition

Status: `11/11 GENERATED GLYPH RECIPES SOURCE-PINNED`

Source: `ArsProviders.GlyphProvider` at `zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`.

These are provider datagen recipes of type `ars_nouveau:glyph`. The table records the source-generated acquisition contract; installed datapack/runtime verification remains a separate QA gate.

| Glyph | XP | Learning inputs | Output |
|---|---:|---|---|
| Carve | 27 | Manipulation Essence; Crafting Table; Cobblestone Stairs; Cobblestone Slab; Cobblestone Wall | `ars_technica:glyph_carve` |
| Pack | 27 | Manipulation Essence; Crafting Table; Chest; Iron Block | `ars_technica:glyph_pack` |
| Polish | 55 | Manipulation Essence; Create Sand Paper | `ars_technica:glyph_polish` |
| Obliterate | 160 | Manipulation Essence; Anvil; Diamond Block | `ars_technica:glyph_obliterate` |
| Press | 55 | Manipulation Essence; Create Mechanical Press | `ars_technica:glyph_press` |
| Superheat | 160 | 3× Fire Essence; Blaze Rod; Create Blaze Cake | `ars_technica:glyph_superheat` |
| Fuse | 55 | Manipulation Essence; Fire Essence; 3× Blaze Rod | `ars_technica:glyph_fuse` |
| Whirl | 55 | Manipulation Essence; 3× Air Essence | `ars_technica:glyph_whirl` |
| Insert | 27 | 2× Chest | `ars_technica:glyph_insert` |
| Telefeast | 55 | Manipulation Essence; Golden Apple; Bucket; Glass Bottle; Ender Pearl | `ars_technica:glyph_telefeast` |
| Apply | 27 | Manipulation Essence; Create Brass Hand | `ars_technica:glyph_apply` |

## Other provider acquisition surfaces already confirmed in the same source generator

The same source checkpoint generates provider equipment/infrastructure recipes relevant to magic authority:

- `calibrated_precision_mechanism`: Enchanting Apparatus recipe from a Create Precision Mechanism, 4 Amethyst Shards and 4 Source Gems; source cost 500;
- `mark_of_technomancy`: output count 5, reagent Wilden Tribute plus Create/Ars/metal components; source cost 10,000;
- `blank_disc`: music-disc reagent plus Fire Essence; source cost 0;
- `transmutation_focus`: Manipulation Essence reagent plus brass, Rabbit's Foot, Calibrated Precision Mechanism and Emerald;
- `spy_monocle`: Spyglass reagent plus Calibrated Precision Mechanism;
- `transmutation_turret`: Ars Enchanted Spell Turret reagent plus 3 Manipulation Essence and Transmutation Focus;
- Pressure thread: Ars Blank Thread reagent plus 3 Air Essence, Create Copper Backtank and Calibrated Precision Mechanism.

Those entries establish acquisition paths only. Exact item/perk behavior is cataloged separately under the provider systems/equipment audit and is not inferred from recipes.

## Deduplication consequence

Learning remains Ars Nouveau glyph-learning authority. Black Arcana must not create a parallel unlock ledger for these spell parts, grant them through Black Arcana progression as if it owned them, or charge a second learning/resource cost around the provider's recipe path.