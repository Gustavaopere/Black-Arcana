# Hexalia 1.3.7 — Brew of Gravebloom

Status: `RELEASE-SOURCE-PINNED 1.3.7 / CURRENT RECIPE + EFFECT EVENT AUDITED / ASSEMBLED WORLD QA SEPARATE`

Release source: `AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`.

## Identity and recipe

- item: `hexalia:brew_of_gravebloom`;
- recipe type: `hexalia:small_cauldron`;
- ingredients: `hexalia:spirit_powder`, `minecraft:rotten_flesh`, `hexalia:witchweed`, `hexalia:tree_resin`;
- registered item class: common Hexalia `BrewItem`;
- MobEffect: `hexalia:gravebloom`, beneficial;
- base effect duration: **1800 ticks = 90 s**;
- amplifier: `0`;
- full Moonweave multiplier: `1.5`, producing **2700 ticks = 135 s**.

The recipe JSON also carries `duration: 4800`; that is Small Cauldron recipe/process data and must not be confused with the consumed brew's 1800-tick MobEffect duration.

## Provider behavior

`GravebloomEffect` itself is a marker MobEffect. The gameplay effect is implemented by the provider death event:

- server-side only;
- slain entity must be a `Monster`;
- damage source entity must be a `Player`;
- that player must currently have the Gravebloom MobEffect.

On an admitted kill, Hexalia attempts a local world mutation around the death position:

- candidate patch radius: `2` blocks in X/Z, excluding the four outer corners;
- moss replacement chance: `0.9` within distance <1.5, otherwise `0.55`;
- attempts to place `2..4` sprouts;
- the first successful sprout comes from the provider herb set when possible;
- subsequent sprouts come from `#hexalia:gravebloom_plants`.

## Semantic disposition

Gravebloom is a persistent consumable effect and death-triggered world mutation. Under the Black Arcana semantic metric it is **not** a new standalone spell/ritual identity. Drinking the brew and each later monster death are not promoted into repeated magic-object identities.

Hexalia remains authority for the effect, kill admission and world mutation. Black Arcana must not duplicate moss/plant placement or treat each provider death hook as a cast/mastery event.

## Runtime QA

Still fail-closed for assembled pack behavior: protection mods, altered block tags, structure/world rules, reload behavior and concurrent world mutation should be tested against the physical 1.3.7 JAR.
