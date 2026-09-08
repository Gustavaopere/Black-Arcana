# Ars Hex 5.0.4b — Acquisition

Status: `SOURCE RECIPE SURFACE CLOSED / INSTALLED DATAPACK QA OPEN`

## Active-provider source recipes — Malum 5/5

The release-aligned source tree commits five generated recipe files under `src/generated/resources/data/ars_hex/recipe/`. All five are wrapped with `neoforge:mod_loaded` for `malum`. Malum is present in the physical pack.

### 1. Soul Shatter glyph

`glyph_soul_shatter.json`

- recipe type: `ars_nouveau:glyph`;
- XP: 55;
- inputs: Manipulation Essence + Wicked Spirit + Soul-Stained Steel Sword;
- output: `ars_hex:glyph_soul_shatter`.

### 2. Enchanter's Scythe

`enchanter_scythe.json`

- recipe type: `ars_nouveau:enchanting_apparatus`;
- reagent: `malum:soul_stained_steel_scythe`;
- preserves reagent NBT;
- pedestals:
  - 1 × `c:storage_blocks/gold`;
  - 1 × `c:storage_blocks/source`;
  - 3 × `c:logs/archwood`;
- output: `ars_hex:enchanter_scythe`;
- declared `sourceCost: 0`.

### 3. Soul Ward Thread

`thread_soul_ward.json`

- reagent: `ars_nouveau:blank_thread`;
- pedestals:
  - Malum Rune of Reinforcement;
  - 2 × Refined Soulstone;
  - 2 × Soul-Stained Steel Plating;
  - 1 × Arcane Spirit;
- output: `ars_hex:thread_soul_ward`;
- `sourceCost: 0`.

### 4. Spirit Spoils Thread

`thread_soul_spoils.json`

- reagent: Blank Thread;
- pedestals:
  - Ring of Esoteric Spoils;
  - Refined Soulstone;
  - Arcane Spirit;
  - Wicked Spirit;
  - Eldritch Spirit;
- output: `ars_hex:thread_soul_spoils`;
- `sourceCost: 0`.

### 5. Magic Proficiency Thread

`thread_magic_proficiency.json`

- reagent: Blank Thread;
- pedestals:
  - 2 × Refined Soulstone;
  - 2 × Soulwoven Silk;
  - 2 × Earthen Spirit;
  - 2 × Aerial Spirit;
- output: `ars_hex:thread_magic_proficiency`;
- `sourceCost: 0`.

The source datagen class reproduces all five recipes and contains no production Imbuement recipe; its Imbuement example is commented.

## Dormant manual resources — Hexerei absent

The source tree also contains manual recipe resources under `src/main/resources/data/ars_hex/recipe/`. These are **not active-provider acquisition paths in the current pack** because their providers are absent.

### Hexerei-conditioned

1. `archwood_broom_from_mixing_cauldron.json`
   - 1000 mB water;
   - Source Gem tag, Archwood logs, Air Essence, Magebloom and Hexerei Mandrake Root;
   - output `ars_hex:archwood_broom`.

2. `wet_magebloom_brush_from_mixing_cauldron.json`
   - 500 mB water;
   - Hexerei Herb-Enhanced Broom Brush, Magebloom, Mandrake Root/Flowers;
   - output `ars_hex:wet_magebloom_brush`.

3. `broom_brush_from_drying_rack.json`
   - input `ars_hex:wet_magebloom_brush`;
   - output `ars_hex:magebloom_brush`;
   - drying time 1000.

Hexerei is absent from the physical modlist, so all three condition blocks should fail closed in the current pack.

### Hex Casting-conditioned orphan resource

`archwood_staff.json` is conditioned on mod id `hexcasting` and outputs `ars_hex:archwood_staff`.

Phase 2W found:

- no `hexcasting` top-level JAR in the physical modlist;
- no Java registration for `ars_hex:archwood_staff` in the audited Ars Hex source checkpoint;
- language/tag/resource references exist upstream.

It is therefore cataloged as a **dormant/orphan resource**, not a production item or active acquisition path.

## Packaging boundary

The project build includes `src/generated/resources` as a main resource directory, so the committed Malum recipes belong to the source build surface. Phase 2W still does not assert byte-level presence in the physical installed JAR without JAR extraction.

The source also defines datagen providers for damage/item/block tags, but the committed release-aligned `src/generated/resources/data/ars_hex/` tree contains only `recipe/`. Those tag files are not promoted to packaged-runtime facts without binary inspection.
