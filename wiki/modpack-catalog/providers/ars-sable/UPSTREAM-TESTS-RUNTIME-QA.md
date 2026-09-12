# Ars Sable — upstream test evidence and runtime QA

Status: `UPSTREAM TEST SURFACES INVENTORIED / CURRENT PACK NOT VALIDATED`

## Exact upstream GameTest classes

The exact 1.1.2 source tree includes four GameTest classes:

1. `PlanariumPosTests`
2. `StorageLecternTests`
3. `TrackedBlockEntityPosDataTests`
4. `WarpPortalTests`

Their presence is useful provider evidence that position persistence, storage movement and warp/Planarium behavior were explicit upstream concerns. It is **not** evidence that those tests pass against the current Black Arcana modpack, Ars Nouveau 5.13.1 or Sable 2.0.5.

## Release-specific fixes

Commit `1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba` changes the provider to version 1.1.2 and its changelog states:

- Planarium bound connections persist across sublevel assembly;
- warp portals/scrolls are fixed when the target sublevel is unloaded.

These two statements are release-specific source evidence and may be cataloged as intended 1.1.2 behavior. Current-host PASS still requires runtime validation.

## Required current-pack matrix

1. Client startup with Ars Nouveau 5.13.1 + Ars Sable 1.1.2 + Sable 2.0.5.
2. Dedicated-server startup and mixin application.
3. Source Jar inside Sable sublevel: SourceManager sees the original Ars Source exactly once before/after movement.
4. Source balance unchanged by assembly/disassembly/reload except actual Ars consumption/production.
5. Storage Lectern with multiple handlers: assemble, move, disassemble, verify addresses/caches and no duplicate handlers/items.
6. Bookwyrm transfer/navigation against moved storage.
7. Whirlisprig/Wixie behavior in supported sublevel scenarios.
8. Same-dimension Warp Portal into/out of a sublevel.
9. Cross-dimension Warp Portal with projected destination.
10. Warp Scroll + Stable Warp Scroll with unloaded target sublevel.
11. Planarium connection through repeated assembly/disassembly and restart.
12. Mob Jar behavior and client rendering.
13. Flying item/follow projectile crossing supported Sable space without duplicate impact/effect.
14. Scrying/camera client presentation while server position remains authoritative.
15. Save/reload, chunk unload, server restart and Sable object lifecycle.
16. Full-pack interop with other Sable bridges; verify no double projection of the same coordinates.

## Failure posture

Any mismatch in Sable 2.0.5 API/mixin targets is an integration failure, not permission to fabricate a fallback coordinate transformation. Black Arcana remains fail-closed for any future adapter that would depend on Ars Sable internals.
