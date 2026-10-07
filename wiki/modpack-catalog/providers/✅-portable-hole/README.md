# Portable Hole — 21.1.0

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 1 COUNTED_EXACT MAGICAL TRAVERSAL ACTION / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#452**;
- JAR: `PortableHole-v21.1.0-1.21.1-NeoForge.jar`;
- mod id: `portablehole`;
- runtime: `21.1.0`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `dd651e3c3b15496112ba2bcc3cdce7bf89d3ed85`.

Portable Hole is cross-domain: its physical category is exploration/QoL rather than `Magic`, but the provider describes the item as a magical tool and the exact installed artifact owns one discrete player-invoked supernatural traversal action.

## Exact artifact closure

NON-MERGE evidence PR **#505** audits CurseForge project/file `682568 / 5733788` and hard-gates the publisher JAR against the physical pack SHA-1.

Final audit checkpoint:

- audit HEAD: `3c5d31933145d96d1b5d84e8c651efaaf417c13e`;
- exact-artifact run: `36935857689` — **SUCCESS**;
- evidence artifact: `11198490297`;
- evidence digest: `sha256:7490db93091d16d61e3387c7752cc4ebb7935217f1bfff6daca9d95f6cc0d310`;
- publisher SHA-1: `dd651e3c3b15496112ba2bcc3cdce7bf89d3ed85`;
- publisher SHA-256: `f968b6cfab7eecd0882ecaacc2ecc3efb75f8a622aee954857e73685f473016f`;
- bytes: `100,833`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1.

See [`EXACT-21.1.0-ARTIFACT-ACTION-AUDIT.md`](EXACT-21.1.0-ARTIFACT-ACTION-AUDIT.md).

## Semantic inventory — 1 exact action

### Open Temporary Portable Hole

Owner: `portablehole:portable_hole`.

The exact item exposes one player-facing activation surface, `useOn`. On a valid clicked block the server:

1. derives the clicked position and face;
2. creates the provider temporary-hole blocks in the clicked direction up to the configured depth;
3. plays the provider's Enderman-teleport feedback;
4. applies the provider cooldown;
5. lets each temporary-hole block restore its original block state after the configured lifetime.

The temporary-hole BlockEntity also retains/restores BlockEntity NBT when the provider configuration allows replacement. Tunnel depth, the number of replaced blocks, restoration particles and individual temporary blocks are parameters/consequences of the same causal action, not separate spell identities.

Object card: [`actions/PORTABLE-HOLE.md`](actions/PORTABLE-HOLE.md).

Individual action card: [Open Temporary Portable Hole](actions/open-temporary-portable-hole.md).

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Exact acquisition

The exact JAR packages `data/portablehole/loot_table/chests/inject/stronghold_corridor.json`.

That loot table has one roll with:

- `portablehole:portable_hole` as an item entry;
- an empty entry with weight 4.

This closes catalog-level normal acquisition through Stronghold Corridor loot.

## Metric exclusions

Not counted as additional semantic objects:

- every block replaced along the tunnel;
- the configured tunnel depth;
- the temporary-hole block/entity itself;
- automatic restoration ticks;
- portal overlay, sparkle particles and restoration particles;
- Enderman teleport sound;
- cooldown state;
- block-hardness and immunity-tag checks;
- ordinary block-state/NBT restoration.

Those are implementation details, parameters or consequences of the single player action.

## Authority boundary

Portable Hole remains authority for input validation, eligible blocks, direction/depth, block replacement, BlockEntity preservation, lifetime, restoration, cooldown and visual/audio feedback. Black Arcana catalogs the identity only and must not replay block replacement/restoration or charge a second cost/cooldown.

## Runtime QA remains separate

Catalog closure does not claim assembled-pack runtime PASS. Current serverconfig values, claims/protection integration, chunk unload/restart restoration, BlockEntity safety, player trapping and multiplayer synchronization remain runtime QA.

## Result

**✅ Cataloged — `COUNTED_EXACT`.**

Strict semantic contribution: **+1**.
