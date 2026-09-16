# Werewolves 2.0.3.3 — skill tree catalog

Exact source pin: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`.

## Registry count

`ModSkills` registers **38 Werewolves-owned skill IDs**, including the normal root and Lord root.

The generated configured trees prove:

- normal tree: **33 Werewolves-owned registered skills connected**;
- Lord tree: **3 Werewolves-owned skills connected** plus **3 Vampirism-owned Lord skills referenced**;
- two additional Werewolves-owned registrations have no generated-tree path in the exact 2.0.3.3 source: `resistance` and `sixth_sense`.

A registry entry is not sufficient evidence of normal survival reachability.

## Normal configured tree

Canonical root: `werewolves:werewolf/level_root` → `werewolves:werewolf/skill1` → `werewolves:werewolf/skill2`, then Beast, Survival and utility branches.

### Entry

| Node | Choice |
|---|---|
| `level_root` | Werewolf level root |
| `skill1` | Human Form |
| `skill2` | **Night Vision OR Sense** |

### Beast branch

`skill2 → beast1 → beast2`, then branches onward.

| Node | Choice/effect registration |
|---|---|
| `beast1` | Rage |
| `beast2` | Beast Form |
| `beast3` | Thick Fur |
| `beast3_1` | Damage |
| `beast4` | **Stun Bite OR Bleeding Bite** |
| `beast5` | Health After Kill |
| `beast6` | Beast Rage |
| `beast7` | Fear |

`beast3` and `beast3_1` are sibling children of Beast Form in the generated topology; do not invent a dependency between them.

### Survivalist branch

| Node | Choice/effect registration |
|---|---|
| `survival1` | **Jump OR Speed** |
| `survival2` | Survival Form |
| `survival3` | **Wolf Pawn OR Climber** |
| `survival4` | **Efficient Diet OR Arrow Awareness** |
| `survival31` | Leap |
| `survival5` | Movement Tactics |

`survival4` and `survival31` are sibling children of `survival3` in the generated tree. `survival5` descends from `survival4`.

### Utility / other branch

| Node | Choice/effect registration |
|---|---|
| `util1` | Howling |
| `util2` | **Wolf Pack OR Digger** |
| `util3` | **Not Meat? OR Health Reg** |
| `other1` | Free Will |
| `other2` | Silver Blooded |
| `other3` | Wear Armor |
| `other4` | Water Lover |
| `other5` | Hide Name |
| `other6` | Enhanced Digger |

The generated topology branches from `util3` into the Free Will chain and the Water Lover chain. Do not flatten this into a simple ordered list.

## Lord configured tree

The generated Lord tree has a single Lord root with four direct children:

| Node | Skills |
|---|---|
| `lord_root` | Werewolves `werewolf_lord` root |
| `lord_2` | Werewolves `werewolf_minion_stats_increase` |
| `lord_3` | Vampirism `lord_speed` OR Vampirism `lord_attack_speed` |
| `lord_4` | Werewolves `werewolf_minion_collect` |
| `lord_5` | Vampirism `minion_recovery` |

This is a deliberate provider/host composition. Black Arcana must not copy the Vampirism Lord skills into a second Werewolves-owned implementation.

## Semantic catalog of reachable normal skills

### Transformation and perception

- **Human Form:** unlocks provider Human form action.
- **Night Vision:** toggles provider special state; while transformed, WerewolfPlayer maintains a source-tagged Night Vision effect and restores hidden prior effects on exit.
- **Sense:** unlocks the provider action; actual visual effect is client post-processing/entity outlining.
- **Beast Form:** unlocks Beast action.
- **Survival Form:** unlocks Survivalist action.
- **Free Will:** removes provider full-moon forced-form/deactivation restrictions.
- **Hide Name:** suppresses name rendering while transformed.

### Combat

- **Rage:** unlocks lasting Rage action.
- **Damage:** upgrades form attack-damage modifier from the reduced baseline to the full configured amount where the form supports it.
- **Stun Bite:** successful non-human-like bites add STUN.
- **Bleeding Bite:** successful non-human-like bites add BLEEDING.
- **Health After Kill:** provider kill handler applies a very short high-amplifier Regeneration instance; exact gameplay result must be runtime-tested rather than normalized.
- **Beast Rage:** while Beast + Rage are active, provider applies night-strength form modifiers and suspends transformation-time consumption.
- **Fear:** unlocks crowd-control action that clears nearby non-werewolf mob targets and sends them away.
- **Thick Fur:** modifies form damage-reduction handling when not transformed.

### Mobility/survival

- **Jump:** while transformed, increases jump vertical movement and slightly reduces effective fall distance.
- **Speed:** upgrades form speed modifier from baseline reduced amount to full configured amount.
- **Wolf Pawn:** fall distance and fall-damage multiplier are each reduced to 80%; jump velocity is increased; incoming damage tagged `WEREWOLF_FUR_IMMUNE` is canceled while transformed with the skill.
- **Climber:** Survival form gains +0.4 step height.
- **Efficient Diet:** reduces Survival-form food-consumption attribute cost.
- **Arrow Awareness:** Survivalist, while moving, has a source-coded 40% chance to cancel arrow damage.
- **Movement Tactics:** Survivalist while sprinting may cancel sourced damage according to configured dodge chance; refinement can increase the chance.
- **Leap:** arms the provider leap state; next jump receives form-scaled directional impulse and action ends on landing/fall.
- **Water Lover:** prevents the provider underwater Weakness penalty.

### Diet/digging/utility

- **Howling:** unlocks Howling.
- **Wolf Pack:** Howling additionally spawns temporary tamed Aggressive Wolf entities.
- **Digger:** increments provider digger level/speed and grants transformed empty-hand mining tier starting at Wood.
- **Enhanced Digger:** increments the same state again, raising tier/speed further.
- **Not Meat?:** allows werewolf player to eat non-meat foods; without it, provider mixin can zero nutrition/saturation for non-meat. Raw-meat handling has provider-specific bonuses.
- **Health Reg:** advances the internal FoodData tick timer an extra step while active. The exposed `health_reg_modifier` config is not read by this inspected path.
- **Silver Blooded:** while in a human-like form, weakens Silver-effect application: amplifier can be reduced by one, or non-continuous amplifier-0 duration halved.
- **Wear Armor:** allows ordinary armor in transformed human-like form; non-human forms continue to use provider armor rules.

## Registered but reachability-unproven

### `resistance`

- registered as `SimpleWerewolfSkill`;
- language says “Increase your resistance in werewolf form”;
- config `resistance_amount=3` exists;
- no node in generated normal/Lord configured trees was found;
- no source consumer of `ModSkills.RESISTANCE` was located in the exact pin audit.

Status: `REGISTERED / TREE PATH NOT FOUND / EFFECT CONSUMER NOT FOUND / FAIL-CLOSED`.

### `sixth_sense`

- registered and has a functional event consumer;
- when a mob changes target to a Werewolf player with this skill enabled, server sends `ClientboundAttackTargetEventPacket`;
- no node in the exact generated normal/Lord trees grants it.

Status: `REGISTERED + FUNCTIONAL CONSUMER / TREE PATH NOT FOUND / SURVIVAL REACHABILITY UNPROVEN`.

## Choice semantics

The following nodes contain multiple skills. Treat them as provider choices, not automatically cumulative perks:

- Night Vision / Sense;
- Stun Bite / Bleeding Bite;
- Jump / Speed;
- Wolf Pawn / Climber;
- Efficient Diet / Arrow Awareness;
- Wolf Pack / Digger;
- Not Meat? / Health Reg;
- Lord Speed / Lord Attack Speed.

## Black Arcana rule

A Black Arcana perk may observe, require, enhance or react to provider skill state only through validated provider hooks/state. It must not silently grant a mutually-exclusive sibling, bypass a node prerequisite, fabricate `resistance`/`sixth_sense` reachability, or maintain a second skill wallet.