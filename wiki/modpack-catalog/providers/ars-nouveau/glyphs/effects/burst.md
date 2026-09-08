# Ars Nouveau — Burst

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

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

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:tnt` ×5 + `minecraft:firework_star`.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Burst is an Ars spell-composition fan-out runtime. Black Arcana must not route those child executions through a parallel Black Arcana cast pipeline or duplicate resource/effect settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectBurst`).
