# FamiliarsLib 1.7.1 — Evidence and Provenance

## Purpose

This record documents the strongest evidence available for the physically installed FamiliarsLib component without treating correlated source as an exact binary match and without copying provider implementation.

## Physical layer — authoritative for installed presence/version

Current modlist evidence:

- JAR: `familiarslib-1.21.1-1.7.1.jar`;
- mod id: `familiarslib`;
- displayed mod name: FamiliarsLib;
- runtime version: `1.21.1-1.7`;
- SHA-1: `7fa3f3116e35c12456425ae195924ced33fcc2eb`;
- CurseForge hash recorded by the physical inventory: `2425186301`;
- pack loader: NeoForge `21.1.248`;
- Minecraft: 1.21.1.

The physical JAR is the authority for what is actually installed. The filename suffix `1.7.1` and runtime version `1.21.1-1.7` are preserved as separate identities rather than normalized into one value.

## Publisher layer

CurseForge:

- project: `1316458`;
- file: `8059464`;
- exact filename: `familiarslib-1.21.1-1.7.1.jar`;
- game: Minecraft 1.21.1;
- loader: NeoForge;
- channel: release;
- uploaded: 2026-05-08;
- file changelog: familiar-bed healing bug fix.

Source page: `https://www.curseforge.com/minecraft/mc-mods/familiarslib/files/8059464`.

Modrinth provides the `1.21.1-1.7` changelog. It records the larger 1.7 framework changes and explicitly states that all Sound-school content was removed and moved to Tunes 'n Tomes. This is material to semantic spell deduplication.

Source page: `https://modrinth.com/mod/familiarslib/version/OtvYyM7e`.

## Official-source layer

Repository linked by the publisher: `Alshanex/FamiliarsLib`.

No release tag matching `1.7.1` was established. Commit history around the publisher upload date identifies:

- commit `56561e7fd474fbd5c5166c1ac96f235faae156ab`;
- timestamp: 2026-05-08T19:18:36Z;
- message: `Fixed bug with familiar beds not working`;
- tree `9d39b4751b9e52874f66cf2187afab239d00b251`;
- parent `f1e2094166c41fb9d9ed606f72ccaf4184e70d78`.

The commit date and bug-fix intent align strongly with CurseForge file 8059464. This makes it the strongest release-correlated official-source snapshot found, **not a proven exact source pin for the installed JAR**.

The recursive tree response reports `truncated=false`.

## Correlated source metadata

`gradle.properties` at the correlated commit declares:

- `minecraft_version=1.21.1`;
- `minecraft_version_range=[1.21.1]`;
- `neo_version=21.1.90`;
- `irons_spells_version=1.21.1-3.15.5`;
- `geckolib_version=1.21.1:4.7.5.1`;
- `curios_version=9.2.2`;
- `player_animator_version=2.0.1+1.21.1`;
- `mod_id=familiarslib`;
- `mod_name=FamiliarsLib`;
- `mod_version=1.21.1-1.7`;
- `mod_group_id=net.alshanex.familiarslib`;
- `mod_authors=Alshanex`.

The NeoForge/Iron's/Curios values above describe that source development snapshot. They do not replace the physical versions installed in the pack.

## Provider-owned state and transport observed in source

### Familiar persistence

`registry/AttachmentRegistry.java` registers a serializable NeoForge attachment named `player_familiar_data` backed by `PlayerFamiliarData`.

This proves FamiliarsLib owns persistent familiar-framework state. Black Arcana must not create a duplicate copy of that state merely to integrate a spell or observation mechanic.

### Familiar networking

`setup/PayloadHandler.java` uses FamiliarsLib's own `PayloadRegistrar` and registers 17 optional handlers:

Serverbound — 9:

- summon pet;
- request familiar selection;
- select familiar;
- update multi-selection Curio;
- release familiar;
- move familiar;
- set storage mode;
- update storage settings;
- quick summon.

Clientbound — 8:

- familiar data;
- familiar data sync;
- familiar storage update;
- open familiar storage;
- open familiar selection;
- familiar death;
- open multi-selection screen;
- reload familiar screen.

The exact packet class names remain provider implementation details; Black Arcana does not reuse their code or treat client packets as authority.

### Spellcasting familiar framework

The complete tree contains provider abstractions such as:

- `AbstractSpellCastingPet` and specialized flying/melee/terrestrian familiar bases;
- `AbstractFamiliarSpellbookItem`;
- `SchoolTypeAccessor`;
- familiar spellcasting behavior utilities.

These are framework/consumer surfaces around the installed magic ecosystem. Their existence does not prove FamiliarsLib owns the spells being cast.

### Iron's spell classification

The complete tree contains data under:

`data/familiarslib/tags/irons_spellbooks/spells/**`

including attack/range, buff/debuff, defense and movement classifications. These files are **tags referencing/classifying external Iron's spells**. They do not register new FamiliarsLib spell identities.

No provider-owned spell registry source or `data/familiarslib/spells/**` content was found in the complete release-correlated tree.

## Sound-school correction

Older descriptive prose for FamiliarsLib says developers can create Sound-school spells. That statement is stale for the current 1.7.x line as a description of provider-owned content.

The publisher changelog for `1.21.1-1.7` explicitly says all Sound-school content was removed and moved to Tunes 'n Tomes. Accordingly:

- historical FamiliarsLib Sound content is not counted as current FamiliarsLib semantic magic;
- Tunes 'n Tomes must be inventoried under its own provider identity;
- current FamiliarsLib spell-classification/interoperability code does not inflate the semantic spell denominator.

## Semantic magic-object disposition

For the Black Arcana catalog's user-facing semantic metric:

- independent FamiliarsLib spells: **0**;
- independent FamiliarsLib glyphs/spell-parts: **0 observed**;
- independent FamiliarsLib rituals/rites: **0 observed**;
- external Iron's spell tags: **0 new semantic objects**;
- familiar entities/items/storage/networking: excluded from the spell/magic-object count by definition.

Therefore Phase 2AX contributes **+0 numerator / +0 denominator** to the semantic spell/magic ratio.

## Black Arcana integration boundary

Black Arcana Stage 07.07 requires server-verifiable familiar ownership. The current BA noetic runtime uses its own canonical familiar-ownership registry and revalidates authorization server-side during observation.

This audit does not establish a stable exact-version public ownership query from the installed FamiliarsLib binary. Although the correlated source proves provider-owned familiar state exists, a runtime bridge requires the exact contract intended for external consumption, not direct attachment copying, generic tameable detection, reflection-by-name, or assumptions from class ancestry.

Disposition: **no Phase 2AX runtime adapter; fail closed** until the provider-native ownership seam is proven against the exact installed version.

## Exactness gaps

Not proven:

- installed JAR ↔ source commit byte/reproducible-build equality;
- a tagged source release for 1.7.1;
- exact stable public ownership API suitable for Black Arcana Stage 07.07;
- full-pack runtime compatibility of a hypothetical BA adapter;
- physical-vs-publisher binary hash equality beyond the available inventory hashes.

These gaps do not prevent cataloging the provider's role; they do prevent promoting an unverified integration contract.

## License discrepancy

The observed license surfaces conflict:

- release-correlated `gradle.properties`: `mod_license=All Rights Reserved`;
- current CurseForge project/files surface: GPLv3;
- current Modrinth project surface: MIT.

This record does not adjudicate which grant controls redistribution or derivative reuse. Under Black Arcana clean-room rules, the practical disposition is conservative: source is inspected only to establish factual interoperability/capability evidence; no provider code, assets, text, models or sounds are copied or adapted.

## Evidence URLs

- physical authority: project `modlist.txt` snapshot used by Phase 2AX;
- CurseForge exact file: `https://www.curseforge.com/minecraft/mc-mods/familiarslib/files/8059464`;
- Modrinth 1.7 changelog: `https://modrinth.com/mod/familiarslib/version/OtvYyM7e`;
- official source repository: `https://github.com/Alshanex/FamiliarsLib`;
- release-correlated source commit: `https://github.com/Alshanex/FamiliarsLib/commit/56561e7fd474fbd5c5166c1ac96f235faae156ab`.
