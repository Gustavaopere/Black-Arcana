# More Relics 1.7.7 / Relics 0.12.8 compatibility build — exact ability inventory

Evidence state: `COUNTED_EXACT`

Exact physical/publisher artifact: `morerelics-1.7.7-forRelics-0.12.8-1.0-1.21.1.jar`

- physical/publisher SHA-1: `bc220ed291187c97bd1896f1fdd29b2377879ae1`;
- exact audit SHA-256: `c3d71a841ef483d36e062fed5b17c4724260ce4e78ffe7ab9368264ab64d42d2`;
- exact JAR metadata: `morerelics` / `1.7.7-forRelics-0.12.8-1.0`;
- exact owner count: **29 relics**;
- exact `AbilityTemplate.builder(...)` calls: **61**;
- resolved builder roots: **61/61**;
- owner→ability localization pairs: **61**;
- unique root strings: **56**;
- bytecode-root vs localization-root set difference: **0 / 0**.

## Counting rule

Relics abilities are counted owner-scoped. A root string reused by another relic owner remains a distinct provider power under that second owner. This is the same rule already used by the canonical Relics and Reliquified Artifacts audits.

Shared strings in this artifact:

- `cyberpsychosis` — Biojoint, Bionic Eye, Thermoseismic Heart, VertebraX;
- `blood_bond` — Runic Plate, Swiftedge;
- `head_start` — Runic Plate, Swiftedge.

Therefore **61**, not 56, is the semantic cardinality.

## Exact owner-scoped inventory

| Owner ID | Ability count | Exact ability roots | Acquisition / evolution evidence |
|---|---:|---|---|
| `axolotl_cream` | 1 | `mend_moisturize` | exact JAR `LootEntries.AQUATIC` |
| `biojoint` | 2 | `cyberpsychosis`, `suspension` | exact JAR `LootEntries.THE_NETHER` |
| `bionic_eye` | 2 | `cyberpsychosis`, `seeker` | exact JAR `LootEntries.SCULK` |
| `converging_orb` | 1 | `convergence` | current publisher route: Woodland Mansions |
| `crown_of_the_legend` | 2 | `never_die`, `pig_king` | exact JAR `LootEntries.BASTION` |
| `depleted_spool` | 1 | `restoration` | exact JAR `LootEntries.CAVE` |
| `eject_button` | 1 | `nope` | exact JAR `LootEntries.WILDCARD` |
| `epoch_apple` | 2 | `persistent`, `ripen` | current publisher route: Dungeon chests |
| `gravitum_glove` | 2 | `all_in`, `bonk` | exact JAR `LootEntries.END_LIKE` |
| `gravitum_strider` | 2 | `elevated_steps`, `leap` | exact JAR `LootEntries.END_LIKE` |
| `guts_orb` | 1 | `guts` | exact JAR `LootEntries.BASTION` |
| `king_crimson` | 3 | `epitaph`, `talk_to_the_wind`, `the_court` | provider evolution: Tyrant Mask → King Crimson |
| `made_in_heaven` | 4 | `as_one`, `condemn`, `divine_judgement`, `zenith` | provider evolution: Whispering Amulet → Made in Heaven |
| `mass_gauntlet` | 1 | `heavy_hitter` | exact JAR `LootEntries.WILDCARD` |
| `moodworm` | 2 | `moody`, `tranquillity` | exact JAR `LootEntries.WILDCARD` |
| `opal_necklace` | 1 | `bubble_shield` | exact JAR `LootEntries.DESERT` |
| `runic_plate` | 3 | `blood_bond`, `head_start`, `peaceland` | exact JAR `LootEntries.MOUNTAIN` |
| `sentient_rust` | 1 | `corrosive` | exact JAR `LootEntries.MINESHAFT` |
| `shieldweave_cape` | 2 | `dynamic_thread`, `impact_shield` | exact JAR `LootEntries.CAVE` |
| `slumbering_amulet` | 2 | `awakening_potential`, `odd_aura` | current publisher route: Buried Treasure |
| `swiftedge` | 3 | `blood_bond`, `head_start`, `modal_soul` | exact JAR `LootEntries.MOUNTAIN` |
| `thermoseismic_heart` | 3 | `cyberpsychosis`, `pyromania`, `thermal_discharge` | exact JAR `LootEntries.DESERT` |
| `twin_fangs` | 2 | `blindside`, `two_fold` | current publisher route: Pillager Outposts / Woodland Mansions |
| `tyrant_mask` | 4 | `futility`, `monotony`, `regrets`, `revenge` | exact JAR `LootEntries.BASTION` |
| `vertebrax` | 4 | `acquired_immunity`, `cyberpsychosis`, `fortification`, `inoculation` | exact JAR `LootEntries.THE_END` |
| `weavers_spool` | 4 | `bind`, `soar`, `unravel`, `weaver` | provider evolution: Depleted Spool → Weavers Spool |
| `whims_of_fate` | 1 | `just_one_more` | exact JAR `LootEntries.DESERT` |
| `whispering_amulet` | 1 | `ascend_heaven` | provider evolution: Slumbering Amulet → Whispering Amulet |
| `wonder_of_u` | 3 | `entropy`, `event_horizon`, `flow_of_calamity` | provider evolution: Converging Orb → Wonder of U |

## Reachability boundary

Exact bytecode evidence exposes direct Relics `LootTemplate` entries for **20/29** ability-bearing relic classes. The remaining nine owners are closed by the current 1.7.7 publisher acquisition/evolution inventory already tied to this content-locked compatibility line:

- direct loot: Converging Orb, Epoch Apple, Slumbering Amulet, Twin Fangs;
- evolution-only: King Crimson, Whispering Amulet, Made in Heaven, Weavers Spool, Wonder of U.

These routes establish catalog-level acquisition. Live loot injection, evolution state migration, config values and assembled-pack settlement remain runtime QA.

## Exclusions

Not counted separately:

- relic item containers;
- rank/stat modifiers;
- UI indicators;
- evolution stages as containers;
- repeated ticks/procs of one owner-scoped ability;
- projectiles/entities/effects caused downstream;
- loot entries.

## Result

**61 `COUNTED_EXACT` provider-owned owner-scoped ability roots.**