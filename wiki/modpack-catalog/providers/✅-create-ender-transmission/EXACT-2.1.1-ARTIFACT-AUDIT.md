# Create: Ender Transmission 2.1.1 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO MAGIC-ACTION DENOMINATOR CLOSED`

## Identity gate

- physical JAR: `createendertransmission-2.1.1-1.21.1.jar`;
- mod id: `createendertransmission`;
- runtime: `2.1.1-1.21.1`;
- physical SHA-1: `fbf165d068a3a9c6d24f1bcf68fb1af380ee2603`.

NON-MERGE PR #552 downloads Modrinth version `eI9pk5JC` and fails unless publisher SHA-1 equals the physical fingerprint.

- audit HEAD: `8bad16d1fbd7de8b35e9f6f97a2405159728e187`;
- run: `37145079612` — SUCCESS;
- artifact: `11281133820`;
- digest: `sha256:6a832aac74f650ea4f49240a0ec2600bef18ceeec25dfa49c6f954774c660657`;
- publisher SHA-1: `fbf165d068a3a9c6d24f1bcf68fb1af380ee2603`;
- publisher SHA-256: `13f237796ba51312a385ebd55b252c55598d49bcf677ea68f0bfb9bd88c23b63`;
- bytes: `84,366`.

Result: exact publisher/physical equality is proven.

## Archive inventory

- entries: **107**;
- classes: **32**;
- resources: **75**;
- provider-data paths: **14**;
- provider JSONs: **8**.

Magic-semantic path counts are all zero for spell, magic, ritual, ability, mana, arcane, glyph, summon, soul, teleport, portal, enchant and curse.

## Exact interaction surface

Three block classes declare `useItemOn`:

- `EnergyTransmitterBlock`;
- `FluidTransmitterBlock`;
- `ItemTransmitterBlock`.

All three resolve to the provider configuration screen when the interaction is not being delegated to normal wrench/kinetic placement behavior. The screen configures transmitter channel/password state. `ConfigureTransmitterPacket` applies that state server-side and calls the transmitter reload hooks.

No provider item/player action override establishes a discrete cast, spell, ritual, summon, portal activation or supernatural ability.

## Exact network/chunk surface

Provider classes are organized around item/fluid/energy transmitter networks and one kinetic chunk loader. The loader's block entity evaluates Create kinetic speed and toggles forced chunks; block removal clears forced chunks. These are server infrastructure/lifecycle operations.

## Provider data

The exact eight JSON files are four block loot tables plus four recipes. Transmitters use Create mechanical crafting; the Chunk Loader uses shaped crafting. No ritual/spell recipe type is present.

## Semantic disposition

`ZERO_SEMANTIC_REMOTE_TRANSFER_CHUNK_INFRA / +0 strict`.

Remote/cross-dimension transfer is not counted as teleportation magic because the exact provider implementation is capability/network transfer infrastructure rather than a player-owned supernatural action.

## Clean-room boundary

The durable catalog retains hashes, counts, class/resource names and behavior-level classifications required for denominator work. No third-party JAR bytes, implementation bodies or assets are committed.
