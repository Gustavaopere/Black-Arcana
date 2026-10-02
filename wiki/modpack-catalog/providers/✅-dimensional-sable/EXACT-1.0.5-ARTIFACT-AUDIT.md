# Dimensional Sable 1.0.5 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / DIMENSION-TRANSFER INFRA DENOMINATOR CLOSED`

## Identity gate

- physical JAR: `dimensional_sable-1.0.5.jar`;
- mod id: `dimensional_sable`;
- physical SHA-1: `67e519029aa95e0b4a0694bf31190163ada0bc81`;
- publisher: Modrinth project/version `Iq9c4mLa / l9l5j4Zh`.

NON-MERGE PR #526 run `37003723918` succeeded with exact publisher/physical equality.

- artifact: `11225380703`;
- artifact digest: `sha256:c557fe11da5e8e52ea52418a913acbd1c3ec415a001ec0fa533d42bd49847dec`;
- publisher SHA-256: `7bc4856b39589669bd7e44bafedbaa4d73e4085ec5c69c581a8f64c39d97d35b`;
- bytes: `43,564`.

## Bounded exact inventory

- archive entries: **38**;
- classes: **21**;
- non-class resources: **17**;
- provider data JSON files: **0**;
- bounded dimension/teleport/command/transfer-like paths: **11**.

The keyword count is a discovery aid, not a semantic-action count.

## Exact command seam

`dev.egg.Commands.registerCommands(...)` registers `dev.egg.Commands$DimensionCommand`. The exact command grammar is:

`sable dimension_set <sub_level> <dimension> [position]`

The executor resolves the target dimension and Sable sublevel then calls `SubLevelWarper.WarpSubLevel(...)`. No item-use, spell registry, ritual recipe, glyph registry or player ability registry is present in the exact artifact.

## Exact transfer seam

`SubLevelWarper` operates on Sable `ServerSubLevel` / `ServerSubLevelContainer` state. Exact bytecode includes:

- connected-chain resolution through Sable;
- old/new dimension containers;
- sublevel save/load reconstruction;
- old→new sublevel ID mapping;
- block-entity move context;
- physics-pipeline teleport of reconstructed physics bodies;
- entity relocation when supported;
- removal of the source sublevel.

These are implementation surfaces of one structural transfer transaction, not downstream spell identities.

## Semantic disposition

Exact-current semantic magic objects: **0**.

State: **`ZERO_SEMANTIC_DIMENSION_TRANSFER_INFRA`**.

The dimension transfer is command/API infrastructure rather than a normal player-acquired supernatural action.

## Clean-room boundary

The durable catalog retains hashes, counts, command identity and high-level transfer/control-flow facts needed for classification. It does not redistribute the JAR or implementation bodies.
