# Ars Nouveau — Cold Snap

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_cold_snap`
- Display name: Cold Snap
- School: Elemental Water
- Default tier: 2
- Default mana cost: 30
- Compatible augments: Amplify, Dampen, Extend Time, Reduce Time (`glyph_duration_down`), AOE, Fortune, Randomize
- Default Amplify limit: 2
- Default AOE limit: 1
- Source default base damage: 6
- Source default Amplify scalar: +2.5 damage
- Source default Snare duration: 5 s
- Source default Extend Time increment: 1 s

## Provider-native behavior

Cold Snap only damages living targets that are wet/rained-on, slowed, or already freezing. On success it applies Ars Snare and erupts damaging `IceShardEntity` projectiles around the target. Targets with Ars Freezing are pushed to maximum freeze immediately. Casting on an ice block removes that ice and erupts shards instead. AOE increases shard coverage.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:water_essence` + `minecraft:powder_snow_bucket` + `minecraft:ice`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this condition-gated cold burst, its Snare/Freezing interactions and ice-shard entities. Black Arcana cold/death/control concepts must not clone this wet/frozen-triggered pattern.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectColdSnap`).
