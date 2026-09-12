# Ars Sable — mixin and network boundaries

Status: `29/29 EXACT 1.1.2 MIXINS CLASSIFIED / PROVIDER NETWORK REGISTERS ZERO PAYLOADS`

## Required mixin config

Exact `ars_sable.mixins.json` is `required=true`, declares `compatibilityLevel=JAVA_17`, and contains exactly 29 entries: 24 common + 5 client-only. The Java compatibility declaration is recorded as source fact; the Black Arcana environment remains Java 21.

### Common — 24

1. `sable.SubLevelAssemblyHelperMixin`
2. `camera.ICameraMountableMixin`
3. `camera.ScryerCameraMixin`
4. `camera.SubLevelTrackingSystemMixin`
5. `entity.EntityFlyingItemMixin`
6. `entity.BookwyrmSublevelTrackingMixin`
7. `entity.EntityFollowProjectileMixin`
8. `entity.WhirlisprigSublevelTrackingMixin`
9. `entity.WixieSublevelTrackingMixin`
10. `mob_jar.MobJarTileMixin`
11. `pathnavigate.AbstractPathJobMixin`
12. `pathnavigate.AdvancedNavigateMixin`
13. `pathnavigate.BookwyrmRandomStorageVisitGoalMixin`
14. `pathnavigate.BookwyrmTransferGoalMixin`
15. `planarium.DimBoundaryMixin`
16. `planarium.PlanariumTileMixin`
17. `source_jar.SourceJarMixin`
18. `storage.CraftingLecternBlockMixin`
19. `storage.StorageLecternTileMixin`
20. `util.BlockPosUtilMixin`
21. `util.ParticleUtilMixin`
22. `warp.PortalTileMixin`
23. `warp.StableWarpScrollMixin`
24. `warp.WarpScrollMixin`

### Client-only — 5

25. `camera.CameraControllerMixin`
26. `camera.ClientHandlerMixin`
27. `render.ArcanePedestalRendererMixin`
28. `render.MobJarRendererMixin`
29. `render.PlanariumRendererMixin`

The common/client split is part of the dedicated-server compatibility surface and must be preserved during runtime QA.

## Networking

Exact `ACNetworking.register` obtains payload registrar protocol `2` and registers no Ars Sable-owned payload type. The class also exposes generic forwarding/handling helpers for existing payloads, but those helpers do not mint provider-owned packet identities.

Provider-owned payload count at this source checkpoint: **0**.

Ars packets altered or forwarded through provider bindings remain Ars-owned. Black Arcana must not infer a second teleport/cast authority from packet forwarding or client coordinate presentation.

## Runtime risk under Sable 2.0.5

The source build pin is Sable `1.2.2`, while the physical host is `2.0.5`. Runtime validation must therefore cover common mixin application, server-only classloading, Sable lifecycle/event/helper compatibility, persistent spatial recovery, Ars `5.13.1` target drift and Sable `2.0.5` method/event/signature drift.

No successful loader range check is promoted into runtime PASS.

## Black Arcana boundary

Do not bind BA directly to these mixins as stable APIs. Do not make client camera/render projection authoritative. Do not issue duplicate teleports, Source transactions, inventory transfers or projectile effects after provider settlement. Any future provider boundary must be proven against the exact host and fail closed if the seam is unavailable.
