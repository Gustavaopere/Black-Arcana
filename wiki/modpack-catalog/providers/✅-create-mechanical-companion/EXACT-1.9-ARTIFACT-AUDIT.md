# Create Mechanical Companion 1.9 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO MAGIC-ACTION DENOMINATOR CLOSED`

## Identity gate

- physical JAR: `createmechanicalcompanion-1.9-neoforge-1.21.1.jar`;
- mod id: `createmechanicalcompanion`;
- physical runtime metadata: empty;
- artifact/publication line: `1.9`;
- physical SHA-1: `480d35a7f926c1a2b86521be1feb75710b1c838e`.

NON-MERGE PR #554 downloads Modrinth version `6ZRWru4y` and fails unless publisher SHA-1 equals the physical fingerprint.

- audit HEAD: `a1e2e3bb2ddb7799fb049ece985e3de607482102`;
- run: `37145583077` — SUCCESS;
- artifact: `11281054748`;
- digest: `sha256:3b35aa2d4c459fb5dea51166e6b245ce2a2875941bfb3607d85a659ae0b440ff`;
- publisher SHA-1: `480d35a7f926c1a2b86521be1feb75710b1c838e`;
- publisher SHA-256: `06b216b06ef400fe573303a6acbfb5e599474a61c8fd329356397c69b6f4a2ef`;
- bytes: `357,511`.

Result: exact publisher/physical equality is proven.

## Archive inventory

- entries: **198**;
- classes: **54**;
- resources: **144**;
- provider-data paths: **41**;
- provider JSONs: **26**.

Exact path counts are zero for spell, magic, ritual, ability, mana, arcane, glyph, summon, soul, teleport, portal, enchant and curse.

## Exact activation surface

Exhaustive signature inspection across all 54 classes finds only:

- `BlueprintPaintingItem.useOn`;
- `MechanicalWolfLink.curioTick`;
- `MechanicalWolfLink.onUnequip`.

The painting path is decorative placement. The Curios link is lifecycle infrastructure: it persists `WolfUUID`, resolves or reconstructs the Mechanical Wolf server-side, tracks death/respawn cooldown, saves/restores modules and dismisses the entity on real unequip.

No item/block/player-action override establishes a discrete provider spell, rite, ritual, summon command or supernatural player ability.

## Exact module surface

The exact artifact exposes companion modules including Mounted Crossbow, Tesla Tail, Booster Rocket, Quantum Drive, Mob Radar, Mounted Light, Regenerative Casing and armor/utility modules.

Quantum Drive calls entity teleportation from Mechanical Wolf module/cooldown logic. It is automatic companion movement, not a player-owned teleport action. Tesla Tail and Mounted Crossbow are AI/combat equipment; Booster Rocket is movement equipment; Radar/Light/Casing are utility/support modules.

## Provider data

The exact provider data contains ordinary crafting/smithing-style acquisition, chest loot and Illager Workshop worldgen. No ritual/spell recipe type is present.

## Semantic disposition

`ZERO_SEMANTIC_MECHANICAL_COMPANION_INFRA / +0 strict`.

Companion summon/reconstruction performed automatically by the equipped Curios link is lifecycle settlement for a persistent mechanical pet, not a player-selected summon spell. Module-driven companion teleport/combat/support behavior likewise remains equipment/AI infrastructure.

## Clean-room boundary

The durable catalog retains hashes, counts, class/resource names and behavior-level classifications required for denominator work. No third-party JAR bytes, implementation bodies or assets are committed.
