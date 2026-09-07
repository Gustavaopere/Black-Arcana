# Brew of Daybloom

## Estado

`SOURCE-PINNED HEXALIA 1.3.6 / ITEM+EFFECT+RECIPE+FORMULA VERIFIED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

- Provider: Hexalia
- Source pin: `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`
- Item ID: `hexalia:brew_of_daybloom`
- Effect ID: `hexalia:daybloom`
- Acquisition: Small Cauldron
- Base duration: `4800 ticks = 240 s`
- Full Moonweave duration: `7200 ticks = 360 s`
- Base amplifier: `0`
- Effect cadence: every `100 ticks = 5 s`

## Receita 1.3.6

`hexalia:small_cauldron`, recipe duration `4800`:

1. `hexalia:sunfire_tomato`
2. `hexalia:spirit_powder`
3. `minecraft:glow_berries`
4. `hexalia:witchweed`

Result: `hexalia:brew_of_daybloom`.

## Efeito 1.3.6

The custom Daybloom behavior applies only when the affected entity is a Player.

Every 100 ticks it creates/rechecks Hexalia's `SunlightCheck` at the player's position and reads its generation multiplier.

### No usable sunlight

When `generation <= 0.0`:

- player receives `1.5` magic damage;
- the Daybloom movement-speed modifier is removed.

### Usable sunlight

When `generation > 0.0`:

- healing = `2.0 × generation`;
- movement-speed modifier = `0.05 × (amplifier + 1) × generation`;
- modifier operation = `ADD_MULTIPLIED_TOTAL`;
- the previous Daybloom speed modifier is removed before the updated transient value is applied.

At the brew's base amplifier 0, the speed term is `0.05 × generation`.

The exact range and environmental derivation of `generation` belong to Hexalia's `SunlightCheck`; this fiche does not invent a 0–1 range or convert it into a Black Arcana solar resource.

## Deduplication

Daybloom already owns a prepared witchcraft capability combining:

- environmental sunlight condition;
- periodic healing;
- sunlight-scaled movement bonus;
- self-damage when sunlight generation is absent.

Future Divine/Celestial content cannot claim novelty merely from “sunlight heals/buffs the caster”. A distinct Black Arcana Holy/miracle/authority contract is still required.

## Authority / integration

Hexalia owns sunlight evaluation, the MobEffect lifecycle, damage/heal cadence and movement modifier. Black Arcana must not:

- duplicate its 5-second pulses;
- convert each pulse into a spell cast or Mastery event;
- add a second sunlight meter to emulate it;
- re-settle its healing or damage.

The installed filename/runtime metadata mismatch still requires exact pack QA before the 1.3.6 formulas are labeled installed-runtime validated.
