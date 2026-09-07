# Vampirism 1.10.13 — Progression

Status: `VAMPIRE 1–14 + HUNTER 1–14 + LORD 1–5/1–5 SOURCE-PINNED / RUNTIME QA PENDENTE`

Canonical source: `TeamLapen/Vampirism@e1ed095713cef5e9eb151d0ee58908fa830d6bb7`.

## Hard caps

`REFERENCE.java` defines:

- `HIGHEST_VAMPIRE_LEVEL = 14`;
- `HIGHEST_HUNTER_LEVEL = 14`;
- `HIGHEST_VAMPIRE_LORD = 5`;
- `HIGHEST_HUNTER_LORD = 5`.

The normal faction level and Lord level are distinct provider-native progressions.

## Vampire level progression

### Level 1

Joining the Vampire faction creates the normal level-1 state. Exact infection/transformation entry routes are provider-owned and must be observed through faction state/events rather than reproduced by Black Arcana.

### Levels 2–4 — Altar of Inspiration

`VampireLeveling` defines:

| Target level | Blood units | Equivalent `vampirism:blood` fluid |
|---:|---:|---:|
| 2 | 40 | 4,000 mB |
| 3 | 70 | 7,000 mB |
| 4 | 100 | 10,000 mB |

Conversion is provider-defined: **1 blood food unit = 100 mB fluid blood**.

The Altar of Inspiration:

- has capacity `100 × FOOD_TO_FLUID_BLOOD` = **10,000 mB**;
- accepts only the provider Blood fluid in its internal tank;
- uses a 60-tick ritual state;
- checks target level from current Vampire level + 1;
- settles the actual blood drain and faction-level mutation near ritual completion on the server;
- restores player health shortly before completion;
- applies provider/vanilla post-level effects and fills player blood through the provider's own `drinkBlood(...)` path.

The source contains a tolerance of 99 mB when checking whether the tank has enough blood because supported containers fill in 100 mB increments. Black Arcana must not reinterpret that tolerance as free blood.

### Levels 5–14 — Altar of Infusion

Required provider items and structure score:

| Target | Pure Blood min tier | Pure Blood qty | Human Hearts | Vampire Books | Required structure points |
|---:|---:|---:|---:|---:|---:|
| 5 | 0 | 0 | 5 | 1 | 8 |
| 6 | 0 | 1 | 5 | 1 | 17 |
| 7 | 0 | 1 | 10 | 1 | 17 |
| 8 | 1 | 1 | 10 | 1 | 26 |
| 9 | 1 | 1 | 10 | 1 | 26 |
| 10 | 2 | 1 | 15 | 1 | 35 |
| 11 | 2 | 1 | 15 | 1 | 35 |
| 12 | 3 | 1 | 20 | 1 | 44 |
| 13 | 3 | 2 | 20 | 1 | 44 |
| 14 | 4 | 2 | 25 | 1 | 54 |

A higher-tier Pure Blood item can satisfy a lower-tier Pure Blood requirement.

Activation gates in `AltarInfusionBlockEntity.canActivate(...)`:

1. ritual not already running;
2. a valid requirement exists for exactly current level + 1;
3. **night only**;
4. surrounding pillar/tip structure reaches required score;
5. required inventory is present.

The ritual state machine has `DURATION_TICK = 450`. Required items are consumed at ritual start on server. The faction level is mutated only later at the `LEVELUP` phase after rechecking that the player is still exactly at the expected previous level. This makes the operation resistant to a concurrent/duplicate level change.

Integration consequence: “ritual started”, “items consumed” and “level actually changed” are distinct causal stages. Progress rewards for successful level-up should settle from provider faction-level completion, not merely block activation.

## Hunter level progression

### Levels 2–4 — Basic Hunter interaction

`HunterBasicMenu` confirms that these values are counts of the actual provider item `VAMPIRE_BLOOD_BOTTLE`:

| Target | Vampire Blood Bottles |
|---:|---:|
| 2 | 1 |
| 3 | 5 |
| 4 | 12 |

On a valid click the menu removes the exact item count and calls `setFactionLevel(HUNTER_FACTION, target)`.

### Levels 5–14 — Hunter Table + Hunter Trainer

Each step has two stages:

1. craft the target `Hunter Intel` in a Hunter Table of sufficient tier;
2. deliver that Intel plus Iron/Gold to a Hunter Trainer, which mutates the faction level and consumes the payment.

#### Hunter Table requirements

Every row requires one normal Book and one Vampire Book unless otherwise represented below. `Pure Blood tier` is a minimum; higher tiers are accepted by `countPureBlood(...)`.

| Target | Table tier | Vampire Fangs | Pure Blood qty | Pure Blood min tier | Result Intel |
|---:|---:|---:|---:|---:|---|
| 5 | 0 | 10 | 0 | — | `HUNTER_INTEL_0` |
| 6 | 0 | 0 | 1 | 0 | `HUNTER_INTEL_1` |
| 7 | 0 | 10 | 1 | 0 | `HUNTER_INTEL_2` |
| 8 | 1 | 0 | 1 | 1 | `HUNTER_INTEL_3` |
| 9 | 1 | 15 | 1 | 1 | `HUNTER_INTEL_4` |
| 10 | 2 | 20 | 1 | 2 | `HUNTER_INTEL_5` |
| 11 | 2 | 20 | 1 | 2 | `HUNTER_INTEL_6` |
| 12 | 3 | 20 | 1 | 3 | `HUNTER_INTEL_7` |
| 13 | 3 | 25 | 2 | 3 | `HUNTER_INTEL_8` |
| 14 | 3 | 25 | 2 | 4 | `HUNTER_INTEL_9` |

The output is not produced unless both the item requirements and required Hunter Table tier are satisfied.

#### Hunter Trainer requirements

| Target | Iron ingots | Gold ingots | Required Intel |
|---:|---:|---:|---|
| 5 | 5 | 0 | `HUNTER_INTEL_0` |
| 6 | 10 | 0 | `HUNTER_INTEL_1` |
| 7 | 15 | 0 | `HUNTER_INTEL_2` |
| 8 | 40 | 0 | `HUNTER_INTEL_3` |
| 9 | 20 | 10 | `HUNTER_INTEL_4` |
| 10 | 20 | 20 | `HUNTER_INTEL_5` |
| 11 | 20 | 10 | `HUNTER_INTEL_6` |
| 12 | 30 | 10 | `HUNTER_INTEL_7` |
| 13 | 40 | 20 | `HUNTER_INTEL_8` |
| 14 | 40 | 40 | `HUNTER_INTEL_9` |

On success the trainer:

1. calls `setFactionLevel(HUNTER_FACTION, targetLevel)`;
2. removes Iron, Gold and one Intel;
3. applies the provider Saturation effect;
4. updates the menu to the next level requirement.

## Skill points coupled to leveling

Balance defaults in 1.10.13:

- `skillPointsPerLevel = 2.0`;
- `skillPointsPerLordLevel = 2.0`.

The config comments explicitly warn that changing these values changes balance/completion behavior. Black Arcana should therefore read provider skill state rather than assuming the defaults at runtime.

## Lord progression — task authority

Normal level 14 unlocks the first Lord task. Subsequent Lord tasks use `LordLvlUnlocker(previousLevel, true)` and `LordLevelReward(targetLevel)`.

A Lord reward only applies when current Lord level is exactly `targetLevel - 1`; the reward then calls the provider `setLordLevel(targetLevel)`.

### Vampire Lord 1–5

| Target Lord | Unlock | Requirements in source |
|---:|---|---|
| 1 | Vampire normal max level | infected-creatures stat 25; Pure Blood IV ×5; Gold ×32; `WIN_VILLAGE_CAPTURE` stat ×3 |
| 2 | Lord 1 | entity-tag `HUNTER` ×30; Pure Blood IV ×5; Gold ×48 |
| 3 | Lord 2 | entity-tag `HUNTER` ×30; Pure Blood IV ×5; Gold ×48 |
| 4 | Lord 3 | entity-tag `ADVANCED_HUNTER` ×5; Pure Blood IV ×10; Gold ×64 |
| 5 | Lord 4 | infected-creatures stat 50; Pure Blood IV ×20; Gold ×64; `CAPTURE_VILLAGE` stat ×6 |

The source models Hunter/Advanced-Hunter rows as `EntityTypeRequirement` counters. The static task definition alone identifies the entity-tag requirement and amount; this document does not invent a different kill/interaction semantic beyond what the task runtime records.

### Hunter Lord 1–5

| Target Lord | Unlock | Requirements in source |
|---:|---|---|
| 1 | Hunter normal max level | entity-tag `VAMPIRE` ×50; Gold ×32; `WIN_VILLAGE_CAPTURE` stat ×3 |
| 2 | Lord 1 | entity-tag `VAMPIRE` ×50; Gold ×32 |
| 3 | Lord 2 | entity-tag `VAMPIRE` ×50; Gold ×32 |
| 4 | Lord 3 | entity-tag `VAMPIRE` ×75; Gold ×64 |
| 5 | Lord 4 | entity-tag `VAMPIRE` ×100; Gold ×64; `CAPTURE_VILLAGE` stat ×6 |

## Authority and anti-duplication

- Normal levels remain owned by `FactionPlayerHandler` + provider leveling blocks/NPC menus.
- Lord levels remain owned by the Task system + `LordLevelReward`.
- Skill points remain derived by the provider skill handler/config.
- Black Arcana may mirror progress for UI/quests, but must not create a second authoritative level or Lord-XP track with the same meaning.
- If Black Arcana grants an external reward after a native level change, use the completed `FactionLevelChanged` transition and an idempotency key based on player + faction + old/new level.
- Starting an altar/trainer flow is not equivalent to completing it.

## Runtime QA queue

- Vampire joining/infection routes and exact Faction events;
- Inspiration tank fill/drain in dedicated server;
- Infusion item consumption vs cancellation/death/reload;
- Hunter Table tier detection and higher-tier Pure Blood acceptance;
- Hunter Trainer payment after concurrent state changes;
- normal skill points at levels 1–14 under actual pack config;
- Lord task counters, item consumption and reward idempotency;
- Bloodlines/Vampiric Ageing interaction with level/Lord state.
