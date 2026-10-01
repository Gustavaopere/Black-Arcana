# Bosses'Rise — 2.1.2

Status: `✅ CATALOGED / EXACT PHYSICAL=PUBLISHER ARTIFACT / 8 COUNTED_EXACT SUPERNATURAL PLAYER ACTIONS / RUNTIME QA SEPARATE`

## Current physical identity

Current sibling authority identifies:

- physical row: **#79**;
- JAR: `block_factorys_bosses-2.1.2-neo-1.21.1.jar`;
- mod id: `block_factorys_bosses`;
- runtime: `2.1.2`;
- Minecraft / loader: 1.21.1 / NeoForge;
- physical SHA-1: `249a5f2ba43fd341d4a2831691c154d92aa5a12d`.

Bosses'Rise is cross-domain for the Black Arcana catalog. Most of the mod is boss/worldgen/combat content, but the exact current artifact also owns a bounded set of player-invoked supernatural equipment actions.

## Exact publisher-artifact closure

NON-MERGE evidence PR **#503** audits CurseForge project/file `1314084 / 8123167` and hard-gates the artifact against the physical pack SHA-1.

- audit HEAD: `851c6d17607c8877bb1007e84e0c49164e82e9bb`;
- exact-artifact run: `36932226075` — **SUCCESS**;
- evidence artifact: `11196866408`;
- evidence digest: `sha256:a31172eacf6c45c374414cf2c300b3f31cf440c69b67c53d5efd2e27e58f7348`;
- publisher SHA-1: `249a5f2ba43fd341d4a2831691c154d92aa5a12d`;
- publisher SHA-256: `9e230bd509e7aeb3af4c08125db0340734c0179d83483649a16e45c0ea085e8c`;
- bytes: `23,943,105`.

The publisher SHA-1 exactly equals the physical sibling SHA-1.

The exact artifact contains **2,683 archive entries / 802 classes / 1,881 non-class resources / 61 item-like classes / 30 semantic-action-like classes / 292 provider data paths**. Its normalized acquisition index closes **62 provider item IDs across 141 recipe/loot/tag rows**.

See [`EXACT-2.1.2-ARTIFACT-ACTION-AUDIT.md`](EXACT-2.1.2-ARTIFACT-ACTION-AUDIT.md).

## Semantic action inventory — 8 exact roots

### Skor Gauntlet — 2

1. **Ice Spike Wave** — sneak/right-use release produces the provider's ice-spike wave.
2. **Ice Slam Leap** — jump while actively using the gauntlet performs the provider ice-slam/leap action.

The gauntlet's ordinary shield behavior and freeze-on-hit proc are not additional semantic roots.

### Sirok Gauntlet — 2

3. **Earthquake / Sand Columns** — crouch-use on the supported surface selects the exact `earthquake` mode; continued use creates provider Sand Column effects.
4. **Poison Barrage** — the normal charge/release mode emits the provider poison-spit barrage.

Operation-mode selection is setup, not a third identity.

### Undying Tentacle — 2

5. **Tentacle Hook** — normal use hooks the user to a block or pulls an entity toward the user through the provider tentacle action.
6. **Ghost Tentacle Summon** — alternate/shift use completes the provider summon lifecycle and creates owner-bound Ghost Tentacles around the user.

Hook target variants and multiple summoned tentacles are parameters/consequences, not additional identities.

### Helvar's Sword — 1

7. **Sword Wave** — right-click charge/release creates the provider `SwordWaveEntity` attack with a dedicated cooldown/action path.

Normal melee use remains excluded.

### Pirate Saber — 1

8. **Pirate Crew Summon** — use/finish-use creates owner-bound provider pirate summons (Crossbow Pirate and Pirate Rook) and applies the provider cooldown.

Multiple summoned entity types settle one summon action root.

Object cards: [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md).

## Exact acquisition

Catalog-level normal acquisition is closed in the exact artifact:

- Skor Gauntlet (`block_factorys_bosses:ice_gauntlet`) — Yeti/Skor entity loot;
- Sirok Gauntlet (`block_factorys_bosses:sandworm_gauntlet`) — Sandworm/Sirok entity loot;
- Undying Tentacle (`block_factorys_bosses:undying_tentacle`) — packaged recipe;
- Helvar's Sword (`block_factorys_bosses:knight_sword`) — Underworld Knight/Helvar entity loot;
- Pirate Saber (`block_factorys_bosses:pirate_saber`) — provider Pirate Captain/Pirate Rook entity loot.

## Metric exclusions

Explicitly excluded from the semantic-magic numerator:

- Skor Gauntlet freeze-on-hit;
- Kraken Trident collision pull/damage as a thrown-weapon collision consequence;
- ordinary melee/ranged firing/throwing modes;
- the provider roll/dodge mechanic;
- armor/equipment passive effects;
- boss-native attacks and phases;
- decoration placement items and structure/debug tools;
- particles, animations, cinematics, cooldown/resource state and downstream spawned effects.

These may be mechanically supernatural-looking, but they are not additional discrete player-owned magic identities under the canonical metric.

## Authority boundary

Bosses'Rise remains authority for its item inputs, targeting, summoned entities/projectiles, cooldowns, durability, animation state and settlement. Black Arcana catalogs the identities and must not replay the same ability, duplicate cooldown/resource charging or count downstream projectiles/entities as separate spells.

## Runtime QA remains separate

Catalog closure does not claim assembled-pack runtime PASS. Multiplayer owner targeting, Epic Fight interaction, Better Combat compatibility, GeckoLib animation timing, structure/protection behavior, Distant Horizons coexistence and server configs remain runtime QA.

## Result

**✅ Cataloged — `COUNTED_EXACT`.**

Current Bosses'Rise 2.1.2 semantic contribution: **8 exact-current supernatural player-action identities**.

Strict semantic delta: **+8**.
