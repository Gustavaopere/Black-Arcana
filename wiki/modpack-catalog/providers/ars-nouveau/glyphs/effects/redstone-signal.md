# Ars Nouveau — Redstone Signal

Status: `SOURCE-PINNED 5.13.1 / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_redstone_signal`
- Display name: Redstone Signal
- School: Manipulation
- Default tier: 1
- Default mana cost: 0
- Compatible augments: Amplify, AOE, Dampen, Extend Time, Reduce Time (`glyph_duration_down`), Sensitive
- Source default signal baseline: 10 before Amplify/Dampen, clamped 1..15
- Source default duration: 5 ticks, minimum 2
- Source default duration bonus: 10 ticks per duration multiplier

## Provider-native behavior

Without Sensitive, the spell places a temporary Ars block that mimics a Redstone Block and stores configured power/duration. With Sensitive, it instead records the targeted existing block in `RedstoneSavedData` as a temporary power source and updates neighbors. Placement uses NeoForge entity-place protection events.

## Authority / deduplication

Ars Nouveau owns this temporary redstone-power capability and persistence. Black Arcana must not create a second redstone state ledger or replay provider block updates. Independent Black Arcana world mutations still pass through `WorldEffectPolicy`.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectRedstone`).
