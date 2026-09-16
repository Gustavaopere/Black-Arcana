# GTBC's SpellLib/API 2.2.0 — provider catalog

Status: `EXACT INSTALLED ARTIFACT / PUBLISHER-BOUNDED LIBRARY SURFACE / 0 INDEPENDENT SEMANTIC MAGICS / INTERNALS FAIL-CLOSED`

## Installed authority

- Current JAR: `gtbcs_spell_lib-2.2.0-1.21.1.jar`
- Mod id: `gtbcs_spell_lib`
- Runtime version: `2.2.0-1.21.1`
- Minecraft / loader: `1.21.1` / NeoForge
- Physical SHA-1: `36cce8ab3117e89ae992a84a566d596709db2ffe`
- Physical CurseForge package fingerprint: `1996449855`
- CurseForge project ID: `1194714`
- Exact current CurseForge file ID: `8824651`
- Uploaded: `2026-09-06`
- License: `All Rights Reserved`
- Provider class: `LIBRARY / API / SHARED IRON'S-ADDON INFRASTRUCTURE`

The physical Black Arcana modlist is authority for installed identity. The exact current CurseForge file independently matches GTBC's SpellLib `2.2.0` for NeoForge / Minecraft 1.21.1.

## Publisher-defined role

The author describes this project as a common library/API for the author's Iron's Spells add-ons and explicitly states that it does not provide standalone gameplay on its own. The publisher-facing surface is developer infrastructure rather than an independent spell catalog.

The documented library surface includes, at a high level:

- spell-related attributes;
- reusable particle managers;
- helper/base classes for spell-imbuing Curios and armor;
- trade helpers;
- GeckoLib armor/magic-weapon bases;
- multi-attribute Curio helpers;
- an `AdvancedSpell` base abstraction;
- Curio lookup helpers;
- summon-check helpers.

The exact `2.2.0` changelog adds three attributes: Healing Received, Damage Taken and Summon Health.

These are capability/API surfaces. A reusable spell base class, an item capable of being imbued with external spells or a spell-related attribute does not mint a standalone provider-owned spell identity.

## Semantic magic disposition

For the Black Arcana semantic-magic metric, GTBC's SpellLib contributes:

- standalone provider-owned spells: **0**;
- provider-owned rituals/rites: **0**;
- provider-owned glyph/spell-part primitives: **0**;
- equivalent discrete supernatural player actions: **0**.

Semantic delta: **+0**.

This zero is publisher-bounded, not source-derived: the exact current project is explicitly a library/API with no standalone gameplay, and its current release notes add attributes rather than a spell inventory. Consumer add-ons remain the semantic owners of the spells they register.

## Authority / integration boundary

- Iron's Spells 'n Spellbooks remains authority for Iron's casting, spell identities, mana and school semantics used by consumers.
- GTBC's SpellLib owns its library/API abstractions and attributes where a consumer actually uses them.
- Consumer add-ons such as GTBC's Geomancy Plus own their own registered gameplay content.
- Black Arcana must not mirror GTBC attributes, register a parallel spell ledger, settle a provider cast twice or infer a provider-native hook from a helper class name.

No Black Arcana runtime adapter is authorized by this catalog closure. A future integration may use a documented, exact-version API seam only after that seam is independently verified.

## Clean-room / exactness boundary

The publisher explicitly describes the project as closed-source / All Rights Reserved and forbids extracting, reusing, redistributing or decompiling its code/assets. This audit therefore uses only:

- the physical installed identity/hash;
- public project/file metadata;
- publisher-authored public feature/API descriptions;
- publisher-authored release notes.

No JAR decompilation, copied implementation, copied assets or source-derived signatures are used. Registry internals, exact API signatures and binary implementation details remain `FAIL-CLOSED`.

## Sources

- CurseForge project: `https://www.curseforge.com/minecraft/mc-mods/gtbcs-spelllib`
- Exact NeoForge 1.21.1 release: `https://www.curseforge.com/minecraft/mc-mods/gtbcs-spelllib/files/8824651`
- Physical pack authority: current project `modlist.txt`
