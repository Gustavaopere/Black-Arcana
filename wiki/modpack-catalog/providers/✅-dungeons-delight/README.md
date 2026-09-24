# Dungeon's Delight — 1.5.1

Status: `CURRENT PHYSICAL COMPONENT / EXACT SOURCE-PINNED FOOD + COMBAT-EFFECT MAGIC SURFACE / 12 MOB EFFECTS / 2 ENCHANTMENTS / ZERO SPELL-RITUAL-ABILITY REGISTRY / +0 STRICT SEMANTIC MAGIC / RUNTIME QA FAIL-CLOSED`

## Current physical identity

Current sibling authority:

`neoforge-rpg-skilltree@c3de5878d69a7a6b4441606ef2b9e96a61a8f2e9`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Addons + Adventure and RPG + Armor, Tools, and Weapons + Food + Magic/✅-dungeons-delight v1.5.1.md`

Current certified identity:

- physical/index row: **#416**;
- JAR: `neoforge-dungeonsdelight-1.21.1-1.5.1.jar`;
- mod id: `dungeonsdelight`;
- distribution/release version: `1.5.1`;
- physical-pack dependency line includes Farmer's Delight 1.3.4, RunicLib 5.0.7 and NeoForge 21.1.250;
- the sibling explicitly preserves the known installed-metadata divergence where internal metadata reports `1.5.0`.

No installed-JAR digest is preserved in the certified dossier used here, so byte-for-byte physical ↔ source equality is not claimed.

## Exact source pin

Official source:

`Yirmiri/Dungeons-Delight@0c2d621ebc7dcce3df5dad0ea485209ef2396f9c`

Tree:

`3b7135c479ad2ee53b6e6a17c0fcb1238d57eaed`

The exact commit updates `gradle.properties` to:

- `mod_id=dungeonsdelight`;
- `mod_version=1.5.1`;
- Minecraft `1.21.1`;
- NeoForge minimum/development line `21.1.219`;
- Farmer's Delight dependency updated to the 1.3.4 file line.

The exact commit also adds the 1.5.1 changelog and the Stained Scrap loot-modifier fixes.

## Magic-surface classification

Canonical catalog classification:

`MONSTER-FOOD / COMBAT-EFFECT / ENCHANTMENT SUPPORT CONTENT / ZERO INDEPENDENT SPELL-RITUAL-ACTION REGISTRY`

Dungeon's Delight is magic-themed/cross-domain content because its foods, monster-state system, effects, enchantments, living-fire presentation and dungeon mechanics produce supernatural outcomes. Under the Black Arcana semantic metric, however, food consumption, status effects, enchantments, gear and passive item behavior do not become standalone spell/ritual/action identities merely because they are supernatural.

## Exact registry boundary

The exact 1.5.1 entrypoint registers these provider-owned registry families:

- particles;
- blocks;
- items;
- mob effects;
- block entities;
- recipe serializers/types;
- menu types;
- creative tabs;
- entities;
- sounds;
- enchantment data components;
- features;
- advancement criteria;
- integration items.

There is no provider spell registry registration in the entrypoint.

Exact source search at the 1.5.1 line returns no provider use of:

- `registerSpell`;
- `SpellRegistry`;
- `AbstractSpell`;
- ritual registry/surface;
- ability registry/surface.

## Counted support surfaces

### Mob effects — 12

`DDEffects` registers exactly:

1. `feral_bite`;
2. `serrated`;
3. `putrid_scent`;
4. `ravenous_rush`;
5. `pouncing`;
6. `exudation`;
7. `swift_step`;
8. `rotgut`;
9. `decisive`;
10. `voracity`;
11. `tenacity`;
12. `burrow_gut`.

These are status/effect identities, not spells or ritual actions under the current semantic metric.

### Enchantments — 2

Exact datagen registers:

- `dungeonsdelight:ricochet`;
- `dungeonsdelight:serrated_strike`.

These are gear enchantments and remain metric-excluded.

### Cooking/recipe infrastructure

`DDRecipeRegistries` owns:

- serializer `monster_cooking`;
- serializer `monster_food_serving`;
- recipe type `monster_cooking`.

These are culinary processing identities, not magical action identities.

## 1.5.1 delta

The exact 1.5.1 commit is a maintenance patch over the 1.5 Lull Garden line:

- updates Farmer's Delight compatibility to the 1.3.4 line;
- fixes Stained Scrap drops from Spawners/Rotten Spawners.

No new spell/ritual/action registry is introduced by this patch.

## Black Arcana authority boundary

- Dungeon's Delight owns monster-food recipes, provider mob effects, item/weapon behavior, enchantments, XP/cooking mechanics and its own entity/block systems.
- Farmer's Delight owns the base culinary framework it extends.
- Black Arcana must not reinterpret foods, effects or enchantments as Black Arcana spells merely because they produce supernatural effects.
- RPG Skill Tree remains authority for progression, attributes, Mastery, perks and gates through verified contracts only.

## Runtime fail-closed boundary

Still unresolved for the assembled pack:

- physical JAR digest ↔ source byte equality;
- the installed internal metadata `1.5.0` divergence versus distribution/source `1.5.1`;
- effective common/client config;
- combat scaling for Ricochet/Serrated interactions;
- Putrid Scent and other effect overlap;
- Dungeon Stove XP settlement/stacking;
- dispenser exactly-once behavior;
- item-ID migration behavior;
- save/reload/restart lifecycle;
- current Farmer's Delight/RunicLib integration in the full pack.

## Result

**✅ Cataloged.**

Semantic accounting:

- provider-owned spells: **0**;
- provider-owned ritual/rite identities: **0**;
- provider-owned discrete magic-action registry: **0**;
- 12 mob effects: support/status content, excluded;
- 2 enchantments: gear content, excluded;
- strict semantic delta: **+0**.

This is catalog closure, not a runtime compatibility PASS.
