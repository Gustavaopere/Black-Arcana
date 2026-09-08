# Ars Elemental 0.7.10.1 — production glyph surface

Status: `39/39 PRODUCTION REGISTRATIONS + SOURCE DEFAULTS NORMALIZED / INSTALLED RUNTIME QA PENDING`

Source checkpoints:

- Ars Elemental: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`
- Ars Nouveau 5.13.1 API/base behavior: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

`ArsNouveauRegistry.registerGlyphs()` is the production registration authority. `MethodCarianPhalanx.INSTANCE` is registered only under `!isProduction()` and is excluded from the 39 production spell parts.

Ars `AbstractSpellPart` supplies Tier I when a glyph does not override `defaultTier()`. Ars `AbstractFilter` supplies default mana cost 0 and no compatible augments. General glyph config inherited from Ars defaults to enabled=true, starter=false, per-spell limit=Integer.MAX_VALUE, configured cost equal to the source default below and configured tier equal to the source default tier below.

## Effects — 23

| Glyph | Tier | Mana | Schools | Compatible augments | Provider-specific source defaults / limits |
|---|---:|---:|---|---|---|
| Watery Grave | II | 25 | Water | Extend Time, Duration Down, Amplify, Dampen, Randomize | damage 5; amplify 2; potion 30s; extend 8; Amplify limit 2 |
| Bubble Shield | II | 400 | Water | Extend Time, Duration Down, Amplify | potion 30s; extend 8; amplify 2; absorption_cost 350 |
| Conjure Terrain | I | 20 | Conjuration, Earth | AoE, Pierce, Amplify, Randomize | Amplify limit 2; Randomize limit 1 |
| Charm | II | 30 | provider registry plus Necromancy added in post-init | Extend Time, Duration Down, Amplify | potion 30s; extend 8; charm_hp_limit 150 |
| Phantom Grasp | II | 50 | Necromancy | Amplify, Dampen, Fortune, Randomize | base_heal 3; amplify 3; Amplify limit 3 |
| Life Link | III | 30 | provider registry plus Necromancy added in post-init | Extend Time, Duration Down, Sensitive | potion 30s; extend 8 |
| Poison Spores | II | 30 | Earth | Amplify, Dampen, Extend Time, Duration Down, AoE, Fortune, Randomize | damage 6; amplify 2.5; potion 10s; extend 3; Amplify limit 2 |
| Envenom | II | 20 | Earth | Extend Time, Duration Down, Amplify | potion 5s; extend 5; amplify 5 |
| Spike | II | 30 | Earth, Water | Amplify, Dampen, AoE, Pierce, Extend Time, Randomize, Fortune | damage 8; amplify 2.5; extend 10; maxFallDamage 40; Amplify limit 2 |
| Discharge | II | 40 | Air | Amplify, Dampen, Extend Time, Duration Down, AoE, Randomize, Fortune | damage 7; amplify 3; potion 15s; extend 5; Amplify limit 2 |
| Spark | I | 15 | Air | Extend Time, Duration Down, Amplify, Dampen, Randomize | damage 3; amplify 1.5; potion 15s; extend 5; Amplify limit 2 |
| Conflagrate | III | 80 | Fire | Amplify, Dampen, AoE, Fortune, Randomize | damage 9; amplify 5; Amplify limit 2 |
| Cauterize | III | 80 | Fire | none | damage 3 |
| Rage | III | 100 | Fire, Necromancy | Extend Time, Duration Down, Amplify | duration getter 60s; extend-time getter 120 |
| Water Jet | III | 80 | Water | Split, Randomize, Amplify | damage 4; amplify 1; Split cost override 40; target search radius 10 |
| Create Geyser | II | 40 | Water, Fire | Sensitive, AoE, Amplify, Dampen, Extend Time, Duration Down | potion/lifetime 5s; extend 1; base height 4 + 2× amplification |
| Mist Cloud | II | 40 | Water | AoE, Extend Time, Duration Down | hardcoded lifetime 100 + durationMultiplier×20 ticks; radius 3 + AoE multiplier |
| Sliding | II | 20 | Water, Abjuration | Extend Time, Duration Down | no potion config fields added by the class; duration getters return 10s / extend 10 |
| Cavitate | III | 80 | Water | AoE, Amplify, Extend Time, Duration Down, Randomize, Dampen | damage 8; amplify 3; `addDefaultPotionConfig` => potion 30s / extend 8; pre-config fallback getters are 15/5 |
| Oxidize | III | 80 | Water, Air | Amplify, Extend Time, Duration Down, Pierce, AoE | default potion config 30s / extend 8; executable block path reads Randomize count even though Randomize is not exposed as compatible at this pin |
| Summon Bee | II | 100 | Conjuration, Earth | Extend Time, Duration Down, Split | summons 3 + Split; lifetime 60 + 60×durationMultiplier seconds; Summoning Sickness 80% of summon lifetime when Summon Rework is inactive |
| Summon Slime | II | 100 | Conjuration, Water | Extend Time, Duration Down, Split | summons 3 + Split; lifetime 60 + 60×durationMultiplier seconds; slime size reads 2 + ampMultiplier although Amplify is not exposed as compatible; same 80% sickness rule when Summon Rework is inactive |
| Nullify Defense | III | 1000 | Necromancy | none | executable path sets target `invulnerableTime = 0`; learning recipe is separately config-gated and disabled by source default |

### Source-behavior notes

- Watery Grave drains air, can force downward movement with Extend Time, damages through drowning once air is depleted or for aquatic targets, and starts Zombie-to-Drowned conversion.
- Bubble Shield only applies to a target with an Ars mana capability; its defensive mana consumption remains Ars-owned.
- Conjure Terrain composes provider-side with Conjure Water, Crush and Smelt and uses provider block placement logic; this does not bypass Black Arcana `WorldEffectPolicy` for Black Arcana-owned effects.
- Charm is server/player-driven, blacklist-aware and source-default health-limited to targets below 150 max HP.
- Phantom Grasp heals inverted-heal targets and uses equivalent magic damage against living targets; successful player damage also adds food exhaustion.
- Life Link remains an Ars/provider life-link effect and is not a Black Arcana Vincular contract.
- Discharge only executes its damage chain when the main target has Shocked or Lightning Lure. Lightning Lure grants a 1.3 damage multiplier and is consumed. Each armor item exposing an energy capability is drained by 25% of stored energy and multiplies damage by 1.1.
- Spark deals +2 source damage against a wet target and uses Lightning Lure instead of Shocked when the provider Air-focus check passes.
- Conflagrate requires a burning main target; secondary targets receive 75% of the computed damage and have a 10% source chance to receive Ars Blast for 200 ticks.
- Cauterize damages first, then removes eligible effects according to harmful/milk-cure logic plus Ars dispel allow/deny tags.
- Nullify Defense does not remove armor, resistance or an immunity registry entry in this source path; it resets the vanilla LivingEntity post-hit invulnerability timer.

## Cast methods — 2

| Glyph | Tier | Mana | Compatible augments | Source defaults |
|---|---:|---:|---|---|
| Homing Projectile | III | 75 | Pierce, Split, Accelerate, Decelerate, Sensitive, Dampen | Pierce limit 1; Dampen limit 1; max_lifespan 30s; speed `max(0.2, 0.5 + acc/5)` |
| Arc Projectile | II | 10 | Pierce, Split, Accelerate, Decelerate, Sensitive | max_lifespan 60s; speed `max(0.2, 1.0 + acc/2)` |

These projectile entities and their downstream spell contexts remain children of one Ars causal cast. They do not create a second Black Arcana settlement.

## Propagators — 2

| Glyph | Tier | Mana | School | Compatible augments |
|---|---:|---:|---|---|
| Propagate Homing | III | 400 | Manipulation | Homing Projectile set + Extract |
| Propagate Arc | II | 150 | Manipulation | Arc Projectile set + Extract |

Both register themselves in Ars `EffectReset.RESET_LIMITS`, copy the provider resolver/context and re-emit the remaining provider spell through the corresponding projectile form. They are not independent root casts.

## Filters — 12

All twelve inherit Ars `AbstractFilter` defaults: Tier I, 0 mana, no compatible augments. `ElementalAbstractFilter` changes the type index to 15 and implements normal/inverted cancellation semantics.

| Normal / inverted pair | Predicate source |
|---|---|
| Aquatic / Not Aquatic | vanilla `EntityTypeTags.AQUATIC` |
| Fiery / Not Fiery | provider `FIERY` tag or `LivingEntity.fireImmune()` |
| Aerial / Not Aerial | provider `AERIAL` tag |
| Insect / Not Insect | vanilla `ARTHROPOD` tag or provider `INSECT` tag |
| Undead / Not Undead | vanilla `EntityTypeTags.UNDEAD` |
| Summon / Not Summon | entity implements Ars `ISummon` |

Registered ids are `glyph_aquatic_filter`, `glyph_not_aquatic_filter`, `glyph_fiery_filter`, `glyph_not_fiery_filter`, `glyph_aerial_filter`, `glyph_not_aerial_filter`, `glyph_insect_filter`, `glyph_not_insect_filter`, `glyph_undead_filter`, `glyph_not_undead_filter`, `glyph_summon_filter` and `glyph_not_summon_filter` under namespace `ars_elemental`.

These are provider targeting primitives. Their existence does not establish a Black Arcana Order/law contract.

## Acquisition and runtime boundary

All 39 production spell parts have source-pinned generated learning recipes in [ACQUISITION.md](ACQUISITION.md). Nullify Defense is registered in production but its normal generated learning recipe is gated by source config default `frame_skip_recipe=false`.

This table records source defaults, not the installed generated config. Installed config/datapack verification remains a separate runtime QA gate. Ars Nouveau/Ars Elemental remain authority for mana, glyph config, resolution, child contexts, damage and provider world effects.
