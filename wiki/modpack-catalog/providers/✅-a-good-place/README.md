# A Good Place — 1.21-1.2.5

Status: `CATALOGED / EXACT PHYSICAL VERSION / EXACT PUBLISHER BINARY + SOURCES ARTIFACT / CLIENT PRESENTATION LAYER / ZERO SPELL-RITUAL-MAGIC-ACTION OWNERSHIP / +0 STRICT SEMANTIC MAGIC / RUNTIME UI QA FAIL-CLOSED`

## Current physical identity

Current sibling authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Cosmetic + Magic + Utility & QoL/✅-a-good-place v1.21-1.2.5.md`

Physical identity preserved there:

- JAR: `a_good_place-1.21-1.2.5-neoforge.jar`;
- mod id: `a_good_place`;
- runtime: `1.21-1.2.5`;
- Minecraft: 1.21.1;
- loader: NeoForge;
- environment/function: client-side block-placement animation.

The sibling dossier does not preserve an independent installed-JAR digest for this row, so installed-byte equality with the publisher file is not claimed.

## Exact publisher release

CurseForge project: `1020455`.

Exact NeoForge 1.21 / 1.21.1 release:

- file ID: `5974291`;
- filename: `a_good_place-1.21-1.2.5-neoforge.jar`;
- uploaded: 2024-12-08;
- type: Release;
- loader: NeoForge;
- supported game versions: 1.21 and 1.21.1;
- environment: Client;
- published description: block-placement animations;
- published 1.2.5 change: improved logic for block entities and one issue fix.

Exact publisher sources artifact:

- file ID: `5974293`;
- filename: `a_good_place-1.21-1.2.5-neoforge-sources.jar`;
- same upload date;
- same 1.21 / 1.21.1 release line.

Publisher binary:

`https://www.curseforge.com/minecraft/mc-mods/a-good-place/files/5974291`

Publisher sources:

`https://www.curseforge.com/minecraft/mc-mods/a-good-place/files/5974293`

## Official source / documentation

Official source repository:

`https://github.com/enjarai/a-good-place`

The official README states that A Good Place is a **client-side mod that adds block placement animations**.

The documented data model is Resource Pack-driven and exposes placement-animation presentation fields such as:

- predicates;
- priority;
- duration;
- scale;
- translation;
- rotation;
- rotation pivot;
- height scale;
- curve controls;
- direction restriction;
- optional sound.

The README also documents block-state predicates and animation targeting.

These are visual/presentation definitions. They do not establish a spell, ritual, magical resource or gameplay-power runtime.

## What the mod actually owns

A Good Place owns the client representation of accepted block placement.

The authoritative block placement itself remains owned by Minecraft/server-side gameplay and whichever mod/tool initiated the placement.

Provider-owned surfaces are:

- placement-animation selection;
- temporary visual block representation;
- transform interpolation;
- resource-pack animation definitions;
- block-state targeting predicates;
- block-entity rendering accommodation;
- optional presentation sound;
- client rendering/performance state.

## What the mod does not own

No evidence in the exact publisher description or official documentation establishes provider-owned:

- spells;
- spell schools;
- casting;
- mana/resources;
- rituals/rites;
- magical abilities;
- enchantments;
- magical progression;
- damage/healing powers;
- authoritative block placement;
- inventory consumption;
- recipes/worldgen triggered by the animation.

The CurseForge `Magic` category is therefore taxonomy only. It does not make A Good Place a magic-action provider.

## Semantic accounting

Provider-owned spells: **0**.

Provider-owned rituals/rites: **0**.

Provider-owned equivalent discrete magical actions: **0**.

Placement animation definitions are presentation data and do not enter the Black Arcana semantic magic numerator.

Strict semantic delta:

**+0**

## Authority boundary

- Minecraft/server gameplay owns whether a block is placed and the resulting world state.
- A Good Place owns client-side visual interpolation after placement observation.
- Resource Packs own the selected animation data layered through the normal resource stack.
- Black Arcana must not treat placement-animation callbacks or visuals as a casting/gameplay authority boundary.

## Runtime QA remains fail-closed

Catalog closure does not prove:

- exact installed resource-pack definitions;
- block-entity rendering for every provider block;
- shader/VFX composition;
- resource-pack priority behavior;
- main-hand/off-hand presentation;
- automated high-rate placement performance;
- Replay/Motion Capture compatibility;
- client visual behavior on every block state;
- installed-JAR ↔ publisher-file byte equality.

These are UI/render/runtime QA items, not semantic magic-catalog blockers.

## Result

**✅ Cataloged:** exact physical version and exact publisher binary/source release are identified, and the official provider documentation establishes a client-side Resource Pack-driven placement-animation layer rather than a spell/ritual/magic-action runtime.

Strict semantic contribution: **+0**.
