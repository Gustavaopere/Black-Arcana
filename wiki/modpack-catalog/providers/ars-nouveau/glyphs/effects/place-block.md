# Ars Nouveau — Place Block

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_place_block`
- Display name: Place Block
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: AOE, Pierce, Randomize, Sensitive
- Default Sensitive limit: 2

## Provider-native behavior

Place Block consumes a block item through the Ars inventory manager and places it using a fake-player placement context. AOE/Pierce expand target coverage; Randomize chooses among eligible block items; Sensitive changes placement facing, and two Sensitive augments invert that facing. NeoForge `BlockEvent.EntityPlaceEvent` is posted before placement.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dispenser`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns the inventory extraction and placement transaction for this spell. Black Arcana must not duplicate block consumption/placement or bypass placement/protection events. Independent Black Arcana block placement remains subject to its own `WorldEffectPolicy`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectPlaceBlock`).
