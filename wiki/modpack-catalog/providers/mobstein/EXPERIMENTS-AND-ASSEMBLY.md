# Mobstein 5.4.4 — experiments, surgery and subject assembly

## Evidence status

`PUBLISHER PUBLIC GUIDE / EXACT INSTALLED RELEASE LINE / INTERNAL IDS+API UNVERIFIED / RUNTIME QA PENDING`

## Anatomical material surface

The current official guide documents physical/anatomical acquisition including:

- Piglin Chop, which can be cooked;
- Polar Bear Leather;
- Panda Leather;
- Villager Nose via shears interaction;
- Spider/Cave Spider Legs via shears interaction;
- Dolphin Tail;
- Horse Leather;
- Axolotl Gill;
- Bat Wings and Fangs;
- cooked normal Leather participating in some body-related recipes.

The exact item registry IDs, loot-table probabilities and all recipes remain unverified at this public-only checkpoint.

## Organ Extractor

The official guide documents an **Organ Extractor** that processes compatible full bodies using Tweezers and yields a random organ from the provider organ set. Public Mobstein documentation across the current line identifies the anatomical organ family as Brain, Lungs and Heart.

Authority consequence: organ extraction is a Mobstein-owned acquisition loop. Black Arcana should not generate these organs from generic kills or soul events unless a deliberate provider-native integration exposes that route.

## Full Body Support

The provider documents a **Full Body Support** used to hang/display bodies, with shears used to remove them.

This is corpse/body inventory presentation, not a Black Arcana soul container.

## Surgery Stretch

The official guide presents the **Surgery Stretch** as a mixed-creature reconstruction system using provider body/head/anatomical components plus Mobstein's internal perks.

The current guide states that player heads are not supported in this surgery route and distinguishes the body-part restrictions of this machine from Subject Assembly. Exact internal acceptance predicates remain unverified.

### Mobstein internal perks

Four provider-native modifiers are documented:

| Perk | Public role / range |
|---|---|
| Attack | attack tuning, documented range `0.8–2` |
| Health | health tuning, documented range `20–40` |
| Speed | movement tuning, documented range `0.3–0.5` |
| Template | template/input used in crafting the other perks |

The official guide directs players to JEI for the recipes.

These values are **not** Black Arcana spell coefficients and **not** RPG Skill Tree perk nodes. Any later cross-mod progression should consume real provider outcomes rather than duplicating them.

## Surgery creature types

### Turtle surgery

Publisher-documented behavior:

- tamed with Seagrass;
- provides Regeneration, Luck and Water Breathing.

### Panda surgery

Publisher-documented behavior:

- tamed with Bamboo;
- provides Strength and Resistance.

### Polar Bear surgery

Publisher-documented behavior:

- tamed with fish except cooked fish;
- provides Dolphin's Grace.

### Spider surgery

Publisher-documented behavior:

- tamed with Egg;
- rideable;
- climbs walls;
- when hit, can randomly place a cobweb.

The world mutation/cobweb behavior is provider-owned. Black Arcana must not re-settle or duplicate it through `WorldEffectPolicy`; a future adapter may observe provider consequences but must not claim ownership of the mutation.

### Enderman surgery

Publisher-documented behavior:

- tamed with Grass Block;
- random teleport behavior;
- provides Night Vision.

### Snow Golem surgery

Publisher documentation warns that the resulting creature can break the Surgery Stretch when spawning and describes strong defensive performance.

This world interaction is provider behavior; exact break rules/protection compatibility remain runtime-unverified.

## Subject Assembly Machine

Mobstein 5.4.x publicly documents a separate **Subject Assembly Machine** for mannequin/test-subject creation.

Key distinctions from Surgery Stretch:

- the resulting subject has no special abilities according to the guide;
- it can use any game head supported by the provider's head workflow;
- a Head Creator/Custom Head Machine can generate player heads from a player-head input plus Brain and a supplied player name;
- the created head, torso and pants are then assembled into the mannequin/tester.

This is a visual/testing assembly surface, not a resurrection combat system and not a justification to treat arbitrary player identity as authoritative from client input in Black Arcana.

## Igor and failed experiments

### Igor

Publisher-documented behavior:

- summoned using the Igor Spawner;
- not tameable;
- uses the Igor Table/Station workflow;
- creates random failed experiments;
- public guide excludes experiments 062 and 097 from Igor's random-production pool because those are structure-associated;
- the first attempt is documented to fail;
- Igor must be near the table;
- Suspicious Syringes are thrown at Igor, with the current guide describing multiple attempts and a maximum of four.

No exact probability table, RNG seed semantics or registry IDs are inferred.

### Experiment 097

- tame with Slime Balls;
- passive/random jumping behavior;
- Endermite + Frog visual/body concept;
- does not follow;
- associated with Frankenstein Castle rather than Igor's random pool.

### Experiment 062

- tame with Cocoa Beans;
- passive;
- Cod + Cocoa Block body concept;
- does not follow;
- associated with Frankenstein Castle rather than Igor's random pool.

### Experiment 067

- tame with Seeds;
- Chicken + Enderman body concept;
- random teleport behavior and teleport when hit;
- does not follow;
- obtained through Igor workflow.

### Experiment 077

- tame with Seeds;
- Allay + blue/yellow Parrot body concept;
- flies and performs melee combat;
- does not reproduce Allay item pickup or Parrot shoulder behavior;
- obtained through Igor workflow.

### Experiment 091

Current publisher guide:

- tame with **Strawberries**;
- described as partially passive;
- Fox + dragon concept;
- kills chickens;
- cannot jump.

An older official 5.2.0 changelog instead listed **Sweet Berries** as the tame item. This checkpoint preserves the divergence rather than silently choosing one implementation fact. The current guide is the latest public instruction, while exact 5.4.4 runtime behavior remains QA-pending.

### Experiment 012

- tame with Wheat;
- Llama + Mushroom Cow concept;
- bowl/bucket interaction;
- does not use llama spitting.

### Experiment 007

- tame with any Flower;
- Villager + Bee concept;
- does not lose a stinger/flee like the compared vanilla behavior;
- wanders rather than following normally.

## Deduplication consequences

Mobstein already owns a broad **corpse/anatomy → assembly → reconstructed creature** loop. Black Arcana should avoid duplicate mechanics such as:

- generic organ-harvesting solely to support magical resurrection;
- a second creature-surgery stat system;
- a second failed-experiment RNG table;
- generic corpse-to-minion conversion that merely recreates Mobstein's machines;
- treating Mobstein's Attack/Health/Speed perks as RPG mastery or Black Arcana progression.

A Black Arcana soul-bound summon remains conceptually distinct only if its acquisition, cost, persistence, causal ownership and body/soul identity differ materially from Mobstein reconstruction.