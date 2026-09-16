# Summon Animals

Status: `SOURCE-PINNED 5.13.1 / FAUNA-SUMMON RITUAL`

- Registry id: `ars_nouveau:ritual_animal_summon`
- Class: `RitualAnimalSummoning`
- Work cadence: every `60` game ticks
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native selection

Without consumed modifiers, the ritual builds a weighted list from the current biome's `MobCategory.CREATURE` spawn table, excluding Ars Nouveau's animal-summon blacklist.

Consumed augment items may instead match a provider `SummonRitualRecipe`. When a recipe matches, its own weighted mob list and required summon count replace the biome-default behavior.

`canStart` allows an unmodified ritual immediately; when modifier items are present, a valid summon recipe is mandatory.

## Provider-native lifecycle

Every 60 game ticks on the server, the ritual:

1. picks a nearby randomized summon position;
2. selects a weighted spawn entry;
3. creates and adds the selected entity;
4. increments progress only after a successful creation.

The default ritual finishes after progress reaches `5`; recipe-driven variants finish when progress reaches the recipe's configured `count`.

## Authority / Black Arcana boundary

Biome weighting, summon-recipe overrides, entity identity and completion count remain Ars Nouveau authority. Black Arcana must not reinterpret these entities as Black Arcana familiars, duplicate the spawn, or award one ritual completion per summoned mob.

## QA

Source lifecycle is pinned to 5.13.1. The complete data-driven `SummonRitualRecipe` inventory and interactions with modded biome spawn tables remain separate data/runtime QA.