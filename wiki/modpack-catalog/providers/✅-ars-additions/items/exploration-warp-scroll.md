# Explorer's Warp Scroll

Status: `SOURCE-PINNED 21.3.0 / LOCATE+TELEPORT SEMANTICS AUDITED / WORLDGEN ACQUISITION PINNED / RUNTIME QA PENDING`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:exploration_warp_scroll`.

## Acquisition

The exact `ars_additions:chests/ruined_portal` loot table contains one Explorer's Warp Scroll. Its `ars_additions:exploration_scroll` loot function preconfigures a structure lookup using a search radius of **100 chunks** and `skip_existing_chunks=true` for the configured structure tag.

The same loot table also contains 1–4 normal Codex Entries and 4–64 Sourcestone.

## Locate state

When a scroll has no valid Warp Scroll destination, use starts an asynchronous locate operation. `LocateUtil` stores a UUID in the `structure_lookup_data` component and tracks the lookup in a bounded Guava cache:

- maximum cache size: **5**;
- expiry after write: **5 minutes**.

`AsyncLocator` uses a fixed thread pool. Server config default is **1 locating thread** and requires a world restart to change.

When the locate succeeds, provider code converts the result to Warp Scroll data. Failure removes the pending lookup and reports failure rather than inventing a destination.

## Teleport/use

Once valid Warp Scroll data exists, normal use delegates to provider `TeleportUtil`, which resolves the target dimension and Ars Portal teleport helper, then consumes one scroll.

When dropped inside an Ars Additions ruined-portal structure, a valid scroll can create an `Explorer's Warp Portal`; successful creation consumes the item through provider teleport-decoration settlement and triggers the corresponding advancements.

## Safety note

The structure locator calls Minecraft/ChunkGenerator locate APIs and may inspect/generate structure-location information outside already-loaded gameplay chunks. This provider behavior must not be imported as a Black Arcana destination-search permission. Black Arcana's own displacement remains bounded by its canonical loaded/safe-destination contracts.

## Authority / deduplication

This item owns its pending lookup UUID, search result, Warp Scroll data and item consumption. Black Arcana must not mirror the lookup cache, duplicate the teleport or award a second cast/proc merely because the destination was located asynchronously.
