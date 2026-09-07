# Hexalia 1.3.6 — Sacs and persistent clouds

## Status

`SOURCE-PINNED 1.3.6 / SACS 4/4 / CLOUD EXECUTION AUDITED / INSTALLED-RUNTIME EQUIVALENCE PENDING`

Canonical source pin:

`AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d`

Installed pack identity remains `hexalia-neoforge-1.3.6.jar` with runtime metadata reporting `1.3.5`. Exact installed balance/behavior therefore remains runtime-QA gated.

## Acquisition — 4/4 shapeless recipes

| Sac | Source-pinned recipe |
|---|---|
| Foul Sac | `minecraft:spider_eye` + `hexalia:witchweed` + `minecraft:leather` |
| Frost Sac | `minecraft:snowball` + `hexalia:chillberries` + `minecraft:leather` |
| Searing Sac | `hexalia:rabbage` + `hexalia:sunfire_tomato` + `minecraft:leather` |
| Purifying Sac | `hexalia:salt` + `hexalia:lotus_blossom` + `minecraft:leather` |

These are ordinary shapeless crafting recipes. They are not Small Cauldron brews and do not consume Mortar & Pestle progress.

## Shared thrown-sac contract

Foul, Frost and Searing use Hexalia's `ThrownSacItem` path:

- right-click throws the corresponding provider projectile;
- projectile speed path is `shootFromRotation(..., -20°, 0.5F, 1.0F)`;
- one sac is consumed in survival;
- the projectile uses default gravity `0.05D`;
- on impact, the projectile creates the provider-owned AreaEffectCloud and discards itself;
- if the projectile has a LivingEntity owner, that owner is assigned to the cloud, which affects damage-source causality.

The 1.3.6 source configuration defaults all four sac cloud durations to `8` seconds, configurable in the provider range `1–60` seconds.

For Foul/Frost/Searing, `SacCloudHelper.configureWithHold` initializes radius `3.0`, holds that radius for two seconds, then shrinks it linearly over the remaining lifetime. Wait time is zero.

## Foul Sac

### Cloud

Source-pinned behavior:

- initial radius: `3.0`;
- default lifetime: `8 s`;
- Poison amplifier `2` for 200 ticks = Poison III;
- Slowness amplifier `1` for 200 ticks = Slowness II;
- every 20 ticks, all qualifying living entities currently within the cloud receive `0.5F` magic damage.

Damage attribution uses `indirectMagic(cloud, owner)` when a LivingEntity owner exists, otherwise vanilla magic damage.

### Semantic role

Persistent toxic/debilitating field. Black Arcana poison/corruption design must not classify this as Corruption merely because both can be harmful over time.

## Frost Sac

### Cloud

Source-pinned behavior:

- initial radius: `3.0`;
- default lifetime: `8 s`;
- Weakness amplifier `1` for 200 ticks = Weakness II;
- each server tick, qualifying living entities that can freeze gain up to `+5` frozen ticks, capped at their `getTicksRequiredToFreeze()` threshold.

### Semantic role

Persistent cold/freeze control field. It is provider-owned freeze accumulation, not a Black Arcana Strain or Arcane Danger channel.

## Searing Sac

### Cloud

Source-pinned behavior:

- initial radius: `3.0`;
- default lifetime: `8 s`;
- applies `hexalia:bleeding`, amplifier `0`, duration `200` ticks through the AreaEffectCloud effect surface;
- every 20 ticks, qualifying living entities receive `0.5F` magic damage and are ignited for `3` seconds.

The Hexalia Bleeding effect itself is separately source-pinned: at amplifier 0 it applies generic damage every server tick using default config `0.5`, with `+0.2` per amplifier level. Installed-runtime acceptance of that quantitative value remains blocked by the provider version mismatch.

### Semantic role

Fire + bleeding persistent offensive field. It must not be interpreted as evidence that Hexalia owns Black Arcana blood-volume resources or Hematic Reservoir semantics.

## Purifying Sac

Purifying Sac differs from the other three because it has two use modes and is registered with durability `6`.

### Direct self-use

Without shift:

- use duration: `32` ticks;
- use animation: Bow;
- on successful server-side completion, `ModUtil.removeHarmfulEffects(user)` removes every active MobEffect whose category is `HARMFUL`;
- in survival, the held Purifying Sac loses `1` durability rather than being stack-consumed.

This cleanse is category-based and therefore preserves beneficial/neutral effects.

### Thrown use

While shift-right-clicking:

- a `PurifyingSacProjectile` is spawned;
- one item is consumed in survival;
- on impact, it creates `CleansingCloud`;
- initial radius is `3.0`;
- default lifetime is `8 s`;
- unlike Foul/Frost/Searing, the cleansing cloud shrinks from the start rather than using the two-second hold phase;
- every 20 ticks, all qualifying living entities in radius have `HARMFUL` MobEffects removed.

### Distinction from Censer Hollow Aura

Purifying Sac/Cleansing Cloud removes only effects categorized `HARMFUL`.

Censer `Hollow Aura`, by contrast, removes **all** currently active MobEffects regardless category or namespace. These are distinct provider capabilities and must remain separate in deduplication and compatibility tests.

## Shared cloud target admission

`SacCloudHelper.forEachLivingInRadius` admits targets only when:

- the entity is a `LivingEntity` returned by the cloud bounding box query;
- the entity is alive;
- `isAffectedByPotions()` is true;
- horizontal x/z distance from cloud center is within current radius.

Do not assume arbitrary entities, immune entities or non-living targets are affected.

## Black Arcana integration posture

- Hexalia owns projectile creation, cloud lifetime, radius shrink, status effects and damage attribution.
- A cloud tick is not a Black Arcana cast and must never create repeated Black Arcana/RPG mastery credit.
- If progression credit is ever attached to a thrown provider item, it must preserve the projectile/cloud owner and deduplicate one causal activation from subsequent cloud pulses.
- Do not double-apply damage, freeze, burning or effect removal.
- Purifying Sac does not cleanse Black Arcana Corruption or Arcane Strain unless those channels are deliberately represented as removable harmful MobEffects; current architecture does not require that representation.
- Foul/Searing fields do not become Black Arcana Arcane Danger merely because they are hazardous.
- Source implementation classes are not treated as stable external integration APIs.

## Runtime/API QA blockers

1. reconcile physical filename/source release `1.3.6` against installed runtime metadata `1.3.5`;
2. confirm all four recipes in the installed datapack;
3. confirm default durations and radius-shrink behavior in the installed pack;
4. test cross-mod MobEffect interaction for Purifying Sac and Censer Hollow Aura independently;
5. verify causal owner preservation for projectile/cloud damage before any progression bridge;
6. fail closed if no stable provider completion/use boundary exists.
