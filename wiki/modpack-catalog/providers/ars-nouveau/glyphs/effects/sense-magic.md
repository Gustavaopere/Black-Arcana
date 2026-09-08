# Ars Nouveau — Sense Magic

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

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

## Authority / deduplication

Ars Nouveau owns this magical sensing/reveal capability. Black Arcana Familiars & Divination must provide a materially distinct forbidden/divinatory contract rather than duplicate Magic Find.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectSenseMagic`).
