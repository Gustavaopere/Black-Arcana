# Challenge

Status: `SOURCE-PINNED 5.13.1 / RAID RITUAL`

- Registry id: `ars_nouveau:ritual_challenge`
- Class: `RitualPillagerRaid`
- Exact release checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Provider-native behavior

Once per 20 server ticks the ritual increments progress. At progress `18`, it looks for `ServerPlayer` entities within an AABB inflated by `5.0` blocks around the ritual and asks the vanilla raid manager to create or extend a raid using the first returned player and the ritual position.

The ritual finishes only when a non-null `Raid` is returned.

### Optional Emerald modifier

Outside Hard difficulty, the ritual accepts exactly one emerald-tag item while its consumed-item list is empty. If that Emerald was consumed and a raid is successfully created, the provider sets `raid.numGroups = 7`.

On Hard difficulty the ritual refuses this optional modifier.

The provider description frames the ritual as summoning an illager raid when used inside a village; the actual village/raid validity remains enforced by the vanilla raid creation path.

## Authority / Black Arcana boundary

Raid creation, player association, raid group count and optional item consumption remain provider/vanilla authority. Black Arcana must not create a second raid, consume another Emerald or re-credit raid waves as separate ritual completions.

## QA

Source behavior is pinned to 5.13.1. Effective interaction with other raid modifiers and full-pack village mechanics remains runtime QA.