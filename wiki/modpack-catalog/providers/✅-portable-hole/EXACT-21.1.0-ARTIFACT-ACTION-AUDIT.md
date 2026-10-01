# Portable Hole 21.1.0 — exact artifact action audit

Status: `EXACT PHYSICAL=PUBLISHER / SINGLE PLAYER-ACTION SURFACE CLOSED / STRONGHOLD ACQUISITION CLOSED`

## Identity gate

Physical sibling authority:

- JAR `PortableHole-v21.1.0-1.21.1-NeoForge.jar`;
- mod id `portablehole`;
- version `21.1.0`;
- SHA-1 `dd651e3c3b15496112ba2bcc3cdce7bf89d3ed85`.

NON-MERGE PR #505 downloads CurseForge File `682568 / 5733788` and fails before semantic inspection unless the publisher SHA-1 equals the physical fingerprint.

Final evidence:

- audit HEAD: `3c5d31933145d96d1b5d84e8c651efaaf417c13e`;
- run: `36935857689` — SUCCESS;
- artifact: `11198490297`;
- artifact digest: `sha256:7490db93091d16d61e3387c7752cc4ebb7935217f1bfff6daca9d95f6cc0d310`;
- publisher SHA-1: `dd651e3c3b15496112ba2bcc3cdce7bf89d3ed85`;
- publisher SHA-256: `f968b6cfab7eecd0882ecaacc2ecc3efb75f8a622aee954857e73685f473016f`;
- bytes: `100,833`.

Result: physical and publisher bytes are identical.

## Bounded inventory

The exact artifact contains:

- **98** archive entries;
- **25** classes;
- **73** non-class resources;
- **14** bounded candidate classes;
- **8** `data/portablehole/**` paths;
- **23** `assets/portablehole/**` paths.

The exact provider registers one `portablehole:portable_hole` item, one temporary-hole block/entity and sparkle-particle/config infrastructure.

## Exact player action

Exhaustive method scanning finds one direct player activation root:

- `PortableHoleItem.useOn(UseOnContext)`.

Exact bytecode shows that this root validates the clicked block, then server-side invokes `TemporaryHoleBlockEntity.setTemporaryHoleBlock(...)` in the clicked direction for the configured `temporaryHoleDepth`. It applies the provider cooldown and item-use statistic and returns the standard sided-success result.

The linked temporary-hole BlockEntity owns the continuation/lifecycle:

- stores the source block state;
- optionally stores/restores BlockEntity data;
- decrements the configured lifetime;
- grows the tunnel in the selected direction while growth distance remains;
- restores the source block state when lifetime expires.

That continuation is provider settlement of the original action, not a second semantic identity.

## Exact configuration surface

The exact server config exposes:

- portable-hole cooldown;
- temporary-hole depth;
- temporary-hole duration;
- maximum block hardness;
- spark particles;
- portal overlay;
- particles for reappearing blocks;
- BlockEntity replacement toggle.

These values parameterize the same action and do not alter the semantic denominator.

## Exact acquisition

The exact artifact packages:

`data/portablehole/loot_table/chests/inject/stronghold_corridor.json`

The exact JSON contains one chest pool/roll whose entries are:

- item `portablehole:portable_hole`;
- `minecraft:empty` with weight 4.

Therefore normal provider-native acquisition is closed at catalog level.

## Semantic disposition

- Open Temporary Portable Hole: **1 `COUNTED_EXACT`**;
- temporary blocks/restoration/particles/sound/cooldown/config parameters: **EXCLUDED as separate identities**.

Total provider semantic surface: **1**.

## Clean-room boundary

The durable catalog keeps hashes, counts, identifiers, short control-flow facts and acquisition facts needed for cataloging. It does not redistribute the JAR, source bodies, assets or localization beyond minimal identity labels.
