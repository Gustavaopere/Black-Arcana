# Phase 2BN — Ars Sable 1.1.2 checkpoint

Status: `EXACT SOURCE CATALOG COMPLETE / ZERO SEMANTIC MAGIC / COMPONENT PROMOTION PENDING SHARED-QUEUE RECONCILIATION / CURRENT-HOST RUNTIME QA OPEN`

Execution branch: `docs/magic-catalog-phase2bn-ars-sable`
Base main at phase start: `f1a5b45c01b7b1175de2f756247e3380eaa522df`
Physical JAR: `ars_sable-1.21.1-1.1.2.jar`
Physical mod id/version: `ars_sable` / `1.1.2`
Physical SHA-1: `df43ad58fb9ca3b7acf7f62dc97ed75fd6da3da8`
Physical CurseForge hash: `2760241931`
Physical Sable host: `sable-neoforge-1.21.1-2.0.5.jar` / `sable` / `2.0.5` / SHA-1 `05f666e973d32baaaf405acb9bbed6615b909971`
Physical Ars Nouveau host: `5.13.1`
Exact official source: `baileyholl/ars-sable@1fd83f3a998e3a41b5a21d0d6529140a0b0a55ba`

## Evidence closed in this tranche

- exact physical Ars Sable and current Sable host identities from the current 595-entry modlist;
- exact official source commit matching provider version `1.1.2`;
- Minecraft `1.21.1`, source runtime range `[1.20.6,1.21.2)`, NeoForge build `21.1.219` / range `[21,)`;
- Ars Nouveau build pin `5.11.7.1354` and Sable build pin `1.2.2`;
- exact role as Ars Nouveau ↔ Sable spatial compatibility infrastructure, not a standalone spell system;
- provider registries structurally exist for blocks/block entities/items, but the exact block-item registration method is empty and no gameplay registration is established by that surface;
- exactly 24 required common mixins + 5 client mixins = 29 direct bindings;
- network registrar protocol `2` with zero Ars Sable-owned payload registrations;
- Source Jar/SourceManager projection, Storage Lectern spatial tracking/rebinding, warp/portal projection, Planarium tracking, selected Ars entity/pathfinding/projectile adapters, Mob Jar, camera/scrying and rendering boundaries;
- four upstream GameTest classes inventoried as upstream evidence only;
- Black Arcana authority, causal deduplication and fail-closed runtime boundaries;
- source license-surface conflict recorded without selecting a permissive interpretation.

## Semantic disposition

Ars Sable contributes **0 independent semantic magic objects** under `SEMANTIC-MAGIC-COVERAGE.md`: no provider-owned spell, glyph, ritual, school, mana/resource or equivalent discrete magical action is established by the exact source audit. The strict semantic minimum therefore remains **1316**.

The component is technically auditable as a zero-semantic bridge. Promotion to component **#62 / 62 of 100** is deliberately left for shared-ledger reconciliation after this branch has current CI evidence.

## License / provenance gate

The exact `gradle.properties` declares `mod_license=LGPLv3`, while the root `LICENSE` at the same commit contains the Unlicense/public-domain dedication. These are conflicting license surfaces. Black Arcana therefore records `LICENSE CONFLICT / REVIEW_REQUIRED` and uses the source read-only for factual interoperability/catalog evidence. No upstream implementation body, assets, localization prose, models or sounds are copied or adapted.

## Current-host QA kept open

1. Source was built against Sable `1.2.2`; the physical pack uses Sable `2.0.5`. The declared `[1.0,)` range is not proof that 29 direct mixin/API bindings remain compatible.
2. Source was built against Ars Nouveau `5.11.7.1354`; the physical pack uses `5.13.1`.
3. Client boot, dedicated-server boot with the installed provider set, all mixin applications, save/reload/restart behavior and full-pack interop are not established by this source audit.
4. Source, Storage Lectern, warp, Planarium, entity/pathfinding/projectile and camera/render scenarios remain runtime QA gates.
5. Missing or changed provider hooks must fail closed; Black Arcana must not fabricate fallback coordinate transforms or duplicate provider state.

## Clean-room boundary

The exact source was inspected only to establish factual provider role, dependency declarations, registry/mixin/network footprint, authority boundaries, test surfaces and compatibility risks. No upstream implementation body or creative asset is copied/adapted into Black Arcana.
