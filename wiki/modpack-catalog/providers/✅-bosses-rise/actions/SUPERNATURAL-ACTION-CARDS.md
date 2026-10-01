# Bosses'Rise 2.1.2 — supernatural action cards

Status: `8/8 COUNTED_EXACT`

## 1. Skor Gauntlet — Ice Spike Wave

- owner: `block_factorys_bosses:ice_gauntlet`;
- trigger: sneak/right-use release;
- result: provider ice-spike wave / Ice Spike Cluster action;
- acquisition: exact Yeti/Skor loot;
- state: `COUNTED_EXACT`.

## 2. Skor Gauntlet — Ice Slam Leap

- owner: `block_factorys_bosses:ice_gauntlet`;
- trigger: jump while actively holding right-use;
- result: provider ice-slam/leap action;
- acquisition: exact Yeti/Skor loot;
- state: `COUNTED_EXACT`.

Freeze-on-hit and shield behavior are not additional roots.

## 3. Sirok Gauntlet — Earthquake

- owner: `block_factorys_bosses:sandworm_gauntlet`;
- mode: exact `earthquake` operation mode;
- trigger: select by crouch-use on a valid upper surface, then hold use;
- result: provider Sand Column earthquake sequence;
- acquisition: exact Sandworm/Sirok loot;
- state: `COUNTED_EXACT`.

## 4. Sirok Gauntlet — Poison Barrage

- owner: `block_factorys_bosses:sandworm_gauntlet`;
- mode: exact `poison_barrage` operation mode;
- trigger: charge/release use;
- result: provider poison-spit barrage;
- acquisition: exact Sandworm/Sirok loot;
- state: `COUNTED_EXACT`.

Operation-mode selection itself is not a separate action.

## 5. Undying Tentacle — Hook

- owner: `block_factorys_bosses:undying_tentacle`;
- trigger: normal use;
- result: provider tentacle hook/grab action, parameterized by block/entity target;
- acquisition: exact packaged recipe;
- state: `COUNTED_EXACT`.

## 6. Undying Tentacle — Ghost Tentacle Summon

- owner: `block_factorys_bosses:undying_tentacle`;
- trigger: alternate/shift use through the provider summon lifecycle;
- result: owner-bound Ghost Tentacle summons around the player;
- acquisition: exact packaged recipe;
- state: `COUNTED_EXACT`.

Multiple summoned tentacles are one causal summon identity.

## 7. Helvar's Sword — Sword Wave

- owner: `block_factorys_bosses:knight_sword`;
- trigger: right-click charge/release;
- result: provider `SwordWaveEntity` attack with dedicated cooldown;
- acquisition: exact Underworld Knight/Helvar loot;
- state: `COUNTED_EXACT`.

Normal melee attacks are excluded.

## 8. Pirate Saber — Pirate Crew Summon

- owner: `block_factorys_bosses:pirate_saber`;
- trigger: use/finish-use;
- result: owner-bound Crossbow Pirate and Pirate Rook summons;
- acquisition: exact Pirate Captain/Pirate Rook loot;
- state: `COUNTED_EXACT`.

The two spawned entity classes are outcomes of one summon identity.

## Excluded neighboring surfaces

- Skor Gauntlet freeze-on-hit;
- Kraken Trident collision pull/damage;
- ordinary melee/throw/firing modes;
- roll/dodge;
- passive equipment behavior;
- boss-native attacks/phases;
- placement/decor/debug tools;
- particles, animations, projectiles/entities after settlement.

## Result

**8 exact-current provider-owned supernatural player action roots.**
