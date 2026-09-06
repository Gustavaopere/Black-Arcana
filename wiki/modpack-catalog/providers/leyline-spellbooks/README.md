# Leylines — Iron's Spells 'n Spellbooks Addon

Status: `CURRENT 1.0.3 SYSTEM IDENTITY VERIFIED; GRANULAR SPELL LIST PENDING`

- Current JAR: `leylines-1.0.3.jar`
- Mod id: `leylines`
- Runtime version: `1.0.3`
- Provider class: `SPELL PROVIDER / CONTENT + WORLD SYSTEM ADDON`
- Primary casting authority: Iron's Spells 'n Spellbooks.
- Current license: All Rights Reserved.

## Current public identity

The current public project description defines Leylines around:

- underground ley currents;
- time manipulation;
- portals;
- night-charged pillars;
- wave-based rifts;
- a dedicated new spell school;
- world generation / structures tied to the leyline system.

This is not only a spell pack. It combines spell semantics with world-state encounters and infrastructure.

## Current 1.0.3 rift authority behavior

The public 1.0.3 changelog establishes important encounter rules:

- dying during an active rift immediately fails the encounter and prevents completion reward/crystal;
- boss-bar cleanup occurs on death, respawn, logout and dimension change;
- moving more than **60 blocks** from an active rift collapses/fails it;
- encounter mobs wandering more than **40 blocks** away are pulled back to the arena;
- rift enemies are kept persistent enough that player death cannot falsely clear/complete the event;
- `/leylines spawnpillar` is an operator/debug command, not normal progression.

These are server/gameplay authority facts relevant to any Black Arcana integration around rifts/domains.

## Exact spell catalog status

The current public material collected in this pass proves the provider's thematic/system surface but does not publish a trustworthy complete `1.0.3` named spell table with registry IDs and quantitative values.

Therefore:

- time manipulation — VERIFIED provider capability family;
- portals — VERIFIED provider capability family;
- ley-current infrastructure — VERIFIED;
- wave/rift encounters — VERIFIED;
- exact spell names/IDs — `PENDING`;
- exact spell costs/cooldowns/ranges — `PENDING`;
- exact pillar charging/resource formulas — `PENDING`.

## Deduplication impact

### Order / Space / Doctor Strange-Fate inspiration

Leylines directly occupies **time + portals + spatial rifts**. Combined with Iron's Ender/Eldritch, Ars Blink/Exchange/Rewind, Asterism Astral Echo, Immersive Portals integration and Black Arcana 07.04, generic portal/time-warp spells are already heavily covered.

Order candidates must prove a law/seal/constraint delta rather than merely making a circular portal or slowing/rewinding something.

### Chaos / domains

Wave rifts and ley infrastructure can create high-chaos presentation, but the semantic distinction remains important: Leylines is a structured world-current/rift system. Black Arcana Chaos must not duplicate its encounter/rift lifecycle under a different visual theme.

### Forbidden Domains

The 60-block abandonment rule, 40-block mob leash and explicit cleanup behavior are useful comparison points for Black Arcana 07.06. Black Arcana must preserve its own canonical bounded-domain authority and should integrate with Leyline encounters only through explicit bridge rules, never by hijacking provider-owned rift completion state.

## Provenance / confidence

- Presence/version: current modlist and current public file page — HIGH.
- System identity and 1.0.3 encounter rules: current public CurseForge project/changelog — HIGH.
- Full current spell table: `UNVERIFIED / PENDING`.
- No Java bytecode was decompiled.
