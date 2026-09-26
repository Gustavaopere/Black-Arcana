# Hexalia 1.3.7 — Rituals

## Estado

`RELEASE-SOURCE-PINNED 1.3.7 / NATURE'S RITUAL 23/23 PLAYER-FACING / OUTPUTS 23/23 CLASSIFIED / SOUL-SUMMONING PATH INCLUDED / PHYSICAL SHA-1 KNOWN / ASSEMBLED RUNTIME QA SEPARATE`

Physical provider: `hexalia-neoforge-1.3.7.jar` / SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`.

Release-correlated source: `AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283` (`Hexalia 1.3.7`, 2026-09-13).

## Current catalog

- [Nature's Ritual — 23/23 player-facing recipes and lifecycle](NATURES-RITUAL-CATALOG.md)
- [Nature's Ritual — 23/23 output capability classification](OUTPUT-CAPABILITIES.md)

The current release data contains **23** `hexalia:natures_ritual` recipes and no generated `debug_natures_ritual`. Relative to the previously cataloged 1.3.6 surface, four player-facing identities were added:

- `cinderhew_from_ritual_table`;
- `heartseed_from_ritual_table`;
- `summon_silk_moth`;
- `summon_cacofey`.

The two summon rituals use provider-native `requires_soul` admission and entity results. Their soul capture/manifestation is part of the same ritual identity, not an extra spell or mastery event.

## Current lifecycle boundary

1.3.7 replaces the old four-cardinal-brazier assumption with free-form matching of non-empty Ritual Braziers inside horizontal radius 8. Selected braziers must be salted, offerings are consumed sequentially at 40 ticks each, and the configurable mature-crop requirement remains provider-owned.

For soul-gated recipes, completion of offerings moves the table into `AWAITING_SOUL`; a non-player LivingEntity killed by a player with the Athame can be captured within radius 8, followed by a 50-tick manifestation phase.

## Output classification

The 23 ritual results currently break down as:

- 4 elemental reagent nodes;
- 7 persistent magical plants;
- 1 Rabbage seed/projectile line;
- 3 previously cataloged ritual tools/weapons/accessories;
- 4 Bloomwrap armor pieces;
- 2 new 1.3.7 ritual-created items (`cinderhew`, `heartseed`);
- 2 entity summons (`silk_moth`, `cacofey`).

Created items/entities remain Hexalia-owned after ritual settlement. Their later attacks, passive effects, world mutation, taming, projectiles or AI are downstream consequences and are not additional ritual identities.

## Authority rule

Hexalia owns ritual admission, salt/offerings/crop costs, persistent table state, soul capture and final result settlement. Black Arcana must not run a parallel transaction or count provider ticks/downstream effects as new casts. Any RPG Skill Tree progression hook requires one deduplicated causal completion event through a verified contract.
