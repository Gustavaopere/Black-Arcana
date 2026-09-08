# Ars Elemental 0.7.10.1 — perks and perk providers

Status: `3/3 PERKS + 48/48 ARMOR PERK PROVIDERS SOURCE-PINNED / RUNTIME QA PENDING`

## Registered perks

### `ars_elemental:thread_spore`

`SporePerk` implements Ars `IEffectResolvePerk`.

Before an `IDamageEffect` resolves on a valid LivingEntity target, it applies:

- Poison for normal living targets;
- Hunger for inverted-heal/harm targets.

Duration = `slotValue * 5 * 20` ticks. Amplifier = `slotValue - 1`.

The special local Poison Spores path uses a simplified damage eligibility check to avoid rejecting its own effect path.

Acquisition datagen: Blank Thread reagent; 2× Earth Essence; 1× Spore Blossom; 1× Spider Eye.

### `ars_elemental:thread_shock`

Before a valid damaging effect resolves:

- slot values below 3 apply Ars Shocked for 100 ticks, amplifier equal to the slot value;
- slot value 3 applies provider `LIGHTNING_LURE` for 100 ticks, amplifier 1.

Acquisition datagen: Blank Thread reagent; 2× Air Essence; Lightning Rod; Flashing Pod.

### `ars_elemental:thread_summon`

The perk adds provider `SUMMON_POWER` through an item attribute modifier:

- modifier amount: `slotValue - 1`;
- operation: `ADD_VALUE`;
- modifier id: `ars_elemental:summon_power`.

The provider description additionally claims Summon Sickness reduction by 10% per tier. That reduction path is not established by `SummonPerk` itself in this pass and remains `IMPLEMENTATION PATH AUDIT PENDING` rather than being inferred.

Acquisition datagen: Blank Thread reagent; 2× Conjuration Essence; Echo Shard; 2× Wilden-drop tag ingredient.

## Armor perk providers — 48 pieces

Ars Elemental creates 12 armor sets: Fire, Water/Aqua, Air and Earth, each in Light, Medium and Heavy variants. Four pieces per set produce 48 armor items and `postInit()` registers all of them through Ars `PerkRegistry.registerPerkProvider`.

Per-piece slot list:

- Heavy: head `[ONE,TWO,TWO]`; chest `[ONE,TWO,THREE]`; legs `[ONE,TWO,THREE]`; boots `[ONE,TWO,TWO]`.
- Medium: every piece `[ONE,TWO,THREE]`.
- Light: head `[ONE,TWO,THREE]`; chest `[TWO,TWO,THREE]`; legs `[TWO,TWO,THREE]`; boots `[ONE,TWO,THREE]`.

`makePerkList` wraps the same slot list four times. Phase 2U does not assign semantics to that outer list dimension without checking the exact Ars perk-provider API.

## Resource boundary

Armor mana and regen bonuses are provider-native Ars mana modifications. They are not RPG Skill Tree attributes and do not authorize a second Black Arcana resource.