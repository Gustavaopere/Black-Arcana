# Spell inventory — current public source baseline

Status: `98 SOURCE-BASELINE REGISTRATIONS / EXACT INSTALLED 0.0.16.3 PARITY UNVERIFIED`

The official public source head `1ab9b72af2ea44c3c8b816e665d06531ea44ddc2` registers 98 `AbstractSpell` objects in `ModSpellRegistry`. The registry uses each spell object's own `getSpellName()` as the registration path, so the Java field names below are **source handles/classification labels**, not inferred exact resource IDs for the installed JAR.

| Family | Count | Source-baseline handles |
|---|---:|---|
| Blood | 5 | `ANTICOAGULATION`, `BLOOD_PIERCE`, `BLOOD_THORN`, `HYSTERIA`, `SANGUINITE_EVISCERATION` |
| Ender | 12 | `CORRUPTED_BEACON_RAY`, `CRUSHING_PRESENCE`, `CRUSH`, `DRAGON_CHARGE`, `ENDERSENT_SMASH`, `ENDERSENT_FORM`, `FIRMAMENT_SPLITTER`, `GRAVITY_WELL`, `SPACE_BREAKER`, `SPACE_RUPTURE`, `UNSTABLE_TELEPORT`, `VOID_ARROWS` |
| Evocation | 3 | `ENCHANTERS_BOOST`, `ENCHANTERS_PROTECTION`, `SPELL_OF_UNDYING` |
| Fire | 10 | `BRIMSTONE_BUZZSAW`, `BRIMSTONE_RAIN`, `BRIMSTONE_WRATH`, `CAUTERIZING_TOUCH`, `FRENZIED_BURST`, `FRENZIED_STORM`, `FRENZY_SURGE`, `NAPALM_ORB`, `OVERHEAT`, `WRATH` |
| Holy | 4 | `DIVINE_INTERVENTION`, `HALLOW_SLASH`, `PALADIN_THROW`, `SUMMON_AEGIS_PATROL` |
| Hydro | 8 | `BUBBLE_SPRAY`, `EFFERVESCENCE_BUBBLE`, `GLOW_INK_RELEASE`, `INK_BOMB`, `RAZORBLADE_TYPHOON`, `RIPTIDE_DASH`, `SUMMON_PRISMARINE_SQUAD`, `WATER_TRIDENT` |
| Ice | 8 | `BLIZZARD_ASPECT`, `FROST_BREATH`, `FROST_COATING`, `FROSTED_SNOWBOLT`, `ICE_ARSENAL`, `ORBITAL_SNOWBALL`, `SUMMON_ICE_HYDRA`, `TUNDRA_TERRAIN` |
| Lightning | 14 | `PRIMORDIAL_FLASH`, `DISCHARGE`, `RAIJIN_JUDGEMENT`, `REDSTONE_BOLT`, `REDSTONE_MINES`, `GUARDIANS_NEUTRALIZER`, `REDSTONE_CHAIN`, `REDSTONE_LASERS`, `RAIGO`, `STATIC_CLEAVE`, `THUNDER_STEP`, `THUNDERSTORM_WAVE`, `VOLTAIC_MULTISHOT`, `ZAP` |
| Nature | 7 | `BLAST_FUNGUS`, `INFECTION_SLASH`, `LEAF_CRYSTAL` (implemented by source class `LifeCrystalSpell`), `POISON_QUILL`, `SPIDER_FANGS`, `SUMMON_POISON_VINE`, `VITAL_BLAST` |
| Necro | 25 | `REAPER_ASPECT`, `BANSHEE_SCREAM`, `BONE_DAGGER`, `SUMMON_DEATH_KNIGHT`, `FALL_CURSE`, `GRAVEYARD_FISSURE`, `LICHDOM`, `LIFE_DRAIN`, `PUTRESCENCE_MASS`, `RANCORCALL`, `SOUL_CASTING_FIELD`, `SOUL_CHAIN`, `SOUL_FIREBOLT`, `SOUL_FIRE_TELEPORT`, `SOUL_FORM`, `SOUL_SCORCH`, `SPECTRAL_BLAST`, `SPIRIT_STRIKE`, `STRAY_GRASP`, `SUMMON_SOUL_WIZARD`, `TORMENT_ARROW`, `VILE_SLASH`, `SUMMON_WITHER_ARMY`, `WITHER_BOMB`, `WITHER_NOVA` |
| Technomancy | 2 | `SPINBLADE`, `SUMMON_DWARVEN_DRONES` |
| **Total** | **98** | source baseline only |

## Important exclusions

- The source tree contains Aero-related classes/imports, but `ModSpellRegistry` at this pin registers **no Aero spell objects**.
- The provider's source school registry still registers an Aero school. The exact 0.0.16.3 changelog simultaneously says some remaining Aero content was removed. This disagreement is not resolved by guessing.
- Publisher text says `90+ spells`; this is compatible with a 98-source-registration baseline but does not cryptographically or semantically prove that the installed 0.0.16.3 registry is exactly 98.

## Deduplication use

These names are overlap candidates only. Examples such as `LICHDOM`, `SOUL_*`, `GRAVITY_WELL`, `SPACE_*`, summons, resurrection-like protection and elemental attacks must be compared by actual semantics before any Black Arcana gap decision. Naming similarity alone cannot create a bridge or authorize a clone.