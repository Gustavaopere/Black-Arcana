# Nexus Warp Scroll

Status: `SOURCE-PINNED 21.3.0 / BINDING SEMANTICS AUDITED / STRUCTURE ACQUISITION PINNED / NORMAL RECIPE UNPROVEN`

Exact source pin: `Jarva/Ars-Additions@91f102a90dc058cf40e4eac5a67a881e48b856b4`.

Registry id: `ars_additions:nexus_warp_scroll`.

`NexusWarpScroll` extends Ars Nouveau `StableWarpScroll`.

## Binding

Server-side use on an Ars Additions Warp Nexus calls `LocateUtil.setScrollData`, writing a stable Ars `WarpScrollData` destination from the clicked Nexus position/dimension.

The item deliberately disables the parent dropped-item update path by returning false from `onEntityItemUpdate`.

## Structure acquisition

The exact 21.3.0 worldgen processor for both the Nexus Tower and Arcane Library constructs an ItemStack containing one `ars_additions:nexus_warp_scroll` as part of provider Warp Nexus structure state. This proves structure/worldgen presence.

The current source pass did not find a normal crafting recipe for Nexus Warp Scroll; ordinary player acquisition outside those structure flows remains `UNPROVEN`.

## Warp Nexus use

Warp Nexus accepts provider Warp Scroll entries through its 9-slot player attachment. Teleport settlement is described in [`../systems/warp-and-nexus.md`](../systems/warp-and-nexus.md).

## Authority / deduplication

The scroll is provider destination data, not a Black Arcana teleport token. Its binding and eventual teleport must remain Ars-owned; Black Arcana must not copy the destination into a separate portal ledger or charge a second resource transaction.
