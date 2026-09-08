# Ars Nouveau — Flare

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_flare`
- Display name: Flare
- School: Elemental Fire
- Default tier: 2
- Default mana cost: 40
- Compatible augments: Amplify, Dampen, AOE, Fortune, Randomize
- Source default base damage: 7
- Source default Amplify damage scalar: +3
- Default Amplify limit: 2

## Provider-native behavior

Flare only damages living targets already burning, standing in fire, or carrying Ars' Blasting effect. Successful use spawns damaging Cinder entities around the target; block casts can trigger from nearby fire. If the target has Blasting, Flare removes that effect and immediately detonates the provider Blasting explosion at increased strength. AOE increases the number of spawned Cinders. Cinders use Mage Fire and do not spread normal fire to terrain.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:flint_and_steel` ×2 + `minecraft:fire_charge` ×2 + `minecraft:blaze_rod`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Flare occupies conditional fire detonation/cinder territory. Black Arcana Black Flame content must not be a cosmetic copy of this ignition-conditioned burst or duplicate Blasting settlement.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectFlare`).
