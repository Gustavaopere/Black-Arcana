# Provider Audit Queue — Phase 2J delta

Data: `2026-09-07`

This file is a narrow status overlay over `PROVIDER-AUDIT-QUEUE.md`. It prevails only for the rows named below until the next integral regeneration of the 103-provider queue. It does not supersede `PROVIDER-AUDIT-QUEUE-DELTA-GOETY-ADDONS.md` for Goety Cataclysm/Goety Iron.

## Current rows

| Mod ID | Installed identity | Current effective audit state |
|---|---|---|
| `malum` | `malum-1.21.1-1.8.2.jar` / `1.8.2` | `EXACT VERSION-LINE METADATA + PUBLISHER CHANGELOG AUDITED / SPIRIT RITE ARCHITECTURE + INSTALLED-LINE GEAS NAMES + SPIRIT RESOURCE MODEL ADVANCED / SOURCE-INTERNAL CATALOG BLOCKED BY LGPLv3↔ARR PROVENANCE CONFLICT / COMPLETE REGISTRIES+RUNTIME QA PENDING / FAIL-CLOSED` |
| `hexalia` | `hexalia-neoforge-1.3.6.jar` / runtime metadata `1.3.5` | `PUBLIC RELEASE+SOURCE PIN 1.3.6 / MIT / BREWS 8/8 / NATURE'S RITUAL 19/19 PLAYER-FACING / CELESTIAL INFUSION 6/6 / MUTATION 21/21 / MORTAR 12/12 / CENSER 10/10 / IDOLS+MAJOR CAPABILITY OUTPUTS AUDITED / INSTALLED FILENAME↔RUNTIME VERSION MISMATCH + API/RUNTIME QA PENDING` |
| `toxony` | `toxony-0.10.7.jar` / runtime `0.10.7` | `EXACT INSTALLED ARTIFACT + EXACT PUBLIC 0.10.7 SOURCE VERSION PIN 881bf7fe / EFFECTS 5/5 / OILS 9/9 / MUTAGEN EFFECTS 7/7 / AFFINITIES 11/11 / THRESHOLD MODEL + IRON'S/VAMPIRISM/WEREWOLVES COMPAT FACTUALLY AUDITED / GPLv3↔LGPLv3 LICENSE CONFLICT / RUNTIME+SUPPORTED-API QA PENDING / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED` |
| `mobstein` | `mobstein-5.4.4-neoforge-1.21.1.jar` / runtime `5.4.4` | `EXACT INSTALLED ARTIFACT + EXACT CURSEFORGE RELEASE 8040734 / PUBLISHER GUIDE AUDITED / RESURRECTED FORMS 10/10 / SURGERY TYPES 6/6 / FAILED EXPERIMENTS 7/7 / BODIES+ORGANS+SYRINGES+STRUCTURES+WITHERSTEIN SEMANTICS ADVANCED / 5.4.4 SABLE-COMPAT CLAIM RECORDED / ARR / NO OFFICIAL SOURCE/API PIN LOCATED / REGISTRY+RUNTIME QA PENDING / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED` |
| `monstersspellbooks` | `monstersspellbooks-0.0.16.3.jar` / runtime `0.0.16.3` | `EXACT INSTALLED ARTIFACT + EXACT CURSEFORGE FILE 8788560 / PUBLISHER PROJECT+CHANGELOG AUDITED / NECRO CURRENT PRIMARY SCHOOL / 90+ SPELL CLAIM + GEAR+MOBS+STRUCTURES COVERAGE / AERO SOFT-DELETED 0.0.16.2 + REMNANTS REMOVED 0.0.16.3 / LINKED SOURCE MAIN STILL 0.0.14 + ARR WHILE CURSEFORGE DISPLAYS MIT / EXACT CURRENT REGISTRY+API+ACQUISITION INCOMPLETE / PROVIDER-SPECIFIC IMPLEMENTATION FAIL-CLOSED` |
| `morerelics` | `morerelics-1.7.7-1.21.1.jar` / runtime `1.7.7` | `EXACT INSTALLED ARTIFACT + EXACT CURSEFORGE FILE 8685815 + MODRINTH 1.7.7 / ARR / 29 PUBLISHER-LISTED RELIC NAMES+LOOT ROUTES / EVOLUTION CHAINS MAPPED / CURRENT PACK RELICS 0.12.8 EXPLICITLY UNSUPPORTED BY ADDON PUBLISHER / 0.12.8 SUPPORT DESCRIBED AS FUTURE MINI-BETA / CURATORIAL MANTER PRESERVED AS RISK ACCEPTED / PROVIDER-SPECIFIC RUNTIME+PROGRESSION INTEGRATION FAIL-CLOSED` |

## Malum interpretation

The full queue still describes Malum as a generic base provider with catalog pending. That is stale relative to merged Phase 2I work.

The strongest safe current claim remains limited by provenance:

- installed 1.8.2 identity is known;
- publisher-authored 1.8/1.8.2 changelog evidence establishes the Deferred Registry transition, Rite Locus/Anchors architecture and named Geas/Pact/Oath/Authority surface;
- exact source-internal registry/algorithm promotion remains blocked because upstream licensing evidence conflicts;
- runtime QA remains separate.

Malum is therefore **advanced but not granular-complete**.

## Hexalia interpretation

The full queue row `GUIA+WEB LIDOS / RITUAIS-BREWS CATÁLOGO PENDENTE` is stale.

Merged Phase 2I work source-pinned the public 1.3.6 release and closed the major finite semantic inventories listed above. The remaining blocker is not “catalog absent”; it is exact installed-runtime/API validation because the physical filename says 1.3.6 while installed runtime metadata reports 1.3.5, plus the provider-specific behavior QA already recorded in the Hexalia catalog.

## Toxony interpretation

Phase 2J pins the exact public source version checkpoint:

`MrFrostyDev/Toxony_Mod@881bf7fe632659e748c279966a2bf49b99f7503f`

Factual source coverage now proves:

- 5 harmful effects;
- 9 Oils;
- 7 Mutagen effect IDs;
- 11 Affinities;
- player Tolerance `10..999`, default `30`;
- practical threshold crossings `tox > 100`, `>300`, `>600`;
- max three stored Mutagen entries with duplicate stacking behavior;
- six player Affinity-selected Mutagen candidates plus separate `mob_mutagen` transformation;
- five Iron's School Spell Power mappings at stage 1+;
- source-observed silver compatibility against Vampirism/Werewolves tags;
- source-visible ChangeTox/ChangeTolerance/ChangeThreshold events as candidate, not approved, adapter seams.

A material catalog correction is recorded: exact 0.10.7 executable source uses a **200-tick (10-second)** Necrotic resurrection cooldown; `48000` is commented and must not be presented as active runtime behavior.

### Provenance blocker

At the same exact Toxony commit:

- `gradle.properties` and public distribution metadata declare LGPLv3;
- root `LICENSE` contains GPLv3 text.

Therefore source observations are factual catalog evidence only. Black Arcana does not derive implementation from those internals while the conflict remains unresolved.

## Mobstein interpretation

The full queue row `GUIA LIDO / CATÁLOGO GRANULAR PENDENTE` is now stale for semantic coverage.

Phase 2J re-read the exact physical identity from the current 612-entry modlist and pinned the matching official CurseForge release:

- `mobstein-5.4.4-neoforge-1.21.1.jar`;
- mod id `mobstein`;
- runtime `5.4.4`;
- local SHA-1 `3672d88f940ddd474a5429d7066b099cd0ce0c29`;
- CurseForge project `1193873`;
- exact file `8040734`, uploaded 2026-05-04.

Publisher documentation is sufficient to close the major player-facing semantic families:

- ten resurrected creature forms;
- Clinical Stretch night-time resurrection plus Lightningbolt Syringe daytime route;
- full-body/body-part/organ processing;
- six Surgery Stretch constructed types;
- Mobstein-owned Health/Attack/Speed/Template construction perks, including the published numeric ranges;
- Subject Assembly Machine mannequin flow;
- seven failed-experiment variants;
- Dr. Mobstenio/Igor progression;
- five syringe families;
- Frankenstein Castle, Witherstein Ruins and Old Ruins;
- Witherstein's Reviver-triggered three-stage encounter;
- explicit Reviver exclusions for Resurrected Warden and Frankenstein.

The exact 5.4.4 release note also says Mobstein is compatible with Sable Mod. The current pack uses Sable 2.0.5, but the Mobstein release does not publish a Sable-version contract, so exact current-stack compatibility remains runtime QA.

### Provenance/API blocker

The publisher project is **All Rights Reserved**. No official public source repository or exact source pin was located during this checkpoint, and the installed JAR was not decompiled.

Therefore:

- public gameplay/release semantics are catalog authority;
- registry IDs, private internals and exact formulas remain unverified unless publisher-documented;
- no Mobstein-specific adapter is approved;
- integration remains fail-closed until a supported public boundary and exact-pack runtime behavior are proven.

## Monsters & Spellbooks interpretation

The full queue row `GUIA LIDO / CATÁLOGO GRANULAR PENDENTE` is now stale for provider-level semantic coverage, but **not** for exact spell-registry completion.

Phase 2J revalidated the physical/current release identity:

- `monstersspellbooks-0.0.16.3.jar`;
- mod id `monstersspellbooks`;
- runtime `0.0.16.3`;
- local SHA-1 `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`;
- CurseForge project `1428928`;
- exact file `8788560`, uploaded 2026-09-01.

Publisher evidence establishes substantial current provider coverage:

- `90+` spells;
- `12+` armor sets;
- `30+` weapons;
- `5+` ores;
- `10+` accessories + a new accessory slot;
- `10+` spellcasting mobs;
- `2+` overworld structures;
- Necro as the main current school, focused on debuffs, damage over time and curses;
- Arch single-school and Hybrid paired-school gear progression;
- current-line Iron's Gems 'n Jewelry compatibility.

Exact-release drift also corrects stale Aero assumptions:

- 0.0.16.2 explicitly soft-deletes Aero and points users to SnackPirate's Aeromancy;
- 0.0.16.3 removes remaining Aero files/content to avoid tag interference.

Therefore Monsters & Spellbooks Aero is treated as **legacy/soft-deleted**, not active exact-current school authority without runtime proof.

### Source/license blocker

CurseForge links `RedReaper28/Monsters-Spellbooks-1.21.1`, but the repository's only inspected branch/head still declares:

- `mod_version=0.0.14`;
- `mod_license=All Rights Reserved`;
- Iron's baseline `1.21.1-3.15.4`.

The current CurseForge project displays MIT and the installed release is 0.0.16.3. The repository's `TEMPLATE_LICENSE.txt` applies MIT only to NeoForged MDK template files and does not resolve provider licensing.

Consequently:

- do not derive the exact 0.0.16.3 registry/API from the stale source tree;
- exact current spell membership, IDs, numbers and acquisition remain incomplete unless publisher/runtime evidence closes them;
- provider-specific implementation remains fail-closed;
- publisher changelogs are retained as semantic/historical evidence only, with later removals/reworks taking precedence.

## More Relics interpretation

The full queue already flagged More Relics as high-risk because of the installed Relics 0.12 line. Phase 2J now converts that generic warning into exact provider evidence.

Installed/current artifact:

- `morerelics-1.7.7-1.21.1.jar`;
- mod id `morerelics`;
- runtime `1.7.7`;
- local SHA-1 `ba0c920bc7712d1ff85012327b26e1a808c648f6`;
- CurseForge project `1269280`;
- exact file `8685815`, uploaded 2026-08-19;
- project license ARR.

Current publisher documentation lists 29 named relic entries/loot routes and at least four evolution chains, while describing the addon as containing `25+` relics. Recent changelogs also establish active provider behaviors for Moodworm, Twin Fangs, Eject Button, Bionic Eye, Mass Gauntlet, Made in Heaven and status-indicator UI.

### Exact current-host blocker

Current pack:

- More Relics `1.7.7`;
- Relics `0.12.8`;
- Relics 0.12.8 is an official **Beta** release.

More Relics' current NeoForge notice explicitly states that Relics `0.11` and `0.12` are **not yet supported** and instructs 1.21.1 users to use Relics `0.10.7.8` instead.

The exact More Relics 1.7.7 changelog still describes 0.12.8 support as a possible **future mini-beta**, potentially incomplete and bug-fix-only.

Therefore the exact current pair is:

`INSTALLED / CURATORIALLY MANTER / EXPLICITLY UNSUPPORTED UPSTREAM`

This does not prove a crash. It does block any claim that More Relics-specific Black Arcana/RPG integration is supported or safe.

### Additional migration blocker

More Relics 1.7.0 documents a Made in Heaven stale extended-config path that can crash with `data is null` after upgrading from older provider versions. Persistent pack instances must be checked for the actual Relics extended-config setting and stale provider config before release validation.

No official exact public source repository was located and no JAR decompilation is used. Provider-specific integration remains fail-closed.

## Phase 3 consequence

None of these rows becomes an automatic Phase 3 implementation approval.

- Malum: provenance/API/runtime gates remain.
- Hexalia: installed-runtime/API gates remain.
- Toxony: license/API/runtime gates remain.
- Mobstein: ARR/no-source/API/runtime gates remain.
- Monsters & Spellbooks: exact-current source/license/registry/API/acquisition/runtime gates remain.
- More Relics: upstream-declared Relics 0.12.8 incompatibility/support gap + runtime/API/provenance gates remain.

Provider-native authority and fail-closed integration remain mandatory.

## Next provider checkpoint

After More Relics, the next adjacent unresolved provider in the canonical queue is **Not Enough Glyphs `4.6.1`** (`not_enough_glyphs-1.21.1-4.6.1.jar`).

Before advancing it, revalidate the exact installed artifact, Ars Nouveau host version, public release/source/provenance and its finite glyph/contingency/SpellBinder surface. Do not infer current glyph IDs or Ars API compatibility from older addon versions.