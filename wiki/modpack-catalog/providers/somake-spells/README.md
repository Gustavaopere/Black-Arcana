# Somake Spells

Status: `CURRENT PROVIDER IDENTITY + PUBLIC FEATURE CATEGORIES VERIFIED; FULL SPELL LIST PENDING`

- Current JAR: `somakespells-1.0.8-1.21.1-fix.jar`
- Mod id: `somakespells`
- Runtime version: `1.0.8`
- Provider class: `SPELL PROVIDER / CONTENT ADDON`
- Primary casting authority: Iron's Spells 'n Spellbooks.

## Current public scope

Current public material for the 1.21.1 line describes Somake as an Iron's content expansion with **more than 50 spells**. Its spell identity is concentrated in:

- Lightning;
- Fire;
- Aqua;
- Symmetry;
- one Blood spell;
- one Ender spell.

The 1.21.1 line introduces an **Aqua** school and elemental `charge` mechanics. Public material also describes charges/integrations involving Sound, Symmetry, Spirit and Geo where the corresponding integration/provider exists.

The current 1.0.8 release adds a ritual system using an Ignis altar plus pedestals for Soul Fire and Infernal Fire necklaces and adds/evolves grimoire progression.

## Critical current-pack coexistence issue

Somake's public 1.21.1 documentation explains that Aqua content was created when T.O Magic was not available on 1.21.1 and was intended to be revisited/migrated if T.O Magic returned.

The **current Black Arcana modlist now contains both**:

- `somakespells-1.0.8-1.21.1-fix.jar`;
- `traveloptics-4.4.0.1-1.21.1.jar` (`T.O Magic n' Extras`).

Therefore Phase 2 must treat Somake↔T.O Magic Aqua/Symmetry/elemental overlap as a live compatibility and deduplication question. Historical assumptions that T.O Magic was absent are no longer authoritative.

## Integrations publicly associated with the current line

Public Somake material for 1.21.1 lists:

- L_Ender's Cataclysm — required in the documented setup;
- Apothic Attributes — required;
- Magic From The East — optional integration;
- Born in Chaos — optional integration;
- Geomancy Plus — optional integration;
- Tunes 'n Tomes — optional integration.

The Black Arcana catalog only counts an integration as active after confirming the corresponding current JAR is present. Presence does not imply every optional spell/path is enabled if config/datapack gates say otherwise.

## Full spell-list status

The public material reviewed so far proves the provider's scale and categories but does **not** expose a trustworthy complete 1.0.8 spell-name/ID table with all current values.

Phase 2 therefore records:

- provider identity — VERIFIED;
- `>50 spells` scope — VERIFIED PUBLIC CLAIM;
- school/category emphasis — VERIFIED;
- Aqua school — VERIFIED;
- charge/grimoire/ritual systems — VERIFIED at feature level;
- exact full spell list — `PENDING CURRENT DISTRIBUTED-JAR RESOURCE / OFFICIAL DOC EVIDENCE`;
- exact IDs, mana, cooldown, damage and acquisition per spell — `PENDING`.

No old list will be promoted to current simply because names existed in an earlier release.

## Deduplication impact

### Order / Symmetry

Somake explicitly occupies **Symmetry**. Before Black Arcana approves an Order mechanic, every Somake Symmetry spell must be resolved semantically. Visual geometry or symmetrical particles alone cannot establish a gap.

Order remains conceptually distinct only where it imposes actual rules/laws/seals/constraints not already implemented by Symmetry or other providers.

### Divine / Celestial

Somake's non-Holy focus does not by itself cover the planned Celestial identity, but charges, grimoires and ritual progression can overlap the proposed resource/progression architecture. Those must be compared at system level, not just spell effect level.

### Infernal / Soul Fire

The current 1.0.8 ritual path for Soul Fire and Infernal Fire necklaces directly intersects the proposed Infernal identity. It must be compared jointly with Ignis Soulfires, Soul Fire'd, Iron's Fire and Cataclysm-related providers before Phase 3.

### Chaos

High-impact elemental attacks do not automatically equal Chaos. Somake may consume part of Chaos's visual/action space, but probability/entropy/reality-law semantics remain a separate question to prove after the exact Somake list is cataloged.

## Provenance / confidence

- Presence/JAR/version: current 2026-09-06 modlist — HIGH.
- `>50` scope, school emphasis, Aqua/charge/grimoire/ritual descriptions and integration notes: current public project/release material — HIGH at feature level.
- Exact spell names/IDs and numerical balance: `UNVERIFIED / PENDING`.
- No source-code implementation details were used.
