# Bloodlines 3.0.9 — resource authority

Source authority: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c` plus Vampirism `1.10.13@e1ed095713cef5e9eb151d0ee58908fa830d6bb7` where the addon intentionally delegates settlement to the base provider.

Bloodlines touches three resource domains that must remain distinct:

1. Vampirism player blood/saturation/exhaustion;
2. Bloodline perk-point wallet;
3. Gravebound Souls + Phylactery storage/state.

They are not interchangeable currencies.

## 1. Vampirism blood remains authoritative

Bloodlines does not replace the Vampire blood bar. Its Vampire bloodlines intercept or call the base provider pipeline.

### Noble

`BloodlineNoble.onBloodDrink(...)` listens to `BloodDrinkEvent.PlayerDrinkBloodEvent` before base settlement.

- item/stack blood sources have amount and saturation multiplied by the Noble configured source multiplier;
- direct entity blood may receive a rank-dependent amount/saturation multiplier when `NOBLE_BETTER_BLOOD_DRAIN` is enabled;
- direct entity blood awards Bloodlines `ENTITY_BLOOD_DRUNK` using `VReference.FOOD_TO_FLUID_BLOOD` for its task statistic;
- Leeching calls `VampirePlayer.drinkBlood(...)`, preserving base BloodStats settlement and `DrinkBloodContext` provenance.

Black Arcana must not apply a second gain after observing the same BloodDrinkEvent or damage event.

### Bloodknight

Bloodknight heavily specializes the base blood economy but still settles through Vampirism:

- rank modifies base `BLOOD_EXHAUSTION`;
- non-vampire blood sources are reduced through `PlayerDrinkBloodEvent` amount/saturation mutation;
- Vampire Blood Bottle and vampire entity blood can trigger `blood_frenzy`;
- non-player vampire entity blood may receive rank-dependent amount/saturation bonuses;
- `Sapping Strike` drains Vampire players with `targetVP.useBlood(...)` or ExtendedCreature blood state, then pays the attacker with `vp.drinkBlood(...)`;
- Blood Hunt/Daywalker and other Bloodknight actions may consume blood through their native action logic and must not be charged a second time externally.

### Zealot / Ectotherm food conversions

The addon turns specific vanilla foods into Vampire blood only when the corresponding Bloodline skill is enabled:

- Zealot `Flesh Eating`: Rotten Flesh → `VampirePlayer.drinkBlood(...)` using configured nutrition/saturation;
- Ectotherm `Fishmonger`: raw fish tag (`cod`, `salmon`, `tropical_fish`) → `VampirePlayer.drinkBlood(...)` using configured nutrition/saturation.

Again, these are provider-native blood settlements, not a separate Bloodlines bar.

## 2. Bloodline perk-point wallet

`BloodlineSkillHandler` persists:

- `blSkillPoints` (`taskSkillPoints`);
- `blOtherSkillPoints` (`otherSkillPoints`);
- `blEnabledSkills` (`enabledSkills`).

Total points:

`taskSkillPoints + otherSkillPoints`

Remaining:

`max(0, totalSkillPoints - enabledSkills)`

The wallet is reset when the player leaves/switches bloodline. It is not the same object as the normal Vampirism `ISkillPointProvider`.

### Settlement semantics

`BloodlinePerkReward` adds its reward to `taskSkillPoints` and syncs the BloodlineManager.

The Bloodlines mixin increments `enabledSkills` by exactly one when an `IBloodlineSkill` with `requiresBloodlineSkillPoints()` is newly enabled, and decrements by one when disabled.

Static discrepancy requiring runtime QA:

- some Bloodline skills expose base `getSkillPointCost()` 1–3;
- Vampirism's normal `SkillHandler.canSkillBeEnabled` still checks that cost against normal Vampirism points;
- Bloodlines separately checks whether at least one own Bloodline point remains;
- its own wallet then increments `enabledSkills` by one, not by `getSkillPointCost()`.

Do not write a Black Arcana shim that silently pays/refunds either side until the installed build is behaviorally verified.

## 3. Gravebound Souls

Gravebound replaces normal hunger gameplay with a provider-owned Soul state. Its `BloodlineGravebound.State` persists:

- `gravebound_souls`;
- `gravebound_total_devoured`;
- Phylactery block position;
- Phylactery dimension id;
- Mist Form state;
- Possession state, possessed UUID/network id.

The synchronized cache exposes current Souls, max Souls, Phylactery presence, Mist Form and possession state.

### Soul acquisition

`canDevour(...)` is provider authority for whether a LivingEntity can be consumed:

- target must generally be alive;
- distance must be within player entity-interaction range + 1 unless explicitly bypassed by a provider action;
- entity type must have `EntitySoulData` in the Bloodlines data map;
- target health percentage must be <= its configured/data-map devour threshold, possibly increased by Powerful Devour;
- ServerPlayer targets must have remained alive for the configured minimum time.

`devour(...)` then:

1. reads soul amount from the entity-type data map;
2. optionally deals 1000 `bloodlines:devour_soul` damage;
3. adds Souls to the Gravebound state up to current max;
4. increments `totalSoulsDevoured`;
5. awards `SOULS_DEVOURED` and `MOBS_SOUL_DEVOURED` stats;
6. may heal through Regen Devour;
7. may transfer overflow to the owned Phylactery if Soul Transfer is enabled;
8. syncs Bloodline state.

`devour_soul` is tagged to bypass armor, effects and resistance and has no knockback.

### Max Souls

The player state computes max Souls as:

- **4** if no Phylactery is bound;
- otherwise the rank-indexed `graveboundMaxSouls` config value.

`updateCache(rank)` clamps current Souls to the resulting max.

Destroying/replacing the stored Phylactery is detected on world join. If the block is gone or belongs to another owner, the player loses the binding and the state is resynced.

### Phylactery

A Gravebound State stores both dimension and BlockPos. `tryGetPhylactery()` resolves the server dimension and validates that the block entity is a `PhylacteryBlockEntity`.

`totalSoulsDevoured` feeds `PhylacteryBlockEntity.determineMaxSouls(...)`; the block is therefore a separate provider-owned storage surface related to, but not identical to, the player's Soul meter.

Leaving/switching bloodline calls state `clear(...)`, which:

- clears Phylactery ownership when resolvable;
- clears position/dimension;
- zeroes player Souls and total devoured;
- terminates possession;
- clears Mist Form.

### Mist Form

At or above the configured immortality rank, Bloodlines directly enables the non-manual `GRAVEBOUND_MIST_FORM` skill.

For a lethal hit:

- vulnerable damage types are modified first;
- bypass-invulnerability damage cannot be rescued by the normal path;
- if already in Mist Form, incoming damage is zeroed;
- otherwise the action must not be active/on cooldown;
- player must have at least `GraveboundMistFormAction.getRequiredSouls(...)`;
- Bloodlines toggles the native Mist Form action, stores last damage source, sets health to 1 and zeros the lethal damage.

On a full Gravebound death, Souls are reset to 3. Disconnecting while cached Mist Form is active intentionally reapplies the last damage source or kills the player, preventing logout as a resurrection bypass.

## Authority boundaries for Black Arcana

### Allowed

- read BloodlineManager/attributes/state to gate Black Arcana content;
- use provider events and public/action hooks to observe canonical settlements;
- interact with the real `vampirism:blood` fluid through the Vampirism integration contract where appropriate;
- display Bloodline rank/points/Souls as read-through UI if provenance is explicit;
- add a distinct resource bridge only where reserve/commit/refund and exactly-once ownership are proven.

### Forbidden without redesign/explicit bridge

- second Vampire blood bar;
- converting Gravebound Souls to Goety Soul Energy/Malum spirits/Black Arcana soul currency by name alone;
- treating Phylactery capacity as Vampire blood capacity;
- rewarding a second Bloodline perk point for the same completed Bloodlines task;
- bypassing `BloodDrinkEvent` to inject blood directly after a Noble/Bloodknight modifier already settled;
- charging Bloodknight actions twice;
- resurrecting Gravebound independently of Mist Form/Phylactery/Soul gates;
- persisting shadow copies of Bloodline rank or Souls as authoritative data.

## QA gates

Runtime validation must cover:

- blood event amount/saturation modifications for Noble and Bloodknight;
- Sapping Strike target debit + attacker credit exactly once;
- Flesh Eating/Fishmonger exactly-once food-to-blood settlement;
- Gravebound Devour eligibility, stat increments and overflow transfer;
- Phylactery removal/ownership reconciliation across dimensions and reload;
- Soul max clamp with and without Phylactery;
- Mist Form lethal-hit interception, vulnerable damage and logout behavior;
- Bloodline point dual-gate discrepancy before any Black Arcana respec/payment bridge is implemented.
