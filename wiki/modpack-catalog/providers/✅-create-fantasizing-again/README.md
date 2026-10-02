# Create: Fantasizing Again — 1.2.0-b3

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_INFRA / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#143**;
- JAR: `create_fantasizing-1.21.1-1.2.0-b3.jar`;
- mod id: `create_fantasizing`;
- runtime: `1.2.0-b3`;
- physical SHA-1: `aac8f1460d2b5d21019c8b944b26dc0c184952c0`.

The provider is cross-domain because it includes Warden capture, high-impact batch tools, Chromatic processing and Create engine/storage infrastructure. Exact inspection is required before treating those surfaces as magic.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#536** audits CurseForge project/file `1279337 / 8585611` and hard-gates the publisher artifact against the physical fingerprint.

- audit HEAD: `104b59295629b692409aae68023411077358879c`;
- exact-artifact run: `37018144292` — **SUCCESS**;
- evidence artifact: `11232670660`;
- evidence digest: `sha256:b2a1219e89c7c283372c7c45049e5a52d070fce9a24762b5239b9f60b782d756`;
- publisher SHA-1: `aac8f1460d2b5d21019c8b944b26dc0c184952c0`;
- publisher SHA-256: `1fdf90fdbe9d6dfab24d71793352a0b1c5af2eba0c88422710f5418ced6d09a5`;
- bytes: `633,064`.

The publisher SHA-1 exactly equals the current physical pack SHA-1.

See [`EXACT-1.2.0-B3-ARTIFACT-AUDIT.md`](EXACT-1.2.0-B3-ARTIFACT-AUDIT.md).

## Exact semantic inventory

The exact artifact contains:

- **673** archive entries;
- **175** classes;
- **498** non-class resources;
- **105** `data/create_fantasizing/**` paths.

Archive keyword inventory closes:

`spell=0 · magic=0 · ritual=0 · arcane=0 · glyph=0 · summon=0 · teleport=0 · portal=0`.

The two lexical hits that could look magical are false positives:

- `ability=1` -> vanilla tag path `data/minecraft/tags/item/enchantable/durability.json`;
- `mana=1` -> class name `MountedStorageManagerMixin`, referring to Create mounted-storage management rather than a mana system.

## Exact player-action surfaces

Exhaustive signature indexing finds only three provider item classes with relevant direct player-action methods:

- `SculkEngineFrameItem.interactLivingEntity`;
- `TreeCutterItem.mineBlock`;
- `BlockPlacerItem.use` / `inventoryTick`.

None establishes a spell/glyph/ritual/ability registry.

### Sculk Engine Frame / Warden capture

When the provider config permits it, the frame can interact with a vanilla Warden, consume/replace the frame with the Sculk Engine item and discard the captured Warden. This is a provider conversion/progression mechanic. It is not a player summon/cast identity and does not mint a magical action root.

### Block Placer / Tree Cutter

Block Placer performs configured batch placement/destruction/brush operations using Create-style tool infrastructure. Tree Cutter expands ordinary mining over a tree. These are high-impact tools with protection/performance consequences, not magic actions.

### Engines, Transporter, crates and barrels

Hydraulic/Wind/Sculk/Yin-Yang engines provide Create stress/kinetic infrastructure. Transporter moves inventory contents. Crates and Fluid Barrels provide storage. These remain automation/storage mechanics even where the theme is unusual.

### Chromatic and rare-resource processing

Chromatic Tunnel, Refined Radiance/Shadow Steel processing, alternative Chromatic Compound and rare-resource recipes are Create processing/economy surfaces. Recipe identity is not promoted into the spell/ritual ledger.

Detailed disposition: [`SEMANTIC-SURFACE-DISPOSITION.md`](SEMANTIC-SURFACE-DISPOSITION.md).

## Authority boundary

Create: Fantasizing Again remains authority for its engines, tools, storage, Transporter, Warden conversion, Powder Snow handling, recipes and config. Create remains authority for kinetics/stress and shared Create infrastructure.

Black Arcana records only the semantic classification and must not duplicate item transfer, Warden conversion, stress generation, block operations or storage settlement.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_CREATE_AUTOMATION_TOOLS_INFRA`.**

Strict semantic delta: **+0**.
