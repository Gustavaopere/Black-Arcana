# Create: Mobile Packages 0.7.7 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / SEMANTIC MAGIC DENOMINATOR CLOSED AT ZERO`

## Identity gate

- physical JAR: `create_mobile_packages-1.21.1-0.7.7.jar`;
- mod id: `create_mobile_packages`;
- runtime: `0.7.7`;
- physical SHA-1: `b0eb4d3ae9641c06754b20b9621f23bd607373a8`;
- CurseForge project/file: `1232978 / 8502329`.

NON-MERGE PR #540 / run `37022104060` succeeded with exact physical/publisher equality.

- audit HEAD: `a92c062a6db62170cbfae7a3c2ee98529d5f01fd`;
- evidence artifact: `11234006840`;
- artifact digest: `sha256:fbbd9e193c3693be9bf99e5dd70c43263db2aa663a801d9da349b1c76a20c873`;
- publisher SHA-256: `353bd6cd1e75f9e85241fb4e7147153d83a983569cb67ca9a6cc4d3fe2da7a80`;
- bytes: `605,614`.

## Bounded archive inventory

- entries: **233**;
- top-level provider classes: **130**;
- resources: **103**;
- provider data paths: **13**;
- embedded jarjar entries: **3**, including `create_factory_abstractions-1.21.1-1.6.0.jar`.

Magic-semantic path counts:

`spell=0 · magic=0 · ritual=0 · ability=0 · mana=1 · arcane=0 · glyph=0 · summon=0 · soul=0 · teleport=0 · portal=0 · enchant=0 · curse=0`.

The only `mana` path hit is `de/theidler/create_mobile_packages/robo/RoboManager.class`; this is a lexical substring of `Manager` and does not represent mana.

## Exhaustive activation index

Six provider classes expose methods in the bounded direct-interaction set:

- `BeePortBlockEntity` -> `use`;
- `MobilePackager` -> `use`;
- `LogisticallyLinkedItem` -> `useOn`;
- `PortableStockTicker` -> `use`, `useOn`;
- `StockCheckingItem` -> `use`;
- `RoboBeeItem` -> `use`, `useOn`.

Exact bytecode and release-correlated source identify these as menus, network tuning, stock/package request state and Robo Bee logistics-carrier operations.

`RoboBeeItem.useOn` can instantiate a provider Robo carrier server-side and optionally move an off-hand Create package into that carrier. The action consumes the item and delegates routing/delivery to provider `RoboManager`. It is classified as logistics entity/carrier creation, not a magical summon.

## Exact data surface

The 13 provider data paths include Curios/entity definitions and ordinary recipes for Bee Port, Robo Bee, Mobile Packager and Portable Stock Ticker. No ritual recipe type, spell registry or magic-action data roster is packaged.

## Embedded Factory Abstractions

`create_factory_abstractions-1.21.1-1.6.0.jar` is embedded under jarjar. By project policy it is not materialized as a separate top-level provider unless independently installed. Its presence supports generic logistics abstractions and does not change this provider's magic denominator.

## Semantic result

- standalone spell/glyph/ritual/ability roots: **0**;
- player-owned supernatural action roots: **0**;
- network-link/tuning actions: **EXCLUDED**;
- stock requests/package editing: **EXCLUDED**;
- Robo Bee carrier creation/routing: **EXCLUDED**;
- Bee Port network/menu/filter state: **EXCLUDED**;
- admin/network commands and persistence: **EXCLUDED**.

Disposition: **`ZERO_SEMANTIC_CREATE_LOGISTICS_INFRA`**.

## Clean-room boundary

The durable catalog retains hashes, counts, class/method identifiers and behavior-level classifications required for semantic cataloging. It does not redistribute the JAR, embedded library, implementation bodies, assets or localization prose.
