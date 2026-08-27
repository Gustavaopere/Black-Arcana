# 04.03 — Area Budgets & Chunk Safety

## Objective
Prevent domain/black-flame/explosion mechanics from creating tick spikes or forced chunk-loading storms.

## Rules
- No automatic loading of arbitrary distant chunks for spell effects.
- Bound blocks/entities processed per tick and total per cast.
- Queue overflow policy explicit: degrade/cancel rather than grow unbounded.
- Spatial work stops when caster/effect is invalid according to definition.

## Acceptance
Stress tests demonstrate bounded queue size and processing cost for worst-case configured radii.
