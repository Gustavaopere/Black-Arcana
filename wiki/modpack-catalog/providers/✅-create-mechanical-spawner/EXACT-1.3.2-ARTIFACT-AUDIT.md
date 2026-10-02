# Create: Mechanical Spawner 1.3.2-6.0.10 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / FULL MACHINE-SPAWN SURFACE CLOSED`

## Identity gate

- physical JAR: `create_mechanical_spawner-1.21.1-1.3.2-6.0.10.jar`;
- mod id: `create_mechanical_spawner`;
- publisher/file version: `1.3.2-6.0.10`;
- sibling runtime metadata: `1.3.1-6.0.10`;
- physical SHA-1: `d9a5a2ee44238e4a90f70057ba9ec8414594fe24`;
- CurseForge project/file: `821828 / 8418593`.

NON-MERGE PR #534 run `37016899558` succeeded with exact physical/publisher equality.

- audit HEAD: `f0af3036c0febe075c7aeaaba57ab911bd142074`;
- evidence artifact: `11231435071`;
- artifact digest: `sha256:7853217a8c1ad26fb8d345c5d9297bec29dc4abb3824afd0d882876c28c0b7a8`;
- publisher SHA-256: `f963b0a4e450484b36ec0b5d529fa7f32527dcc60ec93261ceef5c056f0a9134`;
- bytes: `1,215,649`.

## Bounded archive inventory

- entries: **507**;
- classes: **52**;
- resources: **455**;
- provider data paths: **116**;
- provider recipe JSONs: **97**.

Magic-semantic path counts:

`spell=0 · magic=0 · ritual=0 · ability=0 · mana=0 · arcane=0 · glyph=0 · summon=0 · soul=0`

Expected machine-domain counts are positive: spawn, wither, loot and recipe paths are present and were inspected directly.

## Exact recipe inventory

The exact artifact packages **28** recipes of type `create_mechanical_spawner:spawner`:

- concrete output recipes: **27**;
- random-biome recipe: **1**;
- corresponding provider spawn-fluid mixing recipes: **28**.

The concrete recipe list includes `minecraft:wither`. Its exact recipe consumes 300 mB of `create_mechanical_spawner:spawn_fluid_wither`, has provider processing time 5000 and defines three custom-loot entries: Nether Star plus two Experience Nugget outputs, one of them chance-based.

This is machine processing/data settlement. Recipe identity is not promoted into the semantic spell/ritual ledger.

## Exhaustive player-action signature scan

Every provider class was disassembled and every class signature was checked for:

`use · useOn · useWithoutItem · releaseUsing · onUseTick · finishUsingItem · interactLivingEntity · hurtEnemy · inventoryTick · onArmorTick · onItemUseFirst`

Result: **zero matching provider overrides**.

## Exact machine settlement

`SpawnerBlockEntity` is a kinetic block entity. Exact bytecode exposes:

- provider `SmartFluidTankBehaviour` input;
- provider `RecipeRequirementsBehaviour<SpawnerRecipe>`;
- dynamic cycle behavior;
- scroll-value spawn-point configuration;
- server-side fake-player/context infrastructure;
- mob/entity resolution from the active `SpawnerRecipe`;
- custom-loot roll/collection support.

Entity materialization occurs as the consequence of a machine recipe cycle. There is no independent player-owned spell/ritual action registry or cast root.

## KubeJS / recipe mutability

The exact artifact includes `SpawnerKubeRecipe` and `SpawnerRecipeSchema`. KubeJS can alter the machine recipe roster. That surface changes processing data; it does not establish a provider spell/summon-action registry.

## Semantic result

- standalone spell/glyph/ritual/ability roots: **0**;
- player-invoked supernatural summon roots: **0**;
- 28 default spawner machine recipes: **EXCLUDED**;
- random-biome mob generation: **EXCLUDED**;
- Wither recipe/custom loot: **EXCLUDED**;
- Loot Collector: **EXCLUDED**;
- KubeJS recipe schema: **EXCLUDED**.

Disposition: **`ZERO_SEMANTIC_KINETIC_MOB_SPAWN_INFRA`**.

## Clean-room boundary

The durable catalog retains hashes, counts, recipe IDs/counts and behavior-level control-flow classifications required for semantic cataloging. It does not redistribute the JAR, implementation bodies, assets or localization prose.
