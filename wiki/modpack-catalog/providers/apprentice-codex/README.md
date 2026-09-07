# Apprentice's Codex 0.9.7.1 — exact spell/content provider catalog

## Status

`EXACT INSTALLED ARTIFACT 0.9.7.1 / EXACT SOURCE VERSION PIN 305ea6a / MIT CODE + CC0 ORIGINAL ASSETS / IRON'S 3.16.3 BASELINE MATCHES PACK / 83/83 SPELL REGISTRY IDS FROZEN / 9 IRON'S SCHOOLS / PLAYER GUIDE TEXT SOURCE-PINNED / NUMERIC PER-SPELL AUDIT IN PROGRESS / ITEMS+BLOCKS+COMPAT+ACQUISITION INVENTORIES PENDING / RUNTIME QA PENDING`

## Installed identity

Current physical modlist authority:

- provider: **Apprentice's Codex**;
- installed JAR: `apprentice_codex-0.9.7.1+mc1.21.1.jar`;
- mod id: `apprenticecodex`;
- runtime version: `0.9.7.1`;
- mixin config: `mixins.apprenticecodex.json`;
- SHA-1: `b514315add32b93b0049c8673075627d7ef812e0`;
- package fingerprint: `702285225`;
- loader/game: NeoForge 1.21.1.

The physical modlist remains authoritative for the binary actually installed.

## Exact release/source checkpoint

Publisher repository: `hexqua/apprentice_codex`.

Exact version commit:

`305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

The commit's only codebase delta is the version change `0.9.7 -> 0.9.7.1` in `gradle.properties`, which makes it a strong source pin for the installed release line.

Exact checkpoint metadata includes:

- Minecraft `1.21.1`;
- NeoForge `21.1.228` build baseline;
- Java 21 project line;
- mod id `apprenticecodex`;
- mod version `0.9.7.1`;
- Iron's Spells 'n Spellbooks `1.21.1-3.16.3`;
- Curios `9.5.1+1.21.1`;
- GeckoLib `4.8.3`;
- Create `6.0.10` development/optional-compat baseline;
- Sable `2.0.3` development/optional-compat baseline.

The pack also uses Iron's `3.16.3`, so the core spell-provider baseline matches exactly. Optional provider versions must still be reconciled individually; for example, the pack's Sable is `2.0.5`, not source-dev `2.0.3`.

## Provenance

Exact source evidence is internally coherent:

- `LICENSE.txt`: MIT License, copyright 2026 Aquid;
- `gradle.properties`: `mod_license=MIT`;
- `ASSETS_LICENSE.md`: original project assets are CC0-1.0 unless otherwise noted;
- upstream `THIRD_PARTY_NOTICES.md`: third-party assets keep their own terms.

Black Arcana uses the source read-only for factual cataloging. No upstream code/assets are copied or adapted by this catalog.

## Critical registry correction — 83 spells, not approximately 60

The current public project description says the addon contains "around 60 spells". The exact 0.9.7.1 `SpellRegistry` registers **83** spells.

For the installed build, the exact source registry supersedes the approximate marketing count.

| Iron's school | Exact count |
|---|---:|
| Blood | 3 |
| Ender | 15 |
| Evocation | 17 |
| Fire | 5 |
| Holy | 11 |
| Ice | 3 |
| Lightning | 10 |
| Nature | 12 |
| Eldritch | 7 |
| **Total** | **83** |

Apprentice's Codex creates **no new spell school** in this registry. It registers into Iron's canonical school resources.

## Exact spell registry — 83/83

### Blood — 3

- `apprenticecodex:higanbana`
- `apprenticecodex:mist_form`
- `apprenticecodex:blood_brand`

### Ender — 15

- `apprenticecodex:arcane_blast`
- `apprenticecodex:arcane_beam`
- `apprenticecodex:personal_shelf`
- `apprenticecodex:assist_wings`
- `apprenticecodex:manifestation_grimoire`
- `apprenticecodex:mantis_leap`
- `apprenticecodex:auto_magnet`
- `apprenticecodex:remote_eye`
- `apprenticecodex:mana_slash`
- `apprenticecodex:long_stride`
- `apprenticecodex:rift_hole`
- `apprenticecodex:demicreator_wings`
- `apprenticecodex:mirage_avoidance`
- `apprenticecodex:anchor_blink`
- `apprenticecodex:servant_gaze`

### Evocation — 17

- `apprenticecodex:archer_multiple`
- `apprenticecodex:feather_rush`
- `apprenticecodex:slash_blade`
- `apprenticecodex:precision_jack`
- `apprenticecodex:auto_turret`
- `apprenticecodex:companion_trunk`
- `apprenticecodex:search_beacon`
- `apprenticecodex:tamers_pocket`
- `apprenticecodex:silent_assassin`
- `apprenticecodex:tiro_volley`
- `apprenticecodex:bound_sword`
- `apprenticecodex:bound_bow`
- `apprenticecodex:lethal_assault`
- `apprenticecodex:edge_dancer`
- `apprenticecodex:linear_build`
- `apprenticecodex:fujin`
- `apprenticecodex:call_broom`

### Fire — 5

- `apprenticecodex:thermal_process`
- `apprenticecodex:magic_spear`
- `apprenticecodex:artisan_smash`
- `apprenticecodex:combustion_jet`
- `apprenticecodex:catch_flame`

### Holy — 11

- `apprenticecodex:mage_light`
- `apprenticecodex:phalanx_charge`
- `apprenticecodex:mana_charge`
- `apprenticecodex:force_field`
- `apprenticecodex:sense_evil`
- `apprenticecodex:illuminate_stellar`
- `apprenticecodex:unite_luna`
- `apprenticecodex:mystic_shield`
- `apprenticecodex:divine_possession`
- `apprenticecodex:mana_mending`
- `apprenticecodex:wizardlamp`

### Ice — 3

- `apprenticecodex:frost_rune`
- `apprenticecodex:inscribe_ice`
- `apprenticecodex:totem_of_permafrost`

### Lightning — 10

- `apprenticecodex:sky_edge`
- `apprenticecodex:commence_fire`
- `apprenticecodex:quick_arms`
- `apprenticecodex:breaching_enemy`
- `apprenticecodex:bullet_stream`
- `apprenticecodex:fly_swatter`
- `apprenticecodex:shock`
- `apprenticecodex:dual_acrobat`
- `apprenticecodex:field_overseer`
- `apprenticecodex:shiden`

### Nature — 12

- `apprenticecodex:compound_phial`
- `apprenticecodex:tiny_lumberjack`
- `apprenticecodex:graced_rain`
- `apprenticecodex:world_flatter`
- `apprenticecodex:earth_forge`
- `apprenticecodex:grind_runner`
- `apprenticecodex:treasure_divination`
- `apprenticecodex:healing_bloom`
- `apprenticecodex:harvest_moon`
- `apprenticecodex:extract`
- `apprenticecodex:heavenly_fist`
- `apprenticecodex:terra_resonance`

### Eldritch — 7

- `apprenticecodex:palette_shift`
- `apprenticecodex:moon_light`
- `apprenticecodex:deep_sensor`
- `apprenticecodex:spectral_wing`
- `apprenticecodex:echo_cast`
- `apprenticecodex:otherworld_lens`
- `apprenticecodex:mana_transcription`

## Release 0.9.7.1 additions

The exact public 0.9.7.1 changelog explicitly calls out four new spells:

- Combustion Jet;
- Blood Brand;
- Shiden;
- Catch Flame.

All four are present in the exact 83-spell registry.

## Provider identity

Apprentice's Codex is an Iron's-native **spell/content/equipment/utility addon** rather than a second magic engine. Its spells consume/use Iron's spell-school and mana semantics unless a specific provider item deliberately modifies casting.

Public/source-visible capability families include:

- summoned magical firearms/blades/weapons;
- barriers, guard and evasion;
- remote vision and sensing;
- mobility/gliding/flight zones;
- companion constructs;
- private/pet storage;
- structure/treasure detection;
- healing/mana recovery;
- block placement/excavation/harvesting/processing;
- potion/flask interaction;
- enchantment transcription;
- spellcasting equipment and alternative cast triggers;
- a server-owned Spell Dispenser surface for supported spells.

## Authority consequence

Apprentice's Codex remains authority for its spell implementations, custom items/entities/blocks and optional compatibility behavior. Iron's remains authority for the core spell registry, schools, mana and standard spell lifecycle that the addon uses.

Black Arcana must not:

- duplicate these 83 capabilities simply under different names/VFX;
- create a second mana payment for their casts;
- re-settle their damage/healing/world effects;
- treat an Apprentice spell as a Black Arcana cast unless a real cross-provider contract says so;
- infer optional compat activation from source development dependencies alone.

## Canonical navigation

Per-school/per-spell files are being filled from the exact 0.9.7.1 source pin:

- [`blood/`](blood/README.md)
- `ender/`
- `evocation/`
- `fire/`
- `holy/`
- `ice/`
- `lightning/`
- `nature/`
- `eldritch/`

Additional provider-wide inventories for equipment, blocks, recipes/acquisition and optional compatibility remain part of this Phase 2L checkpoint.

## Validation state

`SOURCE REGISTRY EXACT / INSTALLED JAR IDENTITY EXACT / RUNTIME QA NOT YET COMPLETE`

The exact source pin supports factual source-derived cataloging. It does not by itself prove every optional mod bridge is active in the user's full 612-mod runtime.