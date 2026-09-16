# Vampiric Ageing 1.4.21 — progression catalog

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## Canonical state

`AgeingManager` is the provider-owned state machine. For players it persists:

- Age Type id;
- Age Rank;
- current rank progress;
- optional TypeState data.

The attachment is serialized, synchronized and `copyOnDeath()`. Death-reset behavior is therefore an explicit provider event policy layered over persistent state, not an artifact of the attachment disappearing.

## Rank contract

Normal Age Rank range: **0–5**.

`canAge()` requires:

1. a non-null enabled Age Type;
2. a living `ServerPlayer`;
3. current faction level >= the Age Type minimum;
4. Age Rank < 5;
5. the Age Type-specific `canAge()` gate, currently the configured Lord-level requirement.

On `increaseRankPoints(amount)`:

- the amount is added only if `canAge()` is true;
- when progress reaches or exceeds `method.getRankProgressions()[currentAge]`, Age Rank increases by exactly one;
- rank progress is reset to 0;
- excess/overflow progress is not carried into the next rank;
- sound/particles are emitted;
- the manager syncs.

## Age Types

### Vampire — `VAMPIRE`

Faction: Vampirism Vampire.

Defaults:

- ageing enabled: true;
- faction level to begin: 14;
- Lord level requirement: 0;
- max rank: 5.

Default attribute amounts by Age 0..5:

| Attribute | Operation | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---:|---:|---:|---:|---:|---:|
| Attack Damage | `ADD_VALUE` | 0 | 1 | 1.5 | 2 | 3 | 4 |
| Max Health | `ADD_VALUE` | 0 | 2 | 2 | 3 | 4 | 5 |
| Vampirism Blood Exhaustion | `ADD_MULTIPLIED_TOTAL` | -0.0 | -0.1 | -0.2 | -0.3 | -0.4 | -0.5 |
| DBNO Duration | `ADD_MULTIPLIED_BASE` | 1 | 1 | 1 | 0.8 | 0.5 | 0.25 |
| Neonatal Duration | `ADD_MULTIPLIED_BASE` | 1 | 1 | 1 | 1 | 0.75 | 0.5 |

The DBNO/neonatal comments describe shorter durations for decimal values, but the source supplies those positive values as attribute modifier amounts. Runtime semantics must be measured against Vampirism's exact attributes before exposing a normalized percentage.

Other default Vampire age effects include:

- sun damage divisor: 1 / 1.25 / 1.5 / 1.75 / 2 / 2.5;
- fire damage divisor: 1 / 1 / 0.95 / 0.9 / 0.8 / 0.75;
- Holy Water damage divisor: same as fire defaults;
- Hunter-mob incoming damage multiplier: 1 / 1 / 1 / 1.5 / 1.75 / 2;
- villager-price multiplier: 1 / 1.1 / 1.25 / 1.5 / 1.75 / 2;
- optional global healing multiplier is disabled by default;
- Powder Snow immunity is enabled by default for all Vampires while the provider feature is enabled.

Age-granted actions/skills:

- Age 1: Celerity;
- Age 2: Step Assist;
- Age 3: Blood Tap;
- Age 4: Water Walking.

### Hunter — `HUNTER`

Faction: Vampirism Hunter.

Defaults:

- ageing enabled: true;
- faction level to begin: 14;
- Lord level requirement: 0.

Base attribute amounts by Age 0..5:

| Attribute | Operation | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---:|---:|---:|---:|---:|---:|
| Max Health | `ADD_VALUE` | 0 | 1 | 1 | 2 | 2 | 4 |
| Movement Speed | `ADD_VALUE` | 0 | .0125 | .015 | .02 | .025 | .035 |
| Attack Damage | `ADD_VALUE` | 0 | 0 | 1 | 1 | 1.5 | 2 |

Age also modifies provider-owned gameplay through event hooks:

- XP gain is divided by 1 / 1 / 1.25 / 1.5 / 1.75 / 2;
- food exhaustion multiplier: 1 / 1 / 1.25 / 1.5 / 2 / 2.5;
- Faster Regeneration unlock default: Age 3;
- Step Assist default: Age 4;
- Wise Eye default: Age 5;
- Seniority Oil eligibility default: Age 2;
- Tainted Blood eligibility default: Age 2.

Hunter has a serialized `HunterState` with:

- temporary Tainted Age bonus;
- remaining temporary Tainted ticks;
- accumulated sun exposure ticks;
- permanent-transformation flag.

### Werewolf — `WEREWOLF`

Faction: Werewolves.

Registered only when `werewolves` is loaded. Current pack satisfies the condition.

Defaults:

- ageing enabled: true;
- faction level to begin: 14;
- Lord level requirement: 0.

Attributes by Age 0..5:

| Attribute | Operation | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---:|---:|---:|---:|---:|---:|
| Attack Damage | `ADD_VALUE` | 0 | 0 | 1 | 2 | 3 | 4 |
| Max Health | `ADD_VALUE` | 0 | 2 | 2 | 4 | 4 | 6 |
| Werewolves Bite Damage | `ADD_MULTIPLIED_TOTAL` | 0 | 0 | 0 | .125 | .25 | .5 |

Provider overlays by rank include:

- Bite heal: 0 / 0 / 0 / 1 / 2 / 2 health;
- Bite nourishment enabled by default from Age 2: nutrition 1, saturation 0.1 per qualifying bite;
- Werewolf Form time multiplier: 1 / 1.5 / 2 / 3 / 4 / 5;
- Leap strength config multiplier: 1 / 1 / 1.25 / 1.5 / 1.75 / 2;
- raw-meat nutrition multiplier: 1 / 1 / 2 / 2 / 3 / 3;
- raw-meat saturation multiplier: 1 / 1 / 1.5 / 1.5 / 2 / 2;
- Howl summons are buffed by age by default;
- Silver effect incoming-damage multiplier: 1 / 1 / 1.1 / 1.15 / 1.2 / 1.25;
- separate Silver Oil multiplier is all 1.0 by default, so that optional penalty is disabled by default.

Improved Senses unlock default: Age 5 and, by default, Werewolves' native SENSE skill must also be enabled.

## Ageing Methods

### Vampire: `DRAINING` — default

Thresholds: **150 / 300 / 600 / 900 / 1250**.

Progress source: entity-backed Vampirism `BloodDrinkEvent.PlayerDrinkBloodEvent`. The provider adds the event's final amount to Age progress after confirming the selected method and `canAge()`.

This is observational progression over a Vampirism blood settlement. Black Arcana must not credit progress once for raw bite damage and again for the resulting BloodDrinkEvent.

### Vampire: `BITING`

Thresholds: **30 / 45 / 70 / 100 / 200** infected entities.

Progress source: Vampirism Infect action mixin; eligible non-blacklisted infection credits one point.

### Vampire: `TIME`

Thresholds: **72,000 / 144,000 / 288,000 / 576,000 / 1,152,000 ticks**.

The handler runs every 100 player ticks and credits 100 points while `canAge()` remains true.

### Vampire: `V_HUNTING`

Thresholds: **20 / 40 / 80 / 160 / 250 points**.

Default tagged-kill worth:

- petty: 1;
- common: 3;
- greater: 5.

### Hunter: `HUNTING` — default and only configured method in this source line

Thresholds: **20 / 40 / 80 / 160 / 250 points**.

Default tagged-kill worth: 1 / 3 / 5 for petty/common/greater.

### Werewolf: `DEVOUR` — default

Thresholds: **30 / 60 / 100 / 250 / 500 points**.

Qualifying kill must use the Werewolves Bite damage type. Default worth:

- petty: 1;
- common: 2;
- greater: 5;
- exquisite: 10.

### Werewolf: `W_HUNTING`

Thresholds: **20 / 40 / 80 / 160 / 250** with worth 1/3/5.

### Werewolf: `W_MIXED`

Uses devour category values for Bite kills and hunting category values for other qualifying kills.

## Death and faction transitions

Default `deathReset=true` and `ageLostOnDeath=0` mean a normal ServerPlayer death resets Age Rank to 0. If `ageLostOnDeath` is configured >0, only that many ranks are removed.

Faction level 0 or switching away from the current faction clears Age Type/Rank/Progress and runs the provider lifecycle. Do not attempt to preserve Age across an invalid faction by shadow state.

Hunter permanent Tainted transformation has its own `permanentTransformationDeathReset` flag, default false; temporary Tainted state is cleared on Hunter death regardless.

## Optional Sire mechanic

Disabled by default. When enabled, it adds age-bearing Vampire Blood Bottles and inheritance paths tied to aged Player/Advanced Vampire entities. It is intended by the upstream README as an alternative progression model and is explicitly provider-owned.

Integration must preserve the bottle component/rank provenance rather than replacing it with a generic 'vampire age token'.

## Integration consequences

- one canonical Age progress credit per provider event;
- no cross-provider reward should duplicate the same kill/bite/blood event;
- age-granted skills remain real Vampirism/Werewolves `ISkill` entries;
- rank/type changes must flow through `AgeingManager` lifecycle and faction gates;
- UI may read Age Rank/progress, but must not become authoritative;
- config-driven methods and thresholds cannot be hardcoded as permanent Black Arcana constants.