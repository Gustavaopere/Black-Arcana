# Ice And Fire Community Edition 2.1.2 — active magic-action inventory

Evidence basis: exact hash-matched current artifact plus exact 2.1.2 source-semver pin `0cf5a2458e1ccf552b9859531ee21c4816e5a686`.

| Semantic action family | Provider item surface | Current disposition | Strict delta |
|---|---|---|---:|
| Cockatrice Scepter beam | `iceandfire:cockatrice_scepter` | `CONDITIONAL` — active withering beam; assembled survival route not yet bounded | 0 |
| Deathworm Gauntlet lunge/strike | three `deathworm_gauntlet_*` variants | `CONDITIONAL` — one shared active family; assembled survival route not yet bounded | 0 |
| Gorgon Head petrification | `iceandfire:gorgon_head` | `CONDITIONAL` — active petrification; assembled survival route not yet bounded | 0 |
| Dread Lich Staff projectile | `iceandfire:lich_staff` | `CONDITIONAL` — fires Dread Lich skull projectile; assembled survival route not yet bounded | 0 |
| Pixie Wand charge | `iceandfire:pixie_wand` | `CONDITIONAL` — active magic projectile; assembled survival route not yet bounded | 0 |
| Siren Flute charm | `iceandfire:siren_flute` | `CONDITIONAL` — targeted charm action; assembled survival route not yet bounded | 0 |
| Summoning Crystal teleport | Fire/Ice/Lightning summoning crystals | `CONDITIONAL` — one shared dragon-teleport family; assembled survival route not yet bounded | 0 |
| Stymphalian Feather volley | `iceandfire:stymphalian_feather_bundle` | `CONDITIONAL` — eight-direction active projectile volley; assembled survival route not yet bounded | 0 |
| Phantasmal Blade / Ghost Sword projectile | `iceandfire:ghost_sword` | `CONDITIONAL` — swing-triggered projectile; deployed `tools.phantasmalBladeAbility` additionally unresolved | 0 |

**Current candidate total: 9. Strict contribution in this tranche: 0.**

## Excluded technical/utility surfaces

- Dread Queen Staff: no current usage in exact 2.1.2 source.
- Cyclops Eye: passive carried-item aura.
- Dragon Flute: dragon control command.
- Dragon Horn: dragon storage/restore.
- Tide Trident: trident weapon mechanics.
- `BuiltinAbilities` post-hit families for silver/dragonblood/dragonsteel tools: weapon procs triggered by ordinary hits rather than independent selected actions.

The three Summoning Crystal variants and three Deathworm Gauntlet color variants are deduplicated by semantic family.
