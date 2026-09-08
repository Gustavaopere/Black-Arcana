# Ars Nouveau — Sense Magic

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_sense_magic`
- Display name: Sense Magic
- School: Abjuration
- Default tier: 2
- Default mana cost: 50
- Compatible augments: Extend Time, Reduce Time (`glyph_duration_down`)
- Source config default duration: 60 s
- Source config default Extend Time increment: 15 s

## Provider-native behavior

Applies Ars' Magic Find effect. Provider documentation states that Magic Find reveals magical mobs by glow within 75 blocks and reveals spells inscribed on Runes. When targeting a block entity implementing `IPedestalMachine`, the spell invokes that provider highlighting path.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `ars_nouveau:dowsing_rod` + `ars_nouveau:starbuncle_shards`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this magical sensing/reveal capability. Black Arcana Familiars & Divination must provide a materially distinct forbidden/divinatory contract rather than duplicate Magic Find.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSenseMagic`).
