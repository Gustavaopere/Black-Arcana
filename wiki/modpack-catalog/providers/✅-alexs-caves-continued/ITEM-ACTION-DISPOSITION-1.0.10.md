# Alex's Caves Continued 1.0.10 — item action disposition

Status: `42/42 EXACT ITEM-ACTIVATION CLASSES DISPOSITIONED + 1 BLOCK-RITUAL ROOT ACCOUNTED SEPARATELY`

The exact hash-matched artifact exposes **42 top-level item classes** with at least one player-interaction signature. This table prevents the catalog from equating every `use(...)` or `hurtEnemy(...)` method with a spell.

| # | Exact class | Activation surface | State | Disposition |
|---:|---|---|---|---|
| 1 | `BiomeTreatItem` | `use, onUseTick, finishUsingItem` | `EXCLUDED_SETUP` | selects/prepares a cave-biome target and feeds Conversion Crucible; not an independent magic action |
| 2 | `CandyCaneHookItem` | `use` | `EXCLUDED` | mobility/hook utility |
| 3 | `CaveBoatItem` | `use` | `EXCLUDED` | vehicle placement/use |
| 4 | `CaveBookItem` | `use` | `EXCLUDED` | documentation/progression UI |
| 5 | `CaveInfoItem` | `use` | `EXCLUDED` | discovery/progression information item |
| 6 | `CaveMapItem` | `use` | `EXCLUDED` | map/progression utility |
| 7 | `DarkenedAppleItem` | `finishUsingItem` | `EXCLUDED` | food/consumable effect |
| 8 | `DarknessArmorItem` | `onKeyPacket` | `COUNTED_EXACT` | one Cloak of Darkness → Darkness Incarnate active root |
| 9 | `DesolateDaggerItem` | `hurtEnemy` | `EXCLUDED` | primary/on-hit weapon behavior |
| 10 | `DreadbowItem` | `use, releaseUsing, onUseTick` | `EXCLUDED` | primary projectile weapon firing modes |
| 11 | `DrinkableBottledItem` | `use, finishUsingItem` | `EXCLUDED` | drink/consumable behavior |
| 12 | `ExtinctionSpearItem` | `releaseUsing, onUseTick` | `EXCLUDED` | primary spear/throw weapon mode |
| 13 | `FertilizerItem` | `useOn` | `EXCLUDED` | growth/fertilizer utility |
| 14 | `FloaterItem` | `use` | `EXCLUDED` | vehicle/mobility utility |
| 15 | `FrostmintSpearItem` | `releaseUsing` | `EXCLUDED` | primary spear/throw weapon mode |
| 16 | `GalenaGauntletItem` | `use, releaseUsing, onUseTick` | `EXCLUDED` | magnetic/technological weapon-control system |
| 17 | `HotChocolateBottleItem` | `finishUsingItem` | `EXCLUDED` | food/drink consumable |
| 18 | `InkBombItem` | `use` | `EXCLUDED` | ordinary thrown consumable/projectile |
| 19 | `JellyBeanItem` | `onUseTick, finishUsingItem` | `EXCLUDED` | food/consumable behavior |
| 20 | `KeybindUsingArmor` | `onKeyPacket` | `EXCLUDED_TECHNICAL` | shared armor input contract; no standalone action identity |
| 21 | `LimestoneSpearItem` | `releaseUsing` | `EXCLUDED` | primary spear/throw weapon mode |
| 22 | `MagicConchItem` | `use, releaseUsing` | `COUNTED_EXACT` | one deliberate summon-Deep-Ones root |
| 23 | `MarineSnowItem` | `useOn` | `EXCLUDED` | environmental/use-on utility |
| 24 | `MothDustItem` | `use, releaseUsing` | `EXCLUDED` | single-use behavior-manipulation consumable |
| 25 | `OccultGemItem` | `use, useOn` | `COUNTED_EXACT` | one combined Occult Gem + Beholder remote-observation root; useOn binding is setup |
| 26 | `OrtholanceItem` | `use, releaseUsing, hurtEnemy` | `EXCLUDED` | primary weapon/charge-combat mode |
| 27 | `PrehistoricMixtureItem` | `finishUsingItem, interactLivingEntity` | `EXCLUDED` | feeding/food/effect interaction |
| 28 | `PrimitiveClubItem` | `hurtEnemy` | `EXCLUDED` | primary/on-hit weapon behavior |
| 29 | `QuarrySmasherItem` | `use` | `EXCLUDED` | mining/machine deployment utility |
| 30 | `RadiationRemovingFoodItem` | `use, finishUsingItem` | `EXCLUDED` | food/consumable effect |
| 31 | `RaygunItem` | `use, releaseUsing, onUseTick` | `EXCLUDED` | technological energy weapon |
| 32 | `RemoteDetonatorItem` | `use, useOn` | `EXCLUDED` | technological explosive-control utility |
| 33 | `ResistorShieldItem` | `use, releaseUsing, onUseTick` | `EXCLUDED` | defensive shield/equipment behavior |
| 34 | `SeaStaffItem` | `use` | `COUNTED_EXACT` | one Water Bolt cast root |
| 35 | `SharpenedCandyCaneItem` | `hurtEnemy` | `EXCLUDED` | primary/on-hit weapon behavior |
| 36 | `ShotGumItem` | `use` | `EXCLUDED` | ordinary projectile weapon/consumable |
| 37 | `SodaBottleRocketItem` | `use, useOn` | `EXCLUDED` | rocket/transport-projectile utility |
| 38 | `SpearItem` | `use, hurtEnemy` | `EXCLUDED` | generic spear weapon behavior |
| 39 | `SubmarineItem` | `use` | `EXCLUDED` | vehicle placement/use |
| 40 | `SugarStaffItem` | `use` | `COUNTED_EXACT ×2` | two deliberate roots: Peppermint Cast and Hex Cast |
| 41 | `ThrownProjectileItem` | `use` | `EXCLUDED` | generic thrown-projectile base behavior |
| 42 | `TotemOfPossessionItem` | `use, releaseUsing, onUseTick, hurtEnemy` | `COUNTED_EXACT` | one Possession/Remote-Control root; binding/management/downstream combat are not extra identities |

## Item-layer accounting

- exact activation classes: **42**;
- classes carrying counted item-owned roots: **6**;
- counted item-owned roots: **7** because Sugar Staff has two distinct selectable branches;
- excluded/setup/technical item classes: **36**;
- additional counted block-owned root: **1** Conversion Crucible Biome Conversion;
- provider strict total: **8**.

## Separate block pass

The item activation index cannot see block-owned ritual/process identities. Exact run #2 therefore disassembles Conversion Crucible, Beholder and Forsaken Idol surfaces separately.

- Conversion Crucible adds **1 `COUNTED_EXACT`** Biome Conversion root;
- Beholder observation is already counted with `OccultGemItem`, so it adds no second identity;
- Forsaken Idol exposes no player activation seam;
- mob-native Underzealot sacrifice/Forsaken transformation is outside the player-owned semantic metric.

See [`actions/SUPERNATURAL-ACTION-CARDS.md`](actions/SUPERNATURAL-ACTION-CARDS.md) for the eight final action cards.
