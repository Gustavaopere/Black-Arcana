# Ars Elemental 0.7.10.1 — perks and perk providers

Status: `3/3 PERKS + 48/48 ARMOR PERK PROVIDERS SOURCE-PINNED / SUMMONING DESCRIPTION-PATH DIVERGENCE / RUNTIME QA PENDING`

Source checkpoints:

- Ars Elemental: `Alexthw46/Ars-Elemental@fe9d37e947c5fffd4f89a6ae4dd87ae52489b30d`
- Ars Nouveau 5.13.1 perk utility: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

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

`SummonPerk.applyAttributeModifiers` adds provider `SUMMON_POWER`:

- modifier amount: `slotValue - 1`;
- operation: `ADD_VALUE`;
- modifier id: `ars_elemental:summon_power`.

`SummonEvents.summonPowerup` then adds the owner's current `SUMMON_POWER` attribute value to damage dealt by an Ars `ISummon` before the hit resolves.

Acquisition datagen: Blank Thread reagent; 2× Conjuration Essence; Echo Shard; 2× Wilden-drop tag ingredient.

#### Summoning Sickness divergence

The provider description says Summoning Sickness is reduced by 10% for each tier. The exact executable handler is present in `SummonEvents.summonSickReduction` and computes:

`duration = duration * (1 - PerkUtil.countForPerk(SummonPerk.INSTANCE, entity) / 10)`

At the exact Ars Nouveau 5.13.1 pin, `PerkUtil.countForPerk` returns the **maximum perk slot value** found on worn armor. Normal Ars perk slots are values 1, 2 or 3. Because the expression uses integer division, `1/10`, `2/10` and `3/10` all evaluate to 0 before subtraction.

Therefore the source path observed for ordinary slot values leaves the duration multiplier at `1`, not 0.9/0.8/0.7. Phase 2U records this as:

`DESCRIPTION-PATH DIVERGENCE / RUNTIME QA REQUIRED`

The catalog does not silently replace the executable expression with the provider description. A runtime check is still required because event ordering or another installed component could affect the observed final duration.

## Armor perk providers — 48 pieces

Ars Elemental creates 12 armor sets: Fire, Water/Aqua, Air and Earth, each in Light, Medium and Heavy variants. Four pieces per set produce 48 armor items and `postInit()` registers all of them through Ars `PerkRegistry.registerPerkProvider`.

Per-piece slot list:

- Heavy: head `[ONE,TWO,TWO]`; chest `[ONE,TWO,THREE]`; legs `[ONE,TWO,THREE]`; boots `[ONE,TWO,TWO]`.
- Medium: every piece `[ONE,TWO,THREE]`.
- Light: head `[ONE,TWO,THREE]`; chest `[TWO,TWO,THREE]`; legs `[TWO,TWO,THREE]`; boots `[ONE,TWO,THREE]`.

`makePerkList` wraps the same slot list four times. Phase 2U does not assign semantics to that outer list dimension beyond the exact Ars provider contract without runtime/API evidence.

## Authority and deduplication

- Ars Nouveau/Ars Elemental own perk storage, slot values, effect callbacks and `SUMMON_POWER`.
- RPG Skill Tree does not become owner of these Threads merely because it provides progression elsewhere.
- Black Arcana must not add a parallel poison/shock/summon-damage modifier for the same provider callback.
- Armor mana and regen bonuses remain provider-native Ars mana modifications and do not authorize a second Black Arcana resource.
