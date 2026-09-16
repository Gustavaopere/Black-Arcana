# Sunrise

Status: `SOURCE-PINNED 5.13.1 / GLOBAL-TIME RITUAL`

- Registry id: `ars_nouveau:ritual_sunrise`
- Class: `RitualSunrise`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Sunrise operates on the server Overworld because Ars Nouveau treats time as global. While the world is outside the provider's daytime target window, it advances Overworld day time by `100` ticks and synchronizes time packets to Overworld players.

Once per 20 server ticks it also increments ritual progress. At progress `18`, it snaps the Overworld to the provider helper's next day time, synchronizes clients and marks the ritual finished.

Provider description: sets the time to day.

## Authority / Black Arcana boundary

Time mutation and synchronization are Ars Nouveau authority for this ritual. Black Arcana must not reapply them or credit repeated time packets as separate magical actions.

Any independent Black Arcana solar/time ritual must occupy a distinct semantic role and remain server-authoritative/bounded.

## QA

Exact source lifecycle is pinned to 5.13.1. Interaction with other global time-control providers remains full-pack runtime QA.