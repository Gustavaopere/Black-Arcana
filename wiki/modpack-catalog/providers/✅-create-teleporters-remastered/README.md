# Create Teleporters Remastered — 2.0.2b / runtime 2.0.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_TECH_TELEPORT_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#203**;
- JAR: `createteleporters-remastered-2.0.2b-neoforge-1.21.1.jar`;
- mod id: `createteleporters`;
- embedded/runtime version: `2.0.2`;
- publisher/file label: `2.0.2b`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `76fe16fb464351859113102477bf91f100984257`.

The filename/release label and embedded runtime version are intentionally preserved separately. The current sibling dossier classifies the mod as Create-based technology/exploration infrastructure for item/entity teleporters, TP Links, pocket dimensions and custom portal multiblocks.

## Exact artifact closure

NON-MERGE evidence PR **#528** audits CurseForge project/file `829272 / 8010045` and hard-gates the publisher artifact against the physical fingerprint.

- final audit HEAD: `d971064aff1a3932dd6c327ca887fb264942bcd4`;
- exact-artifact run: `37011387498` — **SUCCESS**;
- evidence artifact: `11227509582`;
- artifact digest: `sha256:14dd965153d8ba06aefe832379e4923a2175140a2c91004906f9df7d5f53691d`;
- publisher SHA-1: `76fe16fb464351859113102477bf91f100984257`;
- publisher SHA-256: `49e26d033f7e7e1ba5f310aae105ca4528362f7946d4f95d809e68ab40a9da10`;
- bytes: `1,886,362`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-2.0.2B-ARTIFACT-AUDIT.md`](EXACT-2.0.2B-ARTIFACT-AUDIT.md).

## Exact semantic conclusion

Create Teleporters contributes **0 independent semantic magic objects** under the Black Arcana catalog metric.

The exact artifact contains **431 archive entries / 150 classes / 281 resources / 52 provider data JSON files**. A direct archive-wide keyword audit closes:

- `spell = 0`;
- `magic = 0`;
- `ritual = 0`;
- `ability = 0`;
- `mana = 0`;
- `arcane = 0`;
- `glyph = 0`.

The large number of `teleport`/`portal`/`dimension` paths belongs to the provider's technological transport system and is not treated as magic by name alone.

## Player-facing transport surfaces

### Pocket Dimension Remote

`PocketDimensionRemoteItem.use(...)` delegates to the provider right-click procedure. Exact bytecode shows provider-owned binding metadata, pocket-dimension generation, lookup of `createteleporters:pocket_dimension`, cross-dimension `ServerPlayer.teleportTo(...)`, same-dimension position teleport and an item cooldown.

This is a deliberate player teleport, but it is implemented and presented as a technological Create transport device/pocket-dimension tool. It does not expose a spell, ritual, glyph, focus, mana action or supernatural ability identity. It is therefore **excluded from the semantic-magic numerator**.

### TP Link / Advanced TP Link

Both items are right-click setup tools that persist coordinates/dimension/link state into item custom data. Exact link procedures validate teleporter/portal endpoints and write provider linkage metadata. They are configuration/binding tools for the transport network, not magic actions.

### Custom Portal / Quantum Portal

Custom Portal Base + Quantum Casing/Quantum Portal form provider-owned portal/multiblock infrastructure. Portal validation, orientation, frame cleanup, destination/link state and portal travel are transport-system lifecycle, not separate semantic spell/ritual identities.

### Entity / Item / Block Teleporters

These are machines/blocks with GUI, fluid/state and server-tick transfer behavior. Moving an entity/item through a technological machine does not create a player-owned magic identity.

### Sable / Aeronautics / Immersive Portals compatibility

Compatibility modules transform/link portal coordinates against external moving-sublevel/portal runtimes. They remain integration infrastructure and do not mint independent magic objects.

Detailed classification: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Create Teleporters remains authority for teleporter/link state, pocket-dimension binding/generation, Custom Portal multiblock validity, quantum portal state, item/entity transfer and its compatibility layers. Create/Sable/Aeronautics/Immersive Portals remain authorities for their respective host systems.

Black Arcana records only the semantic disposition and must not replay teleports, duplicate transfers, rebuild provider portals or add a second cost/settlement path.

## Runtime QA remains separate

Catalog closure does not claim assembled-pack runtime PASS. Entity/item exactly-once transfer, chunk lifecycle, pocket-dimension persistence, TP Link range, portal frame rebuild, Sable/Aeronautics transforms, Immersive Portals orientation/migration and Create 6.0.10 coexistence remain runtime QA.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_TECH_TELEPORT_INFRA`.**

Strict semantic delta: **+0**.
