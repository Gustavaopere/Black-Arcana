# Ars Delight 2.2.2 — registries and content surface

Status: `BASE SOURCE INVENTORY CLOSED / OPTIONAL CURRENT-HOST QA OPEN`

## Base foods — 42

The verified `ADFood` registry inventory contains 42 entries across these groups:

### Wilden / Chimera

`wilden_meat`, `grilled_wilden_meat`, `wilden_meat_slice`, `grilled_wilden_meat_slice`, `chimera_meat`, `grilled_chimera_meat`, `chimera_meat_slice`, `grilled_chimera_meat_slice`, `wilden_skewer`, `grilled_wilden_skewer`, `chimera_skewer`, `grilled_chimera_skewer`, `wilden_sauce`, `wilden_stew`, `bowl_of_wilden_salad`, `horn_roll`, `bowl_of_honey_glazed_chimera`.

### Source Berry / Archwood

`source_berry_cookie`, `source_berry_pie_slice`, `source_berry_cupcake`, `arch_sauce`, `arch_soup`.

### Teas

`mendosteen_tea`, `bastion_tea`, `bombegrante_tea`, `frostaya_tea`, `source_berry_tea`.

### Cocktail / hornbeers

`unstable_cocktail`, `mendosteen_hornbeer`, `bastion_hornbeer`, `bombegrante_hornbeer`, `frostaya_hornbeer`, `source_berry_hornbeer`.

### Jams

`activated_mendosteen_jam`, `activated_bastion_jam`, `neutralized_bombegrante_jam`, `neutralized_frostaya_jam`, `source_berry_jam`.

### Fruit/meat dishes

`mendosteen_chicken`, `bastion_pork`, `bombegrante_steak`, `frostaya_mutton`.

## Base non-food items — 8

- `flourishing_bark`;
- `vexing_bark`;
- `cascading_bark`;
- `blazing_bark`;
- `wilden_horn_powder`;
- `wilden_spike_powder`;
- `chimera_horn`;
- `enchanters_knife`.

The first four barks register fuel/compost data; Blazing Bark uses furnace-fuel value 400 while the other three base barks use 200.

## Base storage/feast blocks — 8

Crates:

- `mendosteen_crate`;
- `bastion_crate`;
- `bombegrante_crate`;
- `frostaya_crate`;
- `source_berry_crate`.

Other blocks:

- `archwood_cabinet`;
- `wilden_salad`;
- `honey_glazed_chimera`.

The cabinet is a Farmer's Delight `CabinetBlock`; startup expands Farmer's Delight cabinet valid-block membership to include it. The two feasts use Farmer's Delight serving-state behavior and provider loot tables.

## Base jellies — 5 + one BE type

- `mendosteen_jelly`;
- `bastion_jelly`;
- `bombegrante_jelly`;
- `frostaya_jelly`;
- `source_berry_jelly`;
- block entity type: `jelly`.

Jellies are edible block-items and implement Ars prismatic projectile behavior through the provider block/BE runtime.

## Base pies — 4 blocks + 4 slices

- `mendosteen_pie` / `mendosteen_pie_slice`;
- `bastion_pie` / `bastion_pie_slice`;
- `bombegrante_pie` / `bombegrante_pie_slice`;
- `frostaya_pie` / `frostaya_pie_slice`.

They reuse Farmer's Delight `PieBlock` bite state.

## Base effects — 5

- `blast_resistance`;
- `flourishing`;
- `freezing_spell`;
- `synchronized_shield`;
- `wilden`.

Exact formulas/event semantics are in `EFFECTS-EVENTS.md`.

## Optional source-conditioned content

### Ars Elemental

When Ars Elemental is loaded, source initializes:

- `flashpine_crate`;
- `flashing_bark`;
- `flashpine_jelly`;
- `flashpine_pie` plus its generated slice through `ADPie`;
- `lightning_curse` effect;
- `flashpine_tea`;
- `flashpine_hornbeer`;
- `neutralized_flashpine_jam`.

Ars Elemental 0.7.10.1 is physically present, but current-host runtime registration remains to be validated.

### Archwood Good

When Archwood Good is loaded, source initializes:

- `dawnberry_crate`, `lightchee_crate`;
- `dawn_bark`, `bleak_bark`, `fading_bark`;
- `dawnberry_jelly`, `lightchee_jelly`;
- `dawnberry_pie`, `lightchee_pie` plus slices through `ADPie`;
- 7 `AWFood` entries: three Dawnberry consumables, three Lightchee consumables and `skittle_stew`.

Archwood Good was not found as a top-level physical JAR in the current checkpoint, so this is source capability, not active-runtime evidence.

## Counting rule

Do not sum block entries, block items, pie slices, edible jellies and optional content into a single “unique content” number without a registry-specific definition. This catalog preserves the upstream registration surfaces separately.
