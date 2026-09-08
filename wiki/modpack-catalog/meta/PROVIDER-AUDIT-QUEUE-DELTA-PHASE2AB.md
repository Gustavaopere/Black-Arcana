# Provider Audit Queue Delta — Phase 2AB Ars Sable 1.1.2

Status: `EXACT SOURCE CATALOG COMPLETE / CURRENT SABLE 2.0.5 RUNTIME QA OPEN`

This narrow overlay prevails for `ars_sable` until the shared provider queue is regenerated.

| Mod ID | JAR | Version | Updated audit state |
|---|---|---|---|
| `ars_sable` | `ars_sable-1.21.1-1.1.2.jar` | `1.1.2` | `PHASE2AB — EXACT SOURCE-PINNED / 0 SPELLS / 0 GLYPHS / 0 RITUALS / NO GAMEPLAY REGISTRATIONS / 24 COMMON + 5 CLIENT MIXINS / 0 PROVIDER PAYLOADS / SOURCE+STORAGE+WARP+PLANARIUM+ENTITY+CAMERA SPATIAL BRIDGE CATALOGED; SABLE 2.0.5 HOST QA PENDING` |

## Closed

- physical Ars Sable identity/version/hash;
- physical Sable 2.0.5 host identity/version/hash;
- exact official 1.1.2 source commit and tree;
- exact dependency/build pins and LGPLv3 provenance;
- no provider-owned gameplay block/item/spell/glyph/ritual/resource registration;
- 29/29 mixins classified: 24 common + 5 client;
- networking registrar classified: protocol `2`, zero provider-owned payload registrations;
- Source Jar / SourceManager bridge authority;
- Storage Lectern movement/tracking behavior;
- Warp Portal coordinate projection and warp target tracking;
- Warp/Stable Warp, Planarium, selected entity/pathfinding, Mob Jar, camera/render boundaries;
- four upstream GameTest class surfaces inventoried;
- release-specific 1.1.2 Planarium and unloaded-warp fixes recorded;
- Black Arcana authority/deduplication consequences.

## Open

1. Current-pack startup with Ars Nouveau 5.13.1 + Ars Sable 1.1.2 + Sable 2.0.5.
2. All 29 mixin targets under current hosts.
3. Source Jar exactly-once SourceManager visibility and no duplicated Source across movement/reload.
4. Storage Lectern movement, capability-cache rebuild and item/handler deduplication.
5. Bookwyrm/Whirlisprig/Wixie/pathfinding scenarios.
6. Warp Portal same/cross-dimension projection and unloaded-target scroll behavior.
7. Planarium persistence through repeated assembly/disassembly/restart.
8. Mob Jar, flying item/projectile, scrying/camera/render regressions.
9. Save/reload/chunk unload/server restart and full-pack Sable bridge interop.

No runtime PASS is inferred from dependency ranges or upstream source/tests.
