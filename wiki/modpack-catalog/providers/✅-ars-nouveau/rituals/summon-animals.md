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

## Engenharia para perks — contrato de ritual

- **Fonte exata:** [`RitualAnimalSummoning.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/ritual/RitualAnimalSummoning.java) no Ars 5.13.1.
- **Fonte dos mobs:** sem recipe, `getMobs` lê lista ponderada da biome atual para `MobCategory.CREATURE` e exclui tipos `ANIMAL_SUMMON_BLACKLIST`. Com recipe válido em `RecipeRegistry.SUMMON_RITUAL_TYPE`, substitui por `SummonRitualRecipe.mobs` e usa `recipe.value().count` como objetivo. `canStart` sem input é true; com input, exige recipe.
- **Spawn/cadência:** a cada 60 ticks servidor, calcula offset aleatório perto do brazier, seleciona `mobs.getRandom(rand)`; somente entradas `MobSpawnSettings.SpawnerData` que geram entidade não nula acionam `summon(...)` e `incrementProgress()`. Termina com progress >=5 (default) ou >=recipe count.
- **Perks:** weighted entries/regras de bioma e entradas dos datapacks alteram tipos reais. Não inventar tabela de probabilidades/modded species a partir da classe; nem contar cada mob como uma conclusão separada do ritual.
- **Estado:** ✅ identidade/métodos/source pin; ⚠️ valores no modpack, proteções, Save/Restart e multiplayer não testados nesta branch. ⛔ adapter RPG para mutation, bônus de recursos ou acompanhamento de um cast por ritual não implementado; Ars conserva Source e world authority.
