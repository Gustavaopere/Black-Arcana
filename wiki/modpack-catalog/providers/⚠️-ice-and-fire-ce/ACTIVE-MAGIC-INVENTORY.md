# Ice And Fire Community Edition 2.1.2 — active magic-action inventory

Evidence basis: exact hash-matched current artifact, exact 2.1.2 source-semver pin `0cf5a2458e1ccf552b9859531ee21c4816e5a686`, exact current-JAR reachability run `36323035696`, and current-pack NeoForge 21.1.250 equipment-drop audit run `36327488231`.

| Semantic action family | Provider item surface | Current disposition | Strict delta |
|---|---|---|---:|
| Cockatrice Scepter beam | `iceandfire:cockatrice_scepter` | `COUNTED_EXACT` — exact current recipe + recipe advancement | 1 |
| Deathworm Gauntlet lunge/strike | three `deathworm_gauntlet_*` variants | `COUNTED_EXACT` — three exact current recipes, one deduplicated semantic family | 1 |
| Gorgon Head petrification | `iceandfire:gorgon_head` | `COUNTED_EXACT` — exact current Gorgon loot table | 1 |
| Dread Lich Staff projectile | `iceandfire:lich_staff` | `COUNTED_EXACT` — exact 2.1.2 JAR equips every Dread Lich with the staff in `MAINHAND`; exact current-pack NeoForge 21.1.250 `Mob` runtime initializes hand drop chance to `0.085` and its equipment-drop path can spawn the equipped stack | 1 |
| Pixie Wand charge | `iceandfire:pixie_wand` | `COUNTED_EXACT` — exact current recipe + advancement | 1 |
| Siren Flute charm | `iceandfire:siren_flute` | `COUNTED_EXACT` — exact current recipe | 1 |
| Summoning Crystal teleport | Fire/Ice/Lightning summoning crystals | `COUNTED_EXACT` — three exact current recipes; one shared dragon-teleport family | 1 |
| Stymphalian Feather volley | `iceandfire:stymphalian_feather_bundle` | `COUNTED_EXACT` — exact current recipe | 1 |
| Phantasmal Blade / Ghost Sword projectile | `iceandfire:ghost_sword` | `CONDITIONAL` — exact current recipe/advancement acquisition is closed; deployed `tools.phantasmalBladeAbility` remains unresolved | 0 |

**Current action-family total: 9. Strict counted: 8. Conditional: 1. Strict contribution: +8.**

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
- Dread Lich Staff: **no provider-data recipe/loot reference**, but exact binary/runtime inheritance closes a separate survival route: Dread Lich equips the staff in `MAINHAND`, does not override drop chance or death-loot handling, and current-pack NeoForge 21.1.250 initializes hand-equipment drop chance at `0.085` before evaluating the standard equipment-drop path.

Variant items are deduplicated by semantic family.

The Dread Lich route is not a generic vanilla assumption: run `36327488231` materialized the current-pack NeoForge 21.1.250 mapped runtime, inspected `Mob` bytecode directly, and hash-gated the exact physical/publisher Ice And Fire CE 2.1.2 JAR before checking the Dread Lich equipment path. See [`DREAD-LICH-STAFF-EXACT-RUNTIME-REACHABILITY.md`](DREAD-LICH-STAFF-EXACT-RUNTIME-REACHABILITY.md).

## Excluded technical/utility surfaces

- Dread Queen Staff: no current usage in exact 2.1.2 source.
- Cyclops Eye: passive carried-item aura.
- Dragon Flute: dragon control command.
- Dragon Horn: dragon storage/restore.
- Tide Trident: trident weapon mechanics.
- `BuiltinAbilities` post-hit families for silver/dragonblood/dragonsteel tools: weapon procs triggered by ordinary hits rather than independent selected actions.
