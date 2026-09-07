# Vampiric Ageing 1.21-1.4.21 — progression and Age Methods

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## Shared Age Rank model

`AgeingManager` stores `ageRank` and `rankProgress`. Ranks range from **0 through 5**. `increaseRankPoints(amount)` only operates while `canAge()` is true. When progress reaches the active method's threshold for the current rank:

1. `ageRank += 1`;
2. `rankProgress = 0` — overflow is not carried to the next rank;
3. provider rank-up audiovisual feedback fires;
4. attachment sync occurs.

A player can age only while alive, with a valid Age Type, below rank 5, at/above the Age Type's faction-level gate and passing that Age Type's `canAge(...)` gate.

Defaults for Vampire, Hunter and Werewolf begin the mechanic at faction level **14** and require Lord level **0**. All are configurable.

## Registered Age Types

| Type ID | Provider | Installed state |
|---|---|---|
| `VAMPIRE` | Vampirism | present |
| `HUNTER` | Vampirism | present |
| `WEREWOLF` | Werewolves | present because Werewolves is installed |

## Registered Age Methods — 8

### Vampire

#### `DRAINING` — default

- valid type: `VAMPIRE`;
- provider default selected by `CommonConfig.ageingMethod="DRAINING"`;
- thresholds: **150 / 300 / 600 / 900 / 1250** units of blood drained;
- progression is awarded from `BloodDrinkEvent.PlayerDrinkBloodEvent` when the blood source is an entity and the active method is `DrinkBloodMethod`.

The provider event amount is the progression input. Do not infer progress from attacks, blood-bar deltas or items when the provider event did not settle a qualifying drink.

#### `BITING`

Despite the Java class name, the progression requirement is **entities infected**.

- thresholds: **30 / 45 / 70 / 100 / 200**;
- valid type: `VAMPIRE`;
- enabled only when config method string is `BITING`.

#### `TIME`

- thresholds in ticks: **72,000 / 144,000 / 288,000 / 576,000 / 1,152,000**;
- valid type: `VAMPIRE`.

These correspond to 3,600 / 7,200 / 14,400 / 28,800 / 57,600 seconds of provider-counted progress if awarded one point per eligible tick by the handler path.

#### `V_HUNTING`

- thresholds: **20 / 40 / 80 / 160 / 250** hunt points;
- target worth defaults: petty **1**, common **3**, greater **5**;
- only target entity types in Vampiric Ageing's corresponding Vampire-hunt tags award those values.

### Hunter

#### `HUNTING` — default

- valid type: `HUNTER`;
- thresholds: **20 / 40 / 80 / 160 / 250**;
- target worth defaults: petty **1**, common **3**, greater **5**;
- only provider-tagged hunt targets award points.

### Werewolf

Werewolf Age Types/Methods are registered only if `werewolves` is loaded. Black Arcana has it installed.

#### `DEVOUR` — default

- valid type: `WEREWOLF`;
- thresholds: **30 / 60 / 100 / 250 / 500**;
- kill must use Werewolves `ModDamageTypes.BITE`;
- target worth defaults: petty **1**, common **2**, greater **5**, exquisite **10**;
- only provider-tagged devour targets award points.

A normal kill is not equivalent to a Devour progression kill.

#### `W_HUNTING`

- thresholds: **20 / 40 / 80 / 160 / 250**;
- any qualifying kill may award provider hunt points according to Werewolf-specific petty/common/greater tags;
- worth defaults **1 / 3 / 5**.

#### `W_MIXED`

- thresholds: **20 / 40 / 80 / 160 / 250**;
- BITE kills use the Devour tag/value path **1 / 2 / 5 / 10**;
- non-BITE kills use Werewolf hunt tags/value path **1 / 3 / 5**.

This causal split is provider-owned. A Black Arcana progression bridge must use the actual provider method and DamageSource/target classification rather than an approximate kill counter.

## Vampire Age defaults by rank

Rank-indexed configuration has six entries: index 0 = unaged, indices 1–5 = Age 1–5.

| Surface | Age 0 | Age 1 | Age 2 | Age 3 | Age 4 | Age 5 |
|---|---:|---:|---:|---:|---:|---:|
| Max Health additive | 0 | 2 | 2 | 3 | 4 | 5 |
| Attack Damage additive | 0 | 1 | 1.5 | 2 | 3 | 4 |
| Blood Exhaustion modifier | 0 | -0.1 | -0.2 | -0.3 | -0.4 | -0.5 |
| Sun damage divisor | 1 | 1.25 | 1.5 | 1.75 | 2 | 2.5 |
| DBNO duration modifier input | 1 | 1 | 1 | 0.8 | 0.5 | 0.25 |
| Neonatal duration modifier input | 1 | 1 | 1 | 1 | 0.75 | 0.5 |

Additional defaults include Celerity Age 1, Step Assist Age 2, Blood Tap Age 3 and Water Walking Age 4.

Optional Vampire mechanics such as age-based generic healing and "only deadly sources can kill" are **disabled by default**. The latter defaults to an Age 4 gate if enabled.

## Hunter base Age defaults

| Surface | Age 0 | Age 1 | Age 2 | Age 3 | Age 4 | Age 5 |
|---|---:|---:|---:|---:|---:|---:|
| Max Health additive | 0 | 1 | 1 | 2 | 2 | 4 |
| Movement Speed additive | 0 | 0.0125 | 0.015 | 0.02 | 0.025 | 0.035 |
| Attack Damage additive | 0 | 0 | 1 | 1 | 1.5 | 2 |
| XP gain divisor | 1 | 1 | 1.25 | 1.5 | 1.75 | 2 |
| Food exhaustion multiplier | 1 | 1 | 1.25 | 1.5 | 2 | 2.5 |
| Seniority Oil damage bonus | 0 | 0 | 0.1 | 0.2 | 0.4 | 0.6 |

Default unlocks: Tainted Blood Age 2, Faster Regeneration Age 3, Step Assist Age 4, Wise Eye Age 5.

## Hunter Tainted cumulative Age

`CapabilityHelper.getCumulativeTaintedAge(...)` is the canonical calculator.

- if player is not Hunter or Tainted Blood is disabled: **0**;
- if no temporary tainted bonus and not transformed: **0**, not base age;
- otherwise: `base Age + temporary bonus`;
- permanently transformed Hunter: provider substitutes a fixed **+6** bonus.

Selected defaults:

- Tainted Blood access: base Age **2**;
- human-heart bad-food penalties disappear: cumulative **6**;
- worse villager trades: cumulative **7**;
- Teleport: cumulative **8**;
- coffin use: cumulative **8**;
- sun susceptibility: cumulative **9**;
- Limited Bat Mode: cumulative **10**;
- infinite underwater breathing: cumulative **11**;
- permanent transformation available: **true**;
- permanent transformation reset on death: **false**.

Tainted cumulative tables extend through index **11**. Examples:

- attack bonus: `[0,0,0,1,1.2,1.4,1.6,1.8,2,2.25,2.5,3]`;
- Max Health: `[0,0,1,1,2,2,3,3,4,4,5,5]`;
- Movement Speed: `[0,0,0,0,0,0,0,0,0.02,0.03,0.04,0.06]`;
- mining multiplier: `[1,1,1,1.05,1.1,1.15,1.2,1.25,1.3,1.325,1.35,1.5]`.

## Werewolf defaults by rank

| Surface | Age 0 | Age 1 | Age 2 | Age 3 | Age 4 | Age 5 |
|---|---:|---:|---:|---:|---:|---:|
| Max Health additive | 0 | 2 | 2 | 4 | 4 | 6 |
| Attack Damage additive | 0 | 0 | 1 | 2 | 3 | 4 |
| Bite `ADD_MULTIPLIED_TOTAL` amount | 0 | 0 | 0 | 0.125 | 0.25 | 0.5 |
| Leap strength multiplier | 1 | 1 | 1.25 | 1.5 | 1.75 | 2 |
| Werewolf-form duration multiplier | 1 | 1.5 | 2 | 3 | 4 | 5 |
| Heal on bite | 0 | 0 | 0 | 1 | 2 | 2 |
| Raw meat nutrition multiplier | 1 | 1 | 2 | 2 | 3 | 3 |
| Raw meat saturation multiplier | 1 | 1 | 1.5 | 1.5 | 2 | 2 |
| Silver damage multiplier | 1 | 1 | 1.1 | 1.15 | 1.2 | 1.25 |

Biting begins to provide food at default Age **2**. Improved Senses unlocks at default Age **5** subject to the Werewolves `SENSE` gate.

## Progression integration rules

- Read `AgeingManager` and current `IAgeMethod`; do not mirror progress.
- Attribute progress to the same provider-native event/damage/target classification that the selected method uses.
- Never award overflow into the next rank unless upstream behavior changes: current source resets progress to 0 on rank-up.
- Configured thresholds are mutable server settings, not immutable protocol constants.
- A perk requiring an exact Age Method must fail closed when the provider method cannot be resolved.
