# Ars Nouveau — Exchange

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_exchange`
- Display name: Exchange
- School: Manipulation
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Amplify, Dampen, Pierce, AOE, Randomize

## Provider-native behavior

On entities, Exchange swaps caster and target positions, subject to teleport support/event checks. On blocks, it replaces matching target blocks with block items extracted from the Ars inventory manager while recovering the replaced block through silk-touch-like harvesting semantics. Randomize can select random eligible block items; AOE/Pierce expand the target set.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:emerald_block` + `#c:ender_pearls` ×2.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns both entity-position swapping and this inventory-backed block exchange transaction. Black Arcana should not clone a generic swap spell or double-consume/return blocks when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectExchange`).
