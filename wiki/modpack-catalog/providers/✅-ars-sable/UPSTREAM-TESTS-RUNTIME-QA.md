# Ars Sable — upstream test evidence and runtime QA

Status: `UPSTREAM TEST SURFACES INVENTORIED / CURRENT PHYSICAL PACK NOT VALIDATED`

## Exact upstream GameTest classes

The exact 1.1.2 source tree contains four GameTest classes:

1. `PlanariumPosTests`
2. `StorageLecternTests`
3. `TrackedBlockEntityPosDataTests`
4. `WarpPortalTests`

Their presence is upstream evidence that these spatial behaviors were explicit test concerns. It is **not** evidence that the tests pass against the current Black Arcana modpack, Ars Nouveau `5.13.1` or Sable `2.0.5`.

## Current-pack validation matrix

Runtime closure would require direct validation of at least:

1. client startup with physical Ars Nouveau + Ars Sable + Sable versions;
2. dedicated-server startup and all required common mixin applications;
3. Source visibility exactly once before/after Sable movement, reload and restart;
4. Storage Lectern addressing/cache recovery without duplicate handlers/items;
5. supported Bookwyrm/pathfinding/logistics behavior after movement;
6. same- and cross-dimension Warp Portal projection;
7. Warp Scroll and Stable Warp Scroll behavior with loaded/unloaded spatial targets;
8. Planarium relation recovery through assembly/disassembly and restart;
9. Mob Jar behavior and client rendering;
10. supported flying-item/follow-projectile traversal without duplicate impact/effect;
11. scrying/camera presentation while server state remains authoritative;
12. save/reload, chunk unload, reconnect and server restart lifecycle;
13. full-pack interop with other Sable/Ars compatibility layers, especially double-projection risks.

## Failure posture

Any mismatch in Sable `2.0.5` or Ars `5.13.1` targets is an integration failure. It is not permission to fabricate a fallback coordinate transform or second provider state ledger. A future Black Arcana adapter must use a proven provider-native seam or fail closed.
