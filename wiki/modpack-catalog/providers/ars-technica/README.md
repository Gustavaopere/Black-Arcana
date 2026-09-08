# Ars Technica 2.7.6

Status: `PHASE 2V — SOURCE CATALOG CLOSED / INSTALLED RUNTIME + CONFIG QA OPEN`

## Exact installed identity

- Mod id: `ars_technica`
- Physical JAR: `ars_technica-1.21.1-2.7.6.jar`
- Runtime version: `2.7.6`
- Physical SHA-1: `adb2641d538375f6eff6a22f0196bb330ab0b171`
- Loader/game: NeoForge 1.21.1
- Phase 2 class: `ARS GLYPH / SYSTEM PROVIDER`

Physical modlist/JAR identity is authoritative for installed presence/version. A stale Notion property currently labels the mod `Removido`, but the physical modlist contains the 2.7.6 JAR; the catalog therefore treats Ars Technica as installed until the physical pack changes.

## Exact source checkpoint

Provider source:

`zeroregard/Ars-Technica@bf34b58ff8908837e5894dee773d3afbd98aa3e3`

That branch head declares:

- `mod_version=2.7.6`;
- `mod_id=ars_technica`;
- Minecraft 1.21.1;
- NeoForge 21.1.205;
- Ars Nouveau 5.11.0.1267;
- Create 6.0.8.

The physical pack uses newer host versions (Ars Nouveau 5.13.1 and Create 6.0.10), so source-catalog completeness does **not** equal installed runtime compatibility PASS.

For the exact Ars dependency build used by the provider, `5.11.0.1267` was published from the successful upstream publication run on `baileyholl/Ars-Nouveau@f89dacc5d7467aae8497d98e95dad8347a8d7d21`. That source is used only where exact inherited Ars behavior is required, such as `Insert` inheriting Tier I from `AbstractSpellPart.defaultTier()`.

## Provider role

Ars Technica is a real Ars Nouveau ↔ Create bridge plus its own technomancy content. It is not interchangeable with Ars Creo:

- Ars Technica adds spell parts, Create-like magical processing, Source→kinetic conversion, equipment, Pressure/backtank integration, Transmutation Focus and Ars/Create block adaptations;
- Ars Creo primarily exposes Ars systems on Create contraptions and occupies a different integration surface.

Similarity is not treated as equivalence; each provider remains independently authoritative for its actual hooks.

## Closed catalog surface

### Spell parts — 11/11

Production registry and exact source defaults are in [`GLYPHS.md`](GLYPHS.md):

1. Carve
2. Pack
3. Polish
4. Obliterate
5. Press
6. Superheat
7. Fuse
8. Whirl
9. Insert
10. Telefeast
11. Apply

The catalog includes tier, mana, school, compatible augments, provider limits and concrete Create-processing semantics for every registered part.

### Acquisition — 11/11 glyph recipes

[`ACQUISITION.md`](ACQUISITION.md) records every generated Ars glyph-learning recipe plus the major Enchanting Apparatus acquisition paths for Technomancy equipment/infrastructure.

### Registries

[`REGISTRIES.md`](REGISTRIES.md) closes:

- 3 blocks;
- 3 block entities;
- 8 misc entity types;
- 12 armor pieces across 3 families;
- one Ars perk, `thread_pressure`;
- 3 persistent provider data components;
- current item/equipment surface and old Runic Spanner migration alias.

### Equipment and perks

[`EQUIPMENT-PERKS.md`](EQUIPMENT-PERKS.md) records:

- Technomancer, Artificer and Machinaguard armor behavior;
- Manipulation mana discounts and school-power differences;
- Ars perk-provider layout on all 12 pieces;
- exact Pressure Thread air generation/cap/depletion and Create backtank bridge;
- Transmutation Focus Fortune/processing behavior;
- Schematicannon proximity acceleration.

### Provider systems

[`SYSTEMS.md`](SYSTEMS.md) closes the major authority/resource surfaces:

- Source Motor Source-cost formula and Create stress/RPM conversion;
- Precise Relay and Ars Rune custom cooldowns;
- Transmutation Turret Source settlement + Ars `TileCaster` execution;
- Fuse/Arcane Fusion item/fluid processing and bounded output placement;
- Whirl processing families;
- Apply/Insert/Telefeast inventory/fluid/world mutation boundaries;
- source-default COMMON config values.

### Mixins and networking

[`MIXIN-NETWORK-BOUNDARIES.md`](MIXIN-NETWORK-BOUNDARIES.md) classifies:

- 18/18 declared mixins — 12 common + 6 client;
- 5 registered payload types across Create/Catnip and NeoForge/Ars-style registration;
- client presentation surfaces versus server gameplay paths;
- two client→server cooldown handlers where explicit range/distance/ownership validation is not visible in the audited source and therefore remains a runtime/security QA item.

## Critical deduplication consequences

Ars Nouveau owns:

- player mana;
- Source capability/network;
- spell recipe/context/resolver;
- glyph configuration/learning;
- Ars armor perk/thread infrastructure.

Create owns:

- kinetic network, speed and stress;
- Create recipe families and machine lifecycle;
- Schematicannon printing/material semantics.

Ars Technica owns the conversion layer it actually implements:

- provider processing entities;
- Source Motor conversion;
- Transmutation Turret Source/cast transaction;
- Pressure reserve/backtank bridge;
- Transmutation Focus processing modifiers;
- provider-specific rune/relay/wrench adaptations.

Black Arcana therefore must not:

- create a second Ars mana, Source, pressure/air or Create kinetic balance;
- replay Create recipe outputs or chance rolls;
- count provider child entities/resolvers as independent user casts;
- duplicate Transmutation Focus Fortune/yield behavior;
- replay Source Motor or Transmutation Turret resource settlement;
- infer a Chaos/Order/Technomancy gap merely because Black Arcana could present the same processing with different VFX.

Black Arcana remains authoritative only for Black Arcana-owned casting, hazards, Corruption, Strain, Arcane Danger and destructive effects through its own `WorldEffectPolicy`.

## Source observations carried into runtime QA

1. Ars Technica 2.7.6 was built against Ars 5.11.0.1267 and Create 6.0.8; the pack is newer on both hosts.
2. Multiple concrete mixins target Ars/Create implementation classes, so version ranges do not prove binary/semantic compatibility.
3. Normal Rune/Relay UIs constrain cooldown values, but exact server handlers do not show their own range/distance/ownership validation before mutating a matching BE.
4. Schematicannon acceleration performs a local ServerPlayer AABB lookup from the machine tick path while enabled; large-pack performance remains a QA concern, not an inferred failure.
5. Fuse can place result fluids into world blocks under provider config. This is provider-owned behavior and does not relax Black Arcana's own world-safety policy.

## Provenance

The exact provider repository has conflicting license signals:

- `neoforge.mods.toml`: `GNU Lesser General Public License v3.0`;
- root `LICENSE`: GNU GPL v3 text.

Phase 2V uses source read-only for factual interoperability/cataloging. No upstream Java implementation, texture, model, sound, animation or other asset is copied/adapted into Black Arcana. Future source/asset reuse remains fail-closed until license/provenance is resolved.

## Remaining validation

The source catalog is complete enough for Phase 2 deduplication, but the following remain explicitly open:

- compare real generated/installed Ars Technica COMMON config against source defaults;
- verify the 11 glyph registrations and learning datapack entries in the installed JAR/runtime;
- full-pack Ars 5.13.1 / Create 6.0.10 mixin compatibility;
- Source Motor Source/stress/save-reload behavior;
- Pressure/backtank equip/unequip/death/dimension behavior;
- Transmutation Turret exactly-once Source/cast behavior;
- Fuse/Whirl/Apply/Insert/Telefeast item/fluid conservation under current addons;
- Rune/Relay/Source-Motor packet validation in multiplayer;
- Schematicannon cadence/material conservation and performance;
- dedicated-server/client interoperability.

None of those runtime checks are reported as PASS by this documentation checkpoint.