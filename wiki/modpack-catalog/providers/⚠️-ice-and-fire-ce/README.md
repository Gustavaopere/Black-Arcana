# Ice And Fire Community Edition — 2.1.2

Status: `⚠️ PARTIAL / EXACT PHYSICAL=PUBLISHER ARTIFACT / EXACT 2.1.2 SOURCE-SEMVER PIN / 9 ACTIVE MAGIC-ACTION CANDIDATES / +0 STRICT PENDING REACHABILITY+CONFIG`

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

## Current semantic candidate inventory

Exact artifact inspection closes the current item/class surface; exact 2.1.2 source closes the player-facing behavior of **9 independent active magic-action candidates**:

1. Cockatrice Scepter — sustained withering beam;
2. Deathworm Gauntlet — active lunge/strike action (three color variants, one semantic family);
3. Gorgon Head — petrification action;
4. Dread Lich Staff — dread-skull projectile;
5. Pixie Wand — pixie magic-charge projectile;
6. Siren Flute — targeted charm/love action;
7. Summoning Crystal — teleport a bound Fire/Ice/Lightning dragon (three crystal variants, one semantic family);
8. Stymphalian Feather Bundle — radial eight-feather volley;
9. Ghost Sword / Phantasmal Blade — swing-triggered ghost-sword projectile.

See [`ACTIVE-MAGIC-INVENTORY.md`](ACTIVE-MAGIC-INVENTORY.md).

## Why the provider remains ⚠️

This tranche deliberately contributes **+0 strict**. The action identities are sufficiently bounded to catalog, but current survival/reachability is not closed one-by-one against the assembled pack. Ghost Sword additionally has an exact provider-native gate: `tools.phantasmalBladeAbility`. The exact 2.1.2 source default is `true`, but source defaults are not substituted for deployed Jupiter config.

## Explicit exclusions

- Dread Queen Staff — exact 2.1.2 source says it currently has no usage;
- Cyclops Eye — passive `inventoryTick` aura, not a player-selected action;
- Dragon Flute — provider creature-command/control utility;
- Dragon Horn — dragon storage/restore lifecycle utility;
- Tide Trident — provider trident weapon mechanics rather than a distinct magic-action identity;
- silver/dragonblood/dragonsteel post-hit `BuiltinAbilities` — downstream weapon procs, not independently selected casts/actions.

## Runtime authority

Ice And Fire CE remains authority for dragons, mythical mobs, tame/ownership/growth state, Dragon Forge, item/power settlement, Jupiter config and worldgen. Black Arcana must not duplicate those runtimes.

## Result

**⚠️ Partial / conditioned.** Exact physical identity and the 9-action candidate surface are cataloged; strict contribution remains **+0** pending reachability/config closure.
