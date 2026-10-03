# Create: Ender Transmission — 2.1.1-1.21.1

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_REMOTE_TRANSFER_CHUNK_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#184**;
- JAR: `createendertransmission-2.1.1-1.21.1.jar`;
- mod id: `createendertransmission`;
- runtime: `2.1.1-1.21.1`;
- physical SHA-1: `fbf165d068a3a9c6d24f1bcf68fb1af380ee2603`.

Create: Ender Transmission provides long-distance/cross-dimension item, fluid and energy transport plus a kinetic chunk loader. Its Ender theme and dimensional reach do not by themselves make those systems semantic magic actions.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#552** audits Modrinth version `eI9pk5JC` and hard-gates the publisher artifact against the physical fingerprint.

- audit HEAD: `8bad16d1fbd7de8b35e9f6f97a2405159728e187`;
- exact-artifact run: `37145079612` — **SUCCESS**;
- evidence artifact: `11281133820`;
- evidence digest: `sha256:6a832aac74f650ea4f49240a0ec2600bef18ceeec25dfa49c6f954774c660657`;
- publisher SHA-1: `fbf165d068a3a9c6d24f1bcf68fb1af380ee2603`;
- publisher SHA-256: `13f237796ba51312a385ebd55b252c55598d49bcf677ea68f0bfb9bd88c23b63`;
- bytes: `84,366`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-2.1.1-ARTIFACT-AUDIT.md`](EXACT-2.1.1-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains **107 entries / 32 classes / 75 resources / 14 provider-data paths / 8 provider JSON files**.

Exact path counts are zero for:

`spell · magic · ritual · ability · mana · arcane · glyph · summon · soul · teleport · portal · enchant · curse`.

The only bounded player-facing block interactions are `useItemOn` on the Energy, Fluid and Item Transmitter blocks. Exact bytecode shows those interactions open the provider `TransmitterScreen`; confirmation sends `ConfigureTransmitterPacket`, which stores channel/password state and reloads the provider transmitter link. They are configuration operations, not supernatural actions.

The Chunk Loader is a kinetic block. Exact control flow forces/releases nearby chunks according to server-side Create speed and block lifecycle. It has no separate player-cast or ritual identity.

## Provider data/acquisition

The exact provider data packages four block loot tables and four acquisition recipes:

- Chunk Loader — shaped vanilla recipe;
- Energy Transmitter — Create mechanical crafting;
- Fluid Transmitter — Create mechanical crafting;
- Item Transmitter — Create mechanical crafting.

Those routes acquire technological/logistics infrastructure and do not create semantic magic objects.

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Create: Ender Transmission remains authority for channel/password pairing, transmitter networks, item/fluid/energy capability settlement and chunk forcing. Create remains authority for kinetic speed/stress. Black Arcana must not create a second transfer, duplicate inventory/fluid/energy settlement or reinterpret remote transfer as teleport magic.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_REMOTE_TRANSFER_CHUNK_INFRA`.**

Strict semantic delta: **+0**.
