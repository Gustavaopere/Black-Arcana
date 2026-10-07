# Ice And Fire: Dread Land — 0.1.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 1 SUPERNATURAL PORTAL-ACTIVATION ROOT / 1 COUNTED_EXACT / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority:

- physical row: **#318**;
- JAR: `iceandfire_dreadland-0.1.2.jar`;
- mod id: `iceandfire_dreadland`;
- runtime: `0.1.2`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `1790b22e21c69485d582b9da50174339a9dc994c`;
- required current hosts: Ice And Fire CE 2.1.2 + Jupiter 2.3.7.

Dread Land is cross-domain for the magic catalog: the sibling classifies it as worldgen/exploration/RPG, but the exact installed artifact owns a deliberate key-driven dimensional portal activation.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#513** audits the exact current publisher artifact and hard-gates it against the physical pack fingerprint.

Final exact progression audit checkpoint:

- audit HEAD: `f5e95a4b7c7095e0c10e8998ca33346593201ad3`;
- exact-artifact run: `36953394134` — **SUCCESS**;
- evidence artifact: `11204564418`;
- evidence digest: `sha256:60f2af0bc1ae7eaa44e30372eaeb3ce9a834bb3789c80d6efafed116031048af`;
- CurseForge project/file: `1664091 / 8708824`;
- publisher SHA-1: `1790b22e21c69485d582b9da50174339a9dc994c`;
- publisher SHA-256: `110090646adbda8d5dc5f6cdd1cef17ea6b5c37a01e05d93909c9e5a600a8db4`;
- bytes: `680,235`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1.

The exact artifact contains **303 archive entries / 32 classes / 271 non-class resources / 197 provider-data paths**. Only three top-level item classes and three block classes exist; exhaustive activation indexing finds player-use surfaces only on Dread Queen Portrait and Dreadland Key.

See [`EXACT-0.1.2-ARTIFACT-AUDIT.md`](EXACT-0.1.2-ARTIFACT-AUDIT.md).

## Semantic-magic result — 1 exact root

### Dreadland Key — Dread Portal Activation

The exact `DreadlandKeyItem.useOn` path establishes one deliberate provider-owned magical action:

1. player uses `iceandfire_dreadland:dreadland_key` on a block accepted by the provider `dreadland_portal_frame` tag;
2. provider searches the adjacent frame for a valid empty Dread Portal shape;
3. on the server, a valid shape is filled with provider `DREAD_PORTAL` blocks;
4. one Dreadland Key is consumed unless the player has creative instabuild;
5. the created portal's provider lifecycle later transports living entities between the Overworld and `iceandfire_dreadland:dreadland`.

The portal travel itself is downstream lifecycle of the one activation root, not a second spell/action identity.

Object card: [`actions/DREAD-PORTAL-ACTIVATION.md`](actions/DREAD-PORTAL-ACTIVATION.md).

Individual action card: [Dreadland Key — Dread Portal Activation](actions/dreadland-key-dread-portal-activation.md).

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Exact progression / acquisition closure

The exact JAR closes the whole normal key progression:

- `fireland_key` is guaranteed in the Fire Dragon trial-spawner reward table;
- `iceland_key` is guaranteed in the Ice Dragon trial-spawner reward table;
- `lightning_key` is guaranteed in the Lightning Dragon trial-spawner reward table;
- ominous variants also guarantee the corresponding realm key;
- exact shapeless recipe `iceandfire_dreadland:dreadland_key` combines the three realm keys into one Dreadland Key.

The exact portal-frame tag accepts seven current Ice And Fire Dread Stone block variants:

- `iceandfire:dread_stone`;
- `iceandfire:dread_stone_bricks`;
- `iceandfire:dread_stone_bricks_chiseled`;
- `iceandfire:dread_stone_bricks_cracked`;
- `iceandfire:dread_stone_bricks_mossy`;
- `iceandfire:dread_stone_tile`;
- `iceandfire:dread_stone_face`.

These are host-owned Ice And Fire blocks; Dread Land consumes the host block tag contract rather than re-owning those materials.

## Config gate disposition

Exact common config exposes `portalTeleportTick` and `lightningDestructive`. No boolean registration/activation gate removing Dread Portal creation was observed in the exact artifact.

`portalTeleportTick` changes delay only; it does not remove the semantic identity.

## Excluded surfaces

- Fireland/Iceland/Lightning Keys — progression ingredients only; plain `KeyItem` classes with tooltip behavior and no activation method;
- Dread Queen Portrait — one 3×3 decorative block-placement action using painting-place behavior; not a magical semantic action;
- portal blocks, particles, block entity, portal-shape validation and dimension transition ticks — infrastructure/downstream lifecycle of Dread Portal Activation;
- Scribe Dread Shard→base-Ice-And-Fire Dread Key trade — adventure/progression support and not a Dread Land magic action;
- environmental lightning/weather behavior — world/environment state, not player-selected magic.

## Authority boundary

Ice And Fire: Dread Land remains authority for frame validation, key consumption, portal block creation, portal delay, dimension transition, Dreadland exit-portal creation, structures/trial rewards and realm progression. Ice And Fire CE remains authority for its Dread Stone frame blocks and other host content.

Black Arcana catalogs the one action identity only. It must not create a second portal, consume a second key, duplicate dimension transfer or reinterpret individual portal ticks as separate magic.

## Runtime QA remains separate

Catalog closure does not assert the early-alpha addon is fully stable in the assembled pack. Later QA still includes portal round-trip safety, death/reconnect in Dreadland, multiplayer activation, structure/trial generation, reward settlement, world-save migration and Ice And Fire/Jupiter compatibility.

## Result

**✅ Cataloged — `COUNTED_EXACT`.**

Current Dread Land semantic inventory: **1 exact-current supernatural portal-activation action**.

Strict semantic delta: **+1**.
