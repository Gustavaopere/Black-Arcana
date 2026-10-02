# Create: Mobile Packages — 0.7.7

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_CREATE_LOGISTICS_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#149**;
- JAR: `create_mobile_packages-1.21.1-0.7.7.jar`;
- mod id: `create_mobile_packages`;
- runtime: `0.7.7`;
- physical SHA-1: `b0eb4d3ae9641c06754b20b9621f23bd607373a8`.

Create: Mobile Packages extends Create High Logistics with Logistics Networks, Bee Ports/Robo Bees, Portable Stock Ticker and Mobile Packager. Those systems are remote logistics and item/package delivery; exact inspection is required before treating any apparently remote action as teleportation or magic.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#540** audits CurseForge project/file `1232978 / 8502329` and hard-gates publisher bytes against the physical fingerprint.

- audit HEAD: `a92c062a6db62170cbfae7a3c2ee98529d5f01fd`;
- exact-artifact run: `37022104060` — **SUCCESS**;
- evidence artifact: `11234006840`;
- evidence digest: `sha256:fbbd9e193c3693be9bf99e5dd70c43263db2aa663a801d9da349b1c76a20c873`;
- publisher SHA-1: `b0eb4d3ae9641c06754b20b9621f23bd607373a8`;
- publisher SHA-256: `353bd6cd1e75f9e85241fb4e7147153d83a983569cb67ca9a6cc4d3fe2da7a80`;
- bytes: `605,614`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-0.7.7-ARTIFACT-AUDIT.md`](EXACT-0.7.7-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact top-level artifact surface contains:

- **233** archive entries;
- **130** top-level provider classes;
- **103** non-class resources;
- **13** `data/create_mobile_packages/**` paths;
- one embedded `create_factory_abstractions-1.21.1-1.6.0.jar` component under jarjar, retained as embedded library rather than a separate top-level provider.

Magic-semantic path counts are zero for:

`spell · magic · ritual · ability · arcane · glyph · summon · soul · teleport · portal · enchant · curse`.

The single lexical `mana` hit is `RoboManager.class`; it is the substring `mana` inside **Manager**, not a mana system.

## Exact interaction surface

Exhaustive signature indexing closes six provider interaction classes:

- `BeePortBlockEntity.use` — Bee Port/logistics menu and membership/access interaction;
- `MobilePackager.use` — package creation/editing menu;
- `LogisticallyLinkedItem.useOn` — binds an item to an existing Create logistics network/frequency;
- `PortableStockTicker.use` / `useOn` — opens stock UI and copies category/link state;
- `StockCheckingItem.use` — validates network tuning before delegating to logistics behavior;
- `RoboBeeItem.use` / `useOn` — places/spawns a provider Robo Bee carrier and optionally transfers a Create package according to provider config.

None establishes a spell/glyph/ritual/arcane action registry. Robo Bee materialization is a logistics-carrier operation backed by provider network state and inventory/package settlement, not a supernatural summon identity.

## Data/acquisition surface

The exact provider data contains ordinary crafting/Curios/entity definitions for Bee Port, Robo Bee, Mobile Packager and Portable Stock Ticker. These are logistics equipment acquisition routes and do not create semantic magic objects.

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Create: Mobile Packages remains authority for logistics networks, membership/ownership, Bee Ports, Robo Bee carriers, Portable Stock Ticker requests, Mobile Packager contents, package delivery and FilterMode behavior. Create remains authority for base package/stock primitives.

Black Arcana records only the semantic classification and must not replay requests, duplicate packages, create a second logistics network, respawn Robo Bees or settle delivery twice.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_CREATE_LOGISTICS_INFRA`.**

Strict semantic delta: **+0**.
