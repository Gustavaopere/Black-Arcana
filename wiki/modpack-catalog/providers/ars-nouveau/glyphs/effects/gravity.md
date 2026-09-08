# Ars Nouveau — Gravity

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_gravity`
- Display name: Gravity
- School: Elemental Air
- Default tier: 2
- Default mana cost: 15
- Compatible augments: Amplify, Dampen, AOE, Pierce, Extend Time, Reduce Time (`glyph_duration_down`)
- Source default potion duration: 30 s
- Source default Extend Time increment: 8 s

## Provider-native behavior

On blocks, Gravity converts eligible targets into Ars `EnchantedFallingBlock` entities. On living entities without Extend Time it applies immediate downward velocity of `-1.0 - amplification`. With Extend Time it applies Ars' Gravity effect instead; provider documentation states this disables player flight while active and causes rapid falling with doubled fall damage.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:anvil` ×2 + `#c:feathers` ×3.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this gravity/falling control primitive and its falling-block interaction. Black Arcana Space/Displacement or forbidden-control spells must be mechanically distinct and must not replay provider motion/block conversion.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectGravity`).
