# Portable Hole 21.1.0 — action card

Status: `1/1 COUNTED_EXACT`

## Open Temporary Portable Hole

- owner: `portablehole:portable_hole`;
- trigger: use the item on a valid block face;
- authority: server/provider-owned;
- action: creates a temporary directional passage through eligible solid blocks;
- depth: provider-configured parameter;
- lifetime: provider-configured parameter;
- settlement: provider temporary-hole BlockEntities restore the original block states after expiry;
- acquisition: exact Stronghold Corridor injected chest loot;
- state: `COUNTED_EXACT`.

### Deduplication boundary

The following are not separate magic identities:

- each replaced block;
- tunnel growth steps;
- block restoration ticks;
- particles/portal overlay/sound;
- cooldown;
- NBT restoration;
- target face/direction/depth variants.

They are parameters or consequences of the single Portable Hole action.

## Result

**One exact-current magical traversal action.**
