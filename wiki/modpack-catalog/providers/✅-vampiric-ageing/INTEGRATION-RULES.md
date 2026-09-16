# Black Arcana ↔ Vampiric Ageing 1.4.21 — integration rules

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## Core rule

**Provider-native first.** Vampiric Ageing owns Age Type, Age Rank, rank progress, Tainted Hunter state, its age-granted skills/actions and all native settlement it performs through Vampirism/Werewolves.

Black Arcana may observe and gate on those states. It must not create an authoritative duplicate.

## Canonical authorities

| Domain | Authority |
|---|---|
| Age Type / Age Rank / progress | `AgeingManager` attachment |
| Hunter temporary/permanent Tainted state | `HunterAgeingType.HunterState` |
| Vampire blood/saturation/exhaustion | Vampirism `VampirePlayer` / BloodStats pipeline |
| Age-granted action active/cooldown/duration | Vampirism/Werewolves native `IActionHandler` |
| Age-granted skills | native Vampirism/Werewolves `ISkill` handlers |
| Werewolf Bite/Form/Howl/Sense | Werewolves native mechanics, modified by Ageing overlays |
| Hunter food/exhaustion | vanilla `FoodData`, modified by Ageing hooks |
| Seniority Oil lifecycle | Vampirism OIL/WeaponOil pipeline |

## Read-through integration allowed

Black Arcana may:

- read current Age Type/Rank/progress to gate its own content;
- read cumulative Tainted Age through provider semantics;
- show provider state in a read-through UI with explicit provenance;
- observe canonical BloodDrinkEvent, action completion, damage or faction lifecycle events;
- define Black Arcana perks that require a minimum provider Age without granting that Age;
- react after a provider settlement when an exactly-once causal key can be proven;
- use provider datapack tags/datamaps as classification inputs when version-pinned;
- add separate mechanics whose resource/state identity is explicitly distinct and whose lifecycle does not shadow Ageing state.

## Forbidden without explicit redesign

Do not:

- create `blackarcanaAgeRank` as a competing authority;
- award Age points from both a precursor event and the provider's canonical settlement;
- grant/disable provider ActionSkills by bypassing Ageing Type lifecycle;
- reproduce Blood Tap as generic final-damage lifesteal;
- pay or reward Vampire blood outside Vampirism after Ageing already settled the same attack;
- treat Tainted Blood as mB of `vampirism:blood`;
- convert Tainted Age into Bloodlines Gravebound Souls, Goety Soul Energy or another resource merely because all are supernatural resources;
- grant Limited Bat flight independently of the provider action state;
- teleport a second time after Hunter Teleport succeeds;
- append a second Bite heal/nutrition settlement to Werewolves;
- spawn or buff a second set of Howl wolves from the same native Howl action;
- independently multiply Werewolf Form duration after Ageing's mixin already did so;
- pre-charge blood for optional old-Vampire immortality before the provider's LOWEST lethal-damage path decides that the hit qualifies;
- infer successful mixin behavior solely from declared dependency ranges.

## Exactly-once progression contracts

### Vampire DRAINING

Causal chain can be:

`attack/bite source → Vampirism blood settlement → PlayerDrinkBloodEvent → Ageing progress`

Black Arcana must treat the Ageing progress credit as downstream of the final canonical BloodDrink event. Do not separately credit the attack or `onBite` call as another Age event.

### Blood Tap

Causal chain:

`LivingIncomingDamageEvent with active Blood Tap → determine native bite type → target-specific blood debit → VampirePlayer.drinkBlood → BloodDrinkEvent`

A Black Arcana listener may observe this chain but must not insert another blood gain or another DRAINING progress award.

### Hunting/Devour methods

Causal authority is the selected `IAgeMethod` and its provider tag/damage-source classification.

A single kill may qualify for many game systems; only the selected Ageing method owns the Age-progress credit. Cross-system rewards require separate provenance and anti-duplication keys.

### TIME

Age progress is tick-settled by the provider every 100 ticks while `canAge()`. Do not add another age clock.

## Faction and lifecycle gates

Ageing Type follows faction state. When the underlying playable faction is lost or changed, the provider resets/reselects Age state and applies its own cleanup.

Any Black Arcana perk that depends on Age must fail closed when:

- no valid Age Type is selected;
- current faction no longer matches the required Age Type;
- required rank is not met;
- relevant optional provider (Werewolves) is absent;
- provider runtime state cannot be resolved.

Do not preserve entitlement from stale cached Age after a faction change.

## Tainted Blood contract

Tainted Blood means Hunter transformation state in this provider.

### Safe uses

- gate content on cumulative Tainted Age;
- show temporary/permanent transformation status;
- react to the actual provider cleanse/transformation lifecycle;
- treat Tainted Blood recipes as survival progression prerequisites.

### Unsafe uses

- interpreting the Tainted Blood Bottle's `damageValue` as durability loss rather than rank provenance;
- granting a generic potion effect and assuming HunterState became tainted;
- removing only `tainted_blood_effect` and assuming the state was cleansed;
- storing a second permanent-transformation boolean;
- converting cumulative Age directly to a generic magic power level without an explicit design contract.

## Movement/action contract

### Hunter Teleport

Consume provider action success as the canonical teleport. If a Black Arcana feature needs to trigger after teleport, it must use the provider result/state and must not independently resolve destination/collision.

### Limited Hunter Bat Mode

Treat as a composite provider state involving action handler + special attributes + player abilities + dimensions/pose + interaction restrictions.

Do not use only `mayfly`, `flying`, pose or bounding-box size as proof of the canonical state.

Any bridge that depends on Bat Mode remains fail-closed until dedicated-server tests confirm exact-pack synchronization.

### Wise Eye / Improved Senses

These abilities are invisibility-bypass mechanics backed by Ageing cache/render hooks, not Night Vision. Do not substitute a vanilla potion effect.

## Attribute contract

Ageing applies attributes through its own Age Type lifecycle and mixins.

Black Arcana must not reproduce the same provider modifier under another ID to 'ensure it works'. This would stack instead of repair.

Static discrepancies in Celerity/DBNO/neonatal semantics must be validated first. Until then:

- read raw provider config/source values only for diagnostics;
- do not expose normalized percentages as factual runtime outcomes;
- do not create compensating modifiers.

## Death/resurrection contract

Provider default death policy resets Age to 0. Optional configs can reduce only some ranks.

High-age Vampire immortality is a separate optional late damage-settlement feature and is disabled by default. If enabled, it must remain ordered relative to:

- Vampirism killing-source classification;
- BloodStats debit when configured;
- Bloodlines or other death-interception mechanics;
- Black Arcana resurrection/death-prevention features.

Exactly one system may own a particular lethal-hit prevention settlement. If ordering cannot be proven, Black Arcana must fail closed rather than add another rescue.

## Werewolves contract

Ageing is an overlay provider, not a replacement for Werewolves.

Preserve:

- native Bite damage source and action semantics;
- native Form action duration before Ageing modifier;
- native Howl spawn lifecycle before Ageing wolf modifiers;
- native SENSE skill requirement for Improved Senses when configured;
- native Silver effect/oil systems.

Future Werewolves version changes can invalidate mixin assumptions even when metadata ranges still pass. Revalidate on every installed-version drift.

## Datapack/config contract

Provider thresholds, method selection, feature toggles and entity classifications are config/data-driven.

Black Arcana integrations must:

- query/read the active config/provider state where feasible;
- avoid hardcoding defaults as immutable gameplay law;
- preserve data-map/tag classification;
- fail closed when a configured method string has no valid matching method rather than guessing a replacement;
- not repair misspelled/generated resource paths by assuming intended spelling without checking the actual provider constants/resources.

## Minimum validation before enabling a runtime bridge

A runtime integration depending on Vampiric Ageing is not approved until it verifies, as relevant:

- installed `vampiricageing` version 1.21-1.4.21;
- Vampirism 1.10.13 and Werewolves 2.0.3.3 target compatibility;
- AgeingManager read/sync across login/death/faction change;
- exactly-once Age progress for the selected method;
- exactly-once Blood Tap blood settlement;
- Tainted bottle/permanent/garlic lifecycle;
- action timing discrepancies;
- Hunter Teleport and Limited Bat Mode on dedicated server;
- Werewolf Bite/Form/Howl overlays;
- no stacking with Bloodlines or Black Arcana death/resource/movement systems.

Until evidence exists, integration status is `DESIGN/READ-THROUGH ONLY` for affected runtime surfaces.