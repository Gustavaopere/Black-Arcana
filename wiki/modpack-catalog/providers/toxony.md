# Toxony

Status: `PHASE 2 — PROVIDER AUDIT IN PROGRESS`

## Runtime identity

- Provider: **Toxony**
- Installed JAR: `toxony-0.10.7.jar`
- Runtime version: `0.10.7`
- Loader/game: NeoForge 1.21.1
- Role: `TOXICITY / ALCHEMY / MUTAGEN / OIL PROVIDER`
- Current modlist is authoritative for installed version.

## Provenance / license

Public upstream repository: `MrFrostyDev/Toxony_Mod`.

GitHub repository metadata currently reports `GPL-3.0`. Phase 2 may use provider documentation and source-visible runtime facts for auditing. Any Phase 3 code reuse/derivation must still pass the Black Arcana provenance ledger and GPL compatibility/obligation review; this page is **not** authorization to copy code.

## Provider identity

Toxony is not an Iron's spell school. It is a player-state and preparation system built around:

- Toxicity / tolerance;
- ingredient affinities and knowledge;
- toxin effects;
- oils applicable to equipment/projectiles;
- mutagen transformations at toxicity thresholds;
- Mortar & Pestle / Crucible / Alembic / Alchemical Forge progression;
- monster-hunter gear and delivery systems.

For Black Arcana Witchcraft, Toxony should remain the authority for toxicology and mutagenesis.

## Harmful effect catalog

Current registry exposes five Toxony harmful effects:

| ID | Provider description / role | Dedup impact |
|---|---|---|
| `toxony:hunt` | increases damage taken from wolves and attackers carrying Beast Mutagen | do not create a separate witch 'marked prey' toxin with the same condition |
| `toxony:toxin` | causes large health loss over time and can kill rather than stopping at one heart | canonical lethal-toxin family |
| `toxony:acid` | health loss over time plus temporary armor effectiveness reduction | canonical acid/corrosion family |
| `toxony:flammable` | vulnerability to open flame; proximity can ignite target | canonical flammability primer |
| `toxony:cripple` | increased physical damage taken | canonical physical-vulnerability toxin family |

## Oil registry

Current provider registry exposes nine oils:

| Oil | Applied effects / semantic role |
|---|---|
| `toxony:poison_oil` | Poison |
| `toxony:toxin_oil` | Toxony Toxin |
| `toxony:fatigue_oil` | Slowness + Mining Fatigue + Weakness |
| `toxony:fire_resistance_oil` | Fire Resistance |
| `toxony:glowing_oil` | Glowing; applicability is restricted to weapon-enchantable items |
| `toxony:acid_oil` | Toxony Acid |
| `toxony:smoke_oil` | Slowness + Blindness + Weakness |
| `toxony:regeneration_oil` | Regeneration + Instant Health |
| `toxony:witchfire_oil` | Toxony Toxin + Flammable |

### Current delivery/capacity facts

The installed provider exposes oil pots, tox pots, bolts and wearable storage. Current item definitions show, among others:

- ordinary oil pots generally have 5 durability uses;
- Tox pots generally have 3 durability uses;
- Oil Pot Sash durability 16;
- Oil Pot Bandolier durability 40;
- Eternal Plague durability 64;
- Poison/Glowing/Fire Resistance/Fatigue oil pots use provider max-use metadata 150;
- Acid oil pot duration parameter 400;
- Toxin, Regeneration, Smoke, Acid and Witchfire tox pots use provider max-use metadata 100;
- dedicated bolts exist for Poison, Glowing, Witchfire, Toxin, Smoke and Regeneration.

These parameters are provider internals exposed in current public source and must not be converted into Black Arcana constants without Phase 3 provenance/API review. For deduplication, the important fact is that Toxony already owns both **weapon coating** and **projectile delivery** of these chemical effects.

## Toxicity consumables / blends

Current item definitions prove a tiered toxicity/tolerance economy. Representative current values:

| Item | Tox | Tolerance | Tier | Effect |
|---|---:|---:|---:|---|
| Poison Blend | 30 | 15 | 0 | Poison, 1000 ticks |
| Toxic Blend | 40 | 25 | 1 | Toxin, 1000 ticks |
| Pure Blend | 65 | 40 | 3 | Toxin, 1800 ticks |
| Toxin item | 50 | 10 | 1 | Toxin II, 600 ticks |

Plants/materials also carry toxicity and **affinities** (examples include Forest, Cold, Sun, Ocean, Decay, Wind, Heat and Soul). Those affinities feed mutagen selection.

## Mutagen system

Current registry exposes seven mutagen effects:

- `toxony:beast_mutagen`
- `toxony:spirit_mutagen`
- `toxony:aqua_mutagen`
- `toxony:hollow_mutagen`
- `toxony:necrotic_mutagen`
- `toxony:infernal_mutagen`
- `toxony:mob_mutagen`

When toxicity crosses a new threshold, the provider performs mutagen selection **server-side** from accumulated affinity weights, can award multiple mutagens when multiple thresholds are skipped, clears accumulated affinities after selection, applies the mutagen state, and synchronizes ToxData to the player. This is provider-owned transformation authority and should not be reproduced as a Black Arcana parallel mutation tracker.

### Beast Mutagen

- stage 0: hitting an entity grants a small burst of speed;
- stage 1: +15% damage; meat yields more hunger/saturation;
- stage 2: at night +30% movement speed and attacks apply Hunt.

Public source also contains explicit Iron's compatibility for Nature Spell Power in this mutagen family. Exact modifier values/hooks will be cataloged separately before any bridge design.

### Aqua Mutagen

- stage 0: bonus oxygen in water;
- stage 1: increased swim speed and normal mining speed underwater;
- stage 2: regeneration and 2× oxygen in water; attacks create heavy knockback; +30% damage taken from fire-based sources.

### Hollow Mutagen

- stage 0: faster soul-sand traversal and increased knockback resistance;
- stage 1: 15% damage reduction and slower hunger drain;
- stage 2: permanent night vision, wall climbing, high knockback resistance, Weakness under direct sunlight.

### Necrotic Mutagen

- stage 0: raw food/rotten flesh heals; Hunger immunity;
- stage 1: Poison/Wither immunity, retaliatory Poison, treated as undead;
- stage 2: attacks apply Wither; one fatal-damage recovery to half health with a **2-day lockout**; Weakness under direct sunlight.

### Infernal Mutagen

- stage 0: reduced damage while on fire;
- stage 1: attackers are ignited; crouch-right-click can convert furnace-charcoal-compatible items into charcoal;
- stage 2: Fire/Lava immunity; attacks ignite targets for 6 seconds; Weakness in water/rain.

### Spirit Mutagen

- stage 0: 50% less damage from spirit-family entities (provider description cites Phantoms/Vexes) and 50% less fall damage;
- stage 1: 20% chance to ignore physical damage and turn invisible; attacks may summon one Guided Spirit that damages/slows the target;
- stage 2: permanent Slow Falling; summons three Guided Spirits instead of one; +30% magic damage taken.

### Mob Mutagen

Provider localization currently exposes increased total health and increased speed. Granular tier/selection semantics remain to be traced.

## Explicit current integrations

Public provider documentation declares compatibility with:

- **Vampirism**: silver weapons gain value against vampires/werewolves;
- **Iron's Spells 'n Spellbooks**: certain mutagens grant School Spell Power;
- **Curios**: Toxicity Gauge can occupy a Charm slot.

These integrations are high-priority dedup/authority surfaces. Black Arcana should prefer them rather than recreate spell-power mutagen bonuses.

## Witchcraft consequences

Toxony materially occupies all of the following witchcraft niches:

- toxic ingredient knowledge;
- toxicity/tolerance meter;
- mutagen transformation;
- affinity-driven transformation selection;
- Poison/Toxin/Acid/Flammable/Cripple effects;
- weapon oils;
- throwable tox/oil delivery;
- toxin bolts;
- toxic plants and processing infrastructure.

Therefore future Black Arcana/Hexalia witchcraft may **use Toxony reagents, oils, toxicity state or mutagens as provider-backed ingredients/conditions**, but must not introduce:

- a second generic Toxicity bar;
- duplicate Poison/Toxin/Acid oils;
- duplicate generic mutagen tiers;
- a second affinity-selection system with the same purpose.

## Infernal consequences

`Infernal Mutagen` occupies **personal fire adaptation**, not the planned Nether-only `Infernal Lava` reservoir economy. The planned Infernal school can remain distinct if it is based on external Nether resource authority, binding/reservoir infrastructure and destructive spellcasting rather than duplicating the mutagen's fire immunity/ignition traits.

## Divine/Celestial consequences

Toxony has Sun/Moon ingredient affinities and mutagen weaknesses to sunlight. These are chemistry/affinity semantics, not Holy miracle authority. They still block trivial 'sun ingredient = Divine spell' duplication.

## Binding / Souls consequences

`Spirit Mutagen` already owns spirit-themed evasion and Guided Spirit summons. A future Binding/Soul system must use actual provider-owned soul/spirit resources or contracts and not recreate those combat effects as generic 'spirit bond' perks.

## Acquisition / progression

Toxony progression is tied to:

- Lost Journal / knowledge;
- ingredient discovery;
- ingredient affinities;
- toxicity and tolerance;
- threshold crossing;
- processing blocks (Mortar & Pestle, Redstone Mortar, Copper Crucible, Alembic, Alchemical Forge);
- prepared oils/toxins and delivery gear.

Mutagens are not ordinary potion effects that should be granted freely by Black Arcana. Their provider threshold and affinity progression is part of their identity.

## Open audit items

- enumerate all Affinities and exact mutagen mappings;
- catalog exact oil crafting/processing recipes and acquisition gates;
- catalog every Toxony–Iron's School Spell Power modifier and its values;
- catalog Vampirism silver compatibility quantitatively;
- record toxicity threshold formula/state limits from provider API/public behavior;
- determine clean public API/event surfaces available for Black Arcana integration;
- split oils/mutagens into individual capability pages for the final Wiki navigation.

## Phase 3 gate

Toxony integration is `BLOCKED FOR IMPLEMENTATION` until provider/API surface and semantic overlaps are fully reconciled.
