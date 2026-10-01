# Legendary Monsters — 2.2.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 20 MAGIC-ACTION OWNERS / 22 COUNTED_EXACT ACTION ROOTS / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#371**;
- JAR: `legendary_monsters-2.2.2 MC 1.21.1.jar`;
- mod id: `legendary_monsters`;
- release/runtime line: `2.2.2` (embedded metadata remains provider-owned and is not substituted for the physical release identity);
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `8910859ba94190dd8cbc8c2c1e2f07562db729b4`.

Legendary Monsters is primarily a boss/equipment/world-content mod, but its exact installed artifact also owns a bounded set of deliberate supernatural player actions. The catalog counts those actions without turning every magical-looking weapon, locator, proc or projectile into a spell.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#507** audits CurseForge project/file `944035 / 8715533` and hard-gates the publisher artifact against the physical pack fingerprint.

Final exact audit:

- audit HEAD: `d89c1b882e10ab33365fd9e783e59834ec88aa17`;
- run: `36937980556` — **SUCCESS**;
- evidence artifact: `11197774688`;
- artifact digest: `sha256:fbd5449b4c7e37c41e232e8b1146cb8f0839375854af55fd7bf2ed7b4031e9d9`;
- publisher SHA-1: `8910859ba94190dd8cbc8c2c1e2f07562db729b4`;
- publisher SHA-256: `63cd850d938e96cd708915247d415b74e9e14f89f9498cf416b0f4c0e9a208ac`;
- bytes: `44,757,560`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1.

The exact artifact contains **3,415 archive entries / 1,217 classes / 2,198 non-class resources / 96 item classes / 109 action-shaped classes / 552 provider data paths**. The bounded interaction scan then checks every provider classfile for player-interaction/input signatures and closes the global surface at **49 interaction-reference classes**.

See [`EXACT-2.2.2-ARTIFACT-ACTION-AUDIT.md`](EXACT-2.2.2-ARTIFACT-ACTION-AUDIT.md).

## Semantic action inventory — 22 exact roots

The 49 interaction-reference classes collapse into:

- 12 Eye/locator item classes — excluded;
- 5 key/network infrastructure classes — excluded;
- 7 helper/event classes that settle actions already owned by another counted item — deduplicated;
- 25 direct owner item/armor classes;
- of those 25 owners, 5 are ordinary primary firing/throwing owners — excluded;
- **20 semantic magic-action owners** remain.

Those 20 owners produce **22** action roots because Axe of Lightning and The Great Frost each expose two causally distinct player activations.

Exact current action list:

1. Annihilator Helmet — Targeted Teleport;
2. Axe of Lightning — Lightning Strike;
3. Axe of Lightning — Electric Burst;
4. Buckler of Annihilation — Sweep + Annihilation Bombs;
5. Chorus Blade — Random Teleport;
6. Dinosaur Bone Club — Circular Shockwaves;
7. Entity Warper — Radius Entity Warp;
8. Fiery Boots — Fire Trail;
9. Fiery Jaw — Fire Breath + Repulsion;
10. The Great Frost — Directed Ice Spikes;
11. The Great Frost — Radial Ice Spikes;
12. Guard Summoner — Guard Summon;
13. Knight Summoner — Knight Summon;
14. Monstrous Anchor — Launch + Stun Burst;
15. Mossy Chestplate — Poison Cloud Field;
16. Mossy Hammer — Poison/Moss Shockwave;
17. Soul Great Sword — Phantom Daggers;
18. The Tesseract — Annihilation Portal Star;
19. Totem of Moss — Mossy Golem Summon;
20. Void Entity Warper — Targeted Entity Warp;
21. Wand of Clouds — Explosive Cloud Summon;
22. Withered Scythe — Withering Charge.

All 22 are materialized in [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md).

## Acquisition closure

The exact provider data audit closes **247 normalized acquisition rows across 137 provider item IDs**.

Every counted owner has a current provider-native route:

- recipes: Annihilator Helmet, Atom-independent counted equipment/actions including Axe of Lightning, Buckler, Chorus Blade, Dinosaur Bone Club, Entity Warper, Fiery Boots, Fiery Jaw, The Great Frost, Guard Summoner, Knight Summoner, Monstrous Anchor, Mossy Chestplate, Mossy Hammer, The Tesseract, Totem of Moss, Void Entity Warper, Wand of Clouds and Withered Scythe;
- provider loot: Soul Great Sword from the exact Possessed Paladin loot table;
- Totem of Moss additionally appears in exact Mossy Golem loot.

No counted root is promoted from tooltip text alone.

## Explicit exclusions

### Primary firing/throwing owners — +0

- Atom Splitter — Annihilation Beam and cluster-bomb modes remain primary ranged-weapon firing modes;
- Bottle of Annihilation — ordinary throwable/projectile consumable;
- Chorus Cannon — primary cannon firing mode;
- Sand Cannon / Hand Cannon — primary cannon firing mode;
- Resurrected Javelin — primary javelin throw mode.

These follow the same existing catalog rule used for Pumpkin Pistol, Laser Gatling, ordinary bows/cannons and other primary weapon fire/throw surfaces.

### Other exclusions

- 12 Eye items — locator/encounter-key behavior, not player magic roots;
- Soul Great Sword parry — martial/guard technique; exact `canSoulGreatSwordUseParry` config affects only this excluded branch;
- Monstrous Anchor ordinary attack-area damage — attack consequence, not a second action root;
- Guard/Knight/Moss Golem recolor/stand-still/management interactions — pet management, not extra summons;
- Annihilator chestplate/leggings/boots effects — reactive/passive equipment behavior;
- frost/shulker/spiky shield procs, Golden Halberd bleed, armor reductions and similar on-hit/on-hurt effects — passives/procs;
- `heart_of_tornado` localization/model residue — no exact current registered item/action owner is present;
- particles, sound, cooldowns, spawned sub-projectiles/entities and repeated wave/spike instances — downstream consequences, not new identities;
- boss/mob-native supernatural attacks — not player-owned actions.

## Important deduplications

- Axe of Lightning's Lightning Strike and Electric Burst are separate because they have different player triggers and settlements (`use` versus block `useOn`).
- The Great Frost's directed and radial Ice Spike actions are separate for the same reason.
- Buckler sweep plus its three spawned Annihilation Bombs is one activation root.
- Fiery Jaw push and fire breath settle one right-click action.
- Tesseract's multiple portals and gravity pull settle one charged activation.
- Wand of Clouds' one large + three small clouds settle one entity-interaction action.
- Soul Great Sword's multiple homing daggers settle one action.

## Authority boundary

Legendary Monsters remains authority for input handling, targeting, spawned entities/projectiles, cooldowns, durability/consumption, armor key packets, teleport settlement, summon ownership and config/balance values. Black Arcana catalogs these identities and must not replay provider actions or double-charge their costs/cooldowns.

## Runtime QA remains separate

Catalog closure is not an assembled-pack runtime PASS. Multiplayer owner targeting, keybind conflicts, claims/protection, config values, entity lifecycle, chunk/restart behavior and coexistence with combat/animation mods remain runtime QA.

## Result

**✅ Cataloged — 22 exact-current provider-owned supernatural player actions.**

Strict semantic contribution: **+22 `COUNTED_EXACT`**.
