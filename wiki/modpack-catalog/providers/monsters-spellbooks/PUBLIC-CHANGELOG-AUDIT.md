# Monsters & Spellbooks — publisher changelog audit

## Purpose

This file records **publisher-visible names and changes** that can be established without treating the stale public source tree as the exact installed 0.0.16.3 implementation.

Important limitation:

- the current CurseForge page claims `90+` spells;
- the exact current source registry is not pinned;
- release changelogs name only a subset;
- a spell named by an older changelog is not automatically asserted to remain registered/obtainable in 0.0.16.3;
- removals, reworks and acquisition restrictions take precedence when a later publisher changelog says so.

This is therefore a **public-name lower-bound / drift audit**, not a complete exact registry.

## Exact installed release — 0.0.16.3

File: `monstersspellbooks-0.0.16.3.jar` / CurseForge File ID `8788560` / 2026-09-01.

Publisher changes:

- deleted remaining Aero content from files to prevent tags from interfering;
- increased **Fall Curse** slowness level;
- reduced the previous **Wither Bombs** nerf;
- changed more **Necro** visuals;
- fixed **Necro Rune** jewelry insertion;
- fixed an attribute operation;
- fixed some effects not being removed correctly.

Current-line named magic surfaces explicitly touched here:

- Fall Curse;
- Wither Bomb(s);
- Necro Rune.

No exact numeric slowness/damage/cooldown is published by this release note.

## 0.0.16.2 — current-line semantic correction

File: `monstersspellbooks-0.0.16.2.jar` / CurseForge File ID `8750871` / 2026-08-28.

High-value publisher changes:

- added **Iron's Gems 'n Jewelry compatibility**;
- `Soft Deleted Aero School, download Snackpirates Aeromancy instead`;
- **Summon Death Knights** now scales HP and Attack from spell power;
- reduced **Sanguinite Evisceration** cooldown;
- reduced **Cauterizing Touch** cooldown;
- buffed **Soul Boost** Necro buff;
- nerfed **Overheat**;
- nerfed **Napalm Orb** fire weakness;
- nerfed **Wither Bombs** damage;
- fixed **Soul Chain** debuff application;
- changed Soul Fire particles to the Iron's visual;
- adjusted Elite Draugr and Soul Wraith behavior/spawning.

Named magic surfaces from this release:

- Summon Death Knights;
- Sanguinite Evisceration;
- Cauterizing Touch;
- Soul Boost;
- Overheat;
- Napalm Orb;
- Wither Bombs;
- Soul Chain.

### Aero decision

This release is the strongest publisher evidence that Monsters & Spellbooks should no longer be treated as the canonical active Aero provider. The exact 0.0.16.3 release then removes remaining Aero files/content used by tags.

## 0.0.16.1

File: `monstersspellbooks-0.0.16.1.jar` / CurseForge File ID `8629788` / 2026-08-12.

Publisher changes name:

- **Withered Totem** — Curio increasing the amount of casts of Wither Bomb;
- **Guardian Neutralizer** — reworked to a long-cast single-blast spell;
- **Spectral Blast** — reworked;
- **Vile Slash** — gained a special on-hit effect;
- **Wrath** — nerfed;
- Poison Glaives and Frost Fang weapon passives changed server-side;
- several imbuable spells converted to preset-imbued forms;
- attribute-related effects corrected.

This confirms the current line is not only a spell list: gear/Curios/weapon passives and casting behavior are part of provider authority.

## 0.0.16

File: `monstersspellbooks-0.0.16.jar` / CurseForge File ID `8621268` / 2026-08-11.

Publisher changes include:

- buff-spell rebalancing;
- **Overheat** and **Frost Coating** visuals;
- Deathsilver weapon passive;
- Sanguinite weapon passive;
- Frost Coating application fix.

`Frost Coating` is recorded as a named magical surface; this changelog alone does not prove whether the exact 0.0.16.3 registry classifies it as a spell, effect or another provider construct.

## 0.0.10 — named additions and acquisition restrictions

Publisher changelog for 0.0.10 explicitly added:

- **Summon Soul Wizard**;
- **Poison Quill**;
- **Summon Poison Vine**.

The same release marked the following spells **unlootable** at that checkpoint:

- Fall Curse;
- Wither Nova;
- Raigo;
- Brimstone Buzzsaw;
- Brimstone Wrath;
- Frenzied Burst;
- Frenzied Storm;
- Frenzy Surge;
- Overheat;
- Hysteria;
- Air Propulsion.

It also added **Jungle Whisperer**, described as a hostile spellcasting mob spawning in the jungle.

### Acquisition consequence

A spell being registered is not evidence that ordinary Iron's loot/acquisition should expose it. Any future Black Arcana/RPG integration must preserve provider acquisition restrictions rather than granting scrolls/mastery access from registry presence alone.

## 0.0.9 — named spell additions

Publisher changelog explicitly added:

- Wither Nova;
- Paladin Throw;
- Rancor Call;
- Bone Dagger;
- Graveyard Fissure;
- Raigo;
- Thunder Step;
- Brimstone Wrath.

It also references/reworks:

- Static;
- Lichdom;
- Stray Grasp;
- Soul Chain;
- Putresence Mass;
- Frenzy Surge;
- Banshee Scream;
- Thunderstorm Wave;
- Guardian Neutralizer.

These names establish historical provider overlap, not guaranteed exact 0.0.16.3 registration.

## 0.0.7 — named spell evidence

Publisher changelog explicitly added:

- **Static Cleave**.

It also states that **Frenzy Burst** and future “frenzy flame” spells scale with both Fire and Eldritch power at that release checkpoint.

This is historical evidence of cross-school scaling behavior. It is not safe to assume the same exact formula in 0.0.16.3 without current runtime/API evidence.

## 0.0.4 — named spell evidence

Publisher changelog explicitly added:

- **Space Distortion**.

It also references:

- Ice Coating;
- Charge;
- Overheat;
- Tundra Terrain.

Again, exact current membership/formulas are not promoted from this older checkpoint.

## Current provider-level claims that remain stronger than the incomplete name list

The current publisher project page states:

- `90+` spells;
- `12+` armor sets;
- `30+` weapons;
- `5+` ores;
- `10+` accessories + a new accessory slot;
- `10+` special-spell mobs;
- `2+` overworld structures.

Those cardinalities prove large provider coverage even though exact current registry inventory remains incomplete.

## Schools

### Necro

Current publisher description explicitly identifies **Necro** as the main school, focused on:

- debuffs;
- damage over time;
- curses.

Recent 0.0.16.x changes directly touch Necro visuals, Necro Rune and Soul Boost Necro buff, reinforcing current active provider identity.

### Aero

Historical content existed and external ecosystem compatibility pages may still name Monsters & Spellbooks Aero.

However:

- 0.0.16.2 soft-deleted Aero and directs users to SnackPirate's Aeromancy;
- 0.0.16.3 deletes additional Aero remnants to avoid tag conflicts.

Therefore exact-current matrix state is:

`AERO LEGACY/SOFT-DELETED — NOT ACTIVE PROVIDER AUTHORITY WITHOUT RUNTIME PROOF`

## Named capability families exposed by publisher history

Even without complete registry closure, public evidence establishes substantial overlap in:

- curses/debuffs: Fall Curse, Soul Chain, Guardian Neutralizer and others;
- wither/necrotic offense: Wither Bombs, Wither Nova, Putresence Mass;
- summons: Summon Death Knights, Summon Soul Wizard, Summon Poison Vine;
- soul/necromancy: Soul Boost, Soul Chain, Rancor Call, Graveyard Fissure, Bone Dagger;
- infernal/fire: Overheat, Napalm Orb, Brimstone Wrath, Brimstone Buzzsaw, Frenzy family;
- lightning/storm: Raigo, Thunder Step, Thunderstorm Wave, Static Cleave;
- spatial/control: Space Distortion;
- ice/frost: Frost Coating / Ice Coating / Tundra Terrain references;
- long-cast blast/control: Guardian Neutralizer;
- gear-coupled magic: Curios, runes, weapon passives, Arch/Hybrid armor.

## Confidence rules

Use these labels when consuming this file:

- `EXACT 0.0.16.3 CHANGELOG` — direct statement on installed release;
- `CURRENT 0.0.16.x CHANGELOG` — direct statement on immediately preceding same content line;
- `HISTORICAL PUBLISHER NAME` — direct older publisher changelog, exact current membership not proven;
- `PROJECT CARDINALITY CLAIM` — current publisher total/approximate count, not registry enumeration;
- `UNVERIFIED` — no publisher/runtime evidence sufficient for a precise claim.

Do not upgrade a historical name to exact current registry status merely because it sounds plausible or appears in a stale third-party compatibility list.