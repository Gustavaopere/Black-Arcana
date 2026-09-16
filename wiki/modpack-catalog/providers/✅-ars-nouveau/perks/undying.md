# Undying

- Registry ID: `ars_nouveau:thread_undying`
- Source class: `TotemPerk`
- Minimum slot: Tier 3 (`PerkSlot.THREE`).
- Initial persistent perk tag: `isActive=true`.
- Death trigger: `LivingDeathEvent` for a player with an active Undying holder.
- Provider response: set health to 1, remove all effects, then grant Regeneration 900 ticks amplifier 1, Absorption 100 ticks amplifier 1, Fire Resistance 800 ticks amplifier 0; broadcast entity event 35; set `isActive=false`; cancel death.
- Rearm: `SleepFinishedTimeEvent` sets `isActive=true` for players carrying the perk and persists the updated `ARMOR_PERKS` component.
- Acquisition: Enchanting Apparatus; reagent `ars_nouveau:blank_thread`; Totem of Undying + Phantom Membrane + 2 Abjuration Essence; `sourceCost: 0`.

## Authority / integration

Undying owns its death-cancellation charge, persistent armed state and sleep reset. Black Arcana death interception must never consume or recreate this charge, and competing death-prevention systems require deterministic ordering/deduplication rather than multiple resurrection settlements.

## Evidence state

`SOURCE-PINNED 5.13.1 @ 112920ff774831f204031da75b4c4e73d3765157`.