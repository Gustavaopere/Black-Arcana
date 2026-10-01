# Legendary Monsters 2.2.2 — exact artifact action audit

Status: `EXACT PHYSICAL=PUBLISHER / PLAYER-ACTION DENOMINATOR CLOSED`

## Identity gate

- physical JAR: `legendary_monsters-2.2.2 MC 1.21.1.jar`;
- mod id: `legendary_monsters`;
- physical SHA-1: `8910859ba94190dd8cbc8c2c1e2f07562db729b4`;
- CurseForge project/file: `944035 / 8715533`.

NON-MERGE PR #507 hard-fails before semantic inspection unless publisher SHA-1 equals the physical pack fingerprint.

Final evidence checkpoint:

- HEAD: `c96e9d4e812adc50b65f5fac9859add3a6440cef`;
- audit run: `36940087686` — SUCCESS;
- evidence artifact: `11199527544`;
- artifact digest: `sha256:b7e91eb417b2095c669a6dd102ed797c88b74e6186339545a5f2c03996417ae1`;
- publisher SHA-1: `8910859ba94190dd8cbc8c2c1e2f07562db729b4`;
- publisher SHA-256: `63cd850d2e15b80ffc20cc2319cdac011dd8e675c675a8281bd29376d11a9120`;
- bytes: `44,757,560`.

Result: exact physical/publisher byte identity is proven by SHA-1.

## Bounded exact inventory

- archive entries: **3,415**;
- classes: **1,217**;
- non-class resources: **2,198**;
- item classes: **96**;
- action-shaped classes: **109**;
- `data/legendary_monsters/**` paths: **552**;
- classes referencing player interaction/input surfaces: **49**;
- normalized acquisition rows: **247**;
- provider item IDs with acquisition evidence: **137**.

The audit disassembles the complete exact player-interaction candidate set and separately scans all provider classfiles for use/useOn/release/key/right-click interaction signatures. Public 2.1.15 source is used only as non-authoritative corroboration where useful; 2.2.2 bytecode/resources remain the authority.

## Counted semantic roots

Exact player-action reconciliation closes **22 `COUNTED_EXACT` roots** across 20 owner/activation surfaces.

Two owners contribute two roots each because their triggers/settlements are distinct:

- Axe of Lightning: right-click Lightning Strike versus block-use Electric Burst;
- The Great Frost: directed use versus shift/block-use radial Ice Spikes.

The other 18 owner/activation surfaces contribute one root each, including the exact Teleport Machine + Eye Crystal boss summon.

## Exact Teleport Machine closure

Run 6 adds bounded disassembly of:

- `TeleportMachineBlock`;
- `TeleportMachineBlockEntity`.

Exact bytecode proves:

1. `useItemOn` requires `ModItems.EYE_CRYSTAL` and an inactive machine;
2. one Eye Crystal is shrunk outside creative;
3. provider state is switched active;
4. the BlockEntity tick lifecycle constructs `TheObliteratorEntity` using `ModEntities.THE_OBLITERATOR`;
5. the server calls `Level.addFreshEntity` for the boss;
6. provider state returns inactive after settlement.

Exact provider data also closes `legendary_monsters:eye_crystal` acquisition through `data/legendary_monsters/loot_table/entities/annihilation_pursuer.json`.

This is one deliberate player-triggered summon identity, not a passive world-spawn or proximity event.

## Acquisition closure

Counted item/equipment owners are exact-reachable through provider recipes except Soul Great Sword, whose provider loot table is Possessed Paladin. The Teleport Machine's activation key is exact-reachable through Annihilation Pursuer loot. No counted root is promoted from localization alone.

## Exclusion audit

The exact artifact also exposes magic-adjacent or supernatural-looking surfaces that add **0** semantic identities:

- Atom Splitter's Annihilation Beam / Cluster Annihilation Bomb — primary charged firing modes of the weapon;
- Bottle of Annihilation, Chorus Cannon, Sand Cannon / Hand Cannon and Resurrected Javelin — ordinary primary throw/fire modes;
- Withered Scythe — physical forward charge/damage weapon technique;
- Eye items — locator behavior;
- shield/on-hurt/on-hit/armor effects — reactive/passive;
- Soul Great Sword parry — guard technique;
- summon-management/recolor/stand-still interactions — management of already-created companions;
- unregistered `heart_of_tornado` residue;
- mob/boss-native powers;
- spawned entities/projectiles/particles/waves and repeated ticks produced by a counted activation.

## Clean-room boundary

The durable catalog retains only hashes, identifiers, counts, concise control-flow facts, acquisition paths and semantic dispositions needed for cataloging/interoperability. JAR bytes, implementation bodies and assets are not committed.

## Result

**22 exact-current supernatural player actions; strict delta +22.**
