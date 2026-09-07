# Hexalia 1.3.6 — Rituals

## Estado

`NATURE'S RITUAL SOURCE-PINNED / PLAYER-FACING RECIPES 19/19 / OUTPUTS 19/19 CLASSIFIED / DEBUG RECIPE EXCLUDED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Canonical release-line source:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

## Current catalog

- [Nature's Ritual — 19/19 player-facing recipes and lifecycle](NATURES-RITUAL-CATALOG.md)
- [Nature's Ritual — 19/19 output capability classification](OUTPUT-CAPABILITIES.md)

The 1.3.6 generated/source surface contains one additional `debug_natures_ritual`; it is deliberately excluded from the player-facing count.

## Coverage now closed at source level

The master recipe catalog closes:

- central input;
- brazier ingredients;
- salt admission;
- crop requirement;
- duration;
- output identity;
- cancellation/completion lifecycle.

The output catalog separately classifies all 19 player-facing results:

- 4 elemental reagent nodes;
- 7 persistent magical plants;
- Rabbage Seeds → throwable Bleeding produce;
- Kelpweave Blade;
- Rootshaper;
- Sage Pendant;
- 4 Bloomwrap armor pieces.

This distinction matters because the created outputs remain Hexalia-owned after ritual completion. Their later projectiles, auras, world mutations, block breaks, XP modification and armor event behavior are not additional ritual casts.

## Remaining Hexalia ritual-adjacent work

Nature's Ritual recipe/output coverage is now source-complete for the 1.3.6 pin. Remaining Hexalia audit work belongs to separate systems, especially:

- `hexalia:mutation` recipe inventory used by Morphora/Mutavis;
- Mortar & Pestle transformations;
- idols and other capability-bearing support items;
- installed-JAR/runtime validation for the `filename 1.3.6 / runtime metadata 1.3.5` mismatch.

Any future integration preserves Hexalia authority; ritual ticks, crop scans and persistent output ticks are not Black Arcana cast/mastery events.