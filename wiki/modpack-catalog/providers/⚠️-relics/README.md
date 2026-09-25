# Relics — 0.12.8

Status: `PARTIAL / PHYSICAL SHA-PINNED / EXACT PUBLISHER RELEASE / CURRENT OFFICIAL ABILITY DOCS / COMPLETE DISCRETE ABILITY CARDINALITY NOT YET ARTIFACT-PINNED / RUNTIME QA FAIL-CLOSED`

## Current physical identity

Current sibling authority:

`neoforge-rpg-skilltree@d7c99d23ef1b38fe62c86a362ec521ced8861f96`

Certified dossier:

`PROJECT-INSTRUCTIONS/modlist/Adventure and RPG + Armor, Tools, and Weapons + Cosmetic + Magic + Ores and Resources/✅-relics v0.12.8.md`

Physical identity preserved there:

- JAR: `relics-1.21.1-0.12.8.jar`;
- mod id: `relics`;
- runtime: `0.12.8`;
- Minecraft 1.21.1 / NeoForge;
- physical SHA-1: `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`.

This is stronger than the publisher-only identity used for several other providers: the installed artifact itself is fingerprinted.

## Exact publisher release

CurseForge project: `445274`.

Exact NeoForge 1.21.1 file:

- file ID: `8158315`;
- filename: `relics-1.21.1-0.12.8.jar`;
- uploaded: 2026-05-28;
- release channel: Beta;
- environment: Client & Server.

The release notes explicitly add:

- Shield of Retaliation;
- per-relic target configuration;
- FTB Teams integration;
- relic-experience-gained statistics;
- relic data cache optimization / memory-leak fixes;
- Ghostly Mantle visual update;
- Midnight Mantle visual update;
- Springy Boot screen-shake removal.

Publisher file:
`https://www.curseforge.com/minecraft/mc-mods/relics-mod/files/8158315`

## Current official documentation surface

Official Shatterbyte documentation:

`https://www.shatterbyte.com/docs/mods/relics/`

The documentation describes itself as providing item and ability details for every Relics relic and currently lists 20 base Relics identities:

1. Leafy Mantle;
2. Springy Boot;
3. Kinetic Belt;
4. Reflective Necklace;
5. Jellyfish Necklace;
6. Midnight Mantle;
7. Roller Skate;
8. Chorus Staff;
9. Piglin Mask;
10. Cut Glass Boot;
11. Ring of the Seven Deadly Sins;
12. Sphere of Self-Sacrifice;
13. Hunting Belt;
14. Chef's Hat;
15. Clot of Time;
16. Rider Flute;
17. Experience Disperser;
18. Glitchy Mantle;
19. Ghostly Mantle;
20. Shield of Retaliation.

The inclusion of Shield of Retaliation correlates the current documentation surface with the 0.12.8 content line because that relic is explicitly new in the exact 0.12.8 publisher changelog.

This correlation is useful but is not equivalent to a source commit or byte-equivalent resource inventory for the installed JAR.

## Ability system is provider-owned

Relics is not merely a set of passive accessories. Official documentation exposes named ability state, rank progression, XP, target rules, mode switches, cooldowns/buffers and synergies.

Publisher-documented examples include:

- Leafy Mantle — Camouflage;
- Reflective Necklace — Damage Condensation;
- Jellyfish Necklace — Aquatic Regeneration, Electric Discharge;
- Midnight Mantle — Lunar Phase, Shadow, Constellation, Starfall;
- Roller Skate — Acceleration;
- Chorus Staff — Teleportation;
- Piglin Mask — Neutrality, Barter, Looting;
- Cut Glass Boot — Glass;
- Ring of the Seven Deadly Sins — Pride, Envy, Wrath, Sloth, Greed, Gluttony, Lust;
- Sphere of Self-Sacrifice — Sacrifice;
- Hunting Belt — Arsenal Expansion, Pack;
- Clot of Time — Transgression;
- Rider Flute — Stable;
- Experience Disperser — Experience Dispersion;
- Glitchy Mantle — Surface Tear among its documented ability/synergy surface;
- Ghostly Mantle — Grave Mist among its documented ability surface;
- Shield of Retaliation — Retaliation.

These are discrete provider ability identities and are relevant to Black Arcana capability deduplication.

## Why the semantic count remains pending

The Black Arcana semantic metric may count provider-owned discrete magical actions/powers where the identity is stable and auditable.

Relics clearly qualifies as a provider with such powers. However, this checkpoint does **not** publish a final ability cardinality because:

- the public GitHub branch visible for the 1.21 line is not a demonstrated exact 0.12.8 source pin;
- the exact installed JAR could not be independently resource-inventoried in this audit environment;
- current official documentation is version-correlated through Shield of Retaliation but not itself immutable/version-tagged;
- some documentation pages expose multiple abilities and synergies while others are not consistently retrievable through the current indexing/render path;
- synergies must not be silently counted as base abilities;
- rank modifiers/modes must not be promoted to new ability identities.

Therefore:

`SEMANTIC_DELTA = PENDING`

No fabricated positive count and no false `+0` closure are permitted.

## Authority boundary

Relics owns:

- relic definitions;
- ability identities and ability state;
- ranks/levels and provider XP;
- target configuration;
- cooldown/buffer/state for relic abilities;
- relic loot/generation;
- provider synergies.

Curios owns accessory slot/equip plumbing.

FTB Teams supplies team context when integrated.

Reliquified addons own their addon relic definitions while consuming the Relics framework.

Black Arcana must not duplicate Relics ability state, cooldown, XP, targeting or resource settlement.

RPG Skill Tree remains progression/Mastery/perk/gate authority only for Black Arcana contracts. It does not replace Relics' own relic progression runtime.

## Current physical integrations

Current sibling dossier confirms the relevant installed stack:

- Curios 9.5.1;
- OctoLib 0.6.2;
- Sophisticated Backpacks 3.26.3;
- FTB Teams 2101.1.11;
- Artifacts 13.2.5;
- Reliquified Ars Nouveau 0.8.1;
- Reliquified Artifacts 1.0.8;
- Reliquified Iron's Spells 'n Spellbooks 0.2.7;
- Reliquified L_Ender's Cataclysm 0.1.1 + fix 1.0.2.

This catalog does not infer runtime compatibility from presence alone.

## Known 0.12.8 risk evidence

Two public 0.12.8 reports are relevant as regression risks, not reproduced local bugs:

- Jellyfish Necklace / Electric Discharge target filtering has a reported villager-targeting edge case;
- Experience Disperser has a reported high-stat overflow/progression edge case above the signed 32-bit integer range.

They remain runtime QA items rather than semantic-catalog evidence.

## Still fail-closed

- exact publisher-file ↔ physical SHA equality, because the publisher page does not expose the sibling physical SHA as a comparison digest;
- exact immutable 0.12.8 ability/resource registry inventory;
- complete base-ability cardinality;
- synergy cardinality;
- deployed configs for ability stats, targeting and loot;
- Curios lifecycle exactly-once behavior;
- provider XP persistence;
- cooldown/buffer persistence;
- target/team filtering;
- Sophisticated Backpacks interaction;
- Reliquified addon coexistence;
- server/restart/migration behavior;
- any Black Arcana adapter.

## Result

**⚠️ Partially cataloged:** exact physical version and SHA are pinned, exact publisher release is pinned, all 20 currently documented base relic identities are inventoried, and the provider-owned ability model is established.

The final discrete ability numerator remains pending exact immutable action-surface closure.
