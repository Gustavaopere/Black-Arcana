# Ars Nouveau — Summon Wolves

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_summon_wolves`
- Display name: Summon Wolves
- School: Conjuration
- Default tier: 1
- Default mana cost: 100
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source default duration: 60 s
- Source default Extend Time increment: 60 s

## Provider-native behavior

Summons two tamed `SummonWolf` allies using the biome-appropriate wolf variant. They inherit an initial hostile target from the caster's recent combat state, remain aggressive/tamed, and expire after the configured lifetime. The caster receives Summoning Sickness for the same lifetime.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:conjuration_essence` + `minecraft:bone` ×3 + `ars_nouveau:wilden_wing` ×4.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns these temporary combat summons, ownership, lifetime and Summoning Sickness. They are not Black Arcana familiars and must not be double-counted in a second summon ledger.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSummonWolves`).
