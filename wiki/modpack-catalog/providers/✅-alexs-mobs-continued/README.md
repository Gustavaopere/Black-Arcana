# Alex's Mobs Continued — 2.1.13

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 26 ITEM + 11 BLOCK ACTIVATION CLASSES DISPOSITIONED / 3 SUPERNATURAL ROOTS / 1 COUNTED_EXACT + 2 CONDITIONAL / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling physical authority:

- physical row: **#21**;
- JAR: `alexsmobs-2.1.13-neoforge+1.21.1.jar`;
- mod id: `alexsmobs`;
- runtime: `2.1.13`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`;
- required dependency in the pack: CodxLib 1.6.0+.

Alex's Mobs Continued is cross-domain for the magic catalog: the sibling classifies it as a mobs/exploration provider, but the exact installed artifact exposes one deliberate transmutation action, one Void Worm summoning action and one dimensional-portal action.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#511** audits the exact publisher artifact and hard-gates it against the physical pack fingerprint.

Final audit checkpoint used by this catalog:

- audit HEAD: `59cb7ffaba397a84f64d047be4b51096e5a392e7`;
- exact-artifact run: `36949047824` — **SUCCESS**;
- evidence artifact: `11202548934`;
- evidence digest: `sha256:e134c3ba8552fad8c0f174cf2dcd23eb112294a46506bdd1f8bceec6c5e8d31d`;
- CurseForge project/file: `1635121 / 8856498`;
- publisher SHA-1: `50ddafdf3d12b33331e4eecb4ab514ae451baadd`;
- publisher SHA-256: `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`;
- bytes: `27,452,738`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1.

The exact artifact contains **5,584 archive entries / 1,270 classes / 4,314 non-class resources / 638 provider-data paths**, including **45 item classes, 27 block classes, 12 tile/block-entity classes and 22 message classes**. Exhaustive signature inspection finds **26 item classes** and **11 block classes** with relevant interaction surfaces.

See [`EXACT-2.1.13-ARTIFACT-AUDIT.md`](EXACT-2.1.13-ARTIFACT-AUDIT.md).

## Semantic-magic result — 3 supernatural roots

Three provider-owned roots satisfy the semantic definition of a deliberate magical/supernatural player action:

1. **Transmutation Table — Item Transmutation** — `COUNTED_EXACT`;
2. **Mysterious Worm — Void Worm Summoning** — `CONDITIONAL`;
3. **Dimensional Carver — Void Portal / Dimensional Passage** — `CONDITIONAL`.

Object-level cards are in [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md).

## Why only one is strict

### Transmutation Table

The exact block/menu/server path is directly player-driven: the player inserts an item, selects one of three provider-generated possibilities, pays the configured XP-level cost, the server replaces the input with the selected output and the provider records/rerolls the transmutation state. The exact provider recipe crafts the Transmutation Table from normal reachable ingredients including a Farseer Arm.

This is one parameterized **Item Transmutation** identity. Individual input items, three displayed candidates, rarity tables, XP cost, rerolls and output items are parameters rather than additional spells.

### Void Worm Summoning

`alexsmobs:mysterious_worm` is produced by the exact Capsid recipe from `alexsmobs:mosquito_larva`, and Capsid itself is present in exact Enderiophage loot. However, the exact runtime checks `AMConfig.voidWormSummonable` and `AMConfig.voidWormSpawnDimensions` before spawning the Void Worm after the dropped Mysterious Worm crosses the provider depth condition.

The deployed effective values are not captured in current project evidence. Therefore the summon identity is cataloged but remains **`CONDITIONAL` / +0 strict**.

### Dimensional Carver

The exact item use/channel path creates `EntityVoidPortal`, assigns its attachment/destination/dimension/lifespan and consumes owner durability. This is one dimensional-traversal identity.

The exact crafting recipe requires `alexsmobs:void_worm_eye` and `alexsmobs:void_worm_mandible`, and the exact provider loot surface supplies those only from the Void Worm. Because current normal Void Worm reachability is config-conditioned as above, Dimensional Carver acquisition is also **`CONDITIONAL` / +0 strict** until the deployed summon gate is closed.

## Capsid is not a separate magic denominator

The exact artifact contains **4 Capsid transformation recipes**:

- cod -> Cosmic Cod;
- music disc -> Music Disc Daze;
- mosquito larva -> Mysterious Worm;
- Dimensional Carver -> Shattered Dimensional Carver.

Capsid accepts items and its block entity automatically advances `CapsidRecipe` processing over time. Under the catalog metric this is provider processing/crafting infrastructure, not four player-selected spell identities. It contributes **+0 independent semantic objects**.

## Exact interaction-surface disposition

All 26 item interaction classes and 11 block interaction classes are dispositioned in [`INTERACTION-DISPOSITION-2.1.13.md`](INTERACTION-DISPOSITION-2.1.13.md).

Important exclusions include:

- Blood Sprayer, Hemolymph Blaster, Stink Ray, Pocket Sand and other direct projectile/weapon modes;
- Skelewag Sword shield behavior, Shield of the Deep and Tendon Whip — ordinary weapon/guard/on-hit behavior;
- Squid Grapple and Vine Lasso — grappling/restraint utilities;
- Echolocator — locator/sonar utility rather than a spell identity;
- Ghostly Pickaxe — tool/passive inventory behavior;
- Rainbow Jelly, Fish Oil and other consumable/effect items;
- Straddleboard and Tarantula Hawk Elytra — vehicle/equipment mobility;
- Animal Dictionary, eggs, pupa, Flutter Pot and colony/pet setup items;
- Hummingbird Feeder, anthill/chamber, End Pirate structure controls and environmental blocks;
- Capsid recipe machinery.

## Authority boundary

Alex's Mobs Continued remains authority for Void Worm summon gates/dimensions/depth, entity initialization, portal entity lifecycle, Dimensional Carver targeting/durability, Transmutation Table candidate generation/cost/result/reroll state, Capsid processing and all provider effects/particles/sounds.

Black Arcana catalogs the identities only. It must not spawn a second Void Worm, create a second portal, re-pay/re-consume a transmutation cost or independently settle Capsid recipes.

## Runtime QA remains separate

Catalog closure does not assert assembled-pack runtime PASS. Later QA still includes deployed Alex's Mobs config, CodxLib compatibility, Void Worm summon gate/dimensions, multiplayer/server portal settlement, Transmutation Table loot/config behavior and datapack/recipe overrides.

## Result

**✅ Cataloged — exact current denominator closed.**

Current Alex's Mobs Continued semantic inventory: **3 supernatural roots = 1 strict exact-current + 2 config/reachability-conditional**.

Strict semantic delta: **+1**.
