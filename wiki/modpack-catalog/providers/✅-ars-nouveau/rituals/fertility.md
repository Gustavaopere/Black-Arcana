# Fertility

Status: `SOURCE-PINNED 5.13.1 / BREEDING RITUAL`

- Registry id: `ars_nouveau:ritual_fertility`
- Class: `RitualBreed`
- Source cost declaration: `500`
- Processing cadence: every `200` game ticks
- Radius: `5` blocks
- Local population hard cap: no effect at `20+` nearby animals
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Every 200 ticks, Fertility obtains `Animal` entities inside radius 5. If the local count is at least 20, the work cycle aborts.

Below that cap, each animal not in the provider breeding blacklist is checked for adulthood (`age == 0`) and `canFallInLove()`. Eligible animals are placed into love state through the provider. If at least one animal changes state, the cycle requests Source.

The ritual tooltip independently refreshes the `20+ animals` warning once per second.

## Authority / Black Arcana boundary

Population admission, breeding state and Source use remain Ars Nouveau authority. Black Arcana must not add a second breeding trigger, second Source charge or extra progression credit per animal.

The 20-animal ceiling is part of the provider's bounded operational identity and should not be silently bypassed by integration.

## QA

Source behavior is pinned to 5.13.1. Compatibility with modded animal breeding implementations remains full-pack runtime QA.