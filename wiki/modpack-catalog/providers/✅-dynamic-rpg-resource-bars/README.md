# Dynamic RPG Resource Bars — 0.7.1

Status: `✅ CATALOGED / PHYSICAL SHA-PINNED / EXACT PUBLISHER RELEASE / HUD-PRESENTATION PROVIDER / ZERO SPELL-RITUAL-MAGIC-ACTION OWNERSHIP / +0 STRICT SEMANTIC MAGIC / RUNTIME UI QA FAIL-CLOSED`

## Current physical identity

Current sibling authority at audit start:

`neoforge-rpg-skilltree@5ad350730a16e786f91396336c16c7b193feb7ac`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + API and Library + Cosmetic + Magic + Utility & QoL/✅-dynamic-rpg-resource-bars v0.7.1.md`

Physical identity:

- order: **#232**;
- JAR: `dynamic_resource_bars-neoforge-0.7.1-1.21.1.jar`;
- mod id: `dynamic_resource_bars`;
- runtime: `0.7.1`;
- Minecraft 1.21.1 / NeoForge;
- physical SHA-1: `08512179fdd92b1be480ad16535b036bd30f2d7d`.

## Exact publisher release

CurseForge project: `1188180`.

Exact NeoForge 1.21.1 file:

- file ID: `6964564`;
- filename: `dynamic_resource_bars-neoforge-0.7.1-1.21.1.jar`;
- uploaded: 2025-09-05;
- Release;
- NeoForge;
- Minecraft 1.21.1;
- changelog: adjusts the default stamina-bar color.

Publisher file:

`https://www.curseforge.com/minecraft/mc-mods/dynamic-rpg-resource-bars/files/6964564`

Official source repository:

`https://github.com/muon-rw/Dynamic-Resource-Bars`

The public repository is currently on a later Minecraft line and is therefore used for role/architecture context only, not as an immutable 0.7.1 source pin.

## Provider role

Dynamic RPG Resource Bars is a client-facing HUD/resource-presentation layer.

The exact physical dossier and official project documentation establish that it presents resources such as:

- health;
- mana;
- stamina;
- air;
- armor;
- absorption;
- food/saturation-related overlays;
- mount health / related display substitutions.

It also owns:

- bar layout;
- colors;
- animation;
- sprites/resource-pack presentation;
- HUD editor state;
- client-side positioning/scaling/fade/text.

It does **not** own the underlying gameplay resource values.

## Mana authority

The 0.6.x/0.7.x line supports external mana sources including Ars Nouveau and Iron's Spells 'n Spellbooks.

Current physical pack contains both providers.

Authority remains:

- Ars Nouveau owns Ars mana;
- Iron's Spells owns Iron's mana;
- Minecraft owns vanilla health/air/armor/food state;
- any installed stamina provider owns stamina;
- Dynamic RPG Resource Bars only reads/presents those states.

A visual bar must never be treated as a second resource ledger.

## Semantic accounting

Provider-owned spells: **0**.

Provider-owned glyph/spell-part identities: **0**.

Provider-owned rituals/rites: **0**.

Provider-owned equivalent discrete magical actions: **0**.

Mana/resource bars, HUD animations, overlays, editor actions and resource-pack presentation are not semantic magic actions.

Strict semantic delta:

**+0**

The CurseForge `Magic` category is taxonomy for a mod that visually integrates magical resources; it does not create spell ownership.

## Authority boundary

Black Arcana must not:

- debit or restore mana because the HUD changed;
- infer a cast from a bar animation;
- create a second mana/stamina value;
- duplicate provider regeneration;
- treat HUD interpolation as authoritative gameplay state.

RPG Skill Tree likewise does not own those provider resources unless a separate verified contract explicitly says so.

## Runtime QA remains fail-closed

Catalog closure does not establish:

- correct provider selection when Ars and Iron's are both installed;
- installed stamina-provider compatibility;
- AppleSkin/Farmer's Delight overlay composition;
- mount-health switching;
- config migration;
- GUI-scale/layout correctness;
- resource-pack sprite compatibility;
- login/respawn/dimension/reload lifecycle;
- dedicated-server/client composition.

These are UI/runtime compatibility gates, not semantic catalog blockers.

## Result

**✅ Cataloged.**

The physical 0.7.1 provider is a HUD/presentation component that consumes external resource state and owns no spell, glyph, ritual or equivalent magic-action identity.

Strict semantic contribution: **+0**.
