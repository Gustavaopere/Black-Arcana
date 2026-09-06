# Ars Elemancy

Status: `PHASE 2 — CURRENT 1.18.3 EQUIPMENT SPECIALIZATION VERIFIED; NO GLYPH CATALOG PROVEN`

## Runtime identity

- Mod id: `ars_elemancy`
- Current JAR: `ars_elemancy-1.21.1-1.18.3.jar`
- Runtime version: `1.18.3`
- Loader/game: NeoForge 1.21.1
- Correct Phase 2 class: `GEAR / ENCHANT / SUPPORT CONTENT`
- Granular spell/glyph catalog: `NO / CONDITIONAL`

The PR #62 baseline registry classified Ars Elemancy as `ARS GLYPH / SYSTEM PROVIDER`. Current public 1.18.3 evidence instead describes an Ars Elemental extension centered on dual- and quad-element armor/foci and supporting presentation/progression.

## Verified equipment specializations

The current public project material names these elemental specializations:

- Cindermancer
- Lavamancer
- Miremancer
- Siltmancer
- Tempestmancer
- Vapormancer
- Elemancer — all-four-elements equipment/set identity

These are equipment/focus identities. Their existence does not imply a distinct spell/glyph registry owned by Ars Elemancy.

## Current 1.18.3 notes

Public 1.18.3 material also documents:

- improved/higher thread-slot behavior when the compatible All the Arcanist Gear environment is present;
- Starbuncle reskin behavior through naming;
- a known presentation issue around quad-element armor animations.

Those are gear/compat/presentation surfaces, not evidence for new glyph mechanics.

## Deduplication / authority

Ars Elemancy is relevant to Phase 2 because it can alter how an elemental build is equipped and represented. It must not be counted as an independent spell provider when evaluating whether Black Arcana has a mechanical gap.

- Ars Elemental/Ars Nouveau remain authority for the underlying elemental spell/glyph system.
- Equipment bonuses must not be counted twice through both host and addon paths.
- A Black Arcana school is not novel merely because it combines multiple elemental affinities into a named armor identity.
- No glyph IDs, spell costs or cast semantics are inferred from the equipment names.

## Provenance / confidence

- Presence/version: current 2026-09-06 modlist — HIGH.
- Specialization names and 1.18.3 feature notes: current public Ars Elemancy project/release material — HIGH at feature level.
- Separate glyph inventory: not proven in the current public material used for this pass.
- No Java bytecode was decompiled.
