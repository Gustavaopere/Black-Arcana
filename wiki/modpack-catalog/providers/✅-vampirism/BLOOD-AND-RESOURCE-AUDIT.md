# Vampirism 1.10.13 — Blood and Resource Audit

Status: `PLAYER BLOOD + FLUID BLOOD + EXHAUSTION/SATURATION + STORAGE/CONVERSION SOURCE-PINNED / RUNTIME QA PENDENTE`

Canonical source: `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`.

## There are multiple blood concepts

The provider uses related but non-identical blood representations. They must not be collapsed into one arbitrary Black Arcana number.

1. **Player blood level** — food-like integer resource for Vampire players.
2. **Blood saturation** — hidden/secondary food-style buffer used before blood level is consumed by exhaustion.
3. **Blood exhaustion** — accumulated activity cost; can consume saturation/blood once a threshold is crossed.
4. **`vampirism:blood` fluid** — NeoForge fluid measured in mB.
5. **Impure blood** — separate provider fluid/storage state used by conversion machinery.
6. **Vampire Blood Bottle / Blood Bottle / Pure Blood items** — discrete items with provider-specific semantics; they are not interchangeable merely because their names contain “blood”.

## Player blood state

`BloodStats` initializes:

- `maxBlood = 20`;
- `bloodLevel = 20`;
- `bloodSaturationLevel = 5.0`;
- `bloodExhaustionLevel = 0`.

`IBloodStats` exposes the read-facing blood state. Mutation is performed through provider paths such as `IVampire.drinkBlood(...)`, `IVampire.useBlood(...)` and internal BloodStats methods.

### Vanilla hunger interception

While the player is a Vampire, `BloodStats.onUpdate()`:

1. forces vanilla food level to 10;
2. reads vanilla FoodData exhaustion;
3. clears vanilla exhaustion;
4. transfers that exhaustion into Vampirism blood exhaustion through `addExhaustion(...)`.

This means generic systems that add vanilla food exhaustion can indirectly affect the Vampire blood economy. Black Arcana must not also debit blood for the same activity unless the design explicitly intends an additional cost.

## Exhaustion settlement

Default exhaustion gate:

- normal biome: **4.0**;
- biome tagged `IS_VAMPIRE_BIOME`: **6.0**.

When blood exhaustion exceeds the gate:

1. the gate amount is subtracted from accumulated exhaustion;
2. if blood saturation > 0, saturation loses 1;
3. otherwise blood level loses 1 unless difficulty is Peaceful and `vpBloodUsagePeaceful` disables usage.

The `vampirism:blood_exhaustion` attribute multiplies new exhaustion before it is accumulated. Default attribute base value is 1.0 and valid range is 0–10.

### Consequence for perks

A perk that modifies blood consumption caused by movement/activity should prefer the provider `blood_exhaustion` attribute or an equally canonical hook. Directly refunding blood after the provider settles exhaustion risks fighting the native saturation/exhaustion model.

## Natural regeneration

With vanilla `naturalRegeneration` enabled:

### Saturated full-blood regeneration

If:

- blood saturation > 0;
- player is hurt;
- blood level is at max;

then every 10 bloodTimer ticks the provider:

- heals `(min(saturation, 6) / 6) × healModifier`;
- adds equivalent exhaustion;
- resets bloodTimer.

### Ordinary blood regeneration

If blood > 0 and player is hurt:

- with blood level ≥18, after 80 timer ticks, heal `1 × healModifier` and add 6 exhaustion;
- otherwise after 300 timer ticks, heal `0.5 × healModifier` and add 3 exhaustion.

`healModifier = 1 + (vampireLevel / maxVampireLevel) × 0.5` when Vampire state is available.

This regeneration is provider-owned sustain. A Black Arcana healing observer must not label every resulting heal as a separate magical lifesteal or external regeneration proc.

## Zero-blood state

If blood reaches zero and the player is neither Creative nor Spectator, the provider advances a starvation-like timer. At the 80-tick threshold it applies `NO_BLOOD` depending on current health and difficulty.

This is a native failure state and should remain authoritative.

## Public blood mutation API

`IVampire` exposes:

### `drinkBlood(int amt, float saturationMod, IDrinkBloodContext context)`

Adds blood in **blood food units**, not mB. The overload with `useRemaining` controls whether overflow can be processed elsewhere, e.g. into blood containers/items.

### `useBlood(int amt, boolean allowPartial)`

Consumes blood food units. If `allowPartial=false`, the requested amount is only removed if enough blood is available.

These methods are legitimate provider API, but Black Arcana should call them only for a deliberately designed Vampirism transaction. They should not be used as a generic “blood mana” wallet for unrelated magic.

## BloodDrinkEvent settlement point

`BloodDrinkEvent.PlayerDrinkBloodEvent` is emitted before `BloodStats.addBlood(...)`.

The event exposes and permits changes to:

- amount;
- saturation modifier;
- `useRemaining`;
- source context.

Therefore it is the strongest public hook for perks that intentionally modify **blood intake**. It is not a post-settlement notification: listeners changing the amount change what the provider will subsequently add.

Deduplication rule: one provider drink event receives one causal identity. A later blood-level change is settlement of that same transaction, not a second feeding event.

## Fluid conversion constant

`VReference.FOOD_TO_FLUID_BLOOD = 100`.

Therefore:

**1 player blood unit corresponds to 100 mB of provider fluid blood when the provider explicitly converts between those domains.**

This is a conversion constant, not permission to synchronize every blood-fluid tank with the player's bar.

## Blood Bottle

`BloodBottleItem` defines:

- `AMOUNT = 9` blood units;
- multiplier = 100 mB per unit;
- capacity = **900 mB**.

Its fluid handler only accepts amounts that conform to the provider's blood-unit granularity.

## Blood Container

`BloodContainerBlockEntity` defines:

- `LEVEL_AMOUNT = 9 × 100 = 900 mB`;
- `CAPACITY = LEVEL_AMOUNT × 14 = 12,600 mB`.

The tank accepts either:

- `vampirism:blood`;
- provider impure blood.

The visual level is based on 900 mB increments.

This is already a provider-native blood storage block. A Black Arcana blood reservoir must therefore have a distinct role/scale/contract rather than merely recreating a larger Blood Container.

## Altar of Inspiration

Capacity: **10,000 mB** of provider Blood only.

Level-up requirements:

- level 2: 4,000 mB;
- level 3: 7,000 mB;
- level 4: 10,000 mB.

The altar's internal tank is deliberately non-drainable through its normal external path; its own ritual temporarily enables internal drain for provider settlement.

Integration rule: do not externally bypass the altar's drain restriction to “help” level-up automation unless a design explicitly delegates authority to that block.

## Blood conversion registry

`VampirismAPI.bloodConversionRegistry()` exposes `IBloodConversionRegistry`.

The provider supports data-map-driven conversions for:

- items → impure blood;
- fluids → blood.

The API can:

- inspect whether an item can become impure blood;
- derive item blood representation;
- inspect fluid conversion rates;
- convert a `FluidStack` to provider blood.

Entity blood values are handled separately by the Vampirism entity registry.

This is the canonical extension point for cross-mod fluid/item compatibility. Black Arcana should prefer provider data maps/API over hard-coded foreign-fluid name matching.

## Provider attributes tied to the blood/survival loop

Four attributes are registered by Vampirism:

| Attribute id | Base | Range | Role |
|---|---:|---:|---|
| `vampirism:sundamage` | 0 | 0–1000 | sundamage quantity/behavior input |
| `vampirism:blood_exhaustion` | 1 | 0–10 | multiplier for generated blood exhaustion |
| `vampirism:neonatal_duration` | 1 | 0–Integer.MAX | multiplier/input for Neonatal duration |
| `vampirism:dbno_duration` | 1 | 0–Integer.MAX | multiplier/input for DBNO/resurrection duration |

The latter three are syncable in source.

## Known blood consumers and indirect consumers

### Half Invulnerable

Default `vaHalfInvulnerableBloodCost = 4` blood units.

The cost is not paid when the action is activated. It is attempted later only when a qualifying incoming hit is actually intercepted. If the player cannot pay, the action is deactivated.

This is a canonical example of **late causal settlement**.

### Bat

Bat adds default `0.005` exhaustion per update through `addExhaustion`. It does not directly call `useBlood` in the action class.

Therefore Bat's eventual blood consumption flows through the exhaustion/saturation system.

### Vampire Sword

The provider has explicit config for blood charging/usage (`vampireSwordChargingFactor`, `vampireSwordBloodUsageFactor`) and source paths that interact with fluid/blood storage. Treat the sword as its own provider economy rather than attributing all sword-blood movement to the player bar.

## Known blood producers/sources

Provider-native sources include, among others:

- biting/draining entities through provider bite logic;
- Blood Bottles and blood-compatible items;
- Hearts/provider food paths that call `drinkBlood`;
- fluid storage/conversion;
- minion task `collect_blood` for eligible Vampire minions.

The source audit does not reduce all these paths to one flat amount because each source carries its own context, saturation and overflow behavior.

## Anti-abuse and deduplication contract

- Do not reward both `BloodDrinkEvent` and the resulting blood-level increase as two independent feedings.
- Do not charge a direct blood cost for Bat on top of provider exhaustion settlement.
- Do not pre-charge Half Invulnerable before a hit actually qualifies.
- Do not map arbitrary red fluids to Vampirism blood; use `IBloodConversionRegistry`/data maps.
- Do not treat Blood fluid stored in tanks as automatically spendable player blood.
- Do not refill the player by setting NBT/blood level directly; use provider API when an explicit integration transaction exists.
- Preserve `IDrinkBloodContext` so source/causality remains available to downstream integrations.

## Black Arcana reservoir implication

A future large blood reservoir can interoperate with Vampirism, but its contract should be explicit. Safe candidates include:

1. storage of actual `vampirism:blood` through NeoForge fluid capabilities;
2. conversion of approved foreign fluids through `bloodConversionRegistry`;
3. controlled provider `drinkBlood(...)` transactions with a concrete source context and exact mB→blood conversion;
4. separate magic-resource accounting layered **on top of stored fluid**, without silently replacing the player's native 20-point blood bar.

Unsafe design:

- continuously mirroring tank mB into player `bloodLevel`;
- expanding `BloodStats.maxBlood` based only on tank capacity without a provider-supported design;
- treating the same mB simultaneously as player blood and spell mana without atomic reservation/settlement.

## Runtime QA queue

- BloodDrinkEvent amount/saturation mutation in dedicated server;
- saturation-first exhaustion settlement;
- vampire-biome 6.0 exhaustion gate;
- Peaceful `vpBloodUsagePeaceful` behavior;
- natural-regeneration healing and exhaustion;
- Blood Bottle fill/drain granularity;
- Blood Container capability interop with pack tanks/pipes;
- provider fluid conversion data maps with installed tech/magic fluids;
- Half Invulnerable 4-blood late settlement;
- Bat exhaustion under movement/stamina integrations;
- minion `collect_blood` production and offline cooldown behavior.
