# Iron's Lib 1.21.1-2.1.0 — evidence and provenance

## Physical authority

Current sibling physical evidence:

- JAR `irons_lib-1.21.1-2.1.0.jar`;
- mod id `irons_lib`;
- runtime `1.21.1-2.1.0`;
- Minecraft / loader 1.21.1 / NeoForge;
- SHA-1 `70fba64d12b6ff9553580e52101d989c89297797`.

Sibling authority checkpoint:

`neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`.

## Publisher evidence

CurseForge project:

`https://www.curseforge.com/minecraft/mc-mods/irons-lib`

Public project metadata establishes:

- author/publisher: Iron431;
- project ID `1492763`;
- role: common functionality/content for Iron's mods;
- categories: API and Library / Cosmetic;
- environment: Client & Server;
- license: All Rights Reserved.

The publisher file list records `irons_lib-1.21.1-2.1.0.jar` as a NeoForge 1.21.1 Release uploaded 2026-07-03.

## Public feature/API evidence

Publisher documentation for the pre-2.2.0 1.21.1 line, reconciled by the current sibling dossier for installed 2.1.0, establishes seven common RPG-style attributes:

- Armor Pierce;
- Mining Speed;
- Experience Gained;
- Arrow Damage;
- Crit Damage;
- Dodge Chance;
- Healing Received.

It also documents Attribute Remapper support through `AttributeRemapRegistry#register` and data-driven `irons_lib_attribute_remap` resources with `from`/`to` attribute IDs.

The project description documents transmog framework behavior, dynamic player-statue/multiblock/model infrastructure and Patreon integration services.

## Exactness limit

No official public source repository or exact 2.1.0 source revision was established. Therefore this audit does **not** claim:

- exact internal class names beyond publicly documented API names;
- exact registry IDs for every library-owned attribute or helper;
- packet/persistence/mixin internals;
- physical-JAR↔source reproducibility;
- binary implementation details.

The catalog is intentionally publisher/documentation-bounded.

## Semantic result

The publisher presents Iron's Lib as a reusable shared framework/content library for consumer mods, and no independent library-owned standalone spell catalog is publicly established at this evidence ceiling.

Consumer-owned gameplay is not reassigned to the library merely because it depends on the library.

Semantic disposition:

- standalone spells: **0 established**;
- glyphs/spell parts: **0 established**;
- rituals/rites: **0 established**;
- independent castable supernatural actions: **0 established**;
- strict semantic delta: **+0**;
- classification: `ZERO_SEMANTIC_LIBRARY_INFRA`.

## Later-version exclusion

Current publisher documentation now includes features introduced after the physical 2.1.0 line, including Kinetic Weapon, Soul Fire burning visuals and Projectile Damage in 2.2.0.

Those are later-version context only and are not projected onto physical 2.1.0.

## Clean-room result

Because the publisher license is All Rights Reserved and exact source is unavailable, accepted evidence uses physical fingerprints plus public publisher/documentation facts only.

No JAR decompilation or archive-content reverse engineering is used. No implementation, source, assets, models, textures or publisher prose is copied into Black Arcana beyond minimal factual identifiers/API names needed for interoperability cataloging.
