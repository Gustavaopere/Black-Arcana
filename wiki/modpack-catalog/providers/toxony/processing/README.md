# Toxony 0.10.7 — processing, acquisition and delivery

## Status

`7 RECIPE FAMILIES CONFIRMED / MORTAR 19/19 SOURCE-GENERATED RECIPES AUDITED / CORE OIL DELIVERY CAPACITY PRESERVED / MENDING UNLOCK MISMATCH RECORDED / OTHER FAMILY INVENTORIES PENDING / LICENSE+RUNTIME QA PENDING`

Exact source checkpoint: `MrFrostyDev/Toxony_Mod@881bf7fe632659e748c279966a2bf49b99f7503f`.

This page preserves provider acquisition/delivery facts that previously lived in the top-level Toxony README, while separating them from the core semantic catalog.

## Canonical recipe families

The exact 0.10.7 datagen provider invokes seven recipe families:

1. Crafting Table;
2. Furnace;
3. Mortar & Pestle;
4. Crucible;
5. Alembic;
6. Alchemical Forge;
7. Smithing Table.

This confirms that Toxony progression is a multi-stage alchemical processing system. Black Arcana must not replace it with an instant spell-crafting shortcut.

## Mortar & Pestle — 19/19 generated recipes

The exact `ToxonyMortarRecipes` source builds 19 generated recipes.

### Foundational preparations — 2

1. Poison Paste: Bone Meal + poisonous ingredient tag + poisonous plant tag.
2. Affinity Fusion Mix: three dynamic/possible ingredients + Nether Wart.

### Tier 0 oil pots — 4

| Output | Inputs | Container consumed/used |
|---|---|---|
| Poison Oil Pot | Honeycomb + Poison Paste | Empty Oil Pot |
| Fire Resistance Oil Pot | Honeycomb + Magma Cream | Empty Oil Pot |
| Glowing Oil Pot | Honeycomb + Glow Ink Sac | Empty Oil Pot |
| Fatigue Oil Pot | Honeycomb + Fermented Spider Eye + Water Hemlock | Empty Oil Pot |

### Tier 1 preparations — 2

| Output | Inputs | Container |
|---|---|---|
| Acid Oil Pot | Honeycomb + Toxic Paste + 2× Acid Slimeball | Empty Oil Pot |
| Mending Oil Pot | Honeycomb + Toxic Paste + Toxic Spit + Ocelot Mint | Empty Oil Pot |

`Mending Oil Pot` is a dedicated special item/block path rather than one of the nine entries in the custom Oil registry. It must not be counted as a tenth registered Oil.

### Mending Oil unlock mismatch

The exact datagen source contains a provider-side discovery inconsistency:

- recipe consumption uses `EMPTY_OIL_POT`;
- the `unlockedByItems("has_empty_oil_pot", ...)` criterion is supplied `EMPTY_TOX_POT`.

This is recorded as `SOURCE QA MISMATCH / RUNTIME BEHAVIOR NOT INFERRED`. Black Arcana must not patch around it or assume which item the upstream author intended. Recipe visibility/unlock behavior should be tested against the installed JAR if integration or Wiki acquisition guidance depends on it.

### Tier 2 Tox Pots — 5

| Output | Inputs | Container |
|---|---|---|
| Toxin Tox Pot | Honeycomb + Toxin + Toxic Paste | Empty Tox Pot |
| Regeneration Tox Pot | Honeycomb + Ghast Tear + Sunspot | Empty Tox Pot |
| Smoke Tox Pot | Honeycomb + Fermented Spider Eye + Moonlight Hemlock | Empty Tox Pot |
| Acid Tox Pot | Honeycomb + Warproot + Acid Slimeball + Bog Bone | Empty Tox Pot |
| Witchfire Tox Pot | Honeycomb + Blaze Powder + Warproot | Empty Tox Pot |

### Oil Base — 1

- Honeycomb + Toxic Paste → 2× Oil Base.

### Blends — 3

- Poison Blend: Poison Paste + one dynamic/possible ingredient + Bowl;
- Toxic Blend: Toxic Paste + two dynamic/possible ingredients + Bowl;
- Pure Blend: Toxin + three dynamic/possible ingredients + Bowl.

The dynamic ingredients participate in Toxony's provider knowledge/Affinity system; Black Arcana must not flatten them into fixed generic reagent slots.

### Dye conversions — 2

- Poison Paste → 4 Green Dye;
- Toxic Paste → 8 Green Dye.

## Source-observed consumable Toxicity examples

The exact 0.10.7 item definitions preserve representative player Toxicity/Tolerance progression values that existed in the earlier catalog:

| Item | Toxicity | Tolerance gain | Tier | Additional provider effect |
|---|---:|---:|---:|---|
| Poison Blend | `30` | `15` | `0` | Poison, 1000 ticks |
| Toxic Blend | `40` | `25` | `1` | Toxin, 1000 ticks |
| Pure Blend | `65` | `40` | `3` | Toxin, 1800 ticks |
| Toxin item | `50` | `10` | `1` | Toxin II, 600 ticks |

These numbers are source-observed factual catalog data. Exact installed runtime and balance acceptance remain separate QA gates.

## Oil/Tox Pot delivery capacity

The exact item registration helper constructs Oil Pot items with:

- item durability;
- Oil registry holder;
- block form;
- duration;
- amplifier;
- maximum-use metadata.

Verified source examples:

| Delivery item | Durability | Oil | Duration parameter | Amplifier | Max-use metadata |
|---|---:|---|---:|---:|---:|
| Poison Oil Pot | `5` | Poison Oil | `200` | `0` | `150` |
| Glowing Oil Pot | `5` | Glowing Oil | `600` | `0` | `150` |
| Fatigue Oil Pot | `5` | Fatigue Oil | `300` | `0` | `150` |
| Acid Oil Pot | `5` | Acid Oil | `400` | `0` | `150` |
| Toxin Tox Pot | `3` | Toxin Oil | `120` | `0` | `100` |
| Regeneration Tox Pot | `3` | Regeneration Oil | `200` | `0` | `100` |

Other registered pot variants remain part of the provider delivery family and should be transcribed individually before claiming a final 100% item-delivery catalog.

## Wearable Oil storage

Exact item registration values:

- Oil Pot Sash: durability `16`;
- Oil Pot Bandolier: durability `40`;
- Eternal Plague: durability `64`.

These are Toxony-owned storage/delivery mechanics. Curios or another equipment provider does not become authority over the Oil contents merely because equipment integration is possible.

## Projectile delivery

The provider exposes dedicated bolt/delivery variants for chemical effects. Previous source audit identified dedicated Poison, Glowing, Witchfire, Toxin, Smoke and Regeneration bolt families.

The exact 0.10.7 source also applies its silver-damage helper in Flintlock Ball and Flail Ball hit settlement. That compatibility remains Toxony-owned and is documented separately in the technical/integration pages.

## Acquisition authority

The Lost Journal, recipe unlock criteria, ingredient discovery/knowledge, alchemical processing blocks and provider recipes together define Toxony acquisition. Black Arcana must not grant Oils/Mutagens by bypassing these gates unless an explicit integration design intentionally and safely invokes a provider-native recipe/progression boundary.

## Remaining recipe work

To reach a complete processing Wiki rather than the current high-value semantic checkpoint, Phase 2 still needs individual inventory tables for:

- Crafting Table recipes;
- Furnace recipes;
- Crucible recipes;
- Alembic recipes;
- Alchemical Forge recipes;
- Smithing Table recipes;
- all remaining delivery-item duration/amplifier/max-use values;
- exact recipe unlock/knowledge conditions where gameplay-significant.

Those gaps do not prevent semantic deduplication of Toxony's Toxicity/Oil/Mutagen authority, but they remain open for final Wiki completeness.
