# Ars Nouveau — Toss

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_toss`
- Display name: Toss
- School: Manipulation
- Default tier: 1
- Default mana cost: 10
- Compatible augments: Extract, Randomize, Dampen, Amplify

## Provider-native behavior

Toss routes items out of the Ars caster inventory. Extract constrains the amount to 1; otherwise source stack size is `64 * 2^amplification`, so Dampen halves and Amplify doubles per step. Randomize changes stack selection. A block target with an item-handler capability receives insertion directly; otherwise the spell spawns item entities at the target.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:dropper`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this inventory extraction/transfer path. Black Arcana must not double-remove, double-insert or duplicate dropped stacks when Ars is causal.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectToss`).
