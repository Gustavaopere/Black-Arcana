# More Relics — 1.7.7-forRelics-0.12.8-1.0

Status: `⚠️ PARTIAL / CURRENT SIBLING PHYSICAL 1.7.7-forRelics-0.12.8-1.0 / OFFICIAL FILE 8859015 / 29 PUBLISHED RELIC NAMES / EXACT ABILITY ROOTS + REGISTRY IDS UNVERIFIED / +0 STRICT UNTIL JAR AUDIT`

## Current physical authority

The newest authority available to this catalog is the current sibling dossier `neoforge-rpg-skilltree@a0bf15c16f7e22eb42c4665bbe7a9dace8b8fda8`, revalidated on 2026-09-25 against its newer physical modlist.

It records:

- JAR: `morerelics-1.7.7-forRelics-0.12.8-1.0-1.21.1.jar`;
- mod id: `morerelics`;
- runtime: `1.7.7-forRelics-0.12.8-1.0`;
- Minecraft / loader: 1.21.1 / NeoForge;
- SHA-1: `bc220ed291187c97bd1896f1fdd29b2377879ae1`;
- current base Relics: `0.12.8`.

The Project Library `modlist(1).txt` accessible in this chat is an older 2026-09-16 snapshot and does not contain this reintroduced provider. It is therefore not used to contradict the newer sibling physical authority.

## Official release boundary

Official CurseForge project: `More Relics` / project `1269280`, All Rights Reserved, Client & Server.

Current pack build:

- File ID `8859015`;
- filename `morerelics-1.7.7-forRelics-0.12.8-1.0-1.21.1.jar`;
- Beta, NeoForge 1.21.1;
- uploaded 2026-09-11;
- specifically published to support **Relics 0.12.8**.

The publisher states that this compatibility branch is content-locked to More Relics **1.7.7** and will receive bug fixes rather than automatically inheriting 1.7.8+ content.

## Provider role and authority

More Relics is an addon of the Relics framework. Authority remains split:

- **Relics** owns the base relic framework, generic progression/stat/evolution contracts and shared runtime;
- **More Relics** owns the relic identities, provider-specific effects, evolution rules and loot routes it adds;
- **Curios/Accessories-equivalent infrastructure in the installed stack** owns slot plumbing where applicable;
- Black Arcana owns none of the provider's relic settlement and must not duplicate XP/evolution/effect processing.

## Published current 1.21.1 content inventory

The official project page currently publishes **29 named relics** for the 1.21.1 content line. These are content identities, not automatically 29 semantic magic actions:

| # | Published relic | Published acquisition / evolution note |
|---:|---|---|
| 1 | Axolotl Cream | Aquatic and Tropic loot contexts |
| 2 | Crown of the Legend | Nether / Bastions |
| 3 | Eject Button | low-chance global loot |
| 4 | Guts Orb | Bastions / Deserts / Ruined Portals |
| 5 | Tyrant Mask | Bastions; evolves to King Crimson |
| 6 | King Crimson | evolution only from Tyrant Mask |
| 7 | Slumbering Amulet | Buried Treasure |
| 8 | Whispering Amulet | evolution only from Slumbering Amulet |
| 9 | Made in Heaven | evolution only from Whispering Amulet |
| 10 | Mass Gauntlet | low-chance global loot |
| 11 | Opal Necklace | Deserts / Snow-Ice biomes |
| 12 | Sentient Rust | Mineshafts / Mountains / Swamps |
| 13 | Shieldweave Cape | Caves / Taiga / Mountains / low-chance Overworld |
| 14 | Bionic Eye | Ancient Cities / Deep Dark |
| 15 | Thermoseismic Heart | Desert |
| 16 | Biojoint | Nether / Mineshafts |
| 17 | Whims of Fate | Bastions / Desert |
| 18 | Depleted Spool | Caves / Mineshafts / Mountains |
| 19 | Weavers Spool | evolution only from Depleted Spool |
| 20 | Mood Worm | low-chance global loot |
| 21 | VertebraX | End |
| 22 | Gravitum Glove | End / Stronghold / Sculk |
| 23 | Epoch Apple | Dungeon chests |
| 24 | Converging Orb | Woodland Mansions |
| 25 | Wonder of U | evolution only from Converging Orb |
| 26 | Gravitum Strider | End / Sculk |
| 27 | Twin Fangs | Pillager Outposts / Mansions |
| 28 | Swiftedge | Mountains |
| 29 | Runic Plate | Mountains |

Published evolution chains explicitly include:

- `Tyrant Mask → King Crimson`;
- `Slumbering Amulet → Whispering Amulet → Made in Heaven`;
- `Depleted Spool → Weavers Spool`;
- `Converging Orb → Wonder of U`.

These transitions remain provider-owned and must not be reproduced as a second evolution ledger.

## 1.7.7 behavior notes relevant to integration

Publisher documentation for the 1.7.7 content line identifies several current behavior/config surfaces:

- per-relic icon indicators can be disabled client-side;
- Mood Worm exposes current status visually and common-config mood duration;
- Twin Fangs received a fix for a condition that could cause infinite hits;
- Eject Button health threshold is common-configurable;
- Bionic Eye Vulnerability levels are common-configurable;
- Cyberpsychosis has a visual path that can render Iron Golems as Wardens.

These facts establish real runtime/config surfaces but do not enumerate exact ability-template IDs or registry ownership for the installed 8859015 JAR.

## Semantic disposition

The Black Arcana semantic metric counts discrete provider-owned supernatural actions/abilities, not relic item containers, passive stats, equipment identity, evolution stages or loot entries.

Current evidence is insufficient to determine how many of the 29 published relics expose:

- active ability roots;
- passive/proc-only effects;
- multiple abilities per relic;
- evolution-only replacement abilities;
- provider-specific IDs versus generic Relics framework ability IDs.

Therefore:

- published relic identities: **29**;
- exact provider registry IDs: **UNVERIFIED**;
- exact discrete ability roots: **UNVERIFIED**;
- strict semantic contribution from More Relics at this checkpoint: **+0 pending closure**;
- provider state: **⚠️ partial / conditioned**.

This `+0` is a fail-closed accounting choice, not a claim that More Relics has no magical abilities.

## Why the provider cannot be promoted yet

The exact installed JAR is not currently available to the Black Arcana inspection runtime, and no public source repository for the installed build was established. CurseForge lists the project as All Rights Reserved.

Without the exact JAR or equivalent authoritative registry/ability dump, Black Arcana will not infer:

- registry IDs from display names;
- one ability per relic;
- active/passive classification from marketing text;
- exact config keys/defaults;
- internal Relics `AbilityTemplate` roots;
- survival availability beyond the published acquisition routes.

See [`JAR-CLOSURE-CHECKLIST.md`](JAR-CLOSURE-CHECKLIST.md).

## Runtime QA remains separate

Even after semantic inventory closure, assembled checks remain required for:

- save migration / data-corruption warning around historical Relics 0.10.7.8 → 0.12.8 worlds;
- equip/unequip, death/respawn, dimension change, logout/login and restart persistence;
- relic evolution preserving provider state exactly once;
- Twin Fangs combat reentrancy / infinite-hit regression;
- Eject Button and Bionic Eye effective common config;
- loot injection in the final modpack datapack stack;
- no client-prediction double settlement;
- no duplicate XP/evolution/loot grants.

## Result

**⚠️ Partial / conditioned.**

Physical/provider identity and 29 published relic names are cataloged. Exact ability roots and registry IDs remain blocked on the exact 8859015 artifact or equivalent authoritative runtime evidence. Strict semantic delta remains **+0 pending closure**.
