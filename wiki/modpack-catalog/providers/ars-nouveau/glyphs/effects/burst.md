# Ars Nouveau — Burst

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_burst`
- Display name: Burst
- Default tier: 3
- Default mana cost: 500
- Compatible augments: AOE, Sensitive, Dampen
- Default Sensitive limit: 1
- Per-spell occurrence limit: exactly 1
- Default invalid combinations: Linger, Wall
- School: no explicit school override in the inspected class; do not infer one

## Provider-native behavior

Burst resolves the remaining spell across a spherical target set and then cancels the original context. Radius is `int(AOE multiplier) + 3` for entity targeting or `+1` with Sensitive block targeting. Dampen changes the filled sphere into a shell. Each eligible target receives a cloned child context/new resolver. Burst is registered in `EffectReset.RESET_LIMITS`.

## Authority / deduplication

Burst is an Ars spell-composition fan-out runtime. Black Arcana must not route those child executions through a parallel Black Arcana cast pipeline or duplicate resource/effect settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectBurst`).
