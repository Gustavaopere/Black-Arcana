# Vampiric Ageing 1.4.21 — action catalog

Source authority: `TheDrOfDoctoring/Vampiric-Ageing@16049e9aeadc47b2307995901c373521cef5fd76`.

## Registry closure

The installed pack has **9 registered actions** from Vampiric Ageing:

| Registry id | Faction | Unlock/gate default | Duration default | Cooldown default | Core effect |
|---|---|---|---:|---:|---|
| `vampiricageing:celerity_action` | Vampire | Age >= 1 | 8 s | 60 s | movement-speed modifier |
| `vampiricageing:drain_blood_action` | Vampire | Age >= 3 | 45 s | 150 s | Blood Tap attack→Vampirism blood drain |
| `vampiricageing:water_walking_action` | Vampire | Age >= 4 skill gate | effectively persistent | 0 | water-walking special attribute |
| `vampiricageing:step_assist_action` | Vampire | Age >= 2 | effectively persistent | 0 | +0.5 step height |
| `vampiricageing:hunter_teleport_action` | Hunter | cumulative Tainted Age >= 8; not Bat | instant | 20 s | looked-at teleport up to 35 blocks |
| `vampiricageing:limited_hunter_batmode_action` | Hunter | cumulative Tainted Age >= 10 + environmental gates | 240 s; transformed effectively persistent | 120 s | bat-like flight/size/restrictions |
| `vampiricageing:step_assist_hunter_action` | Hunter | Hunter Age >= 4 | effectively persistent | 0 | +0.5 step height |
| `vampiricageing:hunter_wise_eye_action` | Hunter | Hunter Age >= 5 | **uses Hunter Step Assist duration in source** | raw config 10 | bypass invisibility; optional -95% speed amount |
| `vampiricageing:improved_senses_action` | Werewolf | Age >= 5; default also requires Werewolves SENSE skill | 120 s | raw config 10 | bypass invisibility; optional -95% speed amount |

The first eight are registered by `VampiricAgeingActions`. `improved_senses_action` is registered separately by `WerewolfAgeingSkills` when Werewolves support is loaded.

## Vampire actions

### Celerity

Registry: `vampiricageing:celerity_action`.

Skill: `vampiricageing:celerity_skill`, inserted into Vampirism's Vampire level tree as a zero-cost ActionSkill and enabled/disabled by the Age Type lifecycle.

Defaults:

- unlock/gate: Age 1;
- duration: 8 s;
- cooldown: 60 s;
- enabled: true;
- modifier id: `vampiricageing:celerity_speed_increase`;
- attribute: `minecraft:movement_speed`;
- operation: `ADD_MULTIPLIED_TOTAL`;
- amount: **1.025**.

Activation adds a permanent attribute modifier for the duration lifecycle; deactivation removes it. Particles are emitted server-side while active.

QA gate: under Minecraft attribute semantics, an `ADD_MULTIPLIED_TOTAL` amount of 1.025 is not equivalent to '+2.5%'. Do not normalize this into UI or balancing until the installed runtime is measured.

### Blood Tap / Drain Blood

Registry: `vampiricageing:drain_blood_action`.

Skill: `vampiricageing:blood_drain_skill`.

Defaults:

- unlock/gate: Age 3;
- duration: 45 s;
- cooldown: 150 s;
- enabled: true.

The action class itself only marks the lasting-action window. Actual settlement occurs in `AgeingEventHandler.onHurt` when the damage source entity is a Vampire Player and this action is active.

For each qualifying incoming-damage event against the target, the provider:

1. asks Vampirism `determineBiteType(target)`;
2. uses the canonical target-specific bite path (`IBiteableEntity.onBite`, VampirePlayer target, Hunter exhaustion path or ExtendedCreature blood state);
3. constructs a `DrinkBloodContext(target)`;
4. calls the attacking `VampirePlayer.drinkBlood(blood, saturation, context)`;
5. fires Vampirism's PlayerDrinkBlood event through `VampirismEventFactory`.

Consequences:

- Blood Tap is not generic lifesteal from final damage amount;
- it is a provider-native bite/blood transaction triggered by attacks;
- Black Arcana must not add a second blood gain for the same attack;
- when `DRAINING` is the active Ageing Method, the resulting entity-backed BloodDrink event can also be the canonical progression credit.

### Water Walking

Registry: `vampiricageing:water_walking_action`.

Skill: `vampiricageing:water_walking_skill`.

Defaults:

- skill unlock: Age 4;
- enabled: true;
- cooldown: 0;
- config duration: `Integer.MAX_VALUE`, clamped then converted to ticks.

Activation toggles `IVampSpecialAttributes.ageing$setWaterWalking(true)` on the Vampirism Vampire special-attributes object; deactivation clears it. Client activation/re-activation mirrors the state.

The action does not implement a second fluid or movement engine. Its effect depends on the provider's Vampirism-special-attributes mixin path.

### Vampire Step Assist

Registry: `vampiricageing:step_assist_action`.

Skill: `vampiricageing:step_assist_skill`.

Defaults:

- unlock and explicit `canBeUsedBy`: Age 2;
- duration config: `Integer.MAX_VALUE` then clamped/converted to ticks;
- cooldown config: 0;
- attribute modifier: `STEP_HEIGHT +0.5 ADD_VALUE`.

Static timing caveat: `getCooldown()` returns `CommonConfig.stepAssistCooldown` directly, unlike the ordinary second-based actions that multiply config by 20. Because the default is 0, this is a non-default-config QA issue.

## Hunter actions

### Hunter Teleport

Registry: `vampiricageing:hunter_teleport_action`.

Skill: `vampiricageing:hunter_teleport_skill`.

Defaults:

- cumulative Tainted Age gate: 8;
- cooldown: 20 s;
- maximum look distance: 35 blocks;
- enabled: true.

Additional gate: cannot be used while Limited Bat Mode special state is active.

The provider ray-traces the player's look direction, derives a target BlockPos, temporarily positions the player to validate liquid/collision safety, rolls back on invalid placement, then performs ServerPlayer teleport and spawns the Vampirism particle cloud/sounds.

Do not replace this with raw coordinate assignment in an integration. The action owns its target acquisition, obstruction checks, rollback and action cooldown.

### Limited Hunter Bat Mode

Registry: `vampiricageing:limited_hunter_batmode_action`.

Skill: `vampiricageing:limited_bat_mode_skill`.

Defaults:

- cumulative Tainted Age gate: 10;
- duration: 240 s;
- cooldown: 120 s;
- flight speed: 0.02;
- per-update food exhaustion addition: 0.008;
- sun blocking: disabled by default;
- transformed duration config: `Integer.MAX_VALUE - 1`, clamped to an effectively persistent action.

Use gates include:

- not in water;
- not in The End;
- not in Vampirism's bat-dimension blacklist;
- no vehicle;
- no active disallowed sun condition when that option is enabled.

Activation:

- sets Hunter special Bat state;
- changes dimensions/pose;
- removes 100% Armor and Armor Toughness through `ADD_MULTIPLIED_TOTAL -1` modifiers;
- grants `mayfly` and starts flying;
- applies configured flight speed.

While active, HunterAgeingHandler prevents or cancels:

- normal entity attacks;
- mounting;
- block right-clicks;
- item-use start;
- throwable-potion/crossbow right-click;
- block placement;
- mining through BreakSpeed cancellation.

Deactivation restores flight permission according to spectator/creative state, restores default flight speed, clears provider Bat state/attachment and gives one second of extremely high Resistance if the player is airborne.

This action is a mandatory multiplayer/dedicated-server QA target because it spans player abilities, dimensions, client special attributes, interaction cancellation and server synchronization.

### Hunter Step Assist

Registry: `vampiricageing:step_assist_hunter_action`.

Skill: `vampiricageing:step_assist_hunter_skill`.

Defaults:

- Hunter Age gate: 4;
- duration: effectively persistent;
- cooldown: 0;
- `STEP_HEIGHT +0.5 ADD_VALUE`.

Like the Vampire implementation, cooldown is returned raw rather than multiplied by 20.

### Wise Eye

Registry: `vampiricageing:hunter_wise_eye_action`.

Skill: `vampiricageing:wise_eye_skill`.

Defaults:

- Hunter Age gate: 5;
- configured `wiseEyeDuration`: 120;
- configured `wiseEyeCooldown`: 10;
- slowdown enabled: true.

Activation sets a provider `AgeingPlayerCache.hasBypassInvisibility` flag and, when slowdown is enabled, adds `MOVEMENT_SPEED -0.95 ADD_MULTIPLIED_TOTAL`.

Static discrepancies in the exact 1.4.21 action class:

- `getCooldown()` returns `wiseEyeCooldown` directly, with no ×20;
- `getDuration()` references `HunterAgeingConfig.stepAssistDuration`, not `wiseEyeDuration`.

With defaults, Step Assist duration is effectively persistent, so Wise Eye's actual source-level duration contract does not match the dedicated 120-duration config. Runtime QA is required; Black Arcana must not silently substitute 120 s.

## Werewolf action

### Improved Senses

Registry: `vampiricageing:improved_senses_action`.

Skill: `vampiricageing:improved_senses_skill`.

Registration only exists when Werewolves is loaded.

Defaults:

- Age gate: 5;
- default skill lifecycle additionally requires Werewolves native `SENSE` skill;
- duration: 120 s;
- cooldown config: 10 returned raw;
- slowdown enabled: true.

Like Wise Eye, activation sets `hasBypassInvisibility` and optionally adds `MOVEMENT_SPEED -0.95 ADD_MULTIPLIED_TOTAL`; deactivation clears both.

Static timing caveat: duration is converted to ticks but cooldown is not.

## Action authority rules

- registration in Vampirism's ACTION registry does not turn these into Iron's spells;
- cooldown/duration/active state belongs to the provider/Vampirism `IActionHandler`;
- age-granted ActionSkills must not be copied into a second Black Arcana skill state;
- Blood Tap settlement is downstream from activation and must be deduplicated at the actual blood transaction/event;
- movement actions must fail closed until exact-server runtime validation has confirmed synchronization and collision behavior;
- config comments and dedicated config fields are not allowed to override contradictory executable source semantics.