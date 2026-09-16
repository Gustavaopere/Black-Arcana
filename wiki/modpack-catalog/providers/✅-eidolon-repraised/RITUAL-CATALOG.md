# Eidolon: Repraised 0.5.0.2 — Ritual Catalog

Status: `10/10 GENERIC RITUAL PROTOTYPES + 24/24 OFFICIAL RITUAL RECIPES INVENTORIED / RUNTIME QA PENDING`

Canonical source: `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`

## Runtime architecture

Eidolon 0.5.0.2 has two distinct ritual layers:

1. `RitualRegistry.init()` registers **10 generic ritual prototypes** referenced by `GenericRitualRecipe`;
2. `EidRitualProvider` generates **24 official ritual recipes**, some of which instantiate their ritual class dynamically instead of resolving a hardcoded `RitualRegistry` entry.

This distinction is critical. Commented-out hardcoded summon constants in `RitualRegistry` do **not** mean summoning is inactive: `SummonRitualRecipe.getRitual()` constructs a new `SummonRitual` directly from the recipe's entity id. The committed 0.5.0.2 generated resources contain all 11 summon recipes described below.

## A. Generic provider ritual prototypes — 10/10

| # | Runtime id | Class | Reagent | Pedestal / invariant requirements | Verified effect |
|---:|---|---|---|---|---|
| 1 | `eidolon_repraised:crystal` | `CrystalRitual` | Bone Meal | Redstone Dust ×2 | kills valid undead with ritual damage and drops 1–3 Soul Shards per successful kill |
| 2 | `eidolon_repraised:deceit` | `DeceitRitual` | Emerald-gem tag | Emerald-gem tag; Fermented Spider Eye; Mushroom tag; Soul Shard ×2 | periodically decays villager gossip |
| 3 | `eidolon_repraised:allure` | `AllureRitual` | Rose Bush | Golden Apple; Red Dye ×2; Soul Shard ×2 | periodically injects movement goals that lure animals inward |
| 4 | `eidolon_repraised:repelling` | `RepellingRitual` | Nautilus Shell | Iron-ingot tag; Leather; Quartz-gem tag; Soul Shard ×2 | periodically injects movement goals that drive monsters outward |
| 5 | `eidolon_repraised:daylight` | `DaylightRitual` | Sunflower | Charcoal; Wheat Seeds; Soul Shard ×2 | advances world time toward day |
| 6 | `eidolon_repraised:moonlight` | `MoonlightRitual` | Black-dye tag | Snowball; Spider Eye; Soul Shard ×2 | advances world time toward night |
| 7 | `eidolon_repraised:purify` | `PurifyRitual` | Glistering Melon Slice | Enchanted Ash ×2; Potion of Healing; Soul Shard ×2 | cures/converts selected undead forms |
| 8 | `eidolon_repraised:recharging_soulfire` | `RechargingRitual` | Lesser Soul Gem | Blaze Powder ×2; Redstone Dust; invariant Soulfire Wand | recharges compatible Soulfire Wand focus |
| 9 | `eidolon_repraised:recharging_chill` | `RechargingRitual` | Lesser Soul Gem | Snowball ×2; Redstone Dust; invariant Bonechill Wand | recharges compatible Bonechill Wand focus |
| 10 | `eidolon_repraised:absorption` | `AbsorptionRitual` | Death Essence | Tattered Cloth ×2; Bone; Soul Shard ×2; invariant Summoning Staff | captures eligible weakened entities into the Summoning Staff |

`GenericRitualRecipe.getRitual()` resolves these ids through `RitualRegistry.find(...)`; invariant focus items are restored as `FocusItemPresentRequirement`s when the runtime ritual is materialized.

## B. Data-driven summon rituals — 11/11

`SummonRitualRecipe.getRitual()` dynamically constructs `SummonRitual(entity,count)`. Server-side, the ritual creates the requested entity, runs NeoForge's mob finalize-spawn hook with `MobSpawnType.MOB_SUMMONED`, allows Mob instances to pick up loot and terminates after spawning the configured count.

| Runtime recipe id | Count | Reagent | Pedestal requirements | Focus requirements |
|---|---:|---|---|---|
| `eidolon_repraised:summon_zombie` | 1 | Charcoal | Soul Shard + Rotten Flesh | Rotten Flesh |
| `eidolon_repraised:summon_skeleton` | 1 | Charcoal | Soul Shard + Bone | Bone |
| `eidolon_repraised:summon_phantom` | 1 | Charcoal | Soul Shard + Phantom Membrane | Phantom Membrane |
| `eidolon_repraised:summon_creeper` | 1 | Charcoal | Soul Shard + Gunpowder | Gunpowder |
| `eidolon_repraised:summon_wither_skeleton` | 1 | Charcoal | Soul Shard + Bone | Soul Sand |
| `eidolon_repraised:summon_husk` | 3 | Charcoal | Soul Shard + Rotten Flesh | sand-tag ingredient |
| `eidolon_repraised:summon_drowned` | 3 | Charcoal | Soul Shard + Rotten Flesh | prismarine-gem-tag ingredient |
| `eidolon_repraised:summon_stray` | 1 | Charcoal | Soul Shard + Bone | String |
| `eidolon_repraised:summon_wraith` | 1 | Charcoal | Soul Shard + Tattered Cloth | Tattered Cloth |
| `eidolon_repraised:summon_slimy_slug` | 3 | Pumpkin Seeds | Soul Shard + Slime Ball | none |
| `eidolon_repraised:summon_raven` | 3 | Beetroot Seeds | Soul Shard + Feather | none |

The generator helper names `summon_slugs` / `summon_ravens` are not runtime ids. `SummonRitualRecipe.getId()` derives the actual id from the entity registry path, matching the committed generated files `summon_slimy_slug.json` and `summon_raven.json`.

### Summon authority

The ritual class itself does not mark these mobs as player-owned/tamed. Black Arcana must not infer ownership merely because `MobSpawnType.MOB_SUMMONED` was used. Any perk that distinguishes servant/familiar/summon from ordinary mobs needs a provider-supported ownership signal, not spawn-cause guesswork.

## C. Brazier crafting rituals — 2/2

| Runtime recipe id | Reagent | Pedestal requirements | Focus | Health requirement | Result |
|---|---|---|---|---:|---|
| `eidolon_repraised:brazier_craft_sapping_sword` | Iron Sword | Shadow Gem; Soul Shard ×2; Nether Wart ×2; Ghast Tear | Potion of Harming | 20 | Sapping Sword |
| `eidolon_repraised:brazier_craft_sanguine_amulet` | Basic Amulet | Diamond-gem tag; Redstone Dust ×4; Lesser Soul Gem | Potion of Harming | 40 | Sanguine Amulet |

`ItemRitualRecipe` materializes a `CraftingRitual`/`SanguineRitual`. The health requirement belongs to the provider ritual transaction; Black Arcana must not apply a second life cost or count this as ordinary crafting without classification.

## D. Structure locator ritual — 1/1

Runtime id: `eidolon_repraised:ritual_locate_catacombs`.

- target structure tag: Eidolon's Catacombs;
- reagent: Map;
- pedestal: Compass + Magic Ink + Raven Feather;
- focus: none;
- health requirement: 0.

`LocationRitualRecipe.getId()` derives the runtime id from the structure tag rather than from the unused descriptive `ResourceLocation` argument passed by the datagen helper. This is a provider-native structure-divination capability.

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

## Detailed generic ritual semantics

### Crystal

Finds LivingEntities matching `Eidolon::isValidUndead` inside ritual bounds. It applies `Registry.RITUAL_DAMAGE` equal to `maxHealth × 1000`. Only a successful hurt produces the crystallization effect and **1–3 Soul Shards**. The ritual then terminates.

Integration consequence: the kill and Soul Shard generation are one provider-native ritual transaction; external progression must deduplicate both.

### Deceit

Every 20 game ticks, villagers in an AABB inflated by `(48,16,48)` are inspected. Each independently has a `1/120` chance to call gossip decay on that pass.

### Allure

Every 200 ticks, animals within `(96,16,96)` are evaluated. Animals without an active Eidolon `GoToPositionGoal`, at least 12 blocks from the ritual, have a `1/40` chance to receive a priority-1 movement goal toward a random position around the ritual. The injected goal is removed within 8 blocks.

### Repelling

Every 200 ticks, monsters within `(96,16,96)` are evaluated. Monsters at or within 80 blocks receive a priority-1 movement goal toward a point roughly 90 blocks away along the radial direction; the provider removes the goal beyond roughly 88 blocks.

### Daylight / Moonlight

Both directly mutate `PrimaryLevelData.dayTime` by **+100 per tick** and broadcast a time packet to players on the level.

- Daylight advances while time-of-day is `<1000` or `>=12000` and terminates in daytime.
- Moonlight advances while time-of-day is `<13000` and terminates after reaching night.

A Black Arcana time system must never apply a second increment for the same provider tick.

### Purify

One-shot conversion over default ritual bounds:

- Zombie Villager -> provider invokes native conversion completion;
- Zombified Piglin -> replaced by Piglin;
- Zoglin -> replaced by Hoglin.

### Recharging Soulfire / Chill

Both use `RechargingRitual`; the recipe-level invariant is what distinguishes the required focus:

- Soulfire -> Soulfire Wand;
- Chill -> Bonechill Wand.

The ritual selects a compatible `IRechargeableWand` focus, replaces it with the provider-returned recharged stack and terminates.

### Absorption

Server-side only. The ritual:

1. requires a Summoning Staff focus;
2. selects LivingEntities in bounds that pass Eidolon's undead/enthrall whitelist/blacklist rules, are not players/already enthralled, and are at `<= 1/3` max health;
3. heals each selected entity to max health before serialization;
4. serializes full entity NBT;
5. removes the entity with `RemovalReason.KILLED`;
6. stores the serialized entities as Summoning Staff charges.

This is provider-native capture/serialization, not an ordinary combat kill. Kill/progression systems must explicitly classify it to avoid duplicate or unintended rewards.

## Corrected conclusion

The earlier inference that commented hardcoded summon/sanguine constants meant those gameplay rituals were inactive was incorrect. Exact 0.5.0.2 datagen + committed generated resources prove **24 official ritual recipes**. The provider's ritual surface is therefore substantially larger than the 10-entry `RitualRegistry` alone.

Remaining work before runtime confirmation:

- dedicated-server execution of representative generic, summon, crafting and locator rituals;
- verify health-requirement settlement and ingredient/focus consumption in the installed JAR;
- verify survival visibility/unlocks in Codex/research;
- verify interactions with death/loot/time/AI hooks from the full modpack.