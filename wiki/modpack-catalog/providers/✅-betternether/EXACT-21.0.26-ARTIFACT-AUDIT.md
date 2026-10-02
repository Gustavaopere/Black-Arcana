# BetterNether 21.0.26 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / ZERO SEMANTIC MAGIC ROSTER`

## Identity gate

Physical authority:

- JAR `BetterNether-21.0.26.jar`;
- mod id `betternether`;
- runtime `21.0.26`;
- SHA-1 `69bb15fd21d3ffe6bf18fed83c17d7cdd85b7c85`.

NON-MERGE PR #522 downloads CurseForge File `1422293 / 8615740` and fails before semantic inspection unless publisher SHA-1 equals the physical fingerprint.

Audit result:

- HEAD: `7300e22e7da3d0d53d9b230baca88df5dc22f2e8`;
- run: `36965947196` — SUCCESS;
- artifact: `11210021581`;
- artifact digest: `sha256:6a6d5a7a26e4a80ea610df7a5aa0c0b33a0afb044bb7aa0c99b379e6b7cd8eab`;
- SHA-1: `69bb15fd21d3ffe6bf18fed83c17d7cdd85b7c85`;
- SHA-256: `5c139eccd71d3a44eb3474ff35e6ca97cf26a66944edd10a6bddee16049e78c0`;
- bytes: `26,656,311`.

Physical/publisher equality is exact.

## Archive inventory

- entries: **8,005**;
- classes: **596**;
- resources: **7,409**;
- provider classes: **596**;
- provider data paths: **2,560**;
- item classes: **15**;
- block classes: **161**;
- broad semantic-name hits: **60**.

## Broad semantic-name false-positive resolution

The audit searches paths/classes for `spell|ritual|rite|magic|mana|arcane|glyph|sorcer|wizard|witch|occult|summon|teleport|portal|altar|pedestal|ability`.

The hits resolve to infrastructure/content rather than a semantic action roster:

- `BlockCincinnasitePedestal`: decorative/metal block, no ritual interaction contract;
- `Altars`: random NBT structure template family (`altar_01` through `altar_08`);
- `Portals`: random NBT worldgen structure templates (`portal_01`, `portal_02`);
- `SpawnAltarLadder`: structure template;
- `PortalShapeMixin` + `BNPortalShape`: portal-frame shape/block generation extension;
- `BNCriterion`: advancement triggers (`brew_blue`, `used_forge`, etc.);
- recipe/tag/datagen infrastructure;
- blockstate/model/texture/recipe resources for pedestals and fire bowls.

No spell registry, ritual type registry, offering/result ritual recipe type, mana system, glyph registry or provider player-ability registry is present in the audited surface.

## Direct interaction surface

Whole-provider signature indexing found no candidate cast/ritual interaction rooted in the broad semantic classes. The relevant item overrides are ordinary food/container flows (`ItemBlackApple`, `ItemBowlFood`).

Portal creation is infrastructure invoked through portal-shape logic; the provider does not mint a separate player-owned BetterNether cast/ritual identity for lighting a Nether portal.

## Data reconciliation

The audit parses provider recipe/loot/advancement/brewing/potion-related JSON. Observed surfaces are ordinary recipes, loot, advancement progression and brewing/consumable content. Examples such as Cincinnasite Pedestal, fire bowls and Nether Brewing Stand are crafting/smithing/processing content rather than semantic magic actions.

## Disposition

`ZERO_SEMANTIC_WORLDGEN_BREWING_EQUIPMENT`

Strict semantic contribution: **+0**.

## Clean-room boundary

The durable catalog retains hashes, counts, identifiers and high-level semantic classification. It does not redistribute the JAR, NBT structures, assets or implementation bodies.
