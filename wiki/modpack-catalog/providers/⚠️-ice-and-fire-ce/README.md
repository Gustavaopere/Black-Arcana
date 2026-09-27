# Ice And Fire Community Edition — 2.1.2

Status: `⚠️ PARTIAL / EXACT PHYSICAL=PUBLISHER ARTIFACT / EXACT 2.1.2 SOURCE-SEMVER PIN / 7 COUNTED_EXACT ACTION FAMILIES + 2 CONDITIONAL / +7 STRICT / RUNTIME QA SEPARATE`

## Current physical authority

- pack JAR: `iceandfire-2.1.2.jar`;
- mod id: `iceandfire`;
- runtime: `2.1.2`;
- Minecraft / loader: 1.21.1 / current pack NeoForge 21.1.250;
- physical SHA-1: `0786f4142b7cabd958688f68beef3e63e9c0ae8b`;
- CurseForge project/file: `1040076 / 8757837`.

Exact NON-MERGE audit branch `audit/iceandfire-ce-2.1.2-exact-artifact-2026-09-27` materialized File `8757837` and hard-verified the same SHA-1. Physical↔publisher identity is closed.

## Exact release source authority

The public `IAFEnvoy/IceAndFire-CE` `1.21.1` branch has since advanced to 2.1.3. The exact last 2.1.2 checkpoint is `0cf5a2458e1ccf552b9859531ee21c4816e5a686`. Its `gradle.properties` declares Minecraft 1.21.1, NeoForge 21.1.248, mod id `iceandfire` and `mod_version=2.1.2`. The following gradle-properties change (`7d0bb2f93db02877c23d49f3379b2857caf3105d`) explicitly bumps the branch to 2.1.3.

The source pin is version-exact for semantic corroboration, but is not asserted byte-identical to the publisher JAR.

## Current semantic inventory

Exact artifact inspection + exact 2.1.2 source close **9 independent active magic-action families**. A second hash-gated exact-JAR audit run (`36323035696`) closes provider-native recipe/loot acquisition for seven of them.

### Strict-counted — 7

1. Cockatrice Scepter — sustained withering beam; exact current recipe + recipe advancement;
2. Deathworm Gauntlet — active lunge/strike family; three color recipes, one semantic family;
3. Gorgon Head — petrification action; exact Gorgon entity loot table;
4. Pixie Wand — pixie magic-charge projectile; exact current recipe;
5. Siren Flute — targeted charm/love action; exact current recipe;
6. Summoning Crystal — teleport a bound Fire/Ice/Lightning dragon; three variant recipes, one semantic family;
7. Stymphalian Feather Bundle — radial eight-feather volley; exact current recipe.

These seven contribute **+7 `COUNTED_EXACT`** semantic objects.

### Remaining conditional — 2

- **Dread Lich Staff** — the exact source equips Dread Liches with the staff, but the exact provider data scan contains no staff recipe/loot/advancement reference and no explicit provider drop-chance route has been proven. Vanilla equipment-drop behavior is not inferred.
- **Ghost Sword / Phantasmal Blade** — exact current recipe/advancement acquisition is closed, but the swing projectile reads provider-native Jupiter gate `tools.phantasmalBladeAbility`. The deployed value is not available in authoritative project evidence.

See [`ACTIVE-MAGIC-INVENTORY.md`](ACTIVE-MAGIC-INVENTORY.md).

## Explicit exclusions

- Dread Queen Staff — exact 2.1.2 source says it currently has no usage;
- Cyclops Eye — passive `inventoryTick` aura, not a player-selected action;
- Dragon Flute — provider creature-command/control utility;
- Dragon Horn — dragon storage/restore lifecycle utility;
- Tide Trident — provider trident weapon mechanics rather than a distinct magic-action identity;
- silver/dragonblood/dragonsteel post-hit `BuiltinAbilities` — downstream weapon procs, not independently selected casts/actions.

## Runtime authority

Ice And Fire CE remains authority for dragons, mythical mobs, tame/ownership/growth state, Dragon Forge, item/power settlement, Jupiter config and worldgen. Black Arcana must not duplicate those runtimes.

## Runtime QA remains separate

Strict semantic inventory closure does not certify:

- deployed `tools.phantasmalBladeAbility`;
- actual Dread Lich Staff acquisition in the assembled pack;
- current full-pack worldgen/entity availability;
- multiplayer/network settlement;
- item durability/cooldown/config balance;
- interaction with addons or other magic providers.

## Result

**⚠️ Partial / conditioned.** Seven exact, provider-reachable magic-action families are strict-counted; **2** action families remain fail-closed. Current strict contribution: **+7**.
