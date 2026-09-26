# Iron's Spells 'n Spellbooks: Recolor — 1.3.3+1.21.1

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 1.3.3+1.21.1 / PRESENTATION+SYNC ADDON / 0 INDEPENDENT SPELL IDENTITIES ESTABLISHED / EXACT 1.3.3 SOURCE+BINARY SEMANTIC SURFACE NOT FULLY RECONSTRUCTED / +0 STRICT`

## Current physical identity — authority override

The current physical Project Library modlist captured on 2026-09-16 supersedes the older sibling dossier's 1.3.2 installed-version statement.

Authoritative physical line:

- JAR: `recolor_tablet-1.3.3+1.21.1.jar`;
- mod id: `recolor_tablet`;
- runtime: `1.3.3+1.21.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `f3806de891b04d554d05c279808b057fdf7bdab5`;
- mixin configs recorded by the physical JAR inventory:
  - `mixins.recolor_tablet.json`;
  - `mixins.recolor_tablet.geomancy.json`;
  - `mixins.recolor_tablet.hazennstuff.json`.

The current sibling dossier at `neoforge-rpg-skilltree@a0bf15c16f7e22eb42c4665bbe7a9dace8b8fda8` still describes 1.3.2 as installed and 1.3.3 as upstream drift. That dossier is stale for installed-version identity and is not used to overwrite the newer physical modlist.

## Provider role

Recolor is a presentation/QoL integration for Iron's Spells. Its documented purpose is to let players choose hue/color presentation for compatible Iron's spell schools through a Recolor Tablet and synchronized player state.

Iron's Spells remains authority for:

- spell identities and schools;
- cast admission;
- mana;
- cooldowns;
- targeting;
- damage/effects;
- progression semantics.

Recolor owns only the color/presentation state and compatibility needed to render supported spell effects with the selected hue.

## Current physical integration surface

The physical 1.3.3 inventory still declares the three mixin configurations listed above. This directly proves current binary integration surfaces for:

- Recolor core;
- GTBC's Geomancy Plus compatibility;
- Hazen N Stuff compatibility.

The mixin filenames establish compatibility surfaces, not standalone spell ownership.

## Semantic disposition

No provider-owned standalone spell identity is established by the current physical artifact metadata or the mod's published role.

Recolor acts on existing spells/schools supplied by Iron's and its addons. A per-player hue selection is presentation state, not a second spell, ritual, glyph, rite or provider-owned semantic magic object.

Therefore:

- independent spell identities established: **0**;
- strict semantic delta: **+0**;
- existing host spell ownership remains unchanged.

## Why the provider remains ⚠️

The installed artifact identity and mixin surface are physical-exact, but this Black Arcana audit does not yet have an exact public source pin or bounded decompilation/structural inventory for the installed 1.3.3 JAR.

Accordingly it would be unsafe to claim exhaustive binary closure for every packet, persistence field, command, config key or integration path.

The known role is sufficient to prevent semantic double-counting, while exact internal/runtime behavior remains fail-closed.

Current state:

**⚠️ partial / conditioned / presentation-only known surface / +0 strict**.

## Authority and deduplication

- Do not count a recolored host spell as a second spell identity.
- Do not use color state as evidence of cast success or spell ownership.
- Do not derive damage, mana, cooldown, school membership or progression from hue selection.
- Do not create a second sync/persistence system for provider color state without a verified interoperability contract.
- Black Arcana presentation may coexist, but Black Arcana must retain its own runtime authority and must not route casting through Recolor.
- RPG Skill Tree receives no magic runtime authority from this presentation addon.

## Runtime QA remains fail-closed

Separate assembled checks include:

- two players using different colors without state bleed;
- third-client synchronization;
- relog/reconnect/restart persistence behavior;
- resource reload and render compatibility;
- Geomancy/Hazen compatibility;
- host spell damage/mana/cooldown unchanged before vs after recolor;
- exact behavior against current Iron's 3.16.3.

## Result

**⚠️ Partial / conditioned.**

Current physical identity is 1.3.3+1.21.1. Known semantic contribution: **0 independent spells**. The provider is a presentation/synchronization layer over existing host spells; exhaustive exact-1.3.3 binary closure remains open.
