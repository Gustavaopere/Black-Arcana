# Alex's Mobs Continued 2.1.13 — interaction disposition

Status: `37/37 EXACT-CURRENT INTERACTION CLASSES DISPOSITIONED`

The exact artifact audit found **26 item classes** and **11 block classes** with interaction signatures relevant to player-action triage. This table classifies every one against the semantic-magic rule.

## Item interaction classes

| # | Exact class | Surface | State | Disposition |
|---:|---|---|---|---|
| 1 | `AMBlockItem` | `use, useOn` | `EXCLUDED` | generic provider block-item placement/interaction plumbing |
| 2 | `ItemAnimalDictionary` | `use, interactLivingEntity` | `EXCLUDED` | documentation/bestiary UI |
| 3 | `ItemAnimalEgg` | `use` | `EXCLUDED` | ordinary creature egg/spawn lifecycle |
| 4 | `ItemBearDust` | `use` | `EXCLUDED` | feedback/cooldown utility with no supernatural settlement root |
| 5 | `ItemBloodSprayer` | `use, onUseTick` | `EXCLUDED` | primary ranged weapon mode |
| 6 | `ItemCosmicCodBucket` | `use` | `EXCLUDED` | bucket placement/release utility |
| 7 | `ItemDimensionalCarver` | `use, releaseUsing, onUseTick` | `CONDITIONAL` | one exact dimensional-portal action; owner acquisition depends on config-gated Void Worm reachability |
| 8 | `ItemEcholocator` | `use` | `EXCLUDED` | locator/sonar utility even though it spawns provider echo entities |
| 9 | `ItemEnderiophageRocket` | `use, useOn` | `EXCLUDED` | rocket/projectile utility rather than semantic magic |
| 10 | `ItemFishOil` | `use, finishUsingItem` | `EXCLUDED` | consumable/effect action |
| 11 | `ItemFlutterPot` | `useOn` | `EXCLUDED` | pet/container setup |
| 12 | `ItemGhostlyPickaxe` | `inventoryTick` | `EXCLUDED` | tool/passive inventory behavior |
| 13 | `ItemHemolymphBlaster` | `use, onUseTick` | `EXCLUDED` | primary ranged weapon mode |
| 14 | `ItemLeafcutterPupa` | `useOn` | `EXCLUDED` | colony/mob setup |
| 15 | `ItemMaraca` | `use` | `EXCLUDED` | sound/creature interaction utility |
| 16 | `ItemMysteriousWorm` | `onEntityItemUpdate` | `CONDITIONAL` | one exact Void Worm summon root gated by deployed summon boolean/dimension config |
| 17 | `ItemPocketSand` | `use` | `EXCLUDED` | ordinary projectile/weapon utility |
| 18 | `ItemRainbowJelly` | `finishUsingItem, interactLivingEntity` | `EXCLUDED` | consumable/cosmetic effect application |
| 19 | `ItemShieldOfTheDeep` | `use` | `EXCLUDED` | shield/guard behavior |
| 20 | `ItemSkelewagSword` | `use` | `EXCLUDED` | ordinary sword shield/block use |
| 21 | `ItemSquidGrapple` | `use, releaseUsing, onUseTick` | `EXCLUDED` | grappling/mobility utility |
| 22 | `ItemStinkRay` | `use, releaseUsing` | `EXCLUDED` | primary ranged weapon mode |
| 23 | `ItemStraddleboard` | `use` | `EXCLUDED` | vehicle placement/mobility |
| 24 | `ItemTarantulaHawkElytra` | `use` | `EXCLUDED` | equipment/glide utility |
| 25 | `ItemTendonWhip` | `hurtEnemy` | `EXCLUDED` | on-hit weapon behavior |
| 26 | `ItemVineLasso` | `use, releaseUsing, onUseTick, inventoryTick` | `EXCLUDED` | capture/restraint utility |

## Block interaction classes

| # | Exact class | Surface | State | Disposition |
|---:|---|---|---|---|
| 1 | `BlockBananaPeel` | `entityInside` | `EXCLUDED` | passive environmental trap |
| 2 | `BlockBananaSlugSlime` | `entityInside` | `EXCLUDED` | environmental material effect |
| 3 | `BlockCapsid` | `useItemOn` | `EXCLUDED` | four recipe-defined automatic processing transformations; not standalone casts |
| 4 | `BlockEndPirateAnchor` | `entityInside` | `EXCLUDED` | structure/environment interaction |
| 5 | `BlockEndPirateDoor` | `useItemOn` | `EXCLUDED` | structure door control |
| 6 | `BlockEndPirateShipWheel` | `useItemOn` | `EXCLUDED` | structure control/decor interaction |
| 7 | `BlockHummingbirdFeeder` | `useItemOn` | `EXCLUDED` | feeding/farming utility |
| 8 | `BlockLeafcutterAntChamber` | `useItemOn` | `EXCLUDED` | colony-management surface |
| 9 | `BlockLeafcutterAnthill` | `useItemOn` | `EXCLUDED` | colony-management surface |
| 10 | `BlockSkunkSpray` | `useItemOn` | `EXCLUDED` | environmental/cleaning interaction |
| 11 | `BlockTransmutationTable` | `useItemOn` | `COUNTED_EXACT` | one player-selected server-settled item-transmutation action |

## Accounting

- exact interaction classes dispositioned: **37/37**;
- semantic supernatural roots represented here: **3**;
- `COUNTED_EXACT`: **1**;
- `CONDITIONAL`: **2**;
- all remaining interaction classes: **EXCLUDED**.

Method presence is not counted mechanically. Projectiles, weapons, locators, consumables, pet/colony setup, vehicles, equipment, generic block control and automatic processing remain outside the semantic-magic numerator unless they establish a discrete supernatural player action.
