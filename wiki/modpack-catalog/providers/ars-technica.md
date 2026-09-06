# Ars Technica

Status: `PHASE 2 — CURRENT 2.7.6 PUBLIC CAPABILITIES NORMALIZED; EXACT REGISTRY/BALANCE FIELDS PARTIAL`

## Runtime identity

- Mod id: `ars_technica`
- Current JAR: `ars_technica-1.21.1-2.7.6.jar`
- Runtime version: `2.7.6`
- Loader/game: NeoForge 1.21.1
- Phase 2 class: `ARS GLYPH / SYSTEM PROVIDER`

Ars Technica is content built around Ars Nouveau + Create. It is distinct from Ars Creo: Technica adds player-facing transmutation/processing glyphs, equipment and conversion infrastructure, while Creo focuses on making Ars systems work on Create contraptions.

## Current publicly documented glyph capabilities

| Glyph/capability | Verified semantic behavior |
|---|---|
| Whirl | Create-style processing/transmutation capability; current public docs associate the addon’s transmutation focus with mechanical processing. |
| Obliterate | Current glyph name verified; exact 2.7.6 quantitative semantics remain to be normalized. |
| Press | Current glyph name verified; Create-press-style processing family. |
| Pack | Condenses a 2×2 crafting pattern; Augment expands to 3×3; Dampen reduces to 1×1. |
| Carve | Converts appropriate blocks to stair-like variants; Augment changes to walls and Dampen to slabs. |
| Insert | Moves nearby items into target containers; AOE affects range, Split changes distribution, and item frames can act as filters. |
| Polish | Sandpaper-style refinement/polishing capability. |
| Telefeast | Consumes an eligible food/potion or compatible liquid from the target inventory/tank; configuration influences allowed behavior. |

The provider’s public 1.21.1 migration/changelog history also names `Fuse` and `Superheat` in the current line. This pass records the names but does not invent their exact 2.7.6 formulas or costs.

## Equipment and infrastructure

### Runic Spanner

Public documentation describes a utility tool that can set cooldown behavior for Runes/Relays and can pick up compatible Ars blocks such as turrets, pedestals and containment jars when used with the documented modifier interaction.

### Thread of Pressure

Armor-thread integration with Create’s backtank/air capability. It is not a second breathing resource.

### Spy Monocle

Curios head equipment exposed by the addon. Exact combat/stat semantics are not inferred beyond current public documentation.

### Focus of Transmutation

The current public documentation describes higher luck, faster Whirl-related processing and improved chance-based outputs for Create Haunting/Washing while the focus is active.

### Source Motor

Converts Ars Source into Create kinetic output. RPM, stress capacity and Source consumption are configuration-dependent. This is a provider-owned resource conversion and cannot be treated as free SU or free Source.

### XP gems

The current public documentation lists 48-XP and 192-XP gems. Optional liquid-Source processing may interact with Starbunclemania where the configured integration exists.

## Deduplication / authority

Ars Technica already covers a broad `magic → Create processing` bridge:

- manual magical execution of Create-like processes;
- magical item insertion/logistics;
- Source-to-kinetic conversion;
- backtank/air integration;
- Create-compatible transmutation equipment.

A future Black Arcana technomancy spell cannot be approved merely because it performs Press/Whirl/Polish-style processing with darker VFX. It must prove a distinct gameplay delta.

Provider-native invariants:

- Ars Nouveau owns Source and glyph execution;
- Create owns kinetic/stress semantics;
- conversion must settle exactly once through the provider’s own path;
- Black Arcana must not synthesize Source, SU, outputs or chance rolls around this integration;
- unknown formulas/registry IDs remain `UNVERIFIED`/fail-closed.

## Provenance / confidence

- Presence/version: current 2026-09-06 modlist — HIGH.
- Pack/Carve/Insert/Polish/Telefeast and equipment semantics: current public Ars Technica 2.7.6 project documentation — HIGH at feature level.
- Additional current-line glyph names from public 1.21.1 migration history — HIGH for identity; exact 2.7.6 values remain pending.
- No Java bytecode was decompiled.
