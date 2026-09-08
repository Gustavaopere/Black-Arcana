# Flight

Status: `SOURCE-PINNED 5.13.1 / RANGE-EFFECT RITUAL`

- Registry id: `ars_nouveau:ritual_flight`
- Class: `RitualFlight`
- Effect: provider `FLIGHT_EFFECT`
- Effect duration per application: `60 × 20 = 1200 ticks`
- Range: `60` blocks
- Source cost declaration: `200`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native lifecycle

`RitualFlight` extends Ars Nouveau's `RangeEffectRitual`. A player is eligible only server-side, within range, and while the ritual is not already waiting for Source. When `attemptRefresh` successfully applies the effect, the ritual marks itself as needing Source.

The ritual also exposes a jump-event path: when a `ServerPlayer` jumps without the Flight effect, it attempts to refresh/apply the ritual effect. Successful application synchronizes the player's prior flight state through `PacketUpdateFlight`.

## Authority / Black Arcana boundary

Flight capability, effect refresh and Source debit are Ars Nouveau authority. Black Arcana must not grant a second flight state, consume another resource or convert every jump into a new cast/mastery event.

This provider capability is distinct from Black Arcana mobility spells and from external glider/stamina systems; integration requires a real semantic boundary rather than presentation matching.

## QA

Source lifecycle is pinned to 5.13.1. Interaction with other flight providers, ability modifiers and full-pack movement systems remains runtime QA.