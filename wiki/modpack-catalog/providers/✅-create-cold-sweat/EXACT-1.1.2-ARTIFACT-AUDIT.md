# Create: Cold Sweat 1.1.2 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO SEMANTIC MAGIC BRIDGE`

## Identity gate

- JAR: `create_cold_sweat-1.1.2.jar`;
- mod id: `create_cold_sweat`;
- runtime: `1.1.2`;
- physical SHA-1: `58326378dac966d664ae827dcc76e4b3a284d747`.

NON-MERGE PR #566 audits CurseForge File `1184450 / 7214552` and fails before semantic inspection unless publisher SHA-1 equals the physical fingerprint.

Evidence:

- HEAD: `6095f4ac2be04a369227461d2aac5c1fac7bb547`;
- run: `37172185334` — SUCCESS;
- artifact: `11291667207`;
- digest: `sha256:c4a0294e4f54ef3c7944ff3429947c0458055cb506a137561b0e82c6407299b5`;
- publisher SHA-1: `58326378dac966d664ae827dcc76e4b3a284d747`;
- publisher SHA-256: `7b9260cef82a343e68c7fdbbfd8a955c1cf3bdf1f52b09989ca7971e3cce1224`;
- bytes: `214,958`.

Result: exact physical/publisher equality is proven.

## Complete archive inventory

- entries: **51**;
- classes: **19**;
- resources: **32**;
- provider data paths: **19**;
- semantic-name/path hits: **0**;
- thermal/Create bridge paths: **44**;
- provider JSONs: **13**.

## Complete class surface

The exact JAR contains only:

- `BlockTempRegister`, config/events and mod bootstrap;
- thermal block-effect classes: Blaze Burner, Lit Blaze Burner, Boiler, Encased Fan, Fluid Containers, Pipes/Pumps and Steam Engine;
- block-tag/fluid-temperature datagen;
- heat/tag utilities.

There are no provider item classes, key mappings, packets or player-cast classes in the exact archive.

## Exact runtime seam

`BlockTempRegister` registers provider `BlockTemp` implementations into Cold Sweat's block-temperature registry. Exact bytecode then derives temperatures from Create state, fluid capabilities, kinetic speed and provider config. Encased Fan behavior reads Cold Sweat world temperature and neighboring block/fluid temperature sources; Boiler/containers/pipes/engines remain block-temperature computations.

## Exact data surface

`data/create_cold_sweat/**` contains:

- one fluid-temperature data resource;
- block tags for Blaze Burners, Encased Fans, fluid containers/tanks, pipes and Steam Engines;
- duplicate tag path compatibility between `tags/block` and `tags/blocks` layouts.

No exact provider JSON defines a spell, ritual, glyph, ability or other semantic magic identity.

## Disposition

`ZERO_SEMANTIC_CREATE_THERMAL_BRIDGE`

Strict semantic contribution: **+0**.

## Clean-room boundary

The durable catalog retains hashes, counts, class/resource identifiers and behavior-level classification only. It does not redistribute JAR bytes or implementation bodies.
