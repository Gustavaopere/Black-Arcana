# Ars Creo

Status: `PHASE 2 — CURRENT 5.4.0 BRIDGE CAPABILITIES VERIFIED; NOT A GLYPH PROVIDER`

## Runtime identity

- Mod id: `ars_creo`
- Current JAR: `ars_creo-1.21.1-5.4.0.jar`
- Runtime version: `5.4.0`
- Loader/game: NeoForge 1.21.1
- Correct Phase 2 class: `BRIDGE / COMPAT / PROGRESSION`
- Granular spell/glyph catalog: `NO / CONDITIONAL`

The PR #62 baseline registry classified Ars Creo as `ARS GLYPH / SYSTEM PROVIDER`. Granular verification does not support that interpretation. The current public 5.4.0 surface is a functional Ars Nouveau ↔ Create integration layer centered on contraptions, turrets, Source and rituals.

## Verified bridge capabilities

### Starbuncle Wheel

Generates Create kinetic output through Starbuncle-powered infrastructure. Create remains authority for stress/kinetics; Ars remains authority for its magical actors/resources.

### Spell Turrets on Create contraptions

Current public documentation supports running Ars spell turrets as part of moving Create contraptions.

Variants/behaviors documented by the provider include:

- Timer Turret — fires on an interval while used in the contraption context;
- Basic Spell Turret — can fire from interaction in the contraption context;
- Enhanced Spell Turret — can react to newly reached block positions.

### Source Jars on contraptions

Source Jars can participate in contraptions and provide Source to compatible turret behavior. This must not be reinterpreted as global or free Source access.

### Ritual support on contraptions

The current 5.4.0 changelog explicitly adds ritual support on contraptions.

## Deduplication / authority

Ars Creo proves that `magic on moving Create contraptions` is already a provider-owned capability family. A future Black Arcana spell/system is not novel merely because it casts from a moving airship/contraption.

Required boundaries:

- Create owns contraption/kinetic state;
- Ars Nouveau owns spell execution and Source;
- Ars Creo owns the translation that lets those systems operate together;
- Black Arcana must not create a parallel Create↔Ars bridge or double-fire the same turret/ritual event;
- Source and kinetic settlement remain provider-native;
- moving/sublevel coordinates must still respect whatever Sable/Aeronautics boundary is authoritative for the actual host context.

## Why no glyph catalog

The current public 5.4.0 material verified for this pass does not expose a discrete Ars Creo glyph list. Its player-facing contribution is integration/infrastructure. Therefore the baseline `Granular capability catalog = YES` is corrected to `NO / CONDITIONAL`: catalog bridge behaviors and authority, but do not invent glyphs.

## Provenance / confidence

- Presence/version: current 2026-09-06 modlist — HIGH.
- Contraption turrets, Source Jar behavior, Starbuncle Wheel and 5.4.0 ritual support: current public Ars Creo project/changelog — HIGH at feature level.
- No current public glyph inventory found for 5.4.0 in this pass.
- No Java bytecode was decompiled.
