# Ars Sable — spatial systems and authority

Status: `EXACT 1.1.2 SOURCE CATALOGED`

## Source Jar / SourceManager

`SourceJarMixin` makes Ars `SourceJarTile` a Sable `BlockEntitySubLevelActor`. During Sable sublevel ticks it creates or renews a `SableSourceProvider` when the previous provider is missing/invalid and registers that provider into Ars `SourceManager`.

`SableSourceProvider` implements Ars `ISpecialSourceProvider` and returns the original `ISourceTile`; it does not duplicate Source. Its validity comes from Sable containment, and `getCurrentPos()` projects the Source Jar's current sublevel position back into world space through `Sable.HELPER.projectOutOfSubLevel`.

Authority consequence: one Ars Source balance remains canonical. Black Arcana must never mirror the Jar balance or debit a second resource for provider-native operations.

## Storage Lectern tracking

`StorageLecternTileMixin` adds a persistent UUID key `ars_sable_tracking_id` and implements provider tracking around Ars storage addresses.

Exact behavior includes:

- save/load tracking UUID;
- restore/sync tracked positions on load;
- sync after first/last connection and handler additions;
- track `mainLecternPos` plus connected handler positions;
- replace stale positions after movement;
- recreate `BlockCapabilityCache<ItemHandler>` for moved handlers;
- deduplicate handler positions;
- clear stale `transferTasks` after a position replacement;
- set Ars `updateItems` and `invalidateNextTick` and invalidate capabilities.

The bridge therefore repairs Ars storage addressing after Sable movement; it does not own stored items or crafting execution.

## Warp Portal projection

`PortalTileMixin` keeps Ars portal semantics but changes coordinate interpretation when Sable sublevels are involved.

Exact 1.1.2 hooks:

1. after `PortalTile.setFromScroll`, track the warp target when dimension/position resolve;
2. same-dimension teleport wraps `Entity.teleportTo` and projects the target through `WarpSableHelper`;
3. cross-dimension teleport replaces the `DimensionTransition` target with the projected position;
4. the Ars `PacketWarpPosition` coordinates are changed to the same projected position sent to the client.

One Ars teleport remains the causal operation. Black Arcana must not issue another teleport after this bridge settles the provider operation.

## Warp Scroll / Stable Warp Scroll

Separate mixins plus `WarpSublevelTargetData` preserve and resolve targets linked to Sable spaces. Release 1.1.2 changelog explicitly fixes warp portals/scrolls sending to the wrong location when the sublevel is unloaded.

This provider tracking is adapter metadata, not a Black Arcana destination registry.

## Planarium

`PlanariumTileMixin`, `DimBoundaryMixin`, `PlanariumHelpers` and persistent tracking data adapt Planarium links to Sable assembly/disassembly. The 1.1.2 changelog explicitly states that Planariums persist bound connections between sublevel assembly cycles.

## Entities and logistics

Exact mixins target:

- Bookwyrm sublevel tracking;
- Bookwyrm random storage visit/transfer goals;
- Whirlisprig tracking;
- Wixie tracking;
- generic Ars path job / advanced navigator integration;
- `EntityFlyingItem`;
- `EntityFollowProjectile`.

Support is targeted, not universal. Do not infer every Ars/addon entity or projectile is Sable-safe.

## Mob Jar, scrying and rendering

Mob Jar tile behavior, Scryer camera/tracking, and client renderers for Arcane Pedestal, Mob Jar and Planarium receive explicit adapters. Client-side visual projection remains presentation only and cannot become Black Arcana targeting/casting authority.

## Persistent adapter state

Exact source contains:

- `SublevelPosData`;
- `TrackedBlockEntityPosData`;
- `TrackedPosIndex`;
- `WarpSublevelTargetData`.

These records map/recover spatial identities and targets needed by the bridge. They do not authorize a second BA copy of Ars Source, inventory, spell state or portal ownership.
