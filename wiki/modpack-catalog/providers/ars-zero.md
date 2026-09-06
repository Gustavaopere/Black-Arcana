# Ars Zero

Status: `PHASE 2 — CURRENT 2.0.2 CAPABILITY SURFACE NORMALIZED; EXACT BALANCE/REGISTRY FIELDS PARTIAL`

## Runtime identity

- Mod id: `ars_zero`
- Current JAR: `ars_zero-1.21.1-2.0.2.jar`
- Runtime version: `2.0.2`
- Loader/game: NeoForge 1.21.1
- Phase 2 class: `ARS GLYPH / SYSTEM PROVIDER`

## Multi-phase casting equipment

### Spell Staff

The current public documentation describes a three-phase spell container: begin, tick and end. Each phase can carry up to ten glyph slots and the staff can continuously execute its channel/tick behavior while use is held.

### Psion's Circlet

Tier-3 Curios head equipment using the same begin/tick/end phase model with up to ten glyph slots per phase, triggered through its channel input.

These systems already cover a substantial portion of persistent/channelled and phase-dependent spell sequencing. A Black Arcana design must prove a stronger semantic delta before adding a separate generic “multi-stage cast” engine.

## Current documented glyphs

| Capability | Public semantic role |
|---|---|
| Temporal Context | Form/context primitive for time- or phase-sensitive spell behavior. |
| Near | Form for nearby-context targeting. |
| Push | Forced movement. |
| Select | Selection/context primitive. |
| Conjure Voxel | Creates Ars Zero voxel constructs. |
| Anchor | Anchoring/control primitive. |
| Remove Gravity | Gravity suppression/control. |
| Convergence | Convergence/context primitive. |
| Geometrize | Patterned/geometric application of subsequent spell behavior. |
| Conjure Blight | Blight-oriented conjuration/effect capability. |
| Beam | Beam-form spell delivery. |

The current public 2.0.2 page also lists AOE II/III and Amplifier II/III as disabled-by-default copied compatibility content; they are not treated as unique Ars Zero gaps.

## Geometrize history still relevant to the current line

The public 1.21.1 changelog history for the same provider documents Geometrize augments `Cube`, `Sphere`, `Flatten` and `Hollow`, plus compound uses such as Geometrize + Break and Geometrize + Conjure Terrain. The current 2.0.2 public page still exposes Geometrize itself.

For Phase 2 this proves that generic geometric placement, shape selection and hollow/flatten-style composition are already represented in the installed Ars ecosystem. Exact current registry IDs/costs for each historical augment remain to be normalized before implementation work relies on them.

## Other verified content

- Multi-phase Turret: executes phase-aware Ars Zero spell behavior from a block/turret context.
- Voxel system with documented elemental/material families including Arcane, Fire, Water, Wind, Stone, Ice and Lightning; voxels can participate in environmental interactions and voxel-to-voxel collisions.

## Deduplication impact

Ars Zero materially overlaps these candidate Black Arcana families:

- geometry / patterned placement;
- gravity and forced movement;
- beam delivery;
- blight/corruption-like presentation;
- channelled / multi-phase casting;
- persistent localized constructs.

Overlap of presentation is not equivalence. Black Arcana Corruption remains its own provider-owned danger channel, and an Ars Zero Blight capability must not be silently mapped into Black Arcana Corruption without a verified bridge.

## Authority / fail-closed

- Ars Nouveau/Ars Zero own glyph execution and their spell-container semantics.
- Black Arcana must not re-run a glyph through a second cast path merely to observe it.
- No Black Arcana mechanic may infer corruption, Arcane Strain, mastery or resource settlement from an Ars Zero effect without an explicit causal adapter.
- Unknown numeric/registry details remain fail-closed for implementation.

## Provenance / confidence

- Presence/version: current 2026-09-06 modlist — HIGH.
- Current 2.0.2 equipment/glyph/voxel list: current public project documentation — HIGH at semantic level.
- Geometrize shape augments: public current-line 1.21.1 changelog history — HIGH for feature existence; exact 2.0.2 registry/balance normalization remains pending.
- No Java bytecode was decompiled.
