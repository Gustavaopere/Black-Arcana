# Monsters & Spellbooks 0.0.16.3 — technical/provenance audit

## Scope

This checkpoint separates three different evidence layers that currently disagree:

1. exact installed modlist identity;
2. exact current CurseForge release/project metadata;
3. linked public GitHub source repository, whose only branch is stale relative to the installed release.

No installed-JAR decompilation is used.

## 1. Installed artifact

Current physical modlist:

- JAR: `monstersspellbooks-0.0.16.3.jar`;
- mod id: `monstersspellbooks`;
- runtime name: `Monsters & Spellbooks`;
- runtime version: `0.0.16.3`;
- SHA-1: `b3aa89fd081bf4bfaf8d0f4380bcdc393c66ab0e`;
- CurseForge/package fingerprint: `3089819119`.

This is the runtime identity Black Arcana must target if a future adapter is ever approved.

## 2. Exact publisher release

CurseForge project `1428928`, file `8788560`:

- exact filename matches the installed JAR;
- version `0.0.16.3`;
- Minecraft `1.21.1`;
- NeoForge;
- release date `2026-09-01`;
- Release channel;
- publisher: RedTablos;
- project page currently displays `MIT License`;
- project page currently labels environment `Server`.

The environment label is recorded as publisher metadata only. It is not used to infer that clients never need assets/render code.

## 3. Current publisher content claims

The current project page advertises:

- `90+` spells;
- `2` new spell schools;
- `12+` armor sets;
- `30+` weapons;
- `5+` ores;
- `10+` accessories and a new slot;
- `10+` mobs with special spells;
- `2+` overworld structures.

The longer description explicitly names **Necro** as the main school and gives its semantic identity as debuffs, damage over time and curses.

These values are approximate/project-level claims, not a registry dump.

## 4. Exact-release drift

### 0.0.16.2

Publisher release says:

`Soft Deleted Aero School, download Snackpirates Aeromancy instead`

It also adds Iron's Gems 'n Jewelry compatibility and modifies multiple spells/effects/summons.

### 0.0.16.3

Publisher release says it deleted remaining Aero content from files to avoid tag interference.

### Consequence

The current project header still saying `2 new spell schools` is stale/ambiguous relative to exact current-line release notes.

Do not promote Aero as active 0.0.16.3 provider authority without runtime registry evidence.

## 5. Linked public source repository

CurseForge's Source link resolves to:

`RedReaper28/Monsters-Spellbooks-1.21.1`

Repository state inspected at head:

`1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`

The repository exposes only a `main` branch at that checkpoint.

Its `gradle.properties` declares:

- `mod_id=monstersspellbooks`;
- `mod_name=Monsters & Spellbooks`;
- `mod_version=0.0.14`;
- `mod_license=All Rights Reserved`;
- Iron's dependency baseline `1.21.1-3.15.4`.

This does **not** match the installed/public `0.0.16.3` release.

## 6. License discrepancy

Evidence conflicts:

- current CurseForge project page: **MIT License**;
- linked repository `gradle.properties`: **All Rights Reserved**;
- repository root has no provider LICENSE file at the inspected head;
- `TEMPLATE_LICENSE.txt` is MIT text explicitly limited to NeoForged MDK template files and is not a license grant for Monsters & Spellbooks provider code/assets.

Therefore:

`SOURCE-DERIVED IMPLEMENTATION = REVIEW_REQUIRED / BLOCKED`

until the publisher exposes/reconciles exact 0.0.16.3 source and license terms.

Read-only inspection in this audit was limited to repository metadata/provenance files needed to establish the mismatch. No provider implementation internals are promoted into Black Arcana specifications.

## 7. Dependency surface

Current CurseForge Relations records:

Required:

- Iron's Spells 'n Spellbooks;
- Ace's Spell Utils;
- AzureLib.

Optional:

- AttributeFix;
- Better Combat.

Current pack identities observed in the physical modlist:

- Iron's Spells `1.21.1-3.16.3`;
- Ace's Spell Utils `1.2.7.2-1.21.1`;
- AzureLib `3.1.11`;
- AttributeFix `21.1.3`.

No Better Combat entry was matched in the current modlist grep used for this audit; that absence should be reconfirmed by the full modlist audit if a Better Combat-specific path becomes relevant.

Current source metadata's Iron's `3.15.4` pin is historical/stale relative both to exact 0.0.16.3 and the pack's Iron's `3.16.3`, so it cannot establish current API compatibility.

## 8. Iron's Gems 'n Jewelry compatibility

0.0.16.2 publisher changelog says compatibility was added.

Current pack contains:

- `irons_jewelry-1.21.1-2.0.2.jar`;
- runtime `1.21.1-2.0.2`.

0.0.16.3 additionally fixes Necro Rune insertion into jewelry.

This is strong public evidence that a current-line bridge exists semantically. Exact registry/data/attribute behavior remains runtime/API QA pending because the exact source is not pinned.

## 9. Current named spell evidence

Publisher changelogs directly name current-line or historical spells, including:

- Fall Curse;
- Wither Bomb(s);
- Summon Death Knights;
- Sanguinite Evisceration;
- Cauterizing Touch;
- Soul Boost;
- Overheat;
- Napalm Orb;
- Soul Chain;
- Guardian Neutralizer;
- Spectral Blast;
- Vile Slash;
- Wrath;
- Summon Soul Wizard;
- Poison Quill;
- Summon Poison Vine;
- Wither Nova;
- Paladin Throw;
- Rancor Call;
- Bone Dagger;
- Graveyard Fissure;
- Raigo;
- Thunder Step;
- Brimstone Wrath;
- Static Cleave;
- Space Distortion.

Additional names/references are retained in `PUBLIC-CHANGELOG-AUDIT.md`.

These do not equal a complete current registry.

## 10. Static QA risks

### 10.1 Stale school count

Project card says two schools while current-line changelogs remove Aero. Runtime registry must decide the exact current state.

### 10.2 Public source version mismatch

Using the repository to generate current spell IDs/formulas would silently catalog 0.0.14 as 0.0.16.3. Forbidden.

### 10.3 License metadata mismatch

CurseForge MIT vs source ARR prevents treating repository code as safely reusable exact provider source even if the version were later reconciled without an explicit license answer.

### 10.4 Acquisition drift

0.0.10 explicitly made a set of spells unlootable. Later release notes do not provide a full current acquisition table. Registry presence is insufficient for progression/loot decisions.

### 10.5 Frequent reworks

Publisher states active development and recent 0.0.16.x changelogs repeatedly rework/nerf spells, passives, effects and visuals. Old formulas are especially unsafe to copy forward.

### 10.6 School/compat tags

0.0.16.3 specifically removes Aero remnants to prevent tag interference. Cross-mod integrations that still enumerate Monsters & Spellbooks Aero can be stale and must not override current provider evidence.

## 11. Runtime QA required

| Area | Required evidence |
|---|---|
| Load | exact 0.0.16.3 + pack Iron's 3.16.3 on client and dedicated server |
| School registry | exact active custom schools; verify Aero absence/legacy state |
| Spell registry | current exact spell IDs, school, levels/rarities and acquisition |
| Costs | mana/cooldown/cast-time settlement through Iron's only |
| Summons | owner/lifetime/cap/kill-attribution behavior |
| Effects | no stale effects after expiry/death/dimension changes |
| Gear | Arch/Hybrid stats, weapon passives, accessory slot behavior |
| Jewelry | 0.0.16.x compatibility with Iron's Gems 'n Jewelry 2.0.2, including Necro Rune |
| Loot | current unlootable/lootable status; no provider bypass |
| Mobs | hostile spellcaster behavior, server AI and drops |
| Structures | current structure identities/worldgen and discovery dedup |
| Black Arcana | no duplicate damage/effect/cooldown/mana/hazard settlement |
| RPG | exactly-once cast/mastery event if a future bridge is approved |

## 12. Current disposition

Allowed now:

- semantic deduplication;
- publisher-changelog catalog;
- exact artifact/release identity;
- authority boundaries;
- QA planning.

Not allowed now:

- exact 0.0.16.3 source-derived registry claims;
- source-derived integration implementation;
- treating Aero as active based on stale descriptions/compat lists;
- duplicating Iron's casting or provider effects;
- claiming current API compatibility from the 0.0.14 source tree.

Disposition: `CATALOG ADVANCED / EXACT REGISTRY+SOURCE+LICENSE RECONCILIATION PENDING / FAIL-CLOSED`.