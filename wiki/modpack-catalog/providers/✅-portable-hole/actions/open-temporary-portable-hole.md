# Open Temporary Portable Hole

- Provider: **Portable Hole** (`portablehole`)
- Version: `21.1.0`
- Exact physical/publisher SHA-1: `dd651e3c3b15496112ba2bcc3cdce7bf89d3ed85`
- Owner: `portablehole:portable_hole`
- Trigger: use the item on a valid block face
- Authority: server/provider-owned
- State: `COUNTED_EXACT`

## Semantic identity

The provider performs one magical traversal action: it creates a temporary directional passage through eligible solid blocks up to the configured depth and later restores the original block states. Individual replaced blocks, tunnel-growth steps and restoration ticks are parameters or consequences of this one root.

## Exact acquisition

The exact installed JAR packages `data/portablehole/loot_table/chests/inject/stronghold_corridor.json`, which injects `portablehole:portable_hole` into Stronghold Corridor chest loot.

## Boundary

Portable Hole remains authority for block eligibility, direction/depth, replacement, BlockEntity NBT preservation, lifetime, restoration, cooldown and visual/audio feedback. Black Arcana catalogs the identity only and must not replay block replacement/restoration or charge a second cost/cooldown.

Source: [`../EXACT-21.1.0-ARTIFACT-ACTION-AUDIT.md`](../EXACT-21.1.0-ARTIFACT-ACTION-AUDIT.md).
