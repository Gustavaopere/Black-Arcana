# Eidolon: Repraised 0.5.0.2 — Ritual Catalog

Status: `10/10 ACTIVE HARDCODED RITUALS INVENTORIED / REQUIREMENT RECIPES STILL PENDING`

Canonical source: `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`

## Registry authority

`RitualRegistry.init()` registers exactly 10 active hardcoded rituals in 0.5.0.2. A larger set of summon/sanguine rituals is present only inside a block comment and is **not active registry content** in this build.

| # | Runtime id | Class | Verified effect |
|---:|---|---|---|
| 1 | `eidolon_repraised:crystal` | `CrystalRitual` | kills valid undead in ritual bounds with ritual damage and drops 1–3 Soul Shards per successful kill |
| 2 | `eidolon_repraised:deceit` | `DeceitRitual` | every 20 ticks scans villagers in 48×16×48 inflated area; each has 1/120 chance to decay gossip |
| 3 | `eidolon_repraised:allure` | `AllureRitual` | every 200 ticks can inject movement goals that draw animals from up to 96 horizontal blocks toward the ritual |
| 4 | `eidolon_repraised:repelling` | `RepellingRitual` | every 200 ticks injects movement goals pushing monsters inside ~80 blocks toward ~90-block-away targets, removing goals after ~88 blocks |
| 5 | `eidolon_repraised:daylight` | `DaylightRitual` | advances day time by +100 per tick while in night/very-early-day window until daytime threshold is reached |
| 6 | `eidolon_repraised:moonlight` | `MoonlightRitual` | advances day time by +100 per tick during day until night threshold is reached |
| 7 | `eidolon_repraised:purify` | `PurifyRitual` | immediately cures Zombie Villagers and converts Zombified Piglins/Zoglins back to Piglins/Hoglins in default ritual bounds |
| 8 | `eidolon_repraised:recharging_soulfire` | `RechargingRitual` | recharges the first compatible `IRechargeableWand` ritual focus found |
| 9 | `eidolon_repraised:recharging_chill` | `RechargingRitual` | same generic recharge runtime class; distinction is registry/recipe-side |
| 10 | `eidolon_repraised:absorption` | `AbsorptionRitual` | serializes eligible weakened undead/whitelisted entities into a Summoning Staff, removes them from world and adds them as charges |

## Ritual lifecycle and bounds

The provider `Ritual` base class separates:

- step requirements;
- continuous/invariant requirements;
- `setup(...)` progression;
- `start(...)` one-shot behavior;
- `tick(...)` persistent behavior;
- `PASS` versus `TERMINATE` lifecycle results.

Default search bounds are:

- X: `pos.x - 8` to `pos.x + 9`;
- Y: `pos.y - 6` to `pos.y + 11`;
- Z: `pos.z - 8` to `pos.z + 9`.

Individual rituals may deliberately use larger custom AABBs, as Allure, Repelling and Deceit do.

## Detailed findings

### Crystal — `eidolon_repraised:crystal`

`CrystalRitual.start()` finds LivingEntities matching `Eidolon::isValidUndead` inside its search bounds. It applies `Registry.RITUAL_DAMAGE` equal to `maxHealth × 1000`. Only when the hurt call succeeds does it emit the crystallization effect and spawn **1–3 Soul Shards**. The ritual then terminates.

Integration consequence: Soul Shard generation is provider-native loot/economy and must not be replayed by Black Arcana when observing the same kill.

### Deceit — `eidolon_repraised:deceit`

Every 20 game ticks, villagers within an AABB inflated by `(48,16,48)` are inspected. Each villager independently has a `1/120` chance to call `gossips.decay()` on that pass. The ritual persists.

### Allure — `eidolon_repraised:allure`

Every 200 ticks, animals within `(96,16,96)` are evaluated. Animals without an active Eidolon `GoToPositionGoal`, at least 12 blocks from the ritual, have a `1/40` chance to receive a priority-1 goal toward a random position around the ritual. The injected goal is removed once the animal comes within 8 blocks.

### Repelling — `eidolon_repraised:repelling`

Every 200 ticks, monsters within `(96,16,96)` are evaluated. Monsters at or within 80 blocks receive a priority-1 Eidolon movement goal targeting a point roughly 90 blocks away from the ritual along the radial direction. The goal is removed after the monster moves beyond 88 blocks.

### Daylight / Moonlight

Both rituals directly mutate `PrimaryLevelData.dayTime` by **+100** and broadcast `ClientboundSetTimePacket` to players on the level.

- Daylight continues when time-of-day is `<1000` or `>=12000`, then terminates during daytime.
- Moonlight continues when time-of-day is `<13000`, then terminates once night is reached.

These are provider-native global time mutations. A Black Arcana time system must deduplicate any observation and must not apply a second time increment.

### Purify — `eidolon_repraised:purify`

One-shot ritual over default ritual bounds:

- Zombie Villager -> invokes native `finishConversion`;
- Zombified Piglin -> removes original and spawns a Piglin at the same position;
- Zoglin -> removes original and spawns a Hoglin at the same position.

The ritual then terminates.

### Recharging rituals

Both active registry ids use `RechargingRitual`. It finds ritual item foci, chooses the first focus whose item implements `IRechargeableWand`, replaces it with the provider-returned recharged stack, emits a consume packet when server-side and terminates.

The exact difference between `recharging_soulfire` and `recharging_chill` is not encoded in the runtime class; it depends on the associated ritual recipe/requirements and therefore remains recipe-audit territory.

### Absorption — `eidolon_repraised:absorption`

Server-side only. The ritual:

1. finds a Summoning Staff ritual focus if present;
2. selects LivingEntities in ritual bounds that are undead or in the enthrall whitelist, not blacklisted, not players, not already enthralled, and at `<= 1/3` max health;
3. heals each selected entity to max health before serialization;
4. serializes full entity NBT;
5. removes the entity with `RemovalReason.KILLED`;
6. adds the serialized entities to the Summoning Staff as charges.

Integration consequence: this is a provider-native capture/serialization transaction, not a generic kill. Black Arcana quest/perk logic must distinguish absorption from ordinary combat death and avoid granting duplicate kill/progression credit unless design explicitly allows it.

## Disabled/commented registry content

The source contains commented-out definitions for:

- summon zombie;
- summon skeleton;
- summon phantom;
- summon husk;
- summon drowned;
- summon stray;
- summon wither skeleton;
- summon wraith;
- sanguine sapping sword;
- sanguine amulet.

These are **not active rituals in 0.5.0.2** and must not appear as available gameplay content based only on dead source code.

## Remaining ritual work

The active runtime registry is now 10/10 inventoried. Still pending before `CATÁLOGO GRANULAR COMPLETO`:

- exact ritual recipe/requirement data for each active registry id;
- focus items and sacrifice inputs;
- progression/research gates to learn or invoke each ritual;
- runtime validation on dedicated server;
- interaction with death/loot/progression hooks from other installed mods.