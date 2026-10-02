# Create: Fantasizing Again 1.2.0-b3 — exact artifact audit

Status: `EXACT PHYSICAL=PUBLISHER / SEMANTIC MAGIC DENOMINATOR CLOSED AT ZERO`

## Identity gate

- physical JAR: `create_fantasizing-1.21.1-1.2.0-b3.jar`;
- mod id: `create_fantasizing`;
- runtime: `1.2.0-b3`;
- physical SHA-1: `aac8f1460d2b5d21019c8b944b26dc0c184952c0`;
- CurseForge project/file: `1279337 / 8585611`.

NON-MERGE PR #536 / run `37018144292` succeeded with exact physical/publisher equality.

- audit HEAD: `104b59295629b692409aae68023411077358879c`;
- evidence artifact: `11232670660`;
- artifact digest: `sha256:b2a1219e89c7c283372c7c45049e5a52d070fce9a24762b5239b9f60b782d756`;
- publisher SHA-256: `1fdf90fdbe9d6dfab24d71793352a0b1c5af2eba0c88422710f5418ced6d09a5`;
- bytes: `633,064`.

## Bounded archive inventory

- entries: **673**;
- classes: **175**;
- resources: **498**;
- provider data paths: **105**;
- semantic-like JSONs selected for bounded inspection: **21**.

Magic-semantic path counts:

`spell=0 · magic=0 · ritual=0 · arcane=0 · glyph=0 · summon=0 · teleport=0 · portal=0`.

Lexical `ability=1` resolves only to `data/minecraft/tags/item/enchantable/durability.json`. Lexical `mana=1` resolves only to `MountedStorageManagerMixin`. Neither is a provider magic surface.

## Exhaustive activation index

Only three provider item classes match the bounded player-action signature set:

- `SculkEngineFrameItem` -> `interactLivingEntity`;
- `TreeCutterItem` -> `mineBlock`;
- `BlockPlacerItem` -> `use`, `inventoryTick`.

`SculkEngineFrameItem` checks specifically for vanilla Warden plus provider config, gives the Sculk Engine item and discards the Warden on the authoritative path. This is entity-to-engine conversion, not spell/summon settlement.

`TreeCutterItem` and `BlockPlacerItem` are batch tool/building surfaces. Their effects remain block/tool operations.

## Data and processing surface

Exact provider data closes recipes and loot for:

- compact Hydraulic/Wind/Sculk/Yin-Yang engine infrastructure;
- Block Placer and Sculk Engine Frame;
- Transporter;
- alternative Chromatic Compound;
- Refined Radiance / Shadow Steel chromatic-tunnel processing;
- Create sequencing/mixing/deploying/filling/pressing paths.

These are machine/tool/economy recipes, not ritual recipes or spell acquisition.

## Semantic result

- standalone spell/glyph/ritual/ability roots: **0**;
- player-owned supernatural cast/summon roots: **0**;
- Warden capture/conversion: **EXCLUDED**;
- Block Placer / Tree Cutter batch operations: **EXCLUDED**;
- Create engines / storage / Transporter: **EXCLUDED**;
- Chromatic and resource processing: **EXCLUDED**.

Disposition: **`ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_INFRA`**.

## Clean-room boundary

The durable catalog retains hashes, counts, class/method identifiers and behavior-level classifications needed for semantic cataloging. It does not redistribute the JAR, implementation bodies, assets or localization prose.
