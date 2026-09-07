# Hexalia 1.3.6 — Idols and capability-bearing items

## Status

`SOURCE-PINNED 1.3.6 / WEATHER IDOLS 3/3 + PURITY IDOL AUDITED / SILK IDOL BASE ITEM CONFIRMED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Canonical source pin:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

Installed pack identity remains `hexalia-neoforge-1.3.6.jar` with runtime metadata `1.3.5`; the exact installed behavior therefore remains runtime-QA gated.

## Idol family

Hexalia registers:

- `hexalia:silk_idol` — base item/reagent;
- `hexalia:clarity_idol`;
- `hexalia:rainfall_idol`;
- `hexalia:tempest_idol`;
- `hexalia:purity_idol`.

The base `silk_idol` is registered as an ordinary item. Capability lives in the four derived idols.

## Acquisition recipes confirmed in source

The four capability idols are shapeless recipes:

| Idol | Ingredients |
|---|---|
| Clarity Idol | `hexalia:silk_idol` + `hexalia:air_node` + `hexalia:celestial_crystal` + `minecraft:sunflower` |
| Rainfall Idol | `hexalia:silk_idol` + `hexalia:water_node` + `hexalia:celestial_crystal` + `minecraft:blue_orchid` |
| Tempest Idol | `hexalia:silk_idol` + `hexalia:water_node` + `hexalia:fire_node` + `hexalia:celestial_crystal` |
| Purity Idol | `hexalia:silk_idol` + `hexalia:water_node` + `hexalia:lotus_blossom` + `hexalia:salt` |

The four elemental nodes used here are source-registered ordinary items/reagents. Their existence does not create an autonomous node-resource runtime or elemental casting authority.

## Weather idols

Clarity, Rainfall and Tempest use the same `WeatherIdolItem` execution path.

Shared behavior:

- right-click starts use;
- use animation is `BOW`;
- use duration is 32 ticks;
- weather mutation runs server-side on completion;
- one idol is consumed in survival;
- the server player receives item-use/stat/consume advancement signaling.

### Clarity Idol

`hexalia:clarity_idol` calls:

`setWeatherParameters(6000, 0, false, false)`

Source-level semantic result: clear weather with the provider-specified 6000-tick clear duration and no rain/thunder.

### Rainfall Idol

`hexalia:rainfall_idol` calls:

`setWeatherParameters(0, 6000, true, false)`

Source-level semantic result: rain for the provider-specified 6000-tick duration, without thunder.

### Tempest Idol

`hexalia:tempest_idol` calls:

`setWeatherParameters(0, 6000, true, true)`

Source-level semantic result: rain plus thunder for the provider-specified 6000-tick duration.

## Purity Idol

`hexalia:purity_idol` subclasses the weather-idol use surface but replaces completion behavior.

On use completion it:

1. chooses the item in the user's opposite hand as the target;
2. reads that stack's `DataComponents.ENCHANTMENTS`;
3. removes enchantments whose holders are in `EnchantmentTags.CURSE`;
4. writes the reduced enchantment set back only if at least one curse was removed;
5. consumes one Purity Idol in survival only when a curse was actually removed.

It does not remove potion/status effects, Hexalia Bleeding, Black Arcana Corruption or Arcane Strain.

## Deduplication consequences

### Weather / environment

Hexalia already owns consumable direct weather-setting items for clear, rain and thunderstorm states. Black Arcana should not create a generic duplicate 'weather idol' or trivial weather spell with identical role.

A future forbidden-weather mechanic may still exist if it has materially different identity, costs, hazards, bounds and world-safety behavior. Black Arcana world-changing magic must continue through its own `WorldEffectPolicy`; Hexalia's provider item implementation is not a substitute for Black Arcana world-safety admission.

### Purification / curse removal

Purity Idol already occupies straightforward vanilla-enchantment curse stripping from an item in the opposite hand. A Black Arcana cleansing mechanic should therefore avoid duplicating this exact utility unless there is a deliberate provider bridge.

Purity Idol does not establish authority over:

- Black Arcana Corruption;
- Arcane Strain;
- Arcane Backlash;
- external provider curses/status systems not represented as vanilla curse-tagged enchantments.

## Integration posture

- Weather settlement remains Hexalia-owned for idol use.
- Do not re-fire weather mutation or consume the idol a second time from Black Arcana.
- If RPG/mastery credit is ever attached, use a discrete post-use causal event rather than polling weather state.
- Do not infer a stable Hexalia API from implementation classes alone.
- Installed-runtime equivalence remains pending because of the `1.3.6` filename/source versus `1.3.5` runtime metadata mismatch.
