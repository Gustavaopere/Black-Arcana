# Ars Polymorphia

Status: `PHASE 2 — CURRENT 1.0.3 COMPATIBILITY ROLE VERIFIED; NOT A SPELL/GLYPH PROVIDER`

## Runtime identity

- Mod id: `ars_polymorphia`
- Current JAR: `ars_polymorphia-1.0.3.jar`
- Runtime version: `1.0.3`
- Loader/game: NeoForge 1.21.1
- Correct Phase 2 class: `BRIDGE / COMPAT / PROGRESSION`
- Granular spell/glyph catalog: `NO / CONDITIONAL`

## Verified function

The current public project description is narrow: Ars Polymorphia adds Polymorph compatibility for Ars Nouveau Storage Lecterns. The current 1.0.3 changelog fixes handling of recipes whose result is empty.

No independent spell school, glyph set, mana resource, ritual system or combat mechanic is established by the current public evidence used for this pass.

## Classification correction

The PR #62 baseline registry classified Ars Polymorphia as `ARS GLYPH / SYSTEM PROVIDER | YES`. That is corrected for Phase 2 interpretation to:

`BRIDGE / COMPAT / PROGRESSION | NO / CONDITIONAL`

The mod remains relevant to compatibility/progression because recipe-selection behavior can affect lectern workflows, but it must not inflate the count of magical capability providers.

## Deduplication / authority

- Ars Nouveau owns Storage Lectern behavior and Ars content.
- Polymorph owns recipe-conflict selection behavior where integrated.
- Black Arcana has no reason to create a parallel recipe-conflict system for this surface.
- This component contributes no proven semantic gap for Chaos, Order, Blood, Infernal, Divine, Witchcraft or other planned Black Arcana schools.

## Provenance / confidence

- Presence/version: current 2026-09-06 modlist — HIGH.
- Compatibility role and 1.0.3 fix: current public Ars Polymorphia project/changelog — HIGH.
- No Java bytecode was decompiled.
