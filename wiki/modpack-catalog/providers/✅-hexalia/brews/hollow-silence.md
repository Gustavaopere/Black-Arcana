# Brew of Hollow Silence

## Estado

`SOURCE-PINNED HEXALIA 1.3.6 / ITEM+EFFECT+RECIPE VERIFIED / PLAYER-FACING BEHAVIOR NOT LOCATED IN IMPLEMENTATION PATH / RUNTIME QA REQUIRED`

- Provider: Hexalia
- Source pin: `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`
- Item ID: `hexalia:brew_of_hollow_silence`
- Effect ID: `hexalia:hollow_silence`
- Acquisition: Small Cauldron
- Base duration: `4800 ticks = 240 s`
- Full Moonweave duration: `7200 ticks = 360 s`
- Base amplifier: `0`

## Receita 1.3.6

`hexalia:small_cauldron`, recipe duration `4800`:

1. `minecraft:feather`
2. `hexalia:ghost_powder`
3. `hexalia:chillberries`
4. `minecraft:sculk`

Result: `hexalia:brew_of_hollow_silence`.

## Source path observado

`HollowSilenceEffect` is an otherwise empty `MobEffect` subclass: its exact 1.3.6 class contains only the constructor and no tick logic, hurt hook, add/remove hook or attribute modifier.

A repo-wide search at the exact release pin located the Hollow Silence identifier in:

- effect registration;
- brew item registration;
- recipe/generated data;
- advancement/data/model surfaces;
- localization/player-facing documentation.

No additional Hollow Silence-specific implementation path was located during this audit.

## Public-description delta

The provider's player-facing text describes Hollow Silence as suppressing/silencing the user's presence around sound-sensitive entities, with periodic vision clouding/drawback semantics.

That description is valid evidence of **intended/provider-documented identity**, but current source evidence does not establish how or whether those semantics execute at the 1.3.6 pin.

Status:

`SOUND-SILENCE + VISION DRAWBACK = PUBLIC DESCRIPTION / DIRECT IMPLEMENTATION PATH NOT LOCATED / RUNTIME QA REQUIRED`.

This is not promoted to an exact runtime capability or an integration hook.

## Deduplication

At semantic level, Hexalia claims a prepared stealth/sound-suppression witch brew. Black Arcana should avoid designing an identical potion identity while the provider claim exists, but this row cannot be used as proof that the exact installed runtime successfully suppresses Warden/sculk hearing or any other specific sensor.

## Authority

Black Arcana must not compensate for the apparent source gap by implementing Hollow Silence on Hexalia's behalf. Any future compatibility behavior requires an explicit supported hook or independently owned Black Arcana mechanic with distinct identity.
