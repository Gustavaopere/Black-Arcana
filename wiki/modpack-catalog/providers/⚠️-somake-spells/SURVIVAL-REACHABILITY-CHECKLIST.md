# Somake Spells 1.0.8-fix — Survival Reachability Closure Checklist

Status: `67/67 EXACT_REGISTRY / SURVIVAL REACHABILITY UNVERIFIED`

## Purpose

The exact hash-matched 1.0.8-fix artifact already closes all **67/67 current registry identities** under the physical optional-provider set. This checklist isolates what is still missing before those identities can be promoted from `REACHABILITY_CONDITIONAL`.

Two independent questions must not be collapsed:

1. **Global spell-lock behavior** — Somake registers `enableSpellLockSystem` as a COMMON config in `somakespells/general/common.toml`. The audited code default is `false`, but the effective deployed value is `NÃO VERIFICADO` and source defaults are not accepted as deployed state.
2. **Object-level survival reachability** — every spell needs an authoritative player-reachable acquisition/unlock path in the actual pack. Registry presence alone is insufficient.

## Global deployed config gate

| Config file | Key | Code default | Effective deployed value | Evidence state |
|---|---|---|---|---|
| `somakespells/general/common.toml` | `enableSpellLockSystem` | `false` | `NÃO VERIFICADO` | `DEPLOYED CONFIG REQUIRED` |

When the lock system is disabled, the audited provider path reports effectively unrestricted mastery level for that subsystem. When enabled, Somake's own unlock/mastery path can reject unlearned spell levels. This checklist does not infer which mode the pack is actually using.

## Registry / reachability matrix

`Registration gate` records only predicates already proved by the exact artifact and physical provider set. `Survival reachability` remains `NÃO VERIFICADO` until an authoritative pack path is demonstrated for the individual spell.

| # | Registry ID | Registration gate in current pack | Survival reachability |
|---:|---|---|---|
| 1 | `combustion` | unconditional | `NÃO VERIFICADO` |
| 2 | `ritual_flame` | unconditional | `NÃO VERIFICADO` |
| 3 | `damned_demomans` | unconditional | `NÃO VERIFICADO` |
| 4 | `eruption` | unconditional | `NÃO VERIFICADO` |
| 5 | `fire_blast` | unconditional | `NÃO VERIFICADO` |
| 6 | `firestorm_vortex` | unconditional | `NÃO VERIFICADO` |
| 7 | `pumpkin_bomb` | unconditional | `NÃO VERIFICADO` |
| 8 | `ignis_shield` | unconditional | `NÃO VERIFICADO` |
| 9 | `incinerator_slash` | unconditional | `NÃO VERIFICADO` |
| 10 | `abyssal_burn` | unconditional | `NÃO VERIFICADO` |
| 11 | `fire_orbs` | unconditional | `NÃO VERIFICADO` |
| 12 | `abyssal_orbs` | unconditional | `NÃO VERIFICADO` |
| 13 | `apocalyptic_burst` | unconditional | `NÃO VERIFICADO` |
| 14 | `earthbound` | unconditional | `NÃO VERIFICADO` |
| 15 | `submerge` | unconditional | `NÃO VERIFICADO` |
| 16 | `tidal_grasp` | unconditional | `NÃO VERIFICADO` |
| 17 | `tsunami` | unconditional | `NÃO VERIFICADO` |
| 18 | `tidal_dash` | unconditional | `NÃO VERIFICADO` |
| 19 | `thunder_cloud` | unconditional | `NÃO VERIFICADO` |
| 20 | `water_control` | unconditional | `NÃO VERIFICADO` |
| 21 | `water_spear` | unconditional | `NÃO VERIFICADO` |
| 22 | `hydro_slash` | unconditional | `NÃO VERIFICADO` |
| 23 | `sea_serpent` | unconditional | `NÃO VERIFICADO` |
| 24 | `sea_serpent_jet` | unconditional | `NÃO VERIFICADO` |
| 25 | `storm_aura` | unconditional | `NÃO VERIFICADO` |
| 26 | `water_ball` | unconditional | `NÃO VERIFICADO` |
| 27 | `summon_zombie` | unconditional | `NÃO VERIFICADO` |
| 28 | `lightning_spear` | unconditional | `NÃO VERIFICADO` |
| 29 | `ender_corruption` | unconditional | `NÃO VERIFICADO` |
| 30 | `phantom_barrage` | unconditional | `NÃO VERIFICADO` |
| 31 | `overgrowth` | unconditional | `NÃO VERIFICADO` |
| 32 | `permafrost` | unconditional | `NÃO VERIFICADO` |
| 33 | `blessing` | unconditional | `NÃO VERIFICADO` |
| 34 | `custodia_caeli` | unconditional | `NÃO VERIFICADO` |
| 35 | `blessed_connection` | `mowziesmobs` present | `NÃO VERIFICADO` |
| 36 | `guardian_connection` | `mowziesmobs` present | `NÃO VERIFICADO` |
| 37 | `cursed_connection` | `mowziesmobs` present | `NÃO VERIFICADO` |
| 38 | `blood_rush` | unconditional | `NÃO VERIFICADO` |
| 39 | `blood_cut` | unconditional | `NÃO VERIFICADO` |
| 40 | `bloody_legacy` | unconditional | `NÃO VERIFICADO` |
| 41 | `bloodmark` | unconditional | `NÃO VERIFICADO` |
| 42 | `fragmented_requiem` | unconditional | `NÃO VERIFICADO` |
| 43 | `rose_secret` | unconditional | `NÃO VERIFICADO` |
| 44 | `eldritch_gambit` | unconditional | `NÃO VERIFICADO` |
| 45 | `chain_connection` | unconditional | `NÃO VERIFICADO` |
| 46 | `evocation_fortitude` | unconditional | `NÃO VERIFICADO` |
| 47 | `reverberation` | unconditional | `NÃO VERIFICADO` |
| 48 | `slumber_melody` | unconditional | `NÃO VERIFICADO` |
| 49 | `resonant_pulse` | unconditional | `NÃO VERIFICADO` |
| 50 | `ram_tchum` | unconditional | `NÃO VERIFICADO` |
| 51 | `jingle_bell` | unconditional | `NÃO VERIFICADO` |
| 52 | `lightning_ball` | unconditional | `NÃO VERIFICADO` |
| 53 | `lightning_dance` | unconditional | `NÃO VERIFICADO` |
| 54 | `lightning_field` | unconditional | `NÃO VERIFICADO` |
| 55 | `lightning_strike` | unconditional | `NÃO VERIFICADO` |
| 56 | `lightning_cut` | unconditional | `NÃO VERIFICADO` |
| 57 | `lightning_spark` | unconditional | `NÃO VERIFICADO` |
| 58 | `lightning_swarm` | unconditional | `NÃO VERIFICADO` |
| 59 | `lightning_lash` | unconditional | `NÃO VERIFICADO` |
| 60 | `halberd_strike` | unconditional | `NÃO VERIFICADO` |
| 61 | `mirror_strike` | `iss_magicfromtheeast` present | `NÃO VERIFICADO` |
| 62 | `render_rush` | unconditional | `NÃO VERIFICADO` |
| 63 | `axe_cleave` | unconditional | `NÃO VERIFICADO` |
| 64 | `desert_wrath` | unconditional | `NÃO VERIFICADO` |
| 65 | `soul_grab` | unconditional | `NÃO VERIFICADO` |
| 66 | `spirit_empowerment` | `iss_magicfromtheeast` present | `NÃO VERIFICADO` |
| 67 | `symmetry_empowerment` | `iss_magicfromtheeast` present | `NÃO VERIFICADO` |

## Evidence required per spell

A row may be promoted only from evidence tied to the actual pack/runtime, for example a provider-defined survival recipe, loot route, progression/unlock surface, book/forge/ritual path, or authoritative runtime observation that establishes normal player reachability.

For each promoted row, record:

- exact spell registry ID;
- acquisition or unlock mechanism;
- authoritative source of that mechanism;
- prerequisite provider/item/structure if applicable;
- whether `enableSpellLockSystem` changes the path under the deployed config;
- pack/world checkpoint used for validation.

Creative-only presence, command-only permission-level-2 unlocks, registry existence, source defaults, or guessed Iron's generic behavior do **not** close a row by themselves.

## Cross-provider gate notes

The six optional-provider registration gates are already closed for the physical pack and must not be confused with survival reachability:

- `blessed_connection`, `guardian_connection`, `cursed_connection` — `mowziesmobs` is present;
- `mirror_strike`, `spirit_empowerment`, `symmetry_empowerment` — `iss_magicfromtheeast` is present.

Those six therefore belong to the current 67/67 registry inventory, but remain survival-conditional exactly like the other 61.

## Acceptance boundary

Until authoritative deployed evidence closes both the relevant global config interpretation and object-level survival reachability:

- all 67 identities remain `EXACT_REGISTRY / REACHABILITY_CONDITIONAL`;
- Somake remains `⚠️ Parcial / condicionado`;
- no strict semantic-count increase is claimed;
- Black Arcana does not duplicate Somake unlocks, mastery, charges, rituals or Iron's cast settlement.
