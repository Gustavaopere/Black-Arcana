# Legendary Monsters — 2.2.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 22 COUNTED_EXACT SUPERNATURAL PLAYER ACTIONS / RUNTIME QA SEPARATE`

## Current physical identity

- sibling physical row: **#371**;
- JAR: `legendary_monsters-2.2.2 MC 1.21.1.jar`;
- mod id: `legendary_monsters`;
- release line: `2.2.2` for Minecraft 1.21.1;
- physical SHA-1: `8910859ba94190dd8cbc8c2c1e2f07562db729b4`.

Legendary Monsters is primarily a boss/equipment/world-content provider, but the exact installed artifact also owns a bounded set of deliberate supernatural player actions. The catalog counts those actions without reclassifying every projectile, locator, passive proc, pet-management interaction or mob-native attack as magic.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#507** audits CurseForge project/file `944035 / 8715533` and hard-gates the publisher artifact against the physical pack fingerprint.

Final exact evidence checkpoint:

- audit HEAD: `c96e9d4e812adc50b65f5fac9859add3a6440cef`;
- exact-artifact run: `36940087686` — **SUCCESS**;
- evidence artifact: `11199527544`;
- artifact digest: `sha256:b7e91eb417b2095c669a6dd102ed797c88b74e6186339545a5f2c03996417ae1`;
- publisher SHA-1: `8910859ba94190dd8cbc8c2c1e2f07562db729b4`;
- publisher SHA-256: `63cd850d2e15b80ffc20cc2319cdac011dd8e675c675a8281bd29376d11a9120`;
- bytes: `44,757,560`.

The publisher SHA-1 exactly equals the current physical sibling SHA-1.

The exact artifact contains **3,415 archive entries / 1,217 classes / 2,198 non-class resources / 96 item classes / 109 action-shaped classes / 552 provider data paths**. Exhaustive classfile scanning closes **49 interaction-reference classes** and the provider data audit closes **247 normalized acquisition rows across 137 provider item IDs**.

See [`EXACT-2.2.2-ARTIFACT-ACTION-AUDIT.md`](EXACT-2.2.2-ARTIFACT-ACTION-AUDIT.md).

## Semantic inventory — 22 exact roots

After object-level classification and deduplication, Legendary Monsters 2.2.2 contributes **22 deliberate supernatural player actions**:

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
22. Teleport Machine + Eye Crystal — Obliterator Summon.

All 22 are `COUNTED_EXACT`.

Object-level cards:

- aggregate: [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md);
- [Annihilator Helmet — Targeted Teleport](actions/annihilator-helmet-targeted-teleport.md);
- [Axe of Lightning — Lightning Strike](actions/axe-lightning-strike.md);
- [Axe of Lightning — Electric Burst](actions/axe-electric-burst.md);
- [Buckler of Annihilation — Sweep + Bombs](actions/buckler-annihilation-sweep-bombs.md);
- [Chorus Blade — Random Teleport](actions/chorus-blade-random-teleport.md);
- [Dinosaur Bone Club — Circular Shockwaves](actions/dinosaur-bone-club-shockwaves.md);
- [Entity Warper — Radius Entity Warp](actions/entity-warper-radius-warp.md);
- [Fiery Boots — Fire Trail](actions/fiery-boots-fire-trail.md);
- [Fiery Jaw — Fire Breath + Repulsion](actions/fiery-jaw-fire-breath-repulsion.md);
- [The Great Frost — Directed Ice Spikes](actions/great-frost-directed-ice-spikes.md);
- [The Great Frost — Radial Ice Spikes](actions/great-frost-radial-ice-spikes.md);
- [Guard Summoner — Guard Summon](actions/guard-summoner.md);
- [Knight Summoner — Knight Summon](actions/knight-summoner.md);
- [Monstrous Anchor — Launch + Stun Burst](actions/monstrous-anchor-launch-stun.md);
- [Mossy Chestplate — Poison Cloud Field](actions/mossy-chestplate-poison-field.md);
- [Mossy Hammer — Poison/Moss Shockwave](actions/mossy-hammer-shockwave.md);
- [Soul Great Sword — Phantom Daggers](actions/soul-great-sword-phantom-daggers.md);
- [The Tesseract — Annihilation Portal Star](actions/tesseract-portal-star.md);
- [Totem of Moss — Mossy Golem Summon](actions/totem-moss-golem-summon.md);
- [Void Entity Warper — Targeted Entity Warp](actions/void-entity-warper-targeted-warp.md);
- [Wand of Clouds — Explosive Cloud Summon](actions/wand-clouds-explosive-cloud.md);
- [Teleport Machine + Eye Crystal — Obliterator Summon](actions/teleport-machine-obliterator-summon.md);

Individual-card checkpoint: [`INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md`](INDIVIDUAL-ACTION-CARDS-CHECKPOINT.md).

## Why the summon items count

Guard Summoner, Knight Summoner and Totem of Moss each have a deliberate player activation whose provider settlement creates an owner-bound/tamed combat companion. Existing catalog precedent counts deliberate player-owned summon actions (for example Born in Chaos summon artifacts and Bosses'Rise Pirate Crew Summon) while excluding later pet-management interactions and the summoned mob's own attacks.

## Teleport Machine summon closure

The exact 2.2.2 JAR separately proves one structure/block-based summoning action:

- `TeleportMachineBlock.useItemOn` requires `legendary_monsters:eye_crystal` and consumes one outside creative;
- the activation sets the provider BlockEntity active;
- the exact BlockEntity tick lifecycle instantiates `THE_OBLITERATOR` and calls server `addFreshEntity`;
- the same exact artifact gives `legendary_monsters:eye_crystal` in the Annihilation Pursuer loot table.

This is one player-triggered provider summon identity. Charge particles, delay ticks and boss spawn animation are consequences/parameters, not extra roots.

## Acquisition closure

Every counted item/equipment owner has a provider-native recipe or loot route in the exact artifact. Soul Great Sword is closed through Possessed Paladin loot; Eye Crystal is closed through Annihilation Pursuer loot; the remaining counted item/equipment owners have exact provider recipes.

## Explicit exclusions

- **Atom Splitter** — Annihilation Beam and Cluster Annihilation Bomb are the weapon's two primary charged firing modes; they are not promoted as independent magic roots, matching the existing primary-fire exclusion used for Pumpkin Pistol/cannons and WOM technological weapon actions;
- Bottle of Annihilation, Chorus Cannon, Sand Cannon / Hand Cannon and Resurrected Javelin — ordinary primary throw/fire modes;
- **Withered Scythe** — forward charge/damage is a martial movement/weapon technique, not a supernatural semantic identity;
- 12 Eye items — structure/encounter locators, not player magic roots;
- Soul Great Sword parry — martial guard/parry technique; Phantom Daggers remain the separate counted supernatural branch;
- Annihilator chestplate/leggings/boots, shield procs, Golden Halberd bleed and similar on-hit/on-hurt/armor behavior — passive or reactive effects;
- `heart_of_tornado` — localization/model residue without an exact current registered player-action owner;
- recolor, stand-still and respawn management for tamed summons — pet management, not new summon identities;
- particles, sounds, cooldowns, repeated spikes/waves/clouds/portals, spawned sub-projectiles and individual boss attacks — downstream consequences;
- boss/mob-native supernatural attacks — not player-owned actions.

## Deduplication boundary

Axe of Lightning and The Great Frost each count twice because exact 2.2.2 exposes two causally distinct player triggers with separate settlements. Buckler's sweep plus three bombs, Fiery Jaw's push plus fire breath, Tesseract's multiple portals/gravity pull, Wand of Clouds' multiple cloud entities and each summon lifecycle remain one root per player activation.

## Authority boundary

Legendary Monsters remains authority for input handling, targeting, summon ownership, teleports, projectiles/entities, cooldowns, durability/consumption, armor key packets, block-entity lifecycle and balance/config values. Black Arcana catalogs these identities and must not replay provider actions or double-charge their settlement.

## Runtime QA remains separate

Catalog closure is not an assembled-pack runtime PASS. Multiplayer ownership, keybind conflicts, claims/protection, chunk/restart lifecycle, effective config, entity persistence and coexistence with combat/animation mods remain runtime QA.

## Result

**✅ Cataloged — 22 exact-current provider-owned supernatural player actions.**

Strict semantic contribution: **+22 `COUNTED_EXACT`**.
