# Relics — 0.12.8

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 20 RELICS / 39 BASE ABILITIES + 2 DISTINCT SYNERGIES = 41 DISCRETE PROVIDER POWERS / COUNTED_EXACT / RUNTIME QA FAIL-CLOSED`

## Current physical identity

Current sibling authority rechecked at:

`neoforge-rpg-skilltree@5751321657cea41e77ec7c2be7f191e11c9b68a7`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Armor, Tools, and Weapons + Cosmetic + Magic + Ores and Resources/✅-relics v0.12.8.md`

Physical identity:

- JAR: `relics-1.21.1-0.12.8.jar`;
- mod id: `relics`;
- runtime: `0.12.8`;
- Minecraft 1.21.1 / NeoForge;
- physical SHA-1: `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`.

## Exact publisher artifact

CurseForge project/file:

- project `445274`;
- file `8158315`;
- filename `relics-1.21.1-0.12.8.jar`;
- Beta;
- uploaded 2026-05-28;
- Client & Server.

Clean-room exact-artifact audit observed:

- bytes: `5,007,593`;
- SHA-1: `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`;
- SHA-256: `db6f436053fe717413389e55390a5f98103ccd91cca5fe469e090bdfaef70717`.

The publisher artifact SHA-1 exactly matches the physical sibling fingerprint. Physical ↔ publisher artifact equality is therefore closed.

## Exact artifact inventory

Temporary NON-MERGE evidence:

- inventory commit `2af1ea964a3367d860099e0b32422a663674fe19`;
- final deduplication commit with green evidence `3fa149bdf55c01ac7c3d7ffcbad4935e49545d97`;
- final green CI run `36082547793`;
- `verify`: SUCCESS;
- Foundation GameTest: SUCCESS;
- dedicated-server smoke: SUCCESS;
- Stage 05 companion smoke: SUCCESS.

Exact artifact structural counts:

- classes: **702**;
- provider resources: **789**;
- embedded jar-in-jar libraries: **0**;
- dependency mod IDs: `curios, minecraft, neoforge, octolib, relics`.

The exact artifact contains **20 base relic item classes**, matching the current documented 20-relic roster.

## Exact discrete power inventory

Exact English localization roots under the provider's ability-description namespace close **39 base ability identities**.

| Relic owner | Exact base ability ids |
|---|---|
| `chef_hat` | `satiety` |
| `chorus_staff` | `blink` |
| `clot_of_time` | `rewind` |
| `cut_glass_boot` | `glass` |
| `experience_disperser` | `dispersion` |
| `ghostly_mantle` | `fog`, `gaze`, `spectral_escape` |
| `glitchy_mantle` | `distortion`, `glitch`, `illusion` |
| `hunting_belt` | `pack`, `slots` |
| `jellyfish_necklace` | `regeneration`, `shock` |
| `kinetic_belt` | `gliding`, `slots` |
| `leafy_mantle` | `camouflage`, `revival` |
| `midnight_mantle` | `constellation`, `invisibility`, `phase`, `starfall` |
| `piglin_mask` | `barter`, `looting`, `neutrality` |
| `reflective_necklace` | `reflection` |
| `rider_flute` | `stable` |
| `ring_of_the_seven_deadly_sins` | `envy`, `gluttony`, `greed`, `lust`, `pride`, `sloth`, `wrath` |
| `roller_skate` | `skating` |
| `shield_of_retaliation` | `retaliation` |
| `sphere_of_self_sacrifice` | `sacrifice` |
| `springy_boot` | `bounce` |

Base ability cardinality: **39**.

## Exact synergy inventory and deduplication

The same exact artifact exposes two owner-scoped synergy roots:

1. `glitchy_mantle|electricity`;
2. `kinetic_belt|electricity`.

They are not collapsed merely because the local id is the same:

- each root is scoped to a different relic owner;
- both owner classes reference the provider `SynergyTemplate`/condition surface;
- their owner classes and synergy-relevant token sets are structurally different;
- exact title/disabled-description/enabled-description value hashes differ between the two roots.

Therefore they are two distinct provider-native synergy identities, not one duplicated localization alias.

Synergy cardinality: **2**.

## Semantic accounting

Relics uses a provider-native ability/synergy power model rather than a spell registry. Under the canonical semantic-magic metric, these are discrete provider-owned supernatural powers.

Counted identities:

- base abilities: **39**;
- distinct synergies: **2**;
- rank modifiers: **0 additional identities**;
- modes such as enabled/disabled or lunar phase selection: **0 additional identities**;
- item/relic identities themselves: **0 additional identities**.

Strict semantic delta contributed by Relics:

**+41 `COUNTED_EXACT`**

This provider-specific checkpoint does not edit the shared global total; shared-ledger reconciliation is separate.

## Authority boundary

Relics owns:

- relic definitions;
- base ability and synergy identities/state;
- ranks/levels and provider XP;
- target configuration;
- cooldown/buffer/state;
- provider loot/generation;
- provider progression.

Curios owns accessory slot/equip plumbing.

FTB Teams supplies team context when integrated.

Reliquified addons own their addon relic definitions while consuming the Relics framework; addon identities remain cataloged under their own provider dossiers.

Black Arcana must not duplicate Relics ability/synergy state, cooldown, XP, targeting or resource settlement.

RPG Skill Tree remains progression/Mastery/perk/gate authority only for Black Arcana contracts. It does not replace Relics' runtime.

## Runtime QA remains fail-closed

Catalog closure does not prove:

- deployed ability/stat/target config;
- Curios equip/unequip exactly-once behavior;
- XP/rank persistence;
- cooldown/buffer persistence;
- FTB Teams targeting;
- Sophisticated Backpacks interaction;
- Reliquified addon coexistence;
- death/relog/restart/dimension lifecycle;
- server/full-pack performance;
- any Black Arcana adapter.

Known upstream issue reports remain regression risks, not reproduced local failures.

## Result

**✅ Cataloged.**

Exact physical/publisher 0.12.8 equality is closed, the exact artifact contains 20 base relics, 39 base ability identities and 2 distinct synergy identities, and the current provider contributes **+41 `COUNTED_EXACT`** semantic powers.

Runtime/config/integration QA remains separate and fail-closed.
