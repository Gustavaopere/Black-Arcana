# BetterNether: New Dawn — 21.0.26

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / ZERO_SEMANTIC_WORLDGEN_BREWING_EQUIPMENT / +0 STRICT / RUNTIME QA SEPARATE`

## Current physical identity

- physical sibling row: **#74**;
- JAR: `BetterNether-21.0.26.jar`;
- mod id: `betternether`;
- runtime: `21.0.26`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `69bb15fd21d3ffe6bf18fed83c17d7cdd85b7c85`.

BetterNether is a large Nether content/worldgen provider. It is cross-domain for catalog reconciliation because it contains portal-frame infrastructure, altar-named structures, equipment and brewing, but the exact installed artifact does not expose a provider-owned spell/ritual/glyph/ability roster.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#522** audits CurseForge project/file `1422293 / 8615740` and hard-gates the publisher JAR against the physical pack fingerprint.

- audit HEAD: `7300e22e7da3d0d53d9b230baca88df5dc22f2e8`;
- exact-artifact run: `36965947196` — **SUCCESS**;
- evidence artifact: `11210021581`;
- evidence digest: `sha256:6a6d5a7a26e4a80ea610df7a5aa0c0b33a0afb044bb7aa0c99b379e6b7cd8eab`;
- publisher SHA-1: `69bb15fd21d3ffe6bf18fed83c17d7cdd85b7c85`;
- publisher SHA-256: `5c139eccd71d3a44eb3474ff35e6ca97cf26a66944edd10a6bddee16049e78c0`;
- bytes: `26,656,311`.

The publisher SHA-1 exactly equals the installed physical SHA-1.

See [`EXACT-21.0.26-ARTIFACT-AUDIT.md`](EXACT-21.0.26-ARTIFACT-AUDIT.md).

## Exact provider surface

The hash-matched JAR contains:

- **8,005** archive entries;
- **596** classes;
- **7,409** resources;
- **596** BetterNether provider classes;
- **2,560** `data/betternether/**` paths;
- **15** item classes;
- **161** block classes;
- **60** paths/classes caught by a broad semantic-name filter.

The 60 broad-filter hits are not 60 magic actions. They resolve to:

- decorative `cincinnasite_pedestal` models/recipes and a non-interactive pedestal block class;
- `altar_01` … `altar_08`, `jungle_temple_altar` and `spawn_altar_ladder` NBT/worldgen templates;
- `portal_01` / `portal_02` NBT/worldgen structures;
- `BNPortalShape` and `PortalShapeMixin`, which extend portal-frame/block creation infrastructure;
- fire-bowl models/recipes;
- recipe-manager and item-tag/datagen classes;
- advancement criteria such as brewing/use-of-forge tracking.

None establishes a provider ritual registry, offering settlement, spell registry, player cast/action registry or independent semantic magic identity.

## Player-interaction reconciliation

Exhaustive class-signature inspection finds the notable direct item interactions in ordinary consumables:

- `ItemBlackApple.finishUsingItem(...)`;
- `ItemBowlFood.useOn(...)` and `finishUsingItem(...)`.

These are food/container interactions, not magic actions.

The portal implementation modifies vanilla-style Nether portal shape/frame behavior. It does not expose a distinct BetterNether player spell/ritual activation identity. Structures whose filenames contain `altar` or `portal` are generated structure templates, not callable rites.

## Brewing/equipment boundary

BetterNether owns brewing, consumables, Fire/Flaming Ruby equipment effects, tools and a Nether Brewing Stand. These are ordinary provider processing/equipment mechanics. Potion brewing does not become a spell/ritual identity merely because the output is magical in Minecraft terms.

## Result

**✅ Cataloged — `ZERO_SEMANTIC_WORLDGEN_BREWING_EQUIPMENT`.**

- provider-owned semantic magic identities: **0**;
- strict semantic delta: **+0**;
- altar/portal worldgen names: metric-excluded;
- portal-frame extension: infrastructure, metric-excluded;
- brewing/consumables/equipment: processing/equipment, metric-excluded.

## Authority boundary

BetterNether remains authority for its Nether worldgen, structures, portal-frame compatibility, mobs, equipment, effects, brewing, recipes and consumables. Black Arcana records the zero-semantic disposition and must not reinterpret those systems as spells or rituals.
