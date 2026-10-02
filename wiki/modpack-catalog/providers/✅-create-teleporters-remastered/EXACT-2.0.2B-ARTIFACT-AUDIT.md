# Create Teleporters Remastered 2.0.2b — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / TECHNOLOGICAL TELEPORT SURFACE CLOSED`

## Identity gate

- physical JAR: `createteleporters-remastered-2.0.2b-neoforge-1.21.1.jar`;
- mod id: `createteleporters`;
- embedded/runtime: `2.0.2`;
- publisher label: `2.0.2b`;
- physical SHA-1: `76fe16fb464351859113102477bf91f100984257`;
- publisher: CurseForge project/file `829272 / 8010045`.

NON-MERGE PR #528 final audit run `37011387498` succeeded with exact publisher/physical equality.

- final audit HEAD: `d971064aff1a3932dd6c327ca887fb264942bcd4`;
- artifact: `11227509582`;
- artifact digest: `sha256:14dd965153d8ba06aefe832379e4923a2175140a2c91004906f9df7d5f53691d`;
- publisher SHA-256: `49e26d033f7e7e1ba5f310aae105ca4528362f7946d4f95d809e68ab40a9da10`;
- bytes: `1,886,362`.

## Bounded exact inventory

- archive entries: **431**;
- classes: **150**;
- non-class resources: **281**;
- provider data JSON files: **52**;
- broad teleport/portal/quantum/link/dimension semantic-like paths: **401**.

The broad candidate-path count is a discovery aid, not a semantic-action count.

## Exact magic-registry/resource absence

Archive-wide case-insensitive keyword count:

- spell: **0**;
- magic: **0**;
- ritual: **0**;
- ability: **0**;
- mana: **0**;
- arcane: **0**;
- glyph: **0**.

This does not by itself prove `+0`; it is combined with direct inspection of every player-facing transport seam below.

## Pocket Dimension Remote

Exact `PocketDimensionRemoteItem.use(...)` invokes `PocketDimensionRemoteRightclickedProcedure.execute(...)`.

The exact procedure owns one technological transport lifecycle:

1. reads/writes item `CustomData` and provider pocket bindings;
2. checks the current dimension and provider `PocketDimensionTracker`;
3. can bind/rebind an existing pocket location;
4. can invoke provider `PocketGenProcedure.generateStructure(...)` for the pocket structure;
5. resolves `createteleporters:pocket_dimension` server-side;
6. uses `ServerPlayer.teleportTo(ServerLevel, ...)` for cross-dimension settlement or direct position teleport inside a level;
7. applies provider item cooldown/state.

This is a concrete player-activated teleport action but remains technological item infrastructure rather than a supernatural/spell identity under the catalog metric.

## TP Link / Advanced TP Link

Exact item `use(...)` methods delegate to provider right-click procedures. Their bytecode persists coordinates/dimension/link fields such as linked X/Y/Z/dimension/yaw and validates endpoints. `BindCustomPortalProcedure` links Custom Portal Base endpoints and writes portal-link state.

These surfaces configure the teleport network. Binding/linking is setup state and does not become an independent magic identity.

## Custom/Quantum portal surfaces

The exact artifact contains the Custom Portal Base, Quantum Casing, Quantum Portal blocks, portal validators, portal-link logic and integrations with Sable/Aeronautics/Immersive Portals. These are multiblock/transport lifecycle surfaces.

Portal activation/traversal is infrastructure owned by the provider and its integrations; there is no provider spell/ritual registry behind it.

## Machine transfer surfaces

Entity Teleporter, Item Teleporter and Block Teleporter are server-tick/GUI machine surfaces. Their transfer behavior is technological transport and is not a player-acquired supernatural action roster.

## Semantic disposition

Exact-current semantic magic objects: **0**.

State: **`ZERO_SEMANTIC_TECH_TELEPORT_INFRA`**.

Pocket Dimension Remote, TP Links and portal machinery remain fully cataloged as excluded cross-domain transport surfaces so future audits do not accidentally count teleportation-by-name as magic.

## Clean-room boundary

The durable catalog retains hashes, counts, identifiers and behavior-level control-flow classification needed for cataloging/interoperability. It does not redistribute the JAR, source implementation bodies or assets.
