# Monsters & Spellbooks 0.0.16.3 — integration rules

## Status

`IRON'S ADDON AUTHORITY MAPPED / EXACT CURRENT REGISTRY+API NOT PINNED / PROVIDER-SPECIFIC BLACK ARCANA INTEGRATION FAIL-CLOSED`

## 1. Casting authority

Monsters & Spellbooks is an Iron's Spells 'n Spellbooks addon. The addon owns its content; Iron's owns the host casting framework.

Black Arcana must preserve:

- Iron's mana/resource settlement for Iron's-hosted casts;
- provider spell level/rarity/cooldown/cast-time behavior;
- provider acquisition/lootability restrictions;
- provider damage/effect/summon settlement;
- provider school identity and spell-power scaling;
- provider gear/rune/Curio semantics.

Black Arcana must not add a second cast transaction around a normal Monsters & Spellbooks spell. If Black Arcana observes such a cast for progression/hazard purposes, observation must settle exactly once and must not reapply the provider spell.

## 2. Necro school ownership

Current publisher documentation makes **Necro** the primary school identity of Monsters & Spellbooks, with emphasis on curses, debuffs and damage over time.

Therefore generic concepts such as:

- “necrotic curse projectile”;
- “wither bomb”;
- “summon death knight”;
- “soul wizard summon”;
- “grave fissure”;
- “generic necro rune”;
- “necromancy school armor”

cannot be approved as novel Black Arcana content merely by renaming or changing particles.

Black Arcana Souls & Death remains its own domain where its mechanics are semantically distinct and use Black Arcana's canonical casting/ledger/hazard contracts. It must not absorb Monsters & Spellbooks' Necro school or claim ownership of Iron's spell content.

## 3. Aero/Wind correction

Do not use older Monsters & Spellbooks references as evidence of current Aero authority.

Exact publisher drift:

- 0.0.16.2: Aero School **soft deleted**, with publisher direction to use SnackPirate's Aeromancy instead;
- 0.0.16.3: remaining Aero content/files removed to prevent tag interference.

The current modpack already installs SnackPirate's Aeromancy Additions `1.2.8`.

Safe disposition:

`Monsters & Spellbooks Aero = legacy/soft-deleted; SnackPirate's Aeromancy = current Wind/Aeromancy provider unless runtime evidence proves another active ownership path.`

Do not create duplicate school tags, resistance attributes, gems or spell-power modifiers for stale Aero content.

## 4. Acquisition and unlootable spells

Historical publisher changelog 0.0.10 explicitly marked multiple spells unlootable at that checkpoint.

This demonstrates an important provider rule: registry presence does not imply normal player acquisition.

Any future RPG/Black Arcana bridge that reacts to or gates Monsters & Spellbooks spells must query a supported provider/host acquisition fact if one is needed. It must not:

- auto-grant a scroll because a spell ID exists;
- add every addon spell to generic loot;
- treat creative/debug presence as survival acquisition;
- bypass provider progression through a Black Arcana research recipe.

Where exact current acquisition is unknown, fail closed.

## 5. Summon ownership

Publisher changelogs expose summons such as Summon Death Knights, Summon Soul Wizard and Summon Poison Vine.

A summoned entity remains provider/Iron's-owned unless an explicit shared contract says otherwise.

Black Arcana must not:

- register it as a Black Arcana familiar by class/name heuristic;
- reassign owner UUID;
- duplicate summon lifetime/cap limits;
- grant Mastery per tick while it exists;
- count autonomous summon kills as player-authored progress unless the canonical progression contract explicitly attributes them and deduplicates the event.

## 6. Damage, curses and status effects

Monsters & Spellbooks owns the damage/effect application of its spells.

Black Arcana hazard/Arcane Danger processing may only run when the canonical Black Arcana integration contract says the provider action is eligible. It must never reapply provider damage or a second copy of provider status effects.

Particular caution is required for:

- Wither Bomb / Wither Nova;
- Fall Curse;
- Soul Chain;
- Guardian Neutralizer;
- Napalm Orb;
- Frenzy-family effects;
- Overheat;
- poison/wither/soul-fire surfaces.

Thematic similarity to Black Arcana Corruption, Strain or Backlash is not a conversion rule.

## 7. Gear, runes and jewelry

The provider owns its:

- Arch/Hybrid armor identity;
- weapon passives;
- accessories/Curio slot;
- Necro Rune;
- compatibility with Iron's Gems 'n Jewelry.

Current 0.0.16.3 fixes Necro Rune insertion into jewelry, and 0.0.16.2 claims Iron's Gems 'n Jewelry compatibility.

Black Arcana must not duplicate the same modifier in a second equipment runtime. RPG Skill Tree/itemization may consume a real modifier/equipment boundary later, but must not rewrite provider-owned item data or apply the provider bonus twice.

## 8. RPG Skill Tree boundary

Monsters & Spellbooks' Arch/Hybrid gear language and school specialization are not RPG Skill Tree classes/masteries by themselves.

A future progression bridge may award or gate progression only through real, deduplicated actions such as a verified successful cast or provider milestone. It must not grant Mastery from:

- item equipped per tick;
- passive aura uptime;
- summon existence;
- hostile mob presence;
- mere ownership of a spellbook/weapon;
- repeated UI/tooltip inspection.

## 9. Spellcasting mobs and structures

Publisher claims `10+` special-spell mobs and `2+` overworld structures. Gallery/public changelogs name examples such as Draugr content, Jungle Whisperer and structures like Draugr Camp/Herobrine Shrine in the publisher surface.

These are provider world/content authority. Black Arcana must not infer a unique progression event from simply entering their chunks.

Any progression/discovery integration requires:

- stable structure/entity identity;
- server-side causal event;
- persistent deduplication key;
- no chunk forcing/global scan.

## 10. Source/API fail-closed rule

The public repository currently does not match 0.0.16.3: its metadata says 0.0.14 and All Rights Reserved, while CurseForge displays MIT for the current project.

Therefore Black Arcana must not use the stale repository's private classes/registries as an exact-version adapter contract.

Until exact-current source/API provenance is reconciled:

- no reflection into provider internals;
- no copy/adaptation of provider implementation;
- no guessed class/method/event signatures;
- no hard-coded registry list derived from 0.0.14 and labeled 0.0.16.3;
- no API compatibility claim based only on the source link existing.

## 11. Provider-neutral observations

Black Arcana may still handle provider-neutral Minecraft/NeoForge facts where no Monsters & Spellbooks private contract is needed.

Examples:

- a loaded entity is a living entity;
- a server-observed damage event occurred;
- an Iron's supported API reports an addon spell cast, if the exact host API contract used by Black Arcana already proves that fact.

Provider-neutral observation does not transfer authority over the addon.

## 12. Approval gate for provider-specific work

Before adding a Monsters & Spellbooks-specific adapter, require:

1. exact installed 0.0.16.3 identity confirmed (already true in modlist);
2. exact supported current API/source evidence;
3. license/provenance reconciliation;
4. exact current school/spell registry validation;
5. Iron's 3.16.3 runtime validation;
6. Iron's Gems 'n Jewelry 2.0.2 compatibility validation if consumed;
7. dedicated-server tests;
8. exactly-once cast/progression/hazard tests;
9. no duplicate cooldown/mana/damage/effect settlement;
10. acquisition/lootability preservation.

Until then: `FAIL-CLOSED`.