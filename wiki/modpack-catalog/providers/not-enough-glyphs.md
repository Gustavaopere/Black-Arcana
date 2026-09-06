# Not Enough Glyphs

Status: `PHASE 2 — CURRENT 4.6.1 HIGH-IMPACT CAPABILITIES NORMALIZED; COMPLETE PRIMITIVE PASS STILL OPEN`

## Runtime identity

- Mod id: `not_enough_glyphs`
- Current JAR: `not_enough_glyphs-1.21.1-4.6.1.jar`
- Runtime version: `4.6.1`
- Loader/game: NeoForge 1.21.1
- Phase 2 class: `ARS GLYPH / SYSTEM PROVIDER`

## Verified current capabilities

### Trail / Echoing Projectile

Projectile-oriented form that can resolve the configured spell along the projectile trail before the projectile expires. This is already a provider-native moving-path/repeated-delivery primitive.

### Plow

Agricultural/hoe-style operation exposed as a glyph capability.

### Plane

Area/geometry primitive described as a non-repeating linger-like plane. Public examples include circles/cylinders and hollow-square style applications depending on composition.

### Contingencies

Current 1.21.1+ system that stores a spell and executes it when its condition occurs. Public documentation states:

- mana is paid on the initial contingency cast rather than repeatedly on each later trigger;
- only one contingency is active at a time;
- death is a documented example trigger/use case.

This materially overlaps generic “cast X automatically when Y happens” design space.

### SpellBinder

Stores up to 25 spells using supported carrier sources such as caster tomes or spell parchments.

## Binder threads

Current public documentation exposes binder modifiers including:

- Focus — with Shapers/Summoning/Elemental variants when the relevant integration is available;
- Randomize — causes random buff/debuff behavior per glyph in the documented binder context;
- Slow Power;
- Cheap Damage;
- Sharp Pages;
- Hard Cover.

Exact formulas for every thread are not normalized here unless explicitly present in current public documentation.

## Repacked/migrated glyph families

Not Enough Glyphs includes compatibility/repacked capabilities from earlier addons and automatically disables repacked entries when the original provider is present where supported.

Current public 1.21.1 material references, among others:

- Ray;
- Chain;
- Redirect Placement;
- several filters from Too Many Glyphs;
- vanilla-form propagators + Flatten from Omega;
- Arc/Homing projectile forms and propagators originating from Ars Elemental coverage;
- Filter Self / Filter Not Self from Trinkets-era coverage.

This makes ownership/deduplication especially important: a capability appearing in NEG documentation is not automatically owned uniquely by NEG if the original addon is installed and the repacked copy disables itself.

## Important current ownership correction — Random filter

The current 4.5.1+ changelog explicitly moved the `Random` filter to Ars Controle. Therefore:

- `Filter: Random` is treated as Ars Controle coverage in the current pack;
- NEG's `Randomize` Binder thread remains a different, binder-specific randomization capability;
- Black Arcana must not count these as two independent generic probability gaps.

## Deduplication impact

Not Enough Glyphs already covers or contributes to:

- event-triggered/contingency casting;
- repeated projectile-path spell delivery;
- planar/geometric placement;
- spell storage/containerization;
- binder-specific randomization;
- multiple filter/propagator utility families.

A future Chaos mechanic cannot use “random outcome” alone as novelty. A future Order/geometry mechanic cannot use “plane/hollow geometry” alone as novelty. A future emergency spell cannot use “automatically trigger this stored spell on condition” alone as novelty.

## Authority / fail-closed

- Ars Nouveau remains authority for glyph execution and mana settlement.
- NEG-owned repacked entries must respect the provider's own disable/delegation behavior when original addons are present.
- Contingency must not be mirrored by Black Arcana as a second trigger that executes the same stored action twice.
- Unknown costs, registry IDs and thread formulas remain `UNVERIFIED` rather than inferred.

## Provenance / confidence

- Presence/version: current 2026-09-06 modlist — HIGH.
- Capability semantics and migration notes: current public Not Enough Glyphs 4.6.1 project/changelog — HIGH at feature level.
- Complete current glyph/filter inventory and all numeric values: still `IN PROGRESS`.
- No Java bytecode was decompiled.
