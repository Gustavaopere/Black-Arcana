# Dimensional Sable — 1.0.5

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_DIMENSION_TRANSFER_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- JAR: `dimensional_sable-1.0.5.jar`;
- mod id: `dimensional_sable`;
- runtime: `1.0.5`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `67e519029aa95e0b4a0694bf31190163ada0bc81`;
- sibling physical row: #219.

Dimensional Sable is a server-side/modpack-tool addon over Sable. It owns supported cross-dimension transfer of Sable sublevels and connected sublevels; it is not a player magic system.

## Exact artifact closure

NON-MERGE evidence PR **#526** audits Modrinth project/version `Iq9c4mLa / l9l5j4Zh` and hard-gates the publisher artifact against the physical fingerprint.

- audit HEAD: `d95c2584f18f43993870fd90226dd2667173d5ee`;
- exact-artifact run: `37003723918` — **SUCCESS**;
- evidence artifact: `11225380703`;
- artifact digest: `sha256:c557fe11da5e8e52ea52418a913acbd1c3ec415a001ec0fa533d42bd49847dec`;
- publisher SHA-1: `67e519029aa95e0b4a0694bf31190163ada0bc81`;
- publisher SHA-256: `7bc4856b39589669bd7e44bafedbaa4d73e4085ec5c69c581a8f64c39d97d35b`;
- bytes: `43,564`.

The publisher SHA-1 exactly equals the current physical SHA-1.

See [`EXACT-1.0.5-ARTIFACT-AUDIT.md`](EXACT-1.0.5-ARTIFACT-AUDIT.md).

## Exact semantic surface

The exact JAR contains **38 archive entries / 21 classes / 17 non-class resources / 0 provider data JSON files**. The only provider-facing operation that resembles teleportation is the Brigadier command tree:

`/sable dimension_set <sub_level> <dimension> [position]`

`Commands.DimensionCommand` resolves an existing Sable `ServerSubLevel` plus destination `ServerLevel`, then delegates to `SubLevelWarper.WarpSubLevel(...)`. The warper serializes/recreates supported sublevel state, maps old/new sublevel IDs, restores block-entity state, updates Sable physics state and teleports attached entities when applicable.

This is structural/admin/modpack-tool infrastructure. It is not a standalone player spell, ritual, glyph, focus, item ability or survival-reachable supernatural action under the Black Arcana semantic metric.

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Why the dimension transfer is not counted as magic

The semantic ledger counts provider-owned player-facing spells/rituals or equivalent discrete supernatural player actions. Dimensional Sable exposes a command/API operation over Sable physics state, not a player-acquired cast identity. Its `PhysicsPipeline.teleport(...)` call is an internal settlement step for moved physics bodies; it does not create a spell identity.

The fact that the operation crosses dimensions does not make it a magical action by itself.

## Authority boundary

- Sable remains authority for sublevel/physics identity and state;
- Dimensional Sable owns supported cross-dimension transfer/reconstruction;
- Create Aeronautics remains authority for its own contraption/airship state where optional integration applies;
- Black Arcana catalogs the semantic disposition only and must not duplicate transfer or world-state settlement.

## Runtime QA remains separate

Catalog closure does not claim all stateful modded block entities or moving contraptions survive transfer. Cross-dimension duplicate prevention, chunk lifecycle, passengers/entities, Create Aeronautics integration and known Moving Mechanical Piston limitations remain runtime QA.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_DIMENSION_TRANSFER_INFRA`.**

Strict semantic delta: **+0**.
