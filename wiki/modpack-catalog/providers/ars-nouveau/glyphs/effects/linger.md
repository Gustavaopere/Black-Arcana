# Ars Nouveau — Linger

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_linger`
- Display name: Linger
- School: Manipulation
- Default tier: 3
- Default mana cost: 500
- Compatible augments: Sensitive, AOE, Accelerate, Decelerate, Extend Time, Reduce Time (`glyph_duration_down`), Dampen
- Default Sensitive limit: 1
- Per-spell occurrence limit: exactly 1

## Provider-native behavior

Linger converts the remaining spell into an `EntityLingeringSpell`: it creates a child `SpellContext`, cancels the original continuation, installs a new resolver and stores AOE, targeting mode, speed, duration and gravity behavior on the lingering entity. Sensitive switches targeting from entities to blocks; Dampen suppresses gravity. Linger is also registered in `EffectReset.RESET_LIMITS`.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dragon_breath` + `#c:storage_blocks/diamond` + `#c:rods/blaze` ×2.
- Source-default recipe XP: **160 XP** (Tier III).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

This is a provider-owned persistent spell-execution runtime, not merely an area effect. Black Arcana must not route Ars lingering execution through a second Black Arcana cast pipeline or duplicate provider costs/effect settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectLinger`).
