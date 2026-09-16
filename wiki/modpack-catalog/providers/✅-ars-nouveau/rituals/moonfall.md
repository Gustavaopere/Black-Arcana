# Moonfall

Status: `SOURCE-PINNED 5.13.1 / GLOBAL-TIME RITUAL`

- Registry id: `ars_nouveau:ritual_moonfall`
- Class: `RitualMoonfall`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Moonfall operates on the server Overworld because Ars Nouveau treats time as global. While daytime is before the night threshold, it advances Overworld day time by `100` ticks per ritual tick. It also increments ritual progress once per 20 server ticks.

When progress reaches `18`, it snaps the Overworld to the provider helper's next night time and sends time synchronization packets to Overworld players, then marks the ritual finished.

The provider description is simply: sets the time to night.

## Authority / Black Arcana boundary

Global time mutation belongs to Ars Nouveau for this ritual. Black Arcana must not duplicate the time advance, completion or synchronization merely because it observes ritual completion.

Any future Black Arcana celestial/time ritual must be compared mechanically against Moonfall and remain server-authoritative and bounded rather than becoming a cosmetic duplicate.

## QA

Source lifecycle is pinned to 5.13.1. Runtime interaction with other time-control mods/game rules in the full pack remains pending.