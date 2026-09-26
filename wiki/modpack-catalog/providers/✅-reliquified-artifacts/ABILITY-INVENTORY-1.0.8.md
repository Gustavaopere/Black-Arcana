# Reliquified Artifacts 1.0.8 — owner-scoped ability inventory

Status: `52/52 OWNER-SCOPED ABILITY ROOTS / SOURCE-PINNED 1.0.8 / SURVIVAL ROUTES BOUNDED`

Official source checkpoint: `Octo-Studios/reliquified-artifacts@529fa0cd865a95dbe1bf02081de0275e90c69aee`.

The provider does not register 48 replacement items under its own namespace. Instead, `ModItemsMixin` redirects **48 `artifacts:<id>` owners** to Reliquified implementation classes. `plastic_drinking_hat` and `novelty_drinking_hat` share `DrinkingHatItem`, so 48 owners map to 47 implementation classes.

Counting uses **owner + ability ID**, not ability string alone. Reused IDs such as `meal`, `jump`, and the shared drinking-hat class remain distinct owner-scoped roots when attached to distinct Artifacts item identities.

| # | Artifact owner | Ability root | Reliquified class |
|---:|---|---|---|
| 1 | `artifacts:plastic_drinking_hat` | `drinking` | `DrinkingHatItem` |
| 2 | `artifacts:novelty_drinking_hat` | `drinking` | `DrinkingHatItem` |
| 3 | `artifacts:snorkel` | `snorkeling` | `SnorkelItem` |
| 4 | `artifacts:villager_hat` | `trade_surge` | `VillagerHatItem` |
| 5 | `artifacts:villager_hat` | `golem_guard` | `VillagerHatItem` |
| 6 | `artifacts:superstitious_hat` | `looting` | `SuperstitiousHatItem` |
| 7 | `artifacts:anglers_hat` | `catch` | `AnglersHatItem` |
| 8 | `artifacts:lucky_scarf` | `fortune` | `LuckyScarfItem` |
| 9 | `artifacts:scarf_of_invisibility` | `invisibility` | `ScarfOfInvisibilityItem` |
| 10 | `artifacts:flame_pendant` | `fire` | `FlamePendantItem` |
| 11 | `artifacts:shock_pendant` | `shock` | `ShockPendantItem` |
| 12 | `artifacts:thorn_pendant` | `poison` | `ThornPendantItem` |
| 13 | `artifacts:cowboy_hat` | `riding` | `CowboyHatItem` |
| 14 | `artifacts:universal_attractor` | `magnetism` | `UniversalAttractorItem` |
| 15 | `artifacts:crystal_heart` | `heart` | `CrystalHeartItem` |
| 16 | `artifacts:cross_necklace` | `protection` | `CrossNecklaceItem` |
| 17 | `artifacts:cloud_in_a_bottle` | `jump` | `CloudInBottleItem` |
| 18 | `artifacts:vampiric_glove` | `vampire` | `VampiricGloveItem` |
| 19 | `artifacts:golden_hook` | `hook` | `GoldenHookItem` |
| 20 | `artifacts:onion_ring` | `hunger_mining` | `OnionRingItem` |
| 21 | `artifacts:digging_claws` | `digging` | `DiggingClawsItem` |
| 22 | `artifacts:antidote_vessel` | `antidote` | `AntidoteVesselItem` |
| 23 | `artifacts:power_glove` | `power` | `PowerGloveItem` |
| 24 | `artifacts:withered_bracelet` | `withering` | `WitheredBraceletItem` |
| 25 | `artifacts:night_vision_goggles` | `vision` | `NightVisionGogglesItem` |
| 26 | `artifacts:snowshoes` | `snow` | `SnowshoesItem` |
| 27 | `artifacts:steadfast_spikes` | `resistance` | `SteadfastSpikesItem` |
| 28 | `artifacts:steadfast_spikes` | `wall_slide` | `SteadfastSpikesItem` |
| 29 | `artifacts:rooted_boots` | `devouring` | `RootedBootsItem` |
| 30 | `artifacts:warp_drive` | `warp` | `WarpDriveItem` |
| 31 | `artifacts:charm_of_shrinking` | `size` | `CharmOfShrinkingItem` |
| 32 | `artifacts:whoopee_cushion` | `push` | `WhoopeeCushionItem` |
| 33 | `artifacts:kitty_slippers` | `feline_aura` | `KittySlippersItem` |
| 34 | `artifacts:kitty_slippers` | `nine_lives` | `KittySlippersItem` |
| 35 | `artifacts:bunny_hoppers` | `jump` | `BunnyHoppersItem` |
| 36 | `artifacts:feral_claws` | `feral` | `FeralClawsItem` |
| 37 | `artifacts:charm_of_sinking` | `sinking` | `CharmOfSinkingItem` |
| 38 | `artifacts:panic_necklace` | `panic` | `PanicNecklaceItem` |
| 39 | `artifacts:helium_flamingo` | `flying` | `HeliumFlamingoItem` |
| 40 | `artifacts:pocket_piston` | `piston` | `PocketPistonItem` |
| 41 | `artifacts:obsidian_skull` | `lava` | `ObsidianSkullItem` |
| 42 | `artifacts:fire_gauntlet` | `flame` | `FireGauntletItem` |
| 43 | `artifacts:pickaxe_heater` | `heating` | `PickaxeHeaterItem` |
| 44 | `artifacts:chorus_totem` | `chorus` | `ChorusTotemItem` |
| 45 | `artifacts:running_shoes` | `runner` | `RunningShoesItem` |
| 46 | `artifacts:flippers` | `swim` | `FlippersItem` |
| 47 | `artifacts:strider_shoes` | `lava_stride` | `StriderShoesItem` |
| 48 | `artifacts:aqua_dashers` | `water_dash` | `AquaDashersItem` |
| 49 | `artifacts:umbrella` | `glider` | `UmbrellaItem` |
| 50 | `artifacts:umbrella` | `shield` | `UmbrellaItem` |
| 51 | `artifacts:everlasting_beef` | `meal` | `EverlastingBeefItem` |
| 52 | `artifacts:eternal_steak` | `meal` | `EternalSteakItem` |

## Cardinality checks

- Artifacts owners redirected by `ModItemsMixin`: **48**;
- Reliquified implementation classes for those owners: **47**;
- class-level `AbilityTemplate.builder(...)` roots: **51**;
- owner-scoped roots after expanding the two drinking-hat owners: **52**;
- English localization owner/ability roots: **52**;
- owners whose implementation class has a direct `LootTemplate`: **47**;
- owners without a direct class-local `LootTemplate`: **1** — `artifacts:eternal_steak`.

## Eternal Steak reachability

`artifacts:everlasting_beef` has a provider `LootTemplate` using the Relics village loot entry. Reliquified Artifacts then preserves provider state while converting Everlasting Beef into Eternal Steak through **both** furnace and campfire mixins: the input is recognized as `ModItems.EVERLASTING_BEEF`, and the output is transmuted to `ModItems.ETERNAL_STEAK`.

This closes a source-level acquisition route for the only owner without its own `LootTemplate`.

## Counting boundary

Rank modifiers, statistics, metrics, item containers, loot entries, spawned/projectile entities and downstream effects are not counted separately. The semantic objects here are the 52 owner-scoped Relics ability roots supplied by the Reliquified replacement classes.
