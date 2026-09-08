# Ars Nouveau — Evaporate

Status: `SOURCE-PINNED 5.13.1 / CLAIM/RUNTIME QA PENDING`

- Registry id: `ars_nouveau:glyph_evaporate`
- Display name: Evaporate
- School: Manipulation
- Default tier: 1
- Default mana cost: 50
- Compatible augments: AOE, Pierce

## Provider-native behavior

Evaporate removes fluid blocks in the affected area and clears the `WATERLOGGED` property on compatible waterlogged blocks. AOE/Pierce expand coverage, and the implementation also checks adjacent directions around each calculated target position.

## Safety note

The inspected `EffectEvaporate` path does not itself show the claim check used by several other Ars block-mutating effects. That absence is recorded as a runtime/full-pack protection QA item rather than silently assuming equivalent protection behavior.

## Authority / deduplication

Ars Nouveau owns this fluid-removal spell. Independent Black Arcana fluid destruction must route through `WorldEffectPolicy`; Black Arcana must not replay an Ars Evaporate mutation.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectEvaporate`).
