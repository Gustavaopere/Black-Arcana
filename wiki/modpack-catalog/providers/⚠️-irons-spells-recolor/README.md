# Iron's Spells 'n Spellbooks: Recolor — 1.3.2+1.21.1

Status: `⚠️ PARTIAL / CURRENT PHYSICAL 1.3.2+1.21.1 / PRESENTATION+SYNC ADDON / 0 INDEPENDENT SPELL IDENTITIES ESTABLISHED / EXACT 1.3.2 SOURCE+BINARY SURFACE NOT FULLY RECONSTRUCTED / +0 STRICT`

## Current physical identity

Current sibling authority: `neoforge-rpg-skilltree@a0bf15c16f7e22eb42c4665bbe7a9dace8b8fda8`.

Certified sibling dossier: `PROJECT-INSTRUCTIONS/modlist/✅-irons-spells-n-spellbooks-recolor.md`.

- JAR: `recolor_tablet-1.3.2+1.21.1.jar`;
- mod id: `recolor_tablet`;
- runtime: `1.3.2+1.21.1`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical provider role: client/server presentation/QoL addon for Iron's Spells;
- current Iron's Spells physical line: `1.21.1-3.16.3`.

The sibling dossier records the installed binary as the authority and explicitly preserves later upstream release drift rather than silently upgrading the pack.

## Provider role

Recolor lets a player choose hue/color presentation for compatible Iron's spell schools through the Recolor Tablet and synchronized player state.

Iron's Spells remains authority for:

- spell identities and schools;
- cast admission;
- mana;
- cooldowns;
- targeting;
- damage/effects;
- progression semantics.

Recolor owns only the color/presentation state and the compatibility layer required to render supported spell effects with the selected hue.

## Physical binary evidence already recorded by sibling

The current sibling dossier records three mixin configs present in the installed JAR:

- `mixins.recolor_tablet.json`;
- `mixins.recolor_tablet.geomancy.json`;
- `mixins.recolor_tablet.hazennstuff.json`.

That provides direct evidence of a presentation/compatibility integration surface for:

- Recolor core;
- GTBC's Geomancy Plus;
- Hazen N Stuff.

The same dossier notes publisher-documented compatibility with T.O Magic n' Extras, but does not infer an implementation mechanism not evidenced by the physical mixin list.

## Semantic disposition

No provider-owned standalone spell identity is established by the current physical dossier or publisher-facing function.

Recolor acts on existing spells/schools supplied by Iron's and its addons. A hue-selection state is not a new spell, ritual, glyph, rite or provider-owned gameplay magic object.

Therefore:

- independent spell identities: **0 established**;
- strict semantic delta: **+0**;
- existing host spell ownership remains unchanged.

## Why the provider remains ⚠️

This Black Arcana audit does not promote Recolor to a fully closed zero-semantic ✅ provider yet because the exact installed 1.3.2 class/resource surface has not been independently reconstructed here from the physical JAR, and an exact public source/tag for that installed build is not available in the current evidence set.

The evidence is strong enough to classify the known role and prevent semantic double-counting, but not to claim exhaustive binary closure beyond the recorded physical mixin/config surface.

Accordingly:

**⚠️ partial / conditioned / presentation-only known surface / +0 strict**.

## Authority and deduplication

- Do not count a recolored host spell as a second spell identity.
- Do not use color state as evidence of cast success or spell ownership.
- Do not derive damage, mana, cooldown, school membership or progression from hue selection.
- Do not create a second sync/persistence system for provider color state unless a verified interoperability contract requires it.
- Black Arcana spell presentation may coexist, but Black Arcana must retain its own runtime authority and must not route casting through Recolor.
- RPG Skill Tree receives no magic runtime authority from this presentation addon.

## Runtime QA remains fail-closed

Separate assembled checks include:

- two players using different colors without state bleed;
- third-client synchronization;
- relog/reconnect/restart persistence behavior;
- resource reload and render compatibility;
- Geomancy/Hazen compatibility;
- host spell damage/mana/cooldown unchanged before vs after recolor;
- exact behavior against current Iron's 3.16.3 rather than historical host references in older documentation.

## Result

**⚠️ Partial / conditioned.**

Known semantic contribution: **0 independent spells**. The provider is a presentation/synchronization layer over existing host spells; exhaustive exact-1.3.2 binary closure remains open.
