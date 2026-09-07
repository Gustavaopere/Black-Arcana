# Split

- Registry ID: `ars_nouveau:glyph_split`
- Source class: `AugmentSplit`
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`
- Default tier: **3**
- Default mana: **20**

## Source-pinned behavior

Adds additional simultaneous projectiles where a compatible Form implements Split. Projectile explicitly consumes the Split count to create more projectile entities, each carrying the subsequent spell effects.

## Boundary

Ars Nouveau owns Split count, projectile spawning and compatible-glyph rules. Black Arcana projectile counts remain bounded by its own effect/work budgets and must not inherit Ars behavior implicitly.

Status: `SOURCE-PINNED 5.13.1 / RUNTIME+CONFIG QA PENDING`.