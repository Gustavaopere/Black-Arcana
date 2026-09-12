# Ars Sable — mixin and network boundaries

Status: `29/29 EXACT 1.1.2 MIXINS CLASSIFIED / PROVIDER NETWORK REGISTERS NO PAYLOADS`

## Mixin config

`ars_sable.mixins.json` is required and declares compatibility level `JAVA_17`. The project itself targets Minecraft/NeoForge 1.21.1 and the Black Arcana environment is Java 21; the mixin compatibility declaration is recorded as source fact, not treated as a Java runtime failure.

### Common — 24

Assembly/Sable:
1. `sable.SubLevelAssemblyHelperMixin`

Camera/tracking:
2. `camera.ICameraMountableMixin`
3. `camera.ScryerCameraMixin`
4. `camera.SubLevelTrackingSystemMixin`

Entities/projectiles:
5. `entity.EntityFlyingItemMixin`
6. `entity.BookwyrmSublevelTrackingMixin`
7. `entity.EntityFollowProjectileMixin`
8. `entity.WhirlisprigSublevelTrackingMixin`
9. `entity.WixieSublevelTrackingMixin`

Mob Jar:
10. `mob_jar.MobJarTileMixin`

Pathfinding/storage goals:
11. `pathnavigate.AbstractPathJobMixin`
12. `pathnavigate.AdvancedNavigateMixin`
13. `pathnavigate.BookwyrmRandomStorageVisitGoalMixin`
14. `pathnavigate.BookwyrmTransferGoalMixin`

Planarium:
15. `planarium.DimBoundaryMixin`
16. `planarium.PlanariumTileMixin`

Source:
17. `source_jar.SourceJarMixin`

Storage:
18. `storage.CraftingLecternBlockMixin`
19. `storage.StorageLecternTileMixin`

Spatial utilities:
20. `util.BlockPosUtilMixin`
21. `util.ParticleUtilMixin`

Warp:
22. `warp.PortalTileMixin`
23. `warp.StableWarpScrollMixin`
24. `warp.WarpScrollMixin`

### Client-only — 5

25. `camera.CameraControllerMixin`
26. `camera.ClientHandlerMixin`
27. `render.ArcanePedestalRendererMixin`
28. `render.MobJarRendererMixin`
29. `render.PlanariumRendererMixin`

The common/client split is part of the dedicated-server compatibility surface and must be preserved.

## Networking

`ACNetworking.register` creates payload registrar protocol `2` but registers **no Ars Sable-owned payload type** in exact 1.1.2. The class contains generic helper methods for dispatching existing `CustomPacketPayload` objects to tracking players, a player, or the server, plus a generic Ars `AbstractPacket` handler.

Therefore the exact provider-owned payload count for this source checkpoint is `0`, not an inferred list from helper methods.

Ars packets that are modified or forwarded by mixins remain Ars-owned. For example, `PortalTileMixin` adjusts coordinates passed into Ars `PacketWarpPosition`; it does not create a parallel Ars Sable teleport packet authority.

## Runtime risk under Sable 2.0.5

The high mixin count is a concrete compatibility risk because exact source was compiled against Sable 1.2.2. Current runtime validation must cover at minimum:

- all common mixin application at startup;
- server-only classloading without the five client targets;
- Sable sublevel-ready observer event;
- assembly/disassembly hooks;
- projection helper behavior;
- persistent position recovery;
- Ars 5.13.1 method/field signatures;
- Sable 2.0.5 method/event/signature drift.

No successful loader range check is promoted into runtime PASS.

## Black Arcana boundary

- Do not bind BA integrations directly to these mixins as stable APIs.
- Do not make client render/camera projection authoritative for target validation.
- Do not issue duplicate teleports, Source transactions, inventory transfers or projectile effects after provider settlement.
- BA spatial effects must use BA's own bounded server-side contracts; Ars Sable's provider-specific projection adapters do not replace `WorldEffectPolicy` or Stage 07.04 safety.
