# Monsters & Spellbooks — complete source registration inventory

## Counting rule

This file inventories every spell object registered by the current public `ModSpellRegistry` at source head `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2`.

The physical pack uses `monstersspellbooks-0.0.16.3.jar`. The public source metadata still declares `0.0.14`, so the table deliberately records the **source constant + source class identity** and does not invent exact 0.0.16.3 registry paths or numerical internals.

The public source diff covering the 0.0.16.2/0.0.16.3 work interval does not modify `ModSpellRegistry`, while the exact 0.0.16.3 release notes contain balancing/visual/effect/jewelry fixes rather than spell additions/removals. This supports the 98-entry semantic inventory at the current evidence ceiling without promoting the source tree to an exact binary pin.

## Totals

| Source family | Count |
|---|---:|
| blood | 5 |
| ender | 12 |
| evocation | 3 |
| fire | 10 |
| holy | 4 |
| hydro | 8 |
| ice | 8 |
| lightning | 14 |
| nature | 7 |
| necro | 25 |
| technomancy | 2 |
| **Total** | **98** |

`aero` is absent from `ModSpellRegistry` even though a retained `aero` SchoolType exists in source; the exact 0.0.16.2 release describes Aero as soft-deleted.

## Complete inventory

| # | Source family | Source constant | Source class | Evidence |
|---:|---|---|---|---|
| 1 | `blood` | `ANTICOAGULATION` | `AnticoagulationSpell` | `registered in ModSpellRegistry` |
| 2 | `blood` | `BLOOD_PIERCE` | `BloodPierceSpell` | `registered in ModSpellRegistry` |
| 3 | `blood` | `BLOOD_THORN` | `BloodThornSpell` | `registered in ModSpellRegistry` |
| 4 | `blood` | `HYSTERIA` | `HysteriaSpell` | `registered in ModSpellRegistry` |
| 5 | `blood` | `SANGUINITE_EVISCERATION` | `SanguiniteEviscerationSpell` | `registered in ModSpellRegistry` |
| 6 | `ender` | `CORRUPTED_BEACON_RAY` | `CorruptedBeaconRaySpell` | `registered in ModSpellRegistry` |
| 7 | `ender` | `CRUSHING_PRESENCE` | `CrushingPresenceSpell` | `registered in ModSpellRegistry` |
| 8 | `ender` | `CRUSH` | `CrushSpell` | `registered in ModSpellRegistry` |
| 9 | `ender` | `DRAGON_CHARGE` | `DragonChargeSpell` | `registered in ModSpellRegistry` |
| 10 | `ender` | `ENDERSENT_SMASH` | `EndersentSmashSpell` | `registered in ModSpellRegistry` |
| 11 | `ender` | `ENDERSENT_FORM` | `EndersentFormSpell` | `registered in ModSpellRegistry` |
| 12 | `ender` | `FIRMAMENT_SPLITTER` | `FirmamentSplitterSpell` | `registered in ModSpellRegistry` |
| 13 | `ender` | `GRAVITY_WELL` | `GravityWellSpell` | `registered in ModSpellRegistry` |
| 14 | `ender` | `SPACE_BREAKER` | `SpaceBreakerSpell` | `registered in ModSpellRegistry` |
| 15 | `ender` | `SPACE_RUPTURE` | `SpaceRuptureSpell` | `registered in ModSpellRegistry` |
| 16 | `ender` | `UNSTABLE_TELEPORT` | `UnstableTeleportSpell` | `registered in ModSpellRegistry` |
| 17 | `ender` | `VOID_ARROWS` | `VoidArrowsSpell` | `registered in ModSpellRegistry` |
| 18 | `evocation` | `ENCHANTERS_BOOST` | `EnchantersBoostSpell` | `registered in ModSpellRegistry` |
| 19 | `evocation` | `ENCHANTERS_PROTECTION` | `EnchantersProtectionSpell` | `registered in ModSpellRegistry` |
| 20 | `evocation` | `SPELL_OF_UNDYING` | `SpellOfUndyingSpell` | `registered in ModSpellRegistry` |
| 21 | `fire` | `BRIMSTONE_BUZZSAW` | `BrimstoneBuzzsawSpell` | `registered in ModSpellRegistry` |
| 22 | `fire` | `BRIMSTONE_RAIN` | `BrimstoneRainSpell` | `registered in ModSpellRegistry` |
| 23 | `fire` | `BRIMSTONE_WRATH` | `BrimstoneWrathSpell` | `registered in ModSpellRegistry` |
| 24 | `fire` | `CAUTERIZING_TOUCH` | `CauterizingTouchSpell` | `registered in ModSpellRegistry` |
| 25 | `fire` | `FRENZIED_BURST` | `FrenziedBurstSpell` | `registered in ModSpellRegistry` |
| 26 | `fire` | `FRENZIED_STORM` | `FrenziedStormSpell` | `registered in ModSpellRegistry` |
| 27 | `fire` | `FRENZY_SURGE` | `FrenzySurgeSpell` | `registered in ModSpellRegistry` |
| 28 | `fire` | `NAPALM_ORB` | `NapalmOrbSpell` | `registered in ModSpellRegistry` |
| 29 | `fire` | `OVERHEAT` | `OverheatSpell` | `registered in ModSpellRegistry` |
| 30 | `fire` | `WRATH` | `WrathSpell` | `registered in ModSpellRegistry` |
| 31 | `holy` | `DIVINE_INTERVENTION` | `DivineInterventionSpell` | `registered in ModSpellRegistry` |
| 32 | `holy` | `HALLOW_SLASH` | `HallowSlashSpell` | `registered in ModSpellRegistry` |
| 33 | `holy` | `PALADIN_THROW` | `PaladinThrowSpell` | `registered in ModSpellRegistry` |
| 34 | `holy` | `SUMMON_AEGIS_PATROL` | `SummonAegisPatrolSpell` | `registered in ModSpellRegistry` |
| 35 | `hydro` | `BUBBLE_SPRAY` | `BubbleSpraySpell` | `registered in ModSpellRegistry` |
| 36 | `hydro` | `EFFERVESCENCE_BUBBLE` | `EffervescenceBubbleSpell` | `registered in ModSpellRegistry` |
| 37 | `hydro` | `GLOW_INK_RELEASE` | `GlowInkReleaseSpell` | `registered in ModSpellRegistry` |
| 38 | `hydro` | `INK_BOMB` | `InkBombSpell` | `registered in ModSpellRegistry` |
| 39 | `hydro` | `RAZORBLADE_TYPHOON` | `RazorbladeTyphoonSpell` | `registered in ModSpellRegistry` |
| 40 | `hydro` | `RIPTIDE_DASH` | `RiptideDashSpell` | `registered in ModSpellRegistry` |
| 41 | `hydro` | `SUMMON_PRISMARINE_SQUAD` | `SummonPrismarineSquadSpell` | `registered in ModSpellRegistry` |
| 42 | `hydro` | `WATER_TRIDENT` | `WaterTridentSpell` | `registered in ModSpellRegistry` |
| 43 | `ice` | `BLIZZARD_ASPECT` | `BlizzardAspectSpell` | `registered in ModSpellRegistry` |
| 44 | `ice` | `FROST_BREATH` | `FrostBreathSpell` | `registered in ModSpellRegistry` |
| 45 | `ice` | `FROST_COATING` | `FrostCoatingSpell` | `registered in ModSpellRegistry` |
| 46 | `ice` | `FROSTED_SNOWBOLT` | `FrostedSnowboltSpell` | `registered in ModSpellRegistry` |
| 47 | `ice` | `ICE_ARSENAL` | `IceArsenalSpell` | `registered in ModSpellRegistry` |
| 48 | `ice` | `ORBITAL_SNOWBALL` | `OrbitalSnowballSpell` | `registered in ModSpellRegistry` |
| 49 | `ice` | `SUMMON_ICE_HYDRA` | `SummonIceHydraSpell` | `registered in ModSpellRegistry` |
| 50 | `ice` | `TUNDRA_TERRAIN` | `TundraTerrainSpell` | `registered in ModSpellRegistry` |
| 51 | `lightning` | `PRIMORDIAL_FLASH` | `PrimordialFlashSpell` | `registered in ModSpellRegistry` |
| 52 | `lightning` | `DISCHARGE` | `DischargeSpell` | `registered in ModSpellRegistry` |
| 53 | `lightning` | `RAIJIN_JUDGEMENT` | `RaijinJudgementSpell` | `registered in ModSpellRegistry` |
| 54 | `lightning` | `REDSTONE_BOLT` | `RedstoneBoltSpell` | `registered in ModSpellRegistry` |
| 55 | `lightning` | `REDSTONE_MINES` | `RedstoneMinesSpell` | `registered in ModSpellRegistry` |
| 56 | `lightning` | `GUARDIANS_NEUTRALIZER` | `GuardiansNeutralizerSpell` | `registered in ModSpellRegistry` |
| 57 | `lightning` | `REDSTONE_CHAIN` | `RedstoneChainSpell` | `registered in ModSpellRegistry` |
| 58 | `lightning` | `REDSTONE_LASERS` | `RedstoneLasersSpell` | `registered in ModSpellRegistry` |
| 59 | `lightning` | `RAIGO` | `RaigoSpell` | `registered in ModSpellRegistry` |
| 60 | `lightning` | `STATIC_CLEAVE` | `StaticCleaveSpell` | `registered in ModSpellRegistry` |
| 61 | `lightning` | `THUNDER_STEP` | `ThunderStepSpell` | `registered in ModSpellRegistry` |
| 62 | `lightning` | `THUNDERSTORM_WAVE` | `ThunderstormWaveSpell` | `registered in ModSpellRegistry` |
| 63 | `lightning` | `VOLTAIC_MULTISHOT` | `VoltaicMultishotSpell` | `registered in ModSpellRegistry` |
| 64 | `lightning` | `ZAP` | `ZapSpell` | `registered in ModSpellRegistry` |
| 65 | `nature` | `BLAST_FUNGUS` | `BlastFungusSpell` | `registered in ModSpellRegistry` |
| 66 | `nature` | `INFECTION_SLASH` | `InfectionSlashSpell` | `registered in ModSpellRegistry` |
| 67 | `nature` | `LEAF_CRYSTAL` | `LifeCrystalSpell` | `registered in ModSpellRegistry` |
| 68 | `nature` | `POISON_QUILL` | `PoisonQuillSpell` | `registered in ModSpellRegistry` |
| 69 | `nature` | `SPIDER_FANGS` | `SpiderFangsSpell` | `registered in ModSpellRegistry` |
| 70 | `nature` | `SUMMON_POISON_VINE` | `SummonPoisonVinesSpell` | `registered in ModSpellRegistry` |
| 71 | `nature` | `VITAL_BLAST` | `VitalBlastSpell` | `registered in ModSpellRegistry` |
| 72 | `necro` | `REAPER_ASPECT` | `ReaperAspectSpell` | `registered in ModSpellRegistry` |
| 73 | `necro` | `BANSHEE_SCREAM` | `BansheeScreamSpell` | `registered in ModSpellRegistry` |
| 74 | `necro` | `BONE_DAGGER` | `BoneDaggerSpell` | `registered in ModSpellRegistry` |
| 75 | `necro` | `SUMMON_DEATH_KNIGHT` | `SummonDeathKnightSpell` | `registered in ModSpellRegistry` |
| 76 | `necro` | `FALL_CURSE` | `FallCurseSpell` | `registered in ModSpellRegistry` |
| 77 | `necro` | `GRAVEYARD_FISSURE` | `GraveyardFissureSpell` | `registered in ModSpellRegistry` |
| 78 | `necro` | `LICHDOM` | `LichdomSpell` | `registered in ModSpellRegistry` |
| 79 | `necro` | `LIFE_DRAIN` | `LifeDrainSpell` | `registered in ModSpellRegistry` |
| 80 | `necro` | `PUTRESCENCE_MASS` | `PutrescenceMassSpell` | `registered in ModSpellRegistry` |
| 81 | `necro` | `RANCORCALL` | `RancorCallSpell` | `registered in ModSpellRegistry` |
| 82 | `necro` | `SOUL_CASTING_FIELD` | `SoulCastingFieldSpell` | `registered in ModSpellRegistry` |
| 83 | `necro` | `SOUL_CHAIN` | `SoulChainSpell` | `registered in ModSpellRegistry` |
| 84 | `necro` | `SOUL_FIREBOLT` | `SoulFireBoltSpell` | `registered in ModSpellRegistry` |
| 85 | `necro` | `SOUL_FIRE_TELEPORT` | `SoulFireTeleportSpell` | `registered in ModSpellRegistry` |
| 86 | `necro` | `SOUL_FORM` | `SoulFormSpell` | `registered in ModSpellRegistry` |
| 87 | `necro` | `SOUL_SCORCH` | `SoulScorchSpell` | `registered in ModSpellRegistry` |
| 88 | `necro` | `SPECTRAL_BLAST` | `SpectralBlastSpell` | `registered in ModSpellRegistry` |
| 89 | `necro` | `SPIRIT_STRIKE` | `SpiritStrikeSpell` | `registered in ModSpellRegistry` |
| 90 | `necro` | `STRAY_GRASP` | `StrayGraspSpell` | `registered in ModSpellRegistry` |
| 91 | `necro` | `SUMMON_SOUL_WIZARD` | `SummonSoulWizardSpell` | `registered in ModSpellRegistry` |
| 92 | `necro` | `TORMENT_ARROW` | `TormentArrowSpell` | `registered in ModSpellRegistry` |
| 93 | `necro` | `VILE_SLASH` | `VileSlashSpell` | `registered in ModSpellRegistry` |
| 94 | `necro` | `SUMMON_WITHER_ARMY` | `SummonWitherArmy` | `registered in ModSpellRegistry` |
| 95 | `necro` | `WITHER_BOMB` | `WitherBombSpell` | `registered in ModSpellRegistry` |
| 96 | `necro` | `WITHER_NOVA` | `WitherNovaSpell` | `registered in ModSpellRegistry` |
| 97 | `technomancy` | `SPINBLADE` | `SpinbladeSpell` | `registered in ModSpellRegistry` |
| 98 | `technomancy` | `SUMMON_DWARVEN_DRONES` | `SummonDwarvenDronesSpell` | `registered in ModSpellRegistry` |

## Identity caveat

The constants and Java classes above are exact for the inspected public source head. `registerSpell` registers `spell.getSpellName()`, so a Java constant is not automatically proof of the exact registry path used by the installed 0.0.16.3 binary. Registry paths, translations, tiers, base mana, cooldowns, cast types, per-level scaling and config values remain `NÃO VERIFICADO` unless separately proven by exact-version evidence.

This prevents a source-organizational label from being promoted into a fabricated runtime contract.
