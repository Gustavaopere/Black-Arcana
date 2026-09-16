# Werewolves 2.0.3.3 — minions and refinements

Exact source pin: `TeamLapen/Werewolves@b72635b3e014e406b25bb79adb9d340f7443660b`.

## Werewolf Lord minion

Werewolves registers its minion into the Vampirism faction/minion framework. The provider does **not** maintain a parallel generic summon ownership system.

### Minion data caps

`WerewolfMinionData` defines:

- overall upgrade `MAX_LEVEL = 6`;
- inventory level max 2;
- health level max 3;
- strength level max 3;
- resource-efficiency level max 2.

Provider minion attributes are derived from Vampirism minion balance values and Werewolves minion data. `MINION_STATS_INCREASE` can mark increased stats, producing a 1.2 multiplier in the inspected attribute update path.

### Upgrade items

| Item | Allowed next minion levels |
|---|---|
| `werewolf_minion_upgrade_simple` | 1–2 |
| `werewolf_minion_upgrade_enhanced` | 3–4 |
| `werewolf_minion_upgrade_special` | 5–6 |

The interaction increments `minionData.level` by exactly one only when the next level lies in the held upgrade item's allowed range. The item is consumed outside creative/instabuild.

### Available tasks

Werewolf minions expose five tasks:

- Vampirism `follow_lord`;
- Vampirism `defend_area`;
- Vampirism `stay`;
- Vampirism `protect_lord`;
- Werewolves `collect_werewolf_items`.

Only the final task is Werewolves-owned.

## Collect Werewolf Items

`collect_werewolf_items` uses Vampirism `CollectResourcesTask` and Vampirism's minion resource cooldown, reduced according to Werewolf minion resource-efficiency level.

The task is gated by Werewolves `MINION_COLLECT` skill.

Weighted resource pool:

| Resource | Weight |
|---|---:|
| Liver | 6 |
| Porkchop | 2 |
| Beef | 2 |
| Rotten Flesh | 1 |
| Mutton | 1 |
| Cracked Bone | 2 |
| Werewolf Tooth | 1 |
| Vampirism Human Heart | 1 |

External systems must not treat this as a generic loot table kill/drop event: it is provider minion-task settlement.

## Werewolves-owned refinements — 13/13

1. `werewolf_form_duration_general_1`
2. `werewolf_form_duration_general_2`
3. `werewolf_form_duration_survival_1`
4. `werewolf_form_duration_survival_2`
5. `werewolf_form_duration_beast_1`
6. `werewolf_form_duration_beast_2`
7. `rage_fury`
8. `health_after_kill`
9. `stun_bite`
10. `bleeding_bite`
11. `more_wolves`
12. `greater_doge_chance`
13. `no_leap_cooldown`

Werewolves additionally references Vampirism-owned positive/negative refinements for armor, speed, health, damage and attack speed. Those IDs remain Vampirism authority and must not be counted as Werewolves-owned.

## Provider-specific refinement semantics

- general/specific duration refinements extend daytime transformation budget through form action code;
- `rage_fury`: provider kill path grants Strength and extends the active Rage timer;
- `health_after_kill`: changes the provider post-kill Regeneration instance;
- `stun_bite`: extends Stun Bite duration;
- `bleeding_bite`: raises Bleeding Bite effect amplifier to 3;
- `more_wolves`: adds configured extra wolves to Wolf Pack's Howling summon transaction;
- `greater_doge_chance`: adds provider-configured chance to Survivalist Movement Tactics;
- `no_leap_cooldown`: makes Leap action cooldown 0 when equipped.

## Refinement-set reachability

`ModRefinementSets` composes Werewolves-specific refinements with Vampirism base refinements across Common, Uncommon, Rare, Epic and Legendary sets.

Examples include:

- general form duration 1/2 sets;
- Survival/Beast duration sets;
- Legendary Rage Fury;
- Health After Kill / health hybrid;
- Stun Bite, Bleeding Bite and combined `variable_bite`;
- More Wolves;
- Greater Dodge Chance.

### Reachability anomaly — No Leap Cooldown

Exact-source search found `no_leap_cooldown` in:

1. Werewolves refinement registration;
2. Leap cooldown consumer.

No `RefinementSet` entry or other ordinary source-level acquisition path was located at the 2.0.3.3 pin.

Status: `REGISTERED + FUNCTIONAL CONSUMER / SURVIVAL ACQUISITION PATH UNPROVEN / FAIL-CLOSED`.

Do not grant or advertise it as a normally obtainable refinement until runtime/datapack/JAR evidence establishes the missing acquisition path.

## Static refinement metadata anomaly

A set registered under the name `damage3_n_armor1` uses Vampirism `N_ARMOR_2` in the exact source body. Treat the implementation as authority for runtime until verified; do not infer effect solely from the set ID string.

## Minion integration rules

- Werewolf minion ownership comes from Vampirism Lord/minion data, not visual proximity.
- `Howling` Wolf Pack wolves are temporary tamed `AggressiveWolfEntity` summons and are **not** the same entity/state as Werewolf Lord minions.
- Do not award the same summon/minion perk twice from spawn observation and task/command settlement.
- Reused Vampirism minion tasks remain host-owned; Werewolves only extends the task surface.
- External resource rewards must observe completed `collect_werewolf_items` settlement, not predict the weighted outcome.