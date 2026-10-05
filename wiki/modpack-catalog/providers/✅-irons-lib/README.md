# Iron's Lib — 1.21.1-2.1.0

Status: `✅ CATALOGED / CURRENT PHYSICAL 2.1.0 / PUBLISHER+DOCUMENTATION-BOUNDED CLOSED-SOURCE LIBRARY / 7 COMMON RPG ATTRIBUTES + ATTRIBUTE REMAPPER + TRANSMOG/STATUE INFRA / 0 INDEPENDENT SPELLS+GLYPHS+RITUALS / ZERO_SEMANTIC_LIBRARY_INFRA / +0 STRICT / INTERNALS+RUNTIME QA FAIL-CLOSED`

## Current physical authority

Current sibling authority:

`neoforge-rpg-skilltree@de80b186357cad20ba5b81892a8682777e96e35a`

Canonical sibling dossier:

`PROJECT-INSTRUCTIONS/modlist/API and Library + Cosmetic/✅-irons-lib v1.21.1-2.1.0.md`

- physical JAR: `irons_lib-1.21.1-2.1.0.jar`;
- mod id: `irons_lib`;
- physical/runtime version: `1.21.1-2.1.0`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `70fba64d12b6ff9553580e52101d989c89297797`;
- required GeckoLib is physically present as 4.9.2;
- relevant physical consumers include Iron's Spells 3.16.3 and Iron's Gems 'n Jewelry 2.0.2.

The physical modlist/JAR record remains authority for the installed artifact.

## Publisher evidence ceiling

CurseForge project `1492763` describes Iron's Lib as common functionality/content for Iron's mods and classifies it as **API and Library / Cosmetic**, **Client & Server**, **All Rights Reserved**.

The publisher file list records `irons_lib-1.21.1-2.1.0.jar` as a NeoForge 1.21.1 Release uploaded on **2026-07-03**.

No official public source repository or exact 2.1.0 source pin was established in this audit. The exact implementation classes, registry internals and non-published APIs are therefore intentionally fail-closed.

## Provider role and authority

Iron's Lib is shared framework/content infrastructure for the Iron's ecosystem. It does not become the owner of gameplay registered by its consumers.

Authority split:

- Iron's Lib owns the shared library contracts/content that it publishes, including common attributes, remapping infrastructure, transmog/statue framework surfaces and related shared APIs;
- Iron's Spells owns its spells, schools, mana/casting and spell execution;
- Iron's Gems 'n Jewelry owns its jewelry/content behavior;
- Iron's Apothic owns its compatibility behavior;
- Black Arcana owns Black Arcana casting, rituals, hazards, Corruption, Strain, Arcane Danger, Backlash and world safety;
- RPG Skill Tree remains progression-only through explicit provider contracts.

## Publicly documented 2.1.0-line magic/RPG-relevant surface

### Seven common RPG attributes

Publisher documentation for the pre-2.2.0 1.21.1 library line, reconciled by the current sibling dossier for installed 2.1.0, establishes these shared attributes:

1. Armor Pierce;
2. Mining Speed;
3. Experience Gained;
4. Arrow Damage;
5. Crit Damage;
6. Dodge Chance;
7. Healing Received.

These are shared attribute contracts. They are not standalone spells, glyphs or rituals.

### Attribute Remapper

The public API documentation establishes an Attribute Remapper that can remap item attributes for compatibility:

- code registration through `AttributeRemapRegistry#register`;
- data-driven mappings under `data/<namespace>/irons_lib_attribute_remap/`;
- `from` and `to` fields containing attribute resource IDs;
- native compatibility is advertised for Apothic Attributes.

Black Arcana must not create a parallel remapper or apply the same semantic modifier twice. Any future integration must use a verified public contract and preserve acyclic, exactly-once mapping behavior.

### Transmogs and presentation infrastructure

The publisher describes reusable transmog infrastructure including custom armor models/interfaces and cape-physics handling. The 2.1.0 release line also introduced/updated themed transmogs.

Transmogs are equipment/presentation infrastructure and do not imply spell identity or grant Black Arcana stat authority.

### Statues / multiblocks and shared services

The public project description documents dynamic player-statue asset generation, dynamic multiblock handling, static model rendering and a Patreon integration API layer.

These are shared framework/services. They are not independently castable magical actions under the Black Arcana semantic ledger.

## Semantic magic disposition

At the accepted publisher/documentation evidence ceiling, no standalone Iron's Lib spell catalog is attributed to the library. Consumer mods remain the owners of concrete spells/gameplay built on the shared framework.

Strict semantic result:

- independent provider-owned spells: **0 established**;
- provider-owned glyph/spell-part identities: **0 established**;
- provider-owned rituals/rites: **0 established**;
- equivalent independent castable supernatural actions: **0 established**;
- strict semantic contribution: **+0**;
- classification: **`ZERO_SEMANTIC_LIBRARY_INFRA`**.

This is a publisher/documentation-bounded zero, not a decompiled-binary proof of every internal class in the All Rights Reserved JAR.

## Version boundary: do not project later 2.2.0 features backward

The physical pack remains on **2.1.0**. Current sibling authority was revalidated on 2026-10-05; upstream 1.21.1 has advanced beyond the installed version, but the physical JAR has not.

Later 1.21.1 release 2.2.0 publicly adds surfaces such as:

- kinetic weapon/charge-attack infrastructure;
- Soul Fire burning visuals;
- Projectile Damage as an additional shared attribute.

Those later features are **not** promoted into the installed 2.1.0 catalog unless independent evidence demonstrates that they already exist in the physical 2.1.0 artifact. In particular, the physical 2.1.0 attribute set remains the seven documented attributes above.

## Runtime / compatibility QA remains separate

Catalog closure does not assert physical runtime PASS for:

- registration/synchronization of the seven documented attributes;
- remap behavior, invalid targets or cycle handling;
- equip/unequip/relog modifier accumulation;
- interaction with Apothic Attributes;
- transmog rendering and stat neutrality;
- statue/multiblock persistence through chunk unload/restart;
- dedicated-server classloading of client presentation paths;
- ABI compatibility across all physical consumers;
- exact internal registry/class layout of the closed-source artifact.

Any later failure here is integration/runtime QA and does not manufacture a missing spell identity.

## Clean-room boundary

The publisher labels Iron's Lib **All Rights Reserved**. This catalog therefore uses only:

- current physical identity/hash from the pack authority;
- publisher-authored project/file metadata;
- publisher-authored feature/API descriptions;
- sibling-audited compatibility boundaries.

No JAR decompilation, archive-content reverse engineering, copied source, copied assets, copied implementation or invented internal signature is used for this closure.

## Current result

**✅ Cataloged.**

Iron's Lib 2.1.0 is cataloged as shared RPG/API/content infrastructure with **+0 strict semantic spell/glyph/ritual contribution**. Its consumers remain the owners of their concrete magic.
