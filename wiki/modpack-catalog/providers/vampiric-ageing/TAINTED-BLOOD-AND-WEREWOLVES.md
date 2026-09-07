# Vampiric Ageing 1.4.21 — Tainted Blood and Werewolves

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## Domain separation

This provider uses the word "blood" for two different concepts that must not be collapsed:

1. **Vampirism Vampire blood** — the canonical Vampire blood/saturation/exhaustion resource owned by Vampirism;
2. **Hunter Tainted Blood** — a Vampiric Ageing transformation/progression state stored inside `HunterAgeingType.HunterState`.

Tainted Blood is not a second Vampirism blood bar and is not fluid/tank capacity. It changes the Hunter's cumulative Age and downstream modifiers.

## Hunter Tainted Blood state

The provider serializes four Hunter-specific fields:

- temporary Tainted Age bonus;
- remaining temporary Tainted ticks;
- accumulated sun-exposure ticks;
- permanent-transformation flag.

Canonical cumulative Tainted Age:

- no Tainted bonus/transformation → **0** for Tainted-gated mechanics;
- temporary bottle active → `base Hunter Age + bottle bonus`;
- permanent transformation → `base Hunter Age + 6`.

Normal Hunter Age remains capped at 5. Therefore a fully aged permanently transformed Hunter reaches cumulative Tainted Age **11**.

The cumulative value is provider-computed through `CapabilityHelper.getCumulativeTaintedAge(player)` and should be read from that semantic path rather than reconstructed from UI text.

## Temporary Tainted Blood

### Eligibility

Defaults:

- Tainted Blood system enabled: true;
- Hunter base Age required to drink a Tainted Blood Bottle: **2**;
- already permanently transformed Hunters cannot start the bottle use path.

### Item representation

Registry item: `vampiricageing:tainted_blood_bottle`.

The item has durability 5 and uses its `minecraft:damage` component as the Tainted Age bonus carried by that bottle.

The source includes five Alchemical Table recipes:

- `tainted_blood_bottle_1.json` through `tainted_blood_bottle_5.json`.

Endpoints explicitly audited:

- rank 1: `vampirism:vampire_blood_bottle` + `vampirism:pure_blood_0` → Tainted Blood Bottle with `minecraft:damage=1`;
- rank 5: `vampirism:vampire_blood_bottle` + `vampirism:pure_blood_4` → Tainted Blood Bottle with `minecraft:damage=5`.

All five recipes require the provider's `vampiricageing:tainted_blood_skill` through the Vampirism Alchemical Table recipe `skill` field.

Do not infer custom Black Arcana recipe access from item existence: the native recipe/skill gate is part of survival progression.

### Settlement

On finishing a valid bottle:

1. read the bottle's `damageValue` as the temporary Age bonus;
2. read current base Hunter Age;
3. set temporary duration to `temporaryTaintedBloodBaseTicks × base Hunter Age`;
4. default base duration is 3600 ticks;
5. set the temporary bonus;
6. apply `vampiricageing:tainted_blood_effect` for the same duration;
7. consume one bottle;
8. re-run the Hunter Age Type skill/attribute lifecycle server-side.

The temporary bonus itself is authoritative Hunter state. The MobEffect is not sufficient as a replacement state representation.

### Expiry/death/cleansing

Every Hunter tick cycle, when not permanently transformed, remaining temporary Tainted ticks decrease; when they reach zero the temporary Age bonus is cleared.

Hunter death clears:

- temporary Tainted Age bonus;
- temporary Tainted ticks;
- accumulated sun ticks.

Vampirism Garlic Injection, when used while cumulative Tainted Age >0, clears:

- temporary Tainted bonus;
- temporary ticks;
- permanent transformation;

and consumes one injection in the audited handler.

This is a provider lifecycle transition, not a generic MobEffect cleanse.

## Permanent Tainted transformation

Registry item: `vampiricageing:tainted_elixir`.

Defaults:

- permanent transformation available: true;
- Hunter base Age required: **5**;
- permanent transformation death reset: **false**.

On valid consumption:

- set HunterState `transformed=true`;
- apply brief Blindness and Slowness;
- play provider sound/particles;
- consume the Elixir;
- re-run provider skills/attributes server-side.

Permanent transformation substitutes a fixed Tainted bonus of **6** regardless of temporary bottle state.

### Native acquisition

`vampiricageing:tainted_concentrate` is created in the Vampirism Alchemical Table from:

- one Tainted Blood Bottle carrying `minecraft:damage=5`;
- `vampirism:pure_blood_4`;
- provider Tainted Blood skill gate.

`vampiricageing:tainted_elixir` is then a shaped crafting recipe:

```text
XXX
XYX
XXX
```

where:

- `X` = `vampiricageing:tainted_concentrate`;
- `Y` = `vampirism:mother_core`.

Thus the permanent route is deliberately late-game and consumes eight Concentrates plus one Mother Core.

## Cumulative Tainted Age thresholds

Defaults:

| Cumulative Age | Native consequence/gate |
|---:|---|
| 6 | Holy Water interaction threshold configured |
| 7 | worse villager trade-deal threshold configured |
| 8 | Hunter Teleport + coffin-use threshold |
| 9 | solar-degradation system begins |
| 10 | Limited Hunter Bat Mode |
| 11 | indefinite underwater breathing |

These are config-driven defaults, not permanent integration constants.

## Tainted attribute/gameplay defaults

Arrays are indexed by cumulative Age 0..11.

### Damage bonus

`[0, 0, 0, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.25, 2.5, 3]`

### Fire incoming-damage multiplier

`[1, 1, 1, 1.2, 1.2, 1.4, 1.6, 1.8, 2, 2.25, 2.5, 3]`

### Max-health bonus

`[0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]`

### Movement-speed bonus

`[0, 0, 0, 0, 0, 0, 0, 0, 0.02, 0.03, 0.04, 0.06]`

### Villager-price multiplier

`[1, 1, 1, 1, 1, 1, 1, 1.25, 1.5, 1.75, 2, 2.5]`

### Mining-speed multiplier

`[1, 1, 1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.325, 1.35, 1.5]`

The provider applies these through its Hunter state/lifecycle and event hooks. Black Arcana must not append the same modifier a second time.

## Tainted solar degradation

Defaults:

- enabled: true;
- starts at cumulative Age 9;
- accumulated-sun multiplier by cumulative Age 0..11: `[1,1,1,1,1,1,1,1,1,2,4,8]`;
- Weakness threshold: 1200 accumulated ticks;
- Slowness threshold: 1800;
- stronger Slowness threshold: 2800;
- damage threshold: 3600;
- base damage: 2.5;
- Blindness threshold: 5000;
- max accumulated sun: 10000.

At/above the damage threshold the handler applies provider/Vampirism sun damage; at ≥2× and ≥3× the threshold it applies additional damage instances. Sunscreen and creative-like `instabuild` bypass the effect application path.

Sun exposure decays when no longer actively accumulating. The state stores exposure across ticks and synchronizes it.

Do not model this as a simple boolean `inSun` debuff; it is an accumulated provider-owned hazard state.

## Limited Hunter Bat Mode relationship

Cumulative Age 10 unlocks the provider's Limited Bat Mode. It is not Vampirism's standard Vampire Bat action, although its implementation intentionally reuses similar mechanics.

It grants flight and altered dimensions but also removes Armor/Toughness and disables a broad set of interactions. Any Black Arcana UI/ability integration must read the real active action/special-attribute state rather than a generic `isFlying` test.

## Werewolves integration

Werewolf support is conditional upstream but active in this pack because Werewolves 2.0.3.3 is installed.

### Age progression

Default `DEVOUR` progression credits only qualifying kills whose damage source is Werewolves' native Bite damage type. Alternative `W_HUNTING` and `W_MIXED` methods use the provider's entity tags and point values.

Therefore one Bite kill can have multiple native consequences but must have only one Age-progress settlement according to the selected `IAgeMethod`.

### Bite settlement overlay

On Werewolf Bite incoming damage, for a Werewolf player attacker the provider:

- heals according to Age: `[0,0,0,1,2,2]`;
- when `bitingGivesFood=true` and Age >=2, credits native FoodData with nutrition 1 and saturation 0.1.

It also modifies Werewolves' native `BITE_DAMAGE` attribute by Age with `ADD_MULTIPLIED_TOTAL` amounts `[0,0,0,0.125,0.25,0.5]`.

This is an overlay on the actual Werewolves Bite pipeline, not a separate Black Arcana bite action.

### Raw meat

Age config exposes native raw-meat nutrition/saturation scaling:

- nutrition multiplier: `[1,1,2,2,3,3]`;
- saturation multiplier: `[1,1,1.5,1.5,2,2]`.

The exact settlement is implemented through Werewolves/Vampiric Ageing mixin integration and should not be duplicated from a generic food event without causal provenance.

### Werewolf Form

`WerewolfFormActionMixin` multiplies the native Werewolf Form time modifier by:

`[1,1.5,2,3,4,5]` for Age 0..5.

The native Werewolves action remains the action authority.

### Howl

`HowlActionMixin` modifies each native `AggressiveWolfEntity` spawned by Werewolves Howling when Age >0 and `ageBuffsHowl=true`:

- Attack Damage: `+Age` with `ADD_VALUE`;
- Movement Speed: `+0.045 × Age` with `ADD_VALUE`.

Ageing does not own a separate summon event; it modifies the actual Werewolves-spawned wolf before completion of that native pipeline.

### Improved Senses

At Age 5, by default requiring Werewolves' native `SENSE` skill, the provider exposes `vampiricageing:improved_senses_action`.

It sets the provider cache that bypasses invisibility rendering/visibility logic and optionally applies a very strong movement slowdown. Action timing has a static cooldown-unit discrepancy documented in `ACTION-CATALOG.md`.

### Silver weakness

When a Werewolf player has Werewolves' native Silver effect, incoming damage is multiplied by Age-specific defaults:

`[1,1,1.1,1.15,1.2,1.25]`.

A separate Silver Oil age multiplier exists but defaults to all 1.0, i.e. no extra age scaling by default.

## Seniority Oil

Registry: `vampiricageing:seniority_oil` in Vampirism's native OIL registry.

Default Hunter eligibility: Age >=2.

Default max uses: 15.

It only supplies bonus damage when:

- source is Hunter;
- Hunter meets the configured Age gate;
- target is Vampire or Werewolf.

The bonus uses the target's provider Age to select `seniorityOilDamageBonus`, defaults by target Age 0..5:

`[0,0,0.1,0.2,0.4,0.6]`.

`onDamage` returns `amount × bonusDamage`, leaving Vampirism's native oil pipeline to own the oil application/use lifecycle.

## Integration rules

- Tainted Blood state is not interchangeable with Vampirism blood fluid/bar;
- cumulative Tainted Age must be provider-derived;
- Garlic Injection is the observed provider cleanse for both temporary and permanent Tainted state;
- provider recipes/skill gates are part of survival acquisition and must be preserved;
- Werewolf Bite/Howl/Form remain Werewolves-native causal pipelines;
- do not settle Age progress and native blood/food/heal effects twice from the same action;
- fail closed if a future Werewolves version changes the mixin targets or action/skill contracts.