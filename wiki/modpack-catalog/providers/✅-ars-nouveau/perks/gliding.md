# Gliding

- Registry ID: `ars_nouveau:thread_gliding`
- Source class: `GlidingPerk`
- Minimum slot: Tier 3 (`PerkSlot.THREE`).
- Core condition: `EffectGlide.canGlide(entity)` returns true when the entity has Ars' Glide effect **or** owns at least one Gliding perk.
- Player tick integration: when Caelus is loaded and `canGlide(player)` is true, Ars calls its `CaelusHandler.setFlying(player)` path.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; 2 `ars_nouveau:air_essence` + 1 `minecraft:elytra`; `sourceCost: 0`.

## Authority / integration

Gliding is Ars-owned mobility capability and depends on the provider's Caelus integration path. Black Arcana must not create a second elytra/glide authority for this perk or charge a second resource for the same movement state.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`. Runtime modpack QA remains appropriate for Caelus presence/behavior.