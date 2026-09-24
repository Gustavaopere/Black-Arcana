# Iron's Apothic 2.2.2 — exact source magic-surface inventory

Status: `EXACT SOURCE PIN / SUPPORT-AFFIX INVENTORY / ZERO PROVIDER-OWNED SPELL REGISTRATIONS`

## Source authority

Official source pin:

`muon-rw/Apotheosis-Irons-Spells@c5d501219cc9bbbfb8c69acc08bebac76983d1c1`

Tree:

`2c361b218ae9b1b2f9f25d2f99f4bf37a8daf3f5`

The exact pin declares `mod_version=2.2.2`.

## Custom affix codec registrations

`IronsApothic.commonSetup` registers exactly seven custom codecs into Apotheosis' `AffixRegistry`:

| Codec ID | Source type | Magic role |
|---|---|---|
| `attribute` | `SchoolAttributeAffix` | school-filtered attribute augmentation |
| `spell_effect` | `SpellEffectAffix` | spell heal/damage event → mob-effect response |
| `magic_telepathic` | `MagicTelepathicAffix` | magic-kill/drop routing |
| `spell_level` | `SpellLevelAffix` | school-filtered spell-level modifier |
| `spell_trigger` | `SpellTriggerAffix` | external Iron's spell cast on affix trigger |
| `imbued_spell_trigger` | `ImbuedSpellTriggerAffix` | cast the spell imbued in an eligible item on trigger |
| `mana_cost` | `ManaCostAffix` | school-filtered mana-cost modifier |

No codec is a spell registrar.

## Exact spell-oriented affix resources

There are **48** JSON definitions whose resource path is explicitly under a `spell` group or the `imbued` trigger group.

### Armor — 7

- `armor/spell/ball_lightning`
- `armor/spell/energy_burst`
- `armor/spell/evasive`
- `armor/spell/flamedash`
- `armor/spell/oakskinned`
- `armor/spell/shielding`
- `armor/spell/wither_skull`

### Imbued trigger definitions — 5

- `imbued/hurt`
- `imbued/melee_hit`
- `imbued/projectile_hit`
- `imbued/shield_block`
- `imbued/spell_damage`

### Magic weapons — 5

- `magic_weapons/spell/blessed`
- `magic_weapons/spell/echoing`
- `magic_weapons/spell/oakskinned`
- `magic_weapons/spell/rejuvenating`
- `magic_weapons/spell/thunderous`

### Melee — 15

- `melee/spell/abyssal_echo`
- `melee/spell/blood_slash`
- `melee/spell/divine_smite`
- `melee/spell/flaming_strike`
- `melee/spell/frostbite`
- `melee/spell/hallow_slash`
- `melee/spell/infection_slash`
- `melee/spell/infernal_strike`
- `melee/spell/nephrite_slash`
- `melee/spell/nights_edge_strike`
- `melee/spell/sanguinite_evisceration`
- `melee/spell/static_cleave`
- `melee/spell/stomp`
- `melee/spell/vein_ripper`
- `melee/spell/vile_slash`

### Ranged — 10

- `ranged/spell/clamor_note`
- `ranged/spell/fire_arrow`
- `ranged/spell/ice_arrow`
- `ranged/spell/magic_arrow`
- `ranged/spell/poison_arrow`
- `ranged/spell/splitting_shuriken`
- `ranged/spell/sunbeam`
- `ranged/spell/volley`
- `ranged/spell/water_trident`
- `ranged/spell/wind_blade`

### Shield — 6

- `shield/spell/airbending`
- `shield/spell/airblast`
- `shield/spell/drapes_of_reflection`
- `shield/spell/fortifying`
- `shield/spell/projecting`
- `shield/spell/tundra_terrain`

Total: **48**.

These are affix definitions. They do not become new semantic spell identities merely because their paths contain `spell`.

## Gem definitions — 24

Core:

- `bloody_pearl`
- `celsius_tear`
- `charged_lodestone`
- `dragonfire_spessartite`
- `effervescent_brimstone`
- `golems_onyx`
- `luminous_opal`
- `mossy_agate`
- `void_umbalite`
- `whispering_tentaculite`

External/provider-facing:

- `aeolian_celestite`
- `amethyst_lotus`
- `arcanists_edge`
- `deepsea_heartstone`
- `goetic_stibnite`
- `harmonic_geode`
- `lithographic_moissanite`
- `mycotoxin_crystal`
- `quaking_jasper`
- `resonant_quartz`
- `sepulchral_howlite`
- `sirens_aquamarine`
- `sky_meteoritill`
- `umbral_obsidian`

Total: **24**.

Gem presence is cataloged as bridge/support content and is not added to the strict spell numerator.

## School-family resources

The exact affix tree contains **25** `school_*` resource groups:

`abyssal, aero, aqua, blood, eldritch, ender, evocation, fire, geo, holy, hydro, ice, lightning, nature, necro, none, radiance, ritual, shadow, sound, spellblade, spirit, symmetry, technomancy, wind`.

These names reflect provider integration/taxonomy. They are not 25 new schools owned by Iron's Apothic.

## Spell ownership proof boundary

`SpellTriggerAffix` decodes a holder from:

`SpellRegistry.REGISTRY.holderByNameCodec()`

and then casts the referenced `AbstractSpell`.

`SpellCastUtil` uses Iron's `MagicData`, `AbstractSpell`, `CastSource.COMMAND` and Iron's casting packets/state.

The exact source therefore demonstrates a **consumer/trigger bridge** over external spell identities.

No provider-owned spell registry initializer or provider `AbstractSpell` registration collection is present in the exact 2.2.2 source tree.

## Semantic accounting

- support affix definitions: 140 total;
- spell/imbued spell affix subset: 48;
- gem definitions: 24;
- independent provider-owned spells: **0**;
- strict semantic spell delta: **+0**.

The affixes remain highly relevant to deduplication because they can produce casts, spell effects, mana-cost changes, spell-level changes and school attribute changes without owning the spell identity itself.
