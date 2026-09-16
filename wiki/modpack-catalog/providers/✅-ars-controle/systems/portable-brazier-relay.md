# Portable Brazier Relay

State: `SOURCE-PINNED 1.6.15 / ORIGINAL-RITUAL RELAY / LOADED-BRAZIER REQUIRED / RUNTIME QA PENDING`

Registry id: `ars_controle:portable_brazier_relay`
Data component: `ars_controle:portable_brazier`
Source checkpoint: `Vonr/Ars-Controle@ecbb83ba512bc9ca7a025556fb9c62dbd32b6430`

## Acquisition

Enchanting Apparatus:

- reagent: `ars_nouveau:brazier_relay`;
- 2 × tag `c:ender_pearls`;
- 2 × `minecraft:popped_chorus_fruit`;
- 2 × `ars_nouveau:manipulation_essence`;
- 1 × `minecraft:nether_star`;
- 1 × `ars_nouveau:wilden_tribute`;
- recipe `sourceCost`: `0`.

## Persistent/network state

`PortableBrazierRelayData` stores:

- optional brazier `GlobalPos`;
- optional relay UUID;
- ritual localization/name string.

The item data is persistent and network synchronized. The linked Ritual Brazier receives provider attachments:

- `ars_controle:relay_uuid`;
- `ars_controle:association` containing the associated player's UUID.

## Eligibility

The relay rejects:

- `ConjureBiomeRitual`;
- `StructureRitual`;
- `FeaturePlacementRitual`;
- any ritual tablet in the provider `ritual_blacklist` item tag;
- rituals with no registered ritual item/tablet mapping.

This is a provider-native fail-closed filter for worldgen/high-risk ritual families.

## Loaded-brazier requirement

`getBrazier()` resolves the target dimension and explicitly requires `targetLevel.isLoaded(targetPos)`. If the chunk is not loaded, it returns no brazier and does not add a chunk ticket.

Therefore the Portable Brazier Relay itself is `NO FORCE LOAD` at the audited 1.6.15 source path.

## Same ritual, moved execution context

The provider does not create a second ritual object.

When a brazier has `relay_uuid`, `RitualBrazierTileMixin` suppresses the brazier's normal `AbstractRitual.tryTick()` call. The relay item's inventory tick can then invoke the same ritual object's tick while carried.

Additional mixins alter the original Ars ritual's contextual access:

- `AbstractRitual.getWorld()` returns the associated player's current level for a relayed ritual;
- `AbstractRitual.getPos()` returns the associated player's current block position;
- Ritual Brazier inventory access can resolve through a `PlayerCaster` for the associated online player;
- `RitualEventQueue` excludes the physical relayed brazier from normal lookup and adds the relayed ritual object back through the provider relay map.

This is strong causal evidence that the relay recontextualizes one Ars ritual rather than duplicating its effect.

## Relay discovery/cache

Provider relay discovery is refreshed at most once per 60 server ticks. It iterates online players and their main inventory item list looking for Portable Brazier Relays with valid data, then maps ritual object -> player.

For an active relayed ritual, the carried item's server inventory tick invokes the ritual tick each tick after the target has been validated/cached. Server stop clears the provider relay cache.

## Boundary

- Ars Nouveau owns ritual identity, Source and ritual effect semantics.
- Ars Controle owns relay association, context substitution and duplicate-tick suppression.
- Black Arcana must treat the relayed effect as the same provider causal ritual, never a second cast/ritual.
- Do not grant extra Mastery, Arcane Danger, Source settlement or proc chains because execution follows the player.
- The relay's world/position substitution does not alter Black Arcana `WorldEffectPolicy` for Black Arcana rituals.

## QA pending

1. Validate representative allowed rituals while moving/dimension-changing.
2. Validate unlink/logout/death/drop behavior and association cleanup.
3. Verify Source/inventory consumption originates exactly once from Ars rules.
4. Verify no duplicate tick/event delivery with the installed Ars 5.13.1 runtime.
5. Confirm blacklist tags after effective datapack reload.
