# Life Drain

- Registry ID: `ars_nouveau:thread_life_drain`
- Source class: `VampiricPerk`
- Minimum slot: Tier 1 (inherited default).
- Trigger: `SpellDamageEvent.Post`.
- Runtime formula in 5.13.1: `healAmount = event.damage * (0.2f * countForPerk(thread_life_drain, caster))`; the caster is healed by that amount after spell damage resolves.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; Mendosteen Pod + Sculk Catalyst + 2 Abjuration Essence; `sourceCost: 0`.

## Authority / integration

This is Ars-owned spell lifesteal on post-damage causality. Black Arcana must not apply an additional generic lifesteal proc to the same Ars spell hit. In particular, Black Arcana Backlash remains excluded from normal offensive proc chains by canonical architecture.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.