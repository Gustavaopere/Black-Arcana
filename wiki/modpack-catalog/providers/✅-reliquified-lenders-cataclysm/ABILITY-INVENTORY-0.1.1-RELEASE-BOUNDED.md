# Reliquified L_Ender's Cataclysm 0.1.1 — release-bounded ability inventory

Status: `9 RELIC OWNERS / 11 OWNER-SCOPED ABILITY ROOTS / LAST PUBLIC 0.1 SOURCE + EXACT 0.1.1 PUBLISHER COMPATIBILITY BOUNDARY`

Public source checkpoint: `Octo-Studios/reliquified-lenders-cataclysm@29a3b80febeac6e1fb5726d8b5883cdff4e775da` (`mod_version=0.1`).

Publisher release boundary: CurseForge File `6882649`, version `0.1.1`, whose published delta is compatibility with OctoLib 0.6.

| # | Registered owner | Ability ID | Localized title where present | Source-level loot route |
|---:|---|---|---|---|
| 1 | `scouring_eye` | `glowing_scour` | Pursuit | Cursed Pyramid + The End |
| 2 | `void_vortex_in_bottle` | `spawn_vortex` | Void Tornado | Frosted Prison + The End |
| 3 | `void_cloak` | `void_invulnerability` | Invulnerability | Cursed Pyramid + Frosted Prison + The End |
| 4 | `void_cloak` | `void_rune` | Call of the Void | same owner loot route |
| 5 | `void_cloak` | `seismic_zone` | Final Cry | same owner loot route |
| 6 | `vacuum_glove` | `vacuum_slowdown` | The Edge | Cursed Pyramid + The End |
| 7 | `void_bubble` | `protective_bubble` | Protective Bubble | The End |
| 8 | `ring_of_the_flame_kindler` | `flame_summon` | localization title empty at source checkpoint | The Nether |
| 9 | `mask_of_rage` | `ram_mode` | localization title empty at source checkpoint | The Nether |
| 10 | `fire_plate` | `spawn_shield` | localization title empty at source checkpoint | The Nether |
| 11 | `volcano` | `jetpack` | localization title empty at source checkpoint | The Nether |

## Cardinality checks

- `ItemRegistry`: **9** owner registrations;
- public 0.1 item classes: **9**;
- owner-scoped ability builders/data roots: **11**;
- English localization owner/ability roots: **11**;
- owner classes with loot definitions: **9/9**;
- current compat fix identities counted separately: **0**.

## Deduplication rule

The three Void Cloak roots are intentionally separate ability identities under one owner. Rank modifiers, leveling sources and downstream projectiles/effects remain modifiers/consequences and add zero extra semantic identities.

The New Relics Fix 1.0.2 modifies compatibility/runtime representation for the original addon; it does not mint replacement semantic owners.
