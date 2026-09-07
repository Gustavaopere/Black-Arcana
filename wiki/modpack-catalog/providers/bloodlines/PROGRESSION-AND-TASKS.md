# Bloodlines 3.0.9 — progression and tasks

Source authority: `TheDrOfDoctoring/bloodlines@c8fd517d204d09dfcb9a544c17d7df87755eaa5c`.

## Progression model

Each registered bloodline has four ranks. Rank 1 is represented by the root `BloodlineParentSkill`; ranks 2–4 are separate parent/rank skills and are delivered by Bloodline rank tasks.

Rank and Bloodline perk points are independent state:

- `BloodlineManager.bloodlineRank` controls Bloodline rank;
- `BloodlineSkillHandler.taskSkillPoints` and `otherSkillPoints` form the Bloodline perk-point wallet;
- `BloodlineSkillHandler.enabledSkills` tracks Bloodline skills that consume the wallet;
- rank skills use `hasCost=false` and therefore do not consume Bloodline perk points.

`BloodlineRankReward` only applies when `currentRank == targetRank - 1`. The normal provider pipeline therefore cannot jump rank 1→3 or 2→4.

## Task registry

Bloodlines registers **22 task keys** in `VampirismRegistries.Keys.TASK`:

- 15 rank tasks: 3 per bloodline;
- 7 perk-point tasks: 1 each for Noble, Zealot, Ectotherm and Bloodknight; 3 staged tasks for Gravebound.

It also registers its own TaskUnlocker/TaskReward codecs in the Vampirism task registries:

- `bloodlines:bloodline` — `BloodlineUnlocker`;
- `bloodlines:max_perk_unlocker` — `MaxPerkUnlocker`;
- `bloodlines:bloodline_reward` — rank reward + reward instance;
- `bloodlines:bloodline_perk_reward` — perk reward + reward instance.

All 22 Bloodlines tasks are added to `vampirism:is_unique`. Vampire tasks are added to the Vampire task tag and Gravebound tasks to the Hunter task tag.

## Unlocker semantics

### `BloodlineUnlocker`

Parameters:

- required bloodline id;
- required rank;
- `matchExactly`.

If `matchExactly=true`, current rank must equal the configured rank. This is used for rank progression tasks. If false, current rank may be greater/equal; this is used for perk tasks.

### `MaxPerkUnlocker`

Checks **task-derived Bloodline perk points only**, not `otherSkillPoints` and not remaining points:

`taskSkillPoints >= minPerkPoints && taskSkillPoints < maxPerkPoints`.

Gravebound uses the windows:

- `[0,5)`;
- `[5,10)`;
- `[10,15)`.

Therefore Gravebound task-derived perk progression stops at 15 points through this route.

Static discrepancy: `MaxPerkUnlocker.CODEC` binds serialized field name `maxPerkPoints` to the `minPerkPoints` getter and `minPerkPoints` to `maxPerkPoints`. Internal encode/decode can remain round-trip consistent, but external datapacks must treat these names as risky until runtime/data-pack QA.

## Reward semantics

### Rank reward

`BloodlineRankReward(targetRank, source)`:

1. calls Vampirism `TaskManager.resetUniqueTask(source)`;
2. checks current rank equals `targetRank - 1`;
3. sets the target rank;
4. plays the Vampirism vampire scream and particles;
5. calls `BloodlineManager.onBloodlineChange(...)`, which applies default skills/attributes, rechecks gates and syncs state.

### Perk reward

`BloodlinePerkReward(perkPoints, source)`:

1. calls `resetUniqueTask(source)`;
2. adds the amount to `taskSkillPoints` through `BloodlineSkillHandler.addSkillPoints(perkPoints, true)`;
3. syncs Bloodline state.

Vampirism's `resetUniqueTask` removes the task from `completedTasks` and deletes its current unique-task instance. A Bloodlines perk task can therefore become available again as long as its unlockers still pass.

## Noble tasks

### Rank 1 → 2 — `bloodline_noble_one`

- 16 Diamond;
- 4 Gold Block;
- 16 Emerald;
- defeat 8 Vampire Barons;
- reward: Rank 2.

### Rank 2 → 3 — `bloodline_noble_two`

- 24 Diamond;
- 8 Gold Block;
- 32 Emerald;
- defeat 16 Vampire Barons;
- reward: Rank 3.

### Rank 3 → 4 — `bloodline_noble_three`

- 32 Diamond;
- 12 Gold Block;
- 64 Emerald;
- defeat 24 Vampire Barons;
- reward: Rank 4.

### Perk task — `bloodline_perk_points_noble_1`

- Bloodline Noble, rank >= 1;
- `ENTITY_BLOOD_DRUNK` = 50,000 provider stat requirement;
- `TRADED_WITH_VILLAGER` = 20;
- 24 Emerald;
- reward: +1 task-derived Bloodline perk point.

No `MaxPerkUnlocker` is attached in 3.0.9. Structurally this task is repeatable while its task pipeline requirements/unlockers are satisfied.

## Zealot tasks

### Rank 1 → 2 — `bloodline_zealot_one`

- 16 Diamond;
- 64 Sculk;
- 16 Amethyst Block;
- defeat 12 Endermen;
- reward: Rank 2.

### Rank 2 → 3 — `bloodline_zealot_two`

- 32 Diamond;
- 64 Sculk;
- 24 Amethyst Block;
- defeat 24 Endermen;
- reward: Rank 3.

### Rank 3 → 4 — `bloodline_zealot_three`

- 64 Diamond;
- 48 Amethyst Block;
- Vampirism `MOTHER_DEFEATED` stat: 1;
- defeat 48 Endermen;
- reward: Rank 4.

### Perk task — `bloodline_perk_points_zealot_1`

- Bloodline Zealot, rank >= 1;
- 8 Diamond;
- 12 Amethyst Block;
- defeat 5 `ADVANCED_VAMPIRE` entities;
- defeat 10 Endermen;
- reward: +1 task-derived Bloodline perk point.

No `MaxPerkUnlocker` is attached in 3.0.9.

## Ectotherm tasks

### Rank 1 → 2 — `bloodline_ectotherm_one`

- 32 Cod;
- 1 Heart of the Sea;
- defeat 20 Guardians;
- reward: Rank 2.

### Rank 2 → 3 — `bloodline_ectotherm_two`

- 48 Salmon;
- 10 Frozen Blood Samples;
- defeat 3 Elder Guardians;
- reward: Rank 3.

### Rank 3 → 4 — `bloodline_ectotherm_three`

- 2 Heart of the Sea;
- 20 Frozen Blood Samples;
- defeat 5 Elder Guardians;
- reward: Rank 4.

### Perk task — `bloodline_perk_points_ectotherm_1`

- Bloodline Ectotherm, rank >= 1;
- 10 Frozen Blood Samples;
- 3 Heart of the Sea;
- defeat 1 Elder Guardian;
- reward: +1 task-derived Bloodline perk point.

No `MaxPerkUnlocker` is attached in 3.0.9.

## Bloodknight tasks

### Rank 1 → 2 — `bloodline_bloodknight_one`

- 10 Vampire Blood Bottles;
- 5 Pure Blood 2;
- defeat 50 entities in Vampirism `VAMPIRE` tag;
- reward: Rank 2.

### Rank 2 → 3 — `bloodline_bloodknight_two`

- 10 Vampire Blood Bottles;
- 5 Pure Blood 3;
- 10 Corrupted Blood Samples;
- defeat 25 `ADVANCED_VAMPIRE` entities;
- reward: Rank 3.

### Rank 3 → 4 — `bloodline_bloodknight_three`

- 20 Vampire Blood Bottles;
- 8 Pure Blood 4;
- 20 Corrupted Blood Samples;
- defeat 50 `ADVANCED_VAMPIRE` entities;
- reward: Rank 4.

### Perk task — `bloodline_perk_points_bloodknight_1`

- Bloodline Bloodknight, rank >= 1;
- 4 Pure Blood 3;
- 4 Vampire Blood Bottles;
- 12 Corrupted Blood Samples;
- defeat 20 entities in Vampirism `VAMPIRE` tag;
- reward: +1 task-derived Bloodline perk point.

No `MaxPerkUnlocker` is attached in 3.0.9.

## Gravebound tasks

### Rank 1 → 2 — `bloodline_gravebound_one`

- 20 Frozen Blood Samples;
- defeat 10 Vampire Barons;
- defeat 10 `ADVANCED_VAMPIRE` entities;
- `SOULS_DEVOURED` = 250;
- reward: Rank 2.

### Rank 2 → 3 — `bloodline_gravebound_two`

- 20 Frozen Blood Samples;
- 20 Corrupted Blood Samples;
- defeat 15 Vampire Barons;
- `SOULS_DEVOURED` = 500;
- reward: Rank 3.

### Rank 3 → 4 — `bloodline_gravebound_three`

- 32 Frozen Blood Samples;
- 32 Corrupted Blood Samples;
- defeat 25 Vampire Barons;
- `SOULS_DEVOURED` = 1,000;
- reward: Rank 4.

### Perk tier 1 — `bloodline_perk_points_gravebound_1`

Unlock window: task-derived Bloodline perk points `[0,5)`.

- `MOBS_SOUL_DEVOURED` = 35;
- defeat 5 `ADVANCED_VAMPIRE` entities;
- defeat 3 Vampire Barons;
- reward: +1 task-derived Bloodline perk point.

### Perk tier 2 — `bloodline_perk_points_gravebound_2`

Unlock window: `[5,10)`.

- `MOBS_SOUL_DEVOURED` = 100;
- defeat 10 `ADVANCED_HUNTER` entities;
- defeat 8 Vampire Barons;
- reward: +1 task-derived Bloodline perk point.

### Perk tier 3 — `bloodline_perk_points_gravebound_3`

Unlock window: `[10,15)`.

- `MOBS_SOUL_DEVOURED` = 200;
- defeat 20 `ADVANCED_VAMPIRE` entities;
- defeat 20 `ADVANCED_HUNTER` entities;
- defeat 10 Vampire Barons;
- reward: +1 task-derived Bloodline perk point.

## Anti-abuse / integration rules

1. Do not award Bloodline rank from the same kill/task event a second time in Black Arcana. The Bloodlines TaskReward is canonical settlement.
2. Do not mirror task-derived perk points into the normal Vampirism skill-point wallet.
3. Do not create a second repeatable quest for the exact same provider statistic unless it has a distinct reward contract and deduplication.
4. Gravebound task caps must be read from the provider; do not infer all bloodlines share the 15-point cap.
5. Because the four Vampire perk tasks have no `MaxPerkUnlocker`, balance review should explicitly test repeated completions and practical point accumulation in the installed build.
6. A Black Arcana reset/respec system must preserve the distinction between Bloodline rank, task points, other points and enabled Bloodline skills. Blindly clearing `ISkillHandler` is insufficient.
7. Runtime QA must verify task reset/reappearance on faction representatives, especially across logout/reload and rank transitions.
