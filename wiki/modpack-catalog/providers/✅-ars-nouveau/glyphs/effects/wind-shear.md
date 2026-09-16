# Ars Nouveau — Wind Shear

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_wind_shear`
- Display name: Wind Shear
- School: Elemental Air
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Dampen, Amplify, Randomize
- Default Amplify limit: 2
- Source default base damage: 5
- Source default Amplify scalar: +2.5

## Provider-native behavior

Wind Shear only resolves damage when the target is airborne. The executable source counts open blocks beneath the target up to 10 and uses that count directly in `base damage + amplify scalar * amplification + counted blocks`; grounded targets take no spell damage. The same config class also declares an `airDamage=0.75` field, but the inspected execution path does not use that field in this calculation, so runtime/config QA remains explicit.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:iron_sword` ×3.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this airborne-height damage primitive. Black Arcana aerial control/damage should not clone the same conditional curve or assume the apparently unused config field is authoritative runtime behavior.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectWindshear`).
