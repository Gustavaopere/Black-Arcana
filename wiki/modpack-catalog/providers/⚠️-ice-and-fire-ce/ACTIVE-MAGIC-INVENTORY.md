# Ice And Fire Community Edition 2.1.2 — active magic-action inventory

Evidence basis: exact hash-matched current artifact, exact 2.1.2 source-semver pin `0cf5a2458e1ccf552b9859531ee21c4816e5a686`, and exact current-JAR reachability run `36323035696`.

| Semantic action family | Provider item surface | Current disposition | Strict delta |
|---|---|---|---:|
| Cockatrice Scepter beam | `iceandfire:cockatrice_scepter` | `COUNTED_EXACT` — exact current recipe + recipe advancement | 1 |
| Deathworm Gauntlet lunge/strike | three `deathworm_gauntlet_*` variants | `COUNTED_EXACT` — three exact current recipes, one deduplicated semantic family | 1 |
| Gorgon Head petrification | `iceandfire:gorgon_head` | `COUNTED_EXACT` — exact current Gorgon loot table | 1 |
| Dread Lich Staff projectile | `iceandfire:lich_staff` | `CONDITIONAL` — exact source equips Dread Lich with the staff, but exact provider data has no acquisition ref and no explicit provider drop route is proven | 0 |
| Pixie Wand charge | `iceandfire:pixie_wand` | `COUNTED_EXACT` — exact current recipe + advancement | 1 |
| Siren Flute charm | `iceandfire:siren_flute` | `COUNTED_EXACT` — exact current recipe | 1 |
| Summoning Crystal teleport | Fire/Ice/Lightning summoning crystals | `COUNTED_EXACT` — three exact current recipes; one shared dragon-teleport family | 1 |
| Stymphalian Feather volley | `iceandfire:stymphalian_feather_bundle` | `COUNTED_EXACT` — exact current recipe | 1 |
| Phantasmal Blade / Ghost Sword projectile | `iceandfire:ghost_sword` | `CONDITIONAL` — exact current recipe/advancement acquisition is closed; deployed `tools.phantasmalBladeAbility` remains unresolved | 0 |

**Current action-family total: 9. Strict counted: 7. Conditional: 2. Strict contribution: +7.**

## Exact reachability evidence

Hash-gated run `36323035696` finds:

- Cockatrice Scepter: recipe + advancement;
- all three Deathworm Gauntlets: recipe + advancement;
- Gorgon Head: entity loot table + advancement;
- Pixie Wand: recipe + advancement;
- Siren Flute: recipe;
- all three Summoning Crystals: recipe/reset-recipe surfaces;
- Stymphalian Feather Bundle: recipe;
- Ghost Sword: recipe + advancement + provider tag;
- Dread Lich Staff: **no exact provider data reference**.

Variant items are deduplicated by semantic family.

## Excluded technical/utility surfaces

- Dread Queen Staff: no current usage in exact 2.1.2 source.
- Cyclops Eye: passive carried-item aura.
- Dragon Flute: dragon control command.
- Dragon Horn: dragon storage/restore.
- Tide Trident: trident weapon mechanics.
- `BuiltinAbilities` post-hit families for silver/dragonblood/dragonsteel tools: weapon procs triggered by ordinary hits rather than independent selected actions.
