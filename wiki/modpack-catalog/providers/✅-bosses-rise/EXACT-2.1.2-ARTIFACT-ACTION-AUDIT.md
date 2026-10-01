# Bosses'Rise 2.1.2 — exact artifact action audit

Status: `EXACT PHYSICAL=PUBLISHER / PLAYER-ACTION SURFACE CLOSED`

## Identity gate

Physical sibling authority:

- JAR `block_factorys_bosses-2.1.2-neo-1.21.1.jar`;
- mod id `block_factorys_bosses`;
- version `2.1.2`;
- SHA-1 `249a5f2ba43fd341d4a2831691c154d92aa5a12d`.

NON-MERGE PR #503 downloads CurseForge File `1314084 / 8123167` and fails before semantic inspection unless its SHA-1 equals the physical fingerprint.

Evidence run:

- audit HEAD: `851c6d17607c8877bb1007e84e0c49164e82e9bb`;
- run: `36932226075` — SUCCESS;
- artifact: `11196866408`;
- artifact digest: `sha256:a31172eacf6c45c374414cf2c300b3f31cf440c69b67c53d5efd2e27e58f7348`;
- publisher SHA-1: `249a5f2ba43fd341d4a2831691c154d92aa5a12d`;
- publisher SHA-256: `9e230bd509e7aeb3af4c08125db0340734c0179d83483649a16e45c0ea085e8c`;
- bytes: `23,943,105`.

Result: publisher and physical bytes are identical.

## Bounded inventory

The exact artifact audit records:

- archive entries: **2,683**;
- classes: **802**;
- resources: **1,881**;
- item-like classes: **61**;
- semantic-action-like classes: **30**;
- `data/block_factorys_bosses/**` paths: **292**;
- `assets/block_factorys_bosses/**` paths: **1,430**;
- provider acquisition index: **62 item IDs / 141 rows**.

The item/action scan covers `use`, `useOn`, `releaseUsing`, `finishUsingItem`, `onUseTick`, `hurtEnemy`, `inventoryTick` and provider semantic class references. No JAR bytes are retained in the durable catalog.

## Exact active roots

### IceGauntletItem

Exact localization exposes three behaviors: freeze-on-hit, an ice-spike wave on sneak/right-use release, and an ice-slam leap while jumping during use.

Disposition:

- freeze-on-hit — `EXCLUDED` reactive/on-hit proc;
- ice-spike wave — `COUNTED_EXACT`;
- ice-slam leap — `COUNTED_EXACT`.

`useOn` also interacts with provider Ice Spike Cluster entities; that is a continuation/interaction of the same gauntlet ice system and is not promoted to a third action identity.

### SandwormGauntletItem

The exact binary owns two operation modes:

- `earthquake` — selected through crouch/use-on-top-surface and executed during active use by spawning provider Sand Columns;
- `poison_barrage` — default charge/release path emitting provider Poison Spit projectiles.

Both are deliberate and mechanically distinct player actions, so both are counted. Selecting the operation mode is setup only.

### UndyingTentacleItem

The exact provider exposes two separate use branches:

- normal tentacle hook/grab traversal/control;
- alternate summon lifecycle that spawns owner-bound `GhostTentacleEntity` instances around the player.

Target variants and repeated summon instances are parameters/consequences of the two roots.

### KnightSwordItem

Right-click charge/release emits provider `SwordWaveEntity` objects and settles a dedicated cooldown. This is distinct from ordinary melee swings and is counted once.

### PirateSaberItem

Use/finish-use spawns owner-bound provider pirate summons (`CrossbowPirateEntity` and `PirateRookEntity`) and applies the provider cooldown. The two summon types are outcomes of one summon action root.

## Acquisition closure

The exact provider data closes normal catalog-level reachability:

- `block_factorys_bosses:ice_gauntlet` — `entities/yeti.json` loot;
- `block_factorys_bosses:sandworm_gauntlet` — `entities/sandworm.json` loot;
- `block_factorys_bosses:undying_tentacle` — packaged recipe;
- `block_factorys_bosses:knight_sword` — `entities/underworld_knight.json` loot;
- `block_factorys_bosses:pirate_saber` — Pirate Captain / Pirate Rook entity loot.

## Important exclusions

- `KrakenTridentItem` does not expose a second deliberate cast root; its damage/pull is collision behavior of the thrown weapon and remains excluded;
- ordinary boss-drop weapons without an independent active supernatural action remain excluded;
- provider roll/dodge is martial locomotion, not semantic magic;
- boss AI attacks, phases and arena mechanics are provider-native encounter behavior rather than player-owned magic;
- placement/decor items and debug loot/teleport sticks are not gameplay magic identities.

## Semantic result

Exact current player-owned supernatural action denominator: **8**.

- Ice Spike Wave;
- Ice Slam Leap;
- Earthquake / Sand Columns;
- Poison Barrage;
- Tentacle Hook;
- Ghost Tentacle Summon;
- Sword Wave;
- Pirate Crew Summon.

All eight have current exact identity and catalog-level normal reachability.

Strict semantic contribution: **+8 `COUNTED_EXACT`**.

## Clean-room boundary

The durable catalog retains hashes, counts, identifiers, short behavior classifications and acquisition facts required for cataloging/deduplication. It does not redistribute provider implementation bodies, JAR bytes, models, textures, animations or long localization text.
