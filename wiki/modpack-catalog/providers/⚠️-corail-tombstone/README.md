# Corail Tombstone — 9.5.6

Status: `PARTIAL / PUBLISHER-BOUNDED MAGIC SURFACE / EXACT 9.5.6 PUBLISHER FILE / SEMANTIC CARDINALITY PENDING / RUNTIME QA FAIL-CLOSED`

## Current physical identity

Current sibling authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Magic + Mobs + Utility & QoL/✅-corail-tombstone v9.5.6.md`

Physical identity preserved there:

- JAR: `tombstone-neoforge-1.21.1-9.5.6.jar`;
- mod id: `tombstone`;
- runtime: `9.5.6`;
- Minecraft 1.21.1 / NeoForge / Java 21.

The sibling dossier does not preserve an independent installed-JAR digest for this row. Installed-byte equality with the publisher artifact is therefore not claimed.

## Exact publisher release

CurseForge project: `243707`.

Exact NeoForge 1.21.1 file:

- file ID: `8842741`;
- filename: `tombstone-neoforge-1.21.1-9.5.6.jar`;
- uploaded: 2026-09-09;
- loader: NeoForge;
- supported game version: 1.21.1;
- publisher state: Release.

The exact 9.5.6 changelog fixes XP restoration on death with high level counts caused by integer overflow. The same release page preserves the relevant 1.21.1 lineage:

- 9.5.5: Create Aeronautics vehicle-respawn compatibility;
- 9.5.4: learned Ritual Flute melodies play automatically on the correct block and the old Ritual Flute screen is removed;
- 9.5.3: adds the lore sequence "The Nights of Nour";
- 9.5.2: Grave Guardian trades become data-driven and readable scrolls are adjusted;
- 9.5.0: adds Bone Scepter and spellcasting animation for tamed undeads / Grave Guardian.

Publisher file page:
`https://www.curseforge.com/minecraft/mc-mods/corail-tombstone/files/8842741`

## Publisher-confirmed magic system

The current publisher description explicitly states that Tombstone has a magic system based on enchantable items powered by Souls haunting Decorative Graves.

Confirmed public magic surfaces include:

- Souls used to enchant magic scrolls/tablets and upgrade Grave's Key;
- Forgotten Knowledge readable scrolls;
- Ritual Flute as a starting/rite-support item;
- enhanced prayers unlocked through Elyra's Diary;
- the named "Rite of Silent Bound" archive/knowledge path, associated with undead affinity under conditions;
- Ankh of Pray prayer interaction near Decorative Graves;
- Knowledge of Death progression/perks tied to Soul use, prayer and Tombstone advancements;
- provider enchantments and supernatural effects;
- Bone Scepter and tamed-undead / Grave Guardian magical presentation.

These facts establish a real provider-owned magical subsystem. They do **not** establish a complete action registry or a complete list of discrete rites/prayers/tablet actions for the exact installed release.

## Explicitly enumerated enchantments

The current publisher page enumerates 13 Tombstone enchantments:

1. Soulbound;
2. Shadow Step;
3. Magic Siphon;
4. Plague Bringer;
5. Blessing;
6. Curse of Bones;
7. Frostbite;
8. Spectral Bite;
9. Spectral Conjurer;
10. Incurable Wounds;
11. Decrepitude;
12. Sanctified;
13. Ruthless Strike.

These are gear/enchantment identities and are **not counted as semantic spell/rite actions** under the Black Arcana magic-action metric.

## Explicitly enumerated effects

The current publisher page also enumerates 24 Tombstone effects, including Ghostly Shape, Diversion, Preservation, True Sight, Bone Shield, Aquatic Life, Restoration, Giant Strength, Little World and Beyond the Grave Bond.

These are status/effect identities and are **not counted as independent spell/rite actions** unless a separate provider-owned action identity is independently established.

See `PUBLISHER-9.5.6-MAGIC-SURFACE.md` for the public evidence inventory.

## Semantic accounting

Current strict semantic contribution: **PENDING / NOT YET ADDED TO THE GLOBAL NUMERATOR**.

Reason:

- provider-owned magic is confirmed;
- at least one prayer action family and rite/forgotten-knowledge path are publicly described;
- magic scroll/tablet use exists;
- however, the public publisher material does not expose an exact 9.5.6 registry/list of all discrete prayers, rites, scroll actions or tablet actions;
- the public GitHub repository is an issues/update repository rather than the full current implementation source;
- All Rights Reserved licensing and clean-room rules prohibit filling that gap by copying implementation.

Therefore this provider remains **⚠️ partial / conditioned** rather than being falsely closed as `+0` or assigned an invented count.

## Runtime / authority boundary

Corail Tombstone remains authority for:

- grave creation/recovery;
- Grave Souls and Tombstone magic items;
- Knowledge of Death/perks;
- Forgotten Knowledge;
- provider prayers/rites;
- provider enchantments/effects;
- Tombstone death/teleport utilities.

Black Arcana must not duplicate those runtimes. RPG Skill Tree remains progression/Mastery/perk/gate authority only where a real boundary exists; Tombstone's own Knowledge of Death remains provider-owned state unless an explicit integration contract is implemented.

## Still fail-closed

- installed-JAR ↔ publisher-file byte equality;
- exact registry/resource inventory of all prayers, rites, scrolls/tablets and Forgotten Knowledge actions;
- deployed config enabling/disabling features/items/enchantments;
- exact Ankh prayer cooldown/config in the assembled pack;
- Ritual Flute learned-melody/rite reachability;
- Grave Soul consumption and exactly-once settlement;
- Knowledge of Death persistence;
- death/grave/XP restoration;
- Create Aeronautics respawn-on-vehicle;
- Curios/external inventory recovery;
- multiplayer ownership/protection;
- restart/reload/migration behavior;
- any Black Arcana adapter.

## Result

**⚠️ Partially cataloged:** exact physical/provider release is pinned and the publisher-confirmed magical surface is inventoried, but discrete semantic action cardinality remains unresolved.

No strict semantic delta is published from this checkpoint.
